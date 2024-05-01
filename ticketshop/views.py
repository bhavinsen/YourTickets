import datetime
import string
import random
import json
import requests

from django.shortcuts import render
from django.utils.encoding import uri_to_iri, iri_to_uri
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.db.models import F
from django.utils import timezone
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse

from mollie.api.client import Client as MollieClient
from mollie.api.error import Error as mollie_error

from rest_framework import viewsets

from yourtickets.common import (utils, shop, cart)
from ticketshop.serializers import EventSerializer, TicketSerializer
from yourtickets.common.ticket import send_mail_and_create_pdfs, send_mail_and_create_pdf_for_ticket
from yourtickets.common.log import writeLog, writeOrderLog
from yourtickets.views import iframe_redirect
from ticketshop.forms import SendTicketsToForm
from ticketshop.models import Iframe, Multiticketshop, MultiticketshopEvents
from ticketshop.models import (
    Event, EventOrganiser, Ticket,
    SoldTicket, LineUp, TicketShopCustom,
    UserExtra, Order, Languages,
    GuestTickets, Saleschannel, Orderlog
)
from yourtickets.tasks import (
    send_mail_order
)
from yourtickets.common.log import writeOrderLog

# mollie_apikey = settings.MOLLIE_API_KEY
mollie_apikey = settings.MOLLIE_TEST_API_KEY


@csrf_exempt
def mollie_webhook(request):

    try:
        mollie_client = MollieClient()
        mollie_client.set_api_key(mollie_apikey)

        mollie_payment_id = request.POST.get('id')

        # response = requests.request(
        #     'POST', 'https://api.mollie.com/v2/payments/'+mollie_payment_id,

        #     headers={
        #         'Accept': 'application/json',
        #         'Authorization': 'Bearer live_BLXnVPqB8NAsRQAhBCm26VtK67uphg',

        #     },
        # )

        payment = mollie_client.payments.get(mollie_payment_id)
        # result = response.json()

        # writeLog('mollie_payment_id:'+mollie_payment_id, 'incoming mollie webhook')



        writeOrderLog(mollie_id=mollie_payment_id, type=Orderlog.TYPE_WEBHOOK_MOLLIE_API_RECEIVED)

        # writeLog('mollie_payment_id:' + str(mollie_payment_id), 'status:'+result['status'])

        if payment.status == 'paid':

            #
            # At this point you'd probably want to start the process of delivering the
            # product to the customer.
            #
            # mollie_payment_id = 'tr_cNsw93kVQy'
            order = Order.objects.filter(mollie_id=str(mollie_payment_id)).first()



            if order:
                # print 'order found ======='
                writeOrderLog(order_id=order.id, mollie_id=mollie_payment_id, type=Orderlog.TYPE_WEBHOOK_MOLLIE_ORDER_OK)
                # set the order to paid
                order.order_paid = True
                order.payment_method = payment.method
                order.save()

                # mollie sometimes spams us so thats why i did this
                # mail allready send!
                # dont send the tickets again please!
                # only tell mollie everything is fine for us!
                if order.mail_send:
                    # writeLog('mollie_payment_id:' + str(mollie_payment_id), 'MOLLIE PLEASE STOP SPAMMING MAIL ALLREADY SEND!')
                    return HttpResponse(status=200)

                writeOrderLog(order_id=order.id, mollie_id=mollie_payment_id, type=Orderlog.TYPE_WEBHOOK_MOLLIE_OK)


                # send_mail_order.delay(order_id=order.pk, email=None)
                send_mail_order(order_id=order.pk, email=None)

                # return
                # create the ticket AND send the mail


                # writeLog('mollie_payment_id:'+str(mollie_payment_id), 'order saved and mail send!')
            # else:
            #     print 'order not found'
            # return 'ispaid'
            return HttpResponse(status=200)
        # elif payment.isPending():
        #     #
        #     # The payment has started but is not complete yet.
        #     #
        #     # return 'Pending'
        #     writeLog('mollie_payment_id:'+mollie_payment_id, 'pending')
        #     return HttpResponse(status=200)
        # elif payment.isOpen():
        #     #
        #     # The payment has not started yet. Wait for it.
        #     #
        #     # return 'Open'
        #     writeLog('mollie_payment_id:'+mollie_payment_id, 'open')
        #     return HttpResponse(status=200)
        else:
            #
            # The payment isn't paid, pending nor open. We can assume it was aborted.
            #
            # return 'Cancelled'
            #get order amount tickets
            # writeLog('mollie_payment_id:'+str(mollie_payment_id),'order aborted')
            order = Order.objects.filter(mollie_id=str(mollie_payment_id)).first()
            if order:
                
                order.delete()

            return HttpResponse(status=200)
    except mollie_error as e:
        # writeLog('mollie_payment_id:'+mollie_payment_id,'mollie error')
        try:
            writeLog('mollie error', e)
        except:
            pass
        writeOrderLog(mollie_id=mollie_payment_id, type=Orderlog.TYPE_WEBHOOK_MOLLIE_API_ERROR)
        return HttpResponse(status=200)
    # except Exception as e:

        # msg = EmailMessage('debug mollie called '+str(e), '', 'noreply@yourtickets.nl', ['almerelc@gmail.com'])
        # msg.send()
        # writeOrderLog(mollie_id=mollie_payment_id, type=Orderlog.TYPE_WEBHOOK_MOLLIE_EXCEPTION)
        # return HttpResponse(status=200)


def get_mollie_status(payment):

    if payment.status == 'paid':
        return 'ispaid'
    elif payment.status == 'pending':
        #
        # The payment has started but is not complete yet.
        #
        # return 'Pending'
        return 'pending'
    elif payment.status == 'open':
        #
        # The payment has not started yet. Wait for it.
        #
        # return 'Open'

        return 'open'
    else:
        #
        # The payment isn't paid, pending nor open. We can assume it was aborted.
        #
        # return 'Cancelled'
        #get order amount tickets
        return 'cancelled'


def thank_you(request, order_id, event_id=None):

    order = Order.objects.filter(pk=order_id).first()

    # if there is no order mollie probably allready called the webhook
    if not order:
        event = Event.objects.get(pk=event_id)
        return redirect(reverse('ticketshop_ticket_overview', kwargs={'event_id': event.id, 'event_name': event.event_url}))
    else:
        # from here there is actually an order
        # but to be honest it should NEVER be the case
        # because the webhook is allways called

        # only delete the order IF the user from the request is the same as the
        # user from the order, else users can delete eachother records ( should be such a big deal actually )
        if str(order.user.id) == str(request.user.id):
            
            try:
                mollie_client = MollieClient()
                mollie_client.set_api_key(mollie_apikey)
                payment = mollie_client.payments.get(order.mollie_id)
                status = get_mollie_status(payment)

                if status == 'cancelled':
                    try:
                        event = Event.objects.get(id=event_id)

                        order.delete()
                        # writeLog('mollie_check_thankyou_'+str(order.id), status)
                        return redirect(reverse('ticketshop_ticket_overview', kwargs={'event_id': event.id, 'event_name': event.event_url}))
                    except Exception as e:
                        pass
            except mollie_error as e:
                pass

    tick = SoldTicket.objects.filter(order_nr=order.id).first()
    event_id = str(tick.event.id)
    event = Event.objects.get(pk=event_id)
    #dit moet weg wordt niet gebruikt
    shop_url = reverse('buy_ticket', kwargs={'event_id': event_id, 'event_name': event.title})

    lineup = LineUp.objects.filter(event_id=event)
    cshop = TicketShopCustom.objects.filter(event_id=event_id).first()
    url = reverse('buy_ticket', kwargs={'event_id': event.id, 'event_name': event.title})
    start = timezone.localtime(event.start_date)
    end = timezone.localtime(event.end_date)
    event_date = start.strftime("%d %B %y | %H:%M") + " - " + end.strftime("%H:%M")

    if 'comes_from_iframe' in request.session and request.session['comes_from_iframe'] == True:
        iframe = Iframe.objects.filter(event_id=event)

        if len(iframe) > 0:
            if iframe[0].url != '':
                return redirect(iframe[0].url)

    skip = order.ga_tracked

    order.ga_tracked = True
    order.save()

    return render(request, 'ticketshop/shop_thanks.html', {
        'cur_event': event,
        'lineup': lineup,
        'url': url,
        'cshop': cshop,
        'shop_url': shop_url,
        'event_date': event_date,
        'hostname': settings.HOSTNAME,
        'GA_pagetype': 'Success page',
        'GA_SKIP': skip,
        'order': order
    })


# if posted we save email_allowed
# if page is refreshed it flushed the event data
from django.views.decorators.clickjacking import xframe_options_exempt

@csrf_exempt
@xframe_options_exempt
def index(request, event_id, event_name, channel_url_name=None, some_tickets_soldout=''):

    try:
        event = Event.objects.get(pk=event_id, removed=False)
    except Exception as e:
        raise Http404

    if not event.event_public:
        raise Http404

    session_cart = cart.Cart(request)
    session_cart.flush_event(event.id)

    if request.user.is_authenticated:
        extra = UserExtra.objects.filter(user=request.user).count()
        if extra == 0:
            return redirect(reverse('profiel')+'?next='+request.path)

    # store the email allowed
    if request.POST:

        # normalize the email allowed and store it
        email_allowed = request.POST.get('email_allowed', False)
        if request.POST.get('email_allowed', False):
            email_allowed = True

        # store email allowed
        session_cart.add_email_allowed(event.pk, email_allowed)

        # get the ordered tickets and store them
        tickets_quan = request.POST.getlist('quantity[]')
        tickets_refs = request.POST.getlist('ticketref[]')

        invalid_ticket_found = False
        ordered_tickets_list = dict()

        for key, ticket_quantity in enumerate(tickets_quan):
            ticket_id = tickets_refs[key]
            ticket = Ticket.objects.filter(event=event, deleted=False, pk=ticket_id).first()
            # this means there is an invalid ticket used
            # skip the rest and
            if not ticket:
                invalid_ticket_found = True
                break
            if ticket_quantity != '0':
                ordered_tickets_list[str(ticket_id)] = ticket_quantity

        # store
        if not invalid_ticket_found:
            session_cart.set_tickets(event_id, ordered_tickets_list)

            # this fixes some session issues
            request.session['inv'] = str(datetime.datetime.utcnow())

            return redirect(reverse('ticketshop_ticket_overview', kwargs={'event_id': event.id, 'event_name': event_name}))

    current_datetime = timezone.now()
    lineup = LineUp.objects.filter(event_id=event).order_by('pk')

    today = datetime.datetime.today()
    tickets = Ticket.objects.filter(event=event, deleted=False).order_by('pk')


    for ticket in tickets:
        ticket.price_or = ticket.price
        ticket.price_new = float(ticket.price) / 100
        sold_total = SoldTicket.objects.filter(ticket_type=ticket).count()
        tickets_available = ticket.quantity - sold_total
        if current_datetime > ticket.end_date:
            ticket.old = True
        if current_datetime > event.end_date:
            ticket.old = True
        if current_datetime < ticket.start_date:
            ticket.not_available = True
        if tickets_available < 0:
            tickets_available = 0
        if tickets_available < ticket.max_sold:
            ticket.max_sold = tickets_available

    cshop = TicketShopCustom.objects.filter(event_id=event_id).first()
    Event.objects.filter(pk=event_id).update(views=F('views')+1)
    start = timezone.localtime(event.start_date)
    end = timezone.localtime(event.end_date)

    template = 'ticketshop/ticket.html'

    event_date = start.strftime("%d %B %y | %H:%M") + " - " + end.strftime("%H:%M")

    iframe = False

    if request.GET.get('iframe', '0') == '1':
        iframe = True

    # return False
    if iframe:
        request.session['comes_from_iframe'] = True
        request.session['event_id'] = event.id
    else:
        request.session['comes_from_iframe'] = False


    sales_channel = detect_sales_channel(request, event, channel_url_name)
    return render(request, template, {
        'cshop': cshop,
        'cur_event': event,
        'lineup': lineup,
        'tickets': tickets,
        'event_date': event_date,
        'GA_pagetype': 'Ticket page',
        'language': get_language(),
        'some_tickets_soldout': some_tickets_soldout
    })


def detect_sales_channel(request, event, channel_url_name=None):

    if not channel_url_name:
        return

    channels = Saleschannel.objects.filter(event=event, deleted=False, url_name=iri_to_uri(channel_url_name))

    if len(channels) == 0:
        return False

    channel = channels.first()

    request.session['sales_channel'] = channel.pk



# if posted we save email_allowed
# if page is refreshed it flushed the event data
from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def ticket_overview(request, event_id, event_name):
    try:
        event = Event.objects.get(pk=event_id, removed=False)
    except Event.DoesNotExist:   
        raise Http404
        
    if not event.event_public:
        raise Http404

    if request.user.is_authenticated:
        extra = UserExtra.objects.filter(user=request.user).count()
        if extra == 0:
            return redirect(reverse('profiel')+'?next='+request.path)

    session_cart = cart.Cart(request)

    error_messages = list()
    error_messages_login = list()
    userExtraFormValues = dict()
    ticket_key_amount_list = session_cart.get_tickets(event_id)

    if not session_cart.has_event_and_tickets(event_id):
        return redirect(reverse('buy_ticket', kwargs={'event_id': event.pk, 'event_name': event_name}))

    ticket_keys = [i for i in ticket_key_amount_list.keys()]
    cshop = TicketShopCustom.objects.filter(event_id=event_id).first()

    tickets = Ticket.objects.filter(event=event, deleted=False, pk__in=ticket_keys)

    order_info = shop.get_price_and_ticket_amount(ticket_key_amount_list, tickets)


    # tickets_amount = order_info['tickets_amount_for_service_costs']
    total = order_info['price']

    # url = get_current_site(request).domain + "/ticketshop/" + str(event.id) + "/" + event.event_url
    transaction_fee = 0

    start = timezone.localtime(event.start_date)
    end = timezone.localtime(event.end_date)
    event_date = start.strftime("%d %B %y | %H:%M") + " - " + end.strftime("%H:%M")

    if total > 0:
    #    transaction_fee = shop.get_service_cost(order_info['price'], order_info['tickets_amount_for_service_costs']) - ( (event.service_cost_discount_cents * order_info['tickets_amount_for_service_costs'] )/100.0)
        transaction_fee = shop.get_service_cost(order_info['price'], 
                                                order_info['tickets_amount_for_service_costs'], 
                                                event.service_cost_discount_cents)
    #if transaction_fee < 0:
    #    transaction_fee = 0

    tickets_formatted = list()
    tickets_form_list = list()
    for ticket in tickets:
        amount = int(ticket_key_amount_list[str(ticket.pk)])
        ticket_price = float(ticket.price)

        ticket_formatted = dict()
        ticket_formatted['name'] = ticket.name
        ticket_formatted['amount'] = ticket_key_amount_list[str(ticket.pk)]
        ticket_formatted['price'] = ticket_price * amount/100
        ticket_formatted['forms'] = list()

        # loop over the amount of tickets ordered
        for i in range(int(ticket_key_amount_list[str(ticket.pk)])):
            ticket_form_list = dict()
            ticket_form_list['name'] = ticket.name
            ticket_form_list['forms'] = list()
            some_has_changed = False
            for k in range(ticket.person_amount):
                form_key = str(i)+str(k)+str(ticket.pk)

                if request.POST:
                    frm = SendTicketsToForm(data=request.POST, prefix=form_key)
                    if frm.has_changed():
                        frm.is_valid()
                else:
                    frm = SendTicketsToForm(prefix=form_key)

                if frm.has_changed() and some_has_changed is False:
                    some_has_changed = True

                ticket_form_list['forms'].append(frm)
            ticket_form_list['some_has_changed'] = some_has_changed
            tickets_form_list.append(ticket_form_list)

        tickets_formatted.append(ticket_formatted)

    if request.method == 'POST':

        # is login or new_user
        action_type = request.POST.get('action_type')

        if action_type == 'login':
            username = request.POST.get('username', '').lower()
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
            else:
                error_messages_login.append("Gebruikersnaam en/of wachtwoord incorrect.")
        elif action_type == 'new_user':

            username = request.POST.get('username', '').lower()
            password = request.POST.get('password', '')
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')

            valid_birthdate = True
            try:
                birth_date = datetime.datetime.strptime(request.POST.get('birth_date', ''), '%d-%m-%Y').strftime('%Y-%m-%d')
            except ValueError as e:
                birth_date = ''
                valid_birthdate = False

            postcode = request.POST.get('postcode', '')
            gender = request.POST.get('gender', 'M')

            userExtraFormValues['username'] = username
            userExtraFormValues['first_name'] = first_name
            userExtraFormValues['last_name'] = last_name

            # input is d-m-Y
            # db is Y-m-d
            userExtraFormValues['birth_date'] = request.POST.get('birth_date', '')
            userExtraFormValues['postcode'] = postcode
            userExtraFormValues['gender'] = gender

            users_count = User.objects.filter(username=username).count()

            # validate email
            try:
                validate_email(username)
            except ValidationError as e:
                valid_username_email = False
            else:
                valid_username_email = True

            birth_date_error = False
            if birth_date and datetime.datetime.strptime(request.POST.get('birth_date', ''), '%d-%m-%Y') > datetime.datetime.now():
                birth_date_error = True

            if not first_name \
                    or not last_name \
                    or not birth_date \
                    or users_count > 0 \
                    or not valid_username_email \
                    or not username \
                    or not valid_birthdate \
                    or not password \
                    or birth_date_error \
                    or not postcode: # is woonplaats pffff


                if not valid_birthdate:
                    error_messages.append("Geen correcte geboortedatum ingevuld.")
                if not first_name:
                    error_messages.append("Voornaam is niet ingevuld.")
                if not last_name:
                    error_messages.append("Achternaam is niet ingevuld.")
                if not birth_date:
                    error_messages.append("Geboortedatum is niet ingevuld.")
                if users_count > 0:
                    error_messages.append("Deze gebruikersnaam bestaat al.")
                if not valid_username_email:
                    error_messages.append("Geen correct email adres ingevuld.")
                if not username:
                    error_messages.append("Gebruikersnaam is niet ingevuld.")
                if not password:
                    error_messages.append("Wachtwoord is niet ingevuld.")
                if not postcode:
                    error_messages.append("Woonplaats is niet ingevuld.")
                if birth_date and datetime.datetime.strptime(request.POST.get('birth_date', ''), '%d-%m-%Y') > datetime.datetime.now():
                    error_messages.append("Geboortedatum kan niet in de toekomst zijn.")

            else:
                user = User.objects.create_user(username, username, password, first_name=first_name, last_name=last_name)
                userEx = UserExtra(user=user, birth_date=birth_date, adress=postcode, sex=gender, is_visitor=True, is_organizer=False)
                userEx.save()
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
        elif action_type == 'save':

            tickets_save_form_list = dict()
            # the forms here are purely used in the pay method
            for ticket in tickets:
                # loop over the amount of tickets ordered
                for i in range(int(ticket_key_amount_list[str(ticket.pk)])):
                    for k in range(ticket.person_amount):
                        key = str(i)+str(k)+str(ticket.pk)
                        tickets_save_form_list[key] = SendTicketsToForm(data=request.POST, prefix=key)

            all_valid = True

            # only try to validate if checkbox is true
            if request.POST.get('send_to', 'me') == 'others':

                for f in tickets_save_form_list:
                    form = tickets_save_form_list[f]

                    if form.has_changed() and form.is_valid() is False:
                        all_valid = False

                if all_valid is True:
                    return pay(request, event_id, event_name, tickets_save_form_list)
                else:
                    pass
            else:
                return pay(request, event_id, event_name, tickets_save_form_list)
    # moet onder login
    user_extra = user_extra_bd = ""
    if request.user.is_authenticated:
        user_extra = UserExtra.objects.filter(user=request.user).first()
        user_extra_bd = user_extra.birth_date.strftime("%d-%m-%Y")

    return render(request, 'ticketshop/ticket_overview.html', {
        'cur_event': event,
        'tickets': tickets_formatted,
        'tickets_form_list': tickets_form_list,
        'cshop': cshop,
        # 'url': url,
        'total_price': round(total+transaction_fee,2),
        'trans_fee': transaction_fee,
        'event_date': event_date,
        'user_extra': user_extra,
        'user_extra_bd': user_extra_bd,
        'error_messages': error_messages,
        'error_messages_login': error_messages_login,
        'userExtraFormValues': userExtraFormValues,
        'send_to': request.POST.get('send_to','me'),
        'GA_pagetype': 'Ticket overview'
    })


def getCurrentLanguage(request):
    return request.COOKIES.get('language', "NL")

def getLanguages(request):
    language_list = []
    
    languages = Languages.objects.filter()
    for lg in languages:
        language_list.append([lg.language_code,lg.language_name])
    return language_list

# return redirect(reverse('buy_ticket', kwargs={'event_id': event.id, 'event_name': event_name}))
def all_tickets_buyable(request, event):
    session_cart = cart.Cart(request)

    ticket_key_amount_list = session_cart.get_tickets(event.id)
    ticket_keys = [i for i in ticket_key_amount_list.keys()]
    tickets = Ticket.objects.filter(event=event, deleted=False, pk__in=ticket_keys)

    # tickets = Ticket.objects.filter(event=event, deleted=False).order_by('pk')

    for ticket in tickets:

        sold_total = SoldTicket.objects.filter(ticket_type=ticket, order_nr__order_paid=True).count()

        tickets_available = ticket.quantity - sold_total

        if tickets_available < 0:
            return False

    return True



def generate_uid():
    code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
    return 'YT'+code

# last step in the order process
from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
@csrf_exempt
def pay(request, event_id, event_name, tickets_save_form_list=None):

    scheme_url = request.is_secure() and "https" or "http"
    host_url = request.get_host()
    base_url = f"{scheme_url}://{host_url}"

    # if 'comes_from_iframe' in request.session and request.session['comes_from_iframe'] == True:
    #     return JsonResponse({'url': 'http://www.google.nl'})

    if request.method == 'POST':
        
        session_cart = cart.Cart(request)

        userExtra = UserExtra.objects.get(user=request.user)
        order = Order(user=request.user)

        email_allowed = session_cart.get_email_allowed(event_id)

        order.email_allowed = email_allowed
        order.ordered_in_language = utils.getCurrentLanguage(request)

        sales_channel = None
        if 'sales_channel' in request.session:
            sales_channel = request.session['sales_channel']
            sales_channel_url = Saleschannel.objects.get(pk=sales_channel)
            sales_channel_url = sales_channel_url.url_name

        event = Event.objects.get(pk=event_id)

        if event.show_covid19_info:
            order.agreed_covid19_info = 'y'

        order.sale_channel_id = sales_channel
        order.uid = generate_uid()
        order.event = event
        order.save()

        order_person_amount = 0
        order_sold_tickets = 0

        ticket_key_amount_list = session_cart.get_tickets(event_id)
        ticket_keys = [i for i in ticket_key_amount_list.keys()]
        tickets = Ticket.objects.filter(event=event, deleted=False, pk__in=ticket_keys)

        user_data_logged_in_user = {
            'user_object': request.user,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'birth_date': userExtra.birth_date,
            'gender': userExtra.sex,
            'address': userExtra.adress,
            'email': request.user.email
        }

        for ticket in tickets:
            person_amount = ticket.person_amount
            ticket_amount = int(ticket_key_amount_list[str(ticket.pk)])
            order_person_amount += (ticket_amount * person_amount)
            order_sold_tickets += ticket_amount
            ticket_price = float(ticket.price)/100
            ticket_service_costs_gross = shop.get_service_cost(ticket_price, 1, 0)
            ticket_service_costs = shop.get_service_cost(ticket_price, 1, event.service_cost_discount_cents)
            ticket_service_costs_discount = ticket_service_costs_gross - ticket_service_costs

            for i in range(int(ticket_amount)):

                # sold_ticket = SoldTicket(
                #     ticket_gen_id=gen_id,
                #     ticket_type=ticket,
                #     user=request.user,
                #     sold_date=datetime.datetime.now(),
                #     event=event, order_nr=order,
                #     first_name=request.user.first_name,
                #     last_name=request.user.last_name,
                #     birth_date=userExtra.birth_date,
                #     sex=userExtra.sex,
                #     adress=userExtra.adress,
                #     email_allowed=order.email_allowed,
                #     price=ticket.price/100 #ticket price is in cents bah!
                # )
                # ticket, user_data, event, order, email_allowed='', price=None, is_subticket=False, primary_ticket=None

                # sold_ticket.save()
                # the first record is skipped
                primary_ticket = {}
                for k in range(ticket.person_amount):
                    key = str(i)+str(k)+str(ticket.pk)
                    additional_user_data_form = tickets_save_form_list[key]
                    # if k==0 its more or less a normal save
                    # tickets that have or do not have have a person_amount bigger then 0
                    # are save here
                    if k == 0:

                        if additional_user_data_form.has_changed() and request.POST.get('send_to', 'me') == 'others':

                            if additional_user_data_form.is_valid():
                                data = additional_user_data_form.cleaned_data
                                data['user_object'] = request.user

                                primary_ticket = save_sold_ticket(
                                    ticket=ticket,
                                    event=event,
                                    order=order,
                                    user_data=data,
                                    price=ticket_price,
                                    service_costs_gross=ticket_service_costs_gross,
                                    service_costs=ticket_service_costs,
                                    service_costs_discount=ticket_service_costs_discount,
                                    email_allowed=order.email_allowed
                                )
                            else:
                                return
                        else:
                            primary_ticket = save_sold_ticket(
                                ticket=ticket,
                                event=event,
                                order=order,
                                user_data=user_data_logged_in_user,
                                price=ticket_price,
                                service_costs_gross=ticket_service_costs_gross,
                                service_costs=ticket_service_costs,
                                service_costs_discount=ticket_service_costs_discount,
                                email_allowed=order.email_allowed
                            )
                        # just save
                    else:
                        # set is_subticket op True
                        # set primary_ticket op last inserted id
                        # set price op 0
                        if tickets_save_form_list[key].has_changed() and request.POST.get('send_to', 'me') == 'others':
                            if additional_user_data_form.is_valid():
                                data = additional_user_data_form.cleaned_data
                                data['user_object'] = request.user
                                primary_ticket = save_sold_ticket(
                                    ticket=ticket,
                                    event=event,
                                    order=order,
                                    user_data=data,
                                    is_subticket=True,
                                    primary_ticket=primary_ticket
                                )
                        else:
                            # save with subticket
                            save_sold_ticket(
                                ticket=ticket,
                                event=event,
                                order=order,
                                user_data=user_data_logged_in_user,
                                is_subticket=True,
                                primary_ticket=primary_ticket
                            )

        order_info = shop.get_price_and_ticket_amount(ticket_key_amount_list, tickets)

        order_price = float( order_info['price'])
        order_ticket_amount_for_service_cost = int(order_info['tickets_amount_for_service_costs'])

        order_service_costs_gross = shop.get_service_cost(  order_price, 
                                                order_ticket_amount_for_service_cost,
                                                0) 
        order_service_costs = shop.get_service_cost(  order_price, 
                                                order_ticket_amount_for_service_cost,
                                                event.service_cost_discount_cents) 
        order_service_costs_discount = order_service_costs_gross - order_service_costs
        #service_costs = shop.get_service_cost(order_info['price'], order_info['tickets_amount_for_service_costs']) - (
        #            (event.service_cost_discount_cents * order_info['tickets_amount_for_service_costs']) / 100.0)
        #if service_costs < 0:
        #    service_costs = 0

        order_price_with_service_costs = order_price + order_service_costs

        # alleen gratis ticket
        if order_price == 0:
            order.order_paid = True
            order.mollie_id = ''
            # send_mail_and_create_pdfs.delaay(order=order)
            send_mail_order(order_id=order.pk, base_url=base_url)

            order.mail_send = True
            order.save()

            return redirect(reverse('buy_ticket_mollie', kwargs={'order_id': order.pk}))

        else:
            if request.session.get('comes_from_iframe', False):
                request.session['payment_data'] = {
                    'price': order_price_with_service_costs,
                    'title': event.title + ", Order nr: " + str(order.id),
                    'event_id': event.pk,
                    'order_id': order.id
                }
            else:
                all_tickets_buyablee = all_tickets_buyable(request, event)
                if not all_tickets_buyablee:
                    return redirect(reverse('buy_ticket', kwargs={'event_id': event.id, 'event_name': event_name,
                                                                  'some_tickets_soldout': 'soldout'}))
                payment = shop.payment_custom(
                    order_price_with_service_costs,
                    event.title + ", Order nr: " + str(order.id),
                    event,
                    order.id
                )
                order.mollie_id = payment['id']

            order.price = order_price
            order.service_costs = order_service_costs
            order.service_costs_gross = order_service_costs_gross
            order.service_costs_discount = order_service_costs_discount
            order.sold_tickets  = order_sold_tickets
            order.person_amount = order_person_amount
            order.save()
        if order_price == 0:
            return redirect(reverse('buy_ticket_mollie', kwargs={'order_id': order.id}))
        else:
            if request.session.get('comes_from_iframe', False):
                # request.session['payment_url'] = payment.getPaymentUrl()
                return JsonResponse({'url': reverse(iframe_redirect)})

            else:
                from yourtickets.common.log import writeOrderLog
                from ticketshop.models import Orderlog
                writeOrderLog(order_id=order.id, type=Orderlog.TYPE_BEFORE_MOLLIE_AANVRAAG)
                all_tickets_buyablee = all_tickets_buyable(request, event)

                if not all_tickets_buyablee:
                    return redirect(reverse('buy_ticket', kwargs={'event_id': event.id, 'event_name': event_name,
                                                                  'some_tickets_soldout': 'soldout'}))

                return redirect(payment.checkout_url)

    else:
        return render(request, 'app/error.html', {})


def save_sold_ticket(ticket, event, order, user_data, email_allowed=False, price=0.0, 
                    service_costs=0.0, service_costs_gross=0.0, service_costs_discount=0.0, is_subticket=False, primary_ticket=None):

    # user_data = {
    #     'user_object': '', # always there
    #     'first_name': '', # always there
    #     'last_name': '', # only with no additional data
    #     'birth_date': '', # only with no additional data
    #     'sex': '', # always there
    #     'address': '', # only with no additional data
    #     'email': '' # allways there
    # }

    t = SoldTicket(
        ticket_gen_id=shop.random_ticket_gen(),
        ticket_type=ticket,
        user=user_data['user_object'],
        sold_date=datetime.datetime.now(),
        event=event,
        order_nr=order,
        first_name=user_data.get('first_name'),
        last_name=user_data.get('last_name',''),
        birth_date=user_data.get('birth_date', None),
        sex=user_data.get('gender'),
        adress=user_data.get('address',''),
        email_allowed=email_allowed,
        price=price, #ticket price is in cents bah!
        service_costs_gross=service_costs_gross,
        service_costs=service_costs,
        service_costs_discount=service_costs_discount,
        email=user_data.get('email'),
        is_subticket=is_subticket,
        primary_ticket=primary_ticket
    )

    t.save()

    return t



class EventViewSet(viewsets.ModelViewSet):

    serializer_class = EventSerializer

    def get_queryset(self):

        querysetf = EventOrganiser.objects.filter(user=self.request.user)
        resultlist = []
        for item in querysetf:
            resultlist.append(item.event.id)

        queryset = Event.objects.filter(pk__in=resultlist)
        return queryset

class TicketList(viewsets.ModelViewSet):

    serializer_class = TicketSerializer

    def get_queryset(self):

        event = self.kwargs['event']
        querysetf = Ticket.objects.filter(event=event)
        resultlist = []
        for item in querysetf:
            resultlist.append(item.id)

        print("yeah")
        guest_tickets = SoldTicket.objects.filter(event=event, is_guest_ticket=True)
        special_guest_tickets = SoldTicket.objects.filter(event=event, is_special_guest_ticket=True)
        sold_tickets = SoldTicket.objects.filter(event=event, ticket_type__in=resultlist ,order_nr__order_paid=True)
        records = sold_tickets.union(guest_tickets, special_guest_tickets)
        return records
        #return SoldTicket.objects.filter(Q(event=event), Q(ticket_type__in=resultlist) | Q(is_guest_ticket=True) | Q(is_special_guest_ticket=True),order_nr__order_paid=True)

class TicketCheck(viewsets.ModelViewSet):

    serializer_class = TicketSerializer

    def get_queryset(self):

        gen_id = self.kwargs['gen_id']
        querysetf = SoldTicket.objects.get(ticket_gen_id=gen_id)
        querysetf.checked = True
        querysetf.save()
        querysetf = SoldTicket.objects.filter(ticket_gen_id=gen_id)
        return querysetf

class TicketCheckGet(viewsets.ModelViewSet):

    serializer_class = TicketSerializer

    def get_queryset(self):

        gen_id = self.kwargs['gen_id']
        querysetf = SoldTicket.objects.filter(ticket_gen_id=gen_id)
        return querysetf


def guestlist_profile(request, hash):
    guest_ticket = GuestTickets.objects.filter(hash=hash)

    if len(guest_ticket) == 0:
        raise Http404


    guest_ticket = guest_ticket.first()

    event = guest_ticket.event

    if request.POST:

        birth_date = datetime.datetime.strptime(request.POST.get('birth_date', ''), '%d-%m-%Y').strftime('%Y-%m-%d')
        postcode = request.POST.get('postcode', '')
        gender = request.POST.get('gender', 'M')

        existing_soldtickets = SoldTicket.objects.filter(guest_ticket=guest_ticket)

        # if the ticket is allready some time generated but the user request this url again
        # dont generate the ticket again.. instead just send the ticket again to the user
        if len(existing_soldtickets) > 0:
            send_mail_and_create_pdf_for_ticket(existing_soldtickets.first())
            return HttpResponseRedirect(reverse('guestlist_thankyou', kwargs={'hash':hash}))

        if birth_date != '' and postcode != '':
            # userex = UserExtra(user=request.user, birth_date=birth_date, adress=postcode, sex=gender)
            # userex.save()

            t = SoldTicket(
                ticket_gen_id=shop.random_ticket_gen(),
                # ticket_type=Null,
                # user=user_data['user_object'],
                sold_date=datetime.datetime.now(),
                event=event,
                # order_nr=order,
                first_name=guest_ticket.name,
                last_name='',
                birth_date=birth_date,
                sex=gender,
                adress=postcode,
                email_allowed=False,
                price=0, #ticket price is in cents bah!
                email=guest_ticket.email,
                # is_subticket=is_subticket,
                primary_ticket=None,
                is_guest_ticket=True,
                guest_ticket=guest_ticket
            )

            t.save()

            send_mail_and_create_pdf_for_ticket(t)

            return HttpResponseRedirect(reverse('guestlist_thankyou', kwargs={'hash': hash}))

    return render(request, 'ticketshop/guestlist_profile.html')


def guestlist_thankyou(request, hash):

    guest_ticket = GuestTickets.objects.filter(hash=hash)

    if len(guest_ticket) == 0:
        raise Http404

    guest_ticket = guest_ticket.first()

    event = guest_ticket.event

    cshop = TicketShopCustom.objects.filter(event_id=event.id).first()

    url = reverse('buy_ticket', kwargs={'event_id': event.id, 'event_name': event.event_url})

    return render(request, 'ticketshop/guestlist_thankyou.html', {
        'event': event,
        'cshop': cshop,
        'url': url,
        'hostname': settings.HOSTNAME
    })

from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def multiticketshop(request, multiticketshop_id):

    multiticketshop_obj = Multiticketshop.objects.filter(pk=multiticketshop_id).first()

    if not multiticketshop_obj:
        raise Http404

    # organiser = multiticketshop.organiser

    events = MultiticketshopEvents.objects.filter(multiticketshop=multiticketshop_obj).select_related('event').order_by('order')

    return render(request, 'ticketshop/multiticketshop.html', {
        'events': events,
        'multishop': multiticketshop_obj
    })
