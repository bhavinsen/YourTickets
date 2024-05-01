import json
import csv
import string
import random
import os
import pyexcel as pe

from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from dashboard.forms.visitors import GuestlistUploadForm
from ticketshop.models import (
    Event, EventOrganiser,
    Ticket, SoldTicket,
    GuestTickets
)
from django.shortcuts import render

import datetime
from django.utils import timezone
from django.conf import settings
from django.db.models import F, Sum, Q

from django.http import HttpResponse

from django.urls import reverse
from yourtickets.common import shop
from dashboard.forms.visitors import SendticketForm
from yourtickets.common.ticket import send_mail_and_create_pdf_for_ticket
from django.http import JsonResponse
from django.core.mail import EmailMessage
from youradmin.common.decorators import is_event_from_user

from dashboard.common.base_vars import base_vars
from yourtickets.common.mail import create_mail


@is_event_from_user(login_url='login')
@login_required(login_url='login')
def index(request, event_id):

    event = Event.objects.filter(pk=event_id).first()
    event_url_str = event.event_url
    if event_url_str == "":
        event_url_str = event.title
    visitors = SoldTicket.objects.filter(event=event, order_nr__order_paid=True).order_by('-id')

    start = timezone.localtime(event.start_date)
    end = timezone.localtime(event.end_date)
    event_date = start.strftime("%d %B %y | %H:%M") + " - " + end.strftime("%H:%M")

    form_with_data = SendticketForm(prefix="with_data")
    form_without_data = SendticketForm(prefix="without_data")

    email_send = False

    if request.POST:

        if request.POST.get('type') == 'with':
            form_with_data = SendticketForm(request.POST, prefix="with_data")
            if form_with_data.is_valid():
                form_data = form_with_data.cleaned_data
                rec = GuestTickets(
                    hash=id_generator(30),
                    name=form_data['name'],
                    email=form_data['email'],
                    event=event
                )
                rec.save()

                send_direct_ticket(event=event, name=form_data['name'], email=form_data['email'], hash=rec.hash)
                email_send = True
        elif request.POST.get('type') == 'without':
            form_without_data = SendticketForm(request.POST, prefix="without_data")
            if form_without_data.is_valid():
                form_data = form_without_data.cleaned_data

                guest_ticket = GuestTickets(
                    hash=id_generator(30),
                    name=form_data['name'],
                    email=form_data['email'],
                    event=event
                )
                guest_ticket.save()

                t = SoldTicket(
                    ticket_gen_id=shop.random_ticket_gen(),
                    # ticket_type=Null,
                    # user=user_data['user_object'],
                    sold_date=datetime.datetime.now(),
                    event=event,
                    # order_nr=order,
                    first_name=guest_ticket.name,
                    last_name='',
                    birth_date=None,
                    sex='N',
                    adress='',
                    email_allowed=False,
                    price=0, # ticket price is in cents bah!
                    service_costs=0,
                    service_costs_gross=0,
                    service_costs_discount=0,
                    total=0,
                    email=guest_ticket.email,
                    # is_subticket=is_subticket,
                    primary_ticket=None,
                    is_special_guest_ticket=True,
                    guest_ticket=guest_ticket
                )

                t.save()

                send_mail_and_create_pdf_for_ticket(t, 'ticket_mail_without_data')
                from yourtickets.tasks import (
                    send_mail_order
                )
                # send_mail_order.delay(order_id=order.pk, email=None)
                email_send = True

    '''
        get the new event
    '''
    ticket_objects = Ticket.objects.filter(event_id=event)
    financial_overview = list()
    total_price = 0

    for item in ticket_objects:

        sold_tickets_for_ticket = SoldTicket.objects.filter(
            ticket_type=item, order_nr__order_paid=True,
            is_subticket=False, is_guest_ticket=False,
            is_special_guest_ticket=False
        )

        # holds prices and amount of that price
        ticket_price_types = []

        for sold_ticket in sold_tickets_for_ticket:

            price = sold_ticket.price
            # als de verkochte ticket geen prijs heeft: (alleen voor dingen van het verleden)
            if sold_ticket.price == 0:
                price = float(item.price) / 100

            found = False
            for t in ticket_price_types:
                if t['price'] == price:
                    t['amount'] += 1
                    found = True
                    break

            if not found:
                ticket_price_types.append({
                    'price': price,
                    'amount': 1
                })

        for ticket_price_type in ticket_price_types:
            price = ticket_price_type['price']
            amount = ticket_price_type['amount']
            financial_overview.append({
                'name': item.name,
                'ticket_price': round(float(price),2),
                'total_sold': amount,
                'quantity': item.quantity,
                'total_price': round(amount * float(price), 2),
                'id': item.id
            })
            total_price += round(amount * float(price), 2)

    total_tickets_sold = SoldTicket.objects.filter(event=event, order_nr__order_paid=True, is_subticket=False).count()
    max_tickets = Ticket.objects.filter(event_id=event).aggregate(quantity=Sum(F('quantity')))
    max_tickets = max_tickets['quantity']

    guest_ticket = SoldTicket.objects.filter(event=event, is_guest_ticket=True).count()
    special_guest_ticket = SoldTicket.objects.filter(event=event, is_special_guest_ticket=True).count()

    total_tickets_sold += guest_ticket
    total_tickets_sold += special_guest_ticket

    return render(request, 'dash/event/visitors.html', base_vars(request, event_id, {
        'visitors': visitors,
        'event_date': event_date,
        'form_with_data': form_with_data,
        'form_without_data': form_without_data,
        'financial_overview': financial_overview,
        'total_tickets_sold': total_tickets_sold,
        'max_tickets': max_tickets,
        'total_price': total_price,
        'guest_ticket': guest_ticket,
        'special_guest_ticket': special_guest_ticket,
        'email_send': email_send,
        'datatables_config': json.dumps({
            'columns': get_cols(),
            'info': False,
            'searching': False,
            'ordering': False,
            'ajax': {
                'url': reverse('dashboard_visitors_getlist', kwargs={'event_id': event_id, 'ticket_id': 'placeholder'})
            }
        })
    }))


def send_direct_ticket(event, name, hash, email):

    url = settings.HOSTNAME + reverse('guestlist_profile', kwargs={'hash': hash})

    content = render_to_string('emails/content_guestlist.html', {
        'event': event,
        'name': name,
        'url': url
    })

    create_mail({
        'content': content
    }, 'Hello there!', email)


@is_event_from_user(login_url='login')
@login_required(login_url='login')
def visitors_send(request, event_id):

    event = Event.objects.get(pk=event_id)

    ticket_type = request.POST.get('ticket_type')

    name = request.POST.get('name', False)
    email = request.POST.get('email', False)

    if not email or not name:
        return JsonResponse({'success': False, 'errors': 'Email or name not selected' })

    file_name = settings.TEMP_TICKET_CREATION_DIR + request.session['filename']

    sheet = pe.get_sheet(file_name=file_name, name_columns_by_row=0)

    records = sheet.to_records()

    for record in records:
        rec_mail = record[email].strip().replace('mailto:', '')
        rec_name = record[name].strip()

        rec = GuestTickets(
                hash=id_generator(30),
                name=rec_name,
                email=rec_mail,
                event=event,
                delayed_send=True,
                type=ticket_type
            )
        rec.save()

    email_message = 'event name: ' + event.title + ' \n'
    email_message += 'organisator email: ' + str(request.user.email) + ' \n'
    email_message += 'https://yourtickets.nl/youradmin'

    msg = EmailMessage('New guestlist batch ready (total tickets:'+str(len(records))+') ' + event.title, email_message,
                           'noreply@yourtickets.nl', ['info@yourtickets.nl', 'almerelc@gmail.com'])
    msg.send()

    return JsonResponse({'success': True})


@is_event_from_user(login_url='login')
@login_required(login_url='login')
def visitors_upload(request, event_id):
    if request.method == 'POST':
        form = GuestlistUploadForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['importfile'], event_id)
            file_name = settings.TEMP_TICKET_CREATION_DIR + event_id + os.path.splitext(request.FILES['importfile'].name)[1]
            request.session['filename'] = event_id + os.path.splitext(request.FILES['importfile'].name)[1]
            sheet = pe.get_sheet(file_name=file_name, name_columns_by_row=0)
            return JsonResponse({'success': True, 'sheet': sheet.to_dict()})
        else:
            pass
        return JsonResponse({'success': False, 'errors': str(form.errors) })


@csrf_exempt
@is_event_from_user(login_url='login')
@login_required(login_url='login')
def ajax_get_visitors_for_ticket(request, event_id, ticket_id):
    if not request.user.is_authenticated:
        return
    event = Event.objects.get(pk=event_id)

    event_org = EventOrganiser.objects.filter(user=request.user, event=event)

    if len(event_org) == 0:
        return

    if ticket_id == 'placeholder':
        return JsonResponse({
            "recordsTotal": 0,
            "recordsFiltered": 0,
            "data": []
        })

    source = request.POST

    page_length = int( source.get('length', 20) )
    data_start = int( source.get('start', 0) )
    data_end = data_start + page_length

    if ticket_id == 'guest_ticket':
        records = SoldTicket.objects.filter(event=event, is_guest_ticket=True ).order_by('-id')

    elif ticket_id == 'special_guest_ticket':

        records = SoldTicket.objects.filter(event=event, is_special_guest_ticket=True).order_by('-id')

                          
    elif ticket_id == 'all':

        guest_records = SoldTicket.objects.filter(event=event, is_guest_ticket=True )
        special_guest_records = SoldTicket.objects.filter(event=event, is_special_guest_ticket=True)
        records = SoldTicket.objects.filter(event=event,order_nr__order_paid=True ,is_subticket=False)

        records = records.union(guest_records , special_guest_records ).order_by('-id')      

        total = len(records)                                  
    else:
        ticket = Ticket.objects.filter(pk=ticket_id)

        if len(ticket) == 0:
            return JsonResponse({
                "recordsTotal": 0,
                "recordsFiltered": 0,
                "data": []
            })
        else:
            ticket = ticket.first()

        # if the ticket doesnt belong to this user just skip all
        event_org_check2 = EventOrganiser.objects.filter(user=request.user, event=ticket.event)

        if len(event_org_check2) == 0:
            return

        records = SoldTicket.objects.filter(ticket_type=ticket, order_nr__order_paid=True,is_subticket=False ).order_by('-id')


    total = len(records)
    records = records[data_start:data_end]    
    final_data = []

    for record in records:
        final_data.append({
            'id': record.id,
            'name': record.first_name + ' ' + record.last_name,
            'email': record.email,
            'gender': record.sex,
            'birthdate': record.birth_date,
            'email_allowed': record.email_allowed
        })

    # print(records)

    return JsonResponse({
        "recordsTotal": total,
        "recordsFiltered": total,
        "data": final_data
    })


@is_event_from_user(login_url='login')
@login_required(login_url='login')
def download_visitors_per_ticket(request, event_id, ticket_id):
    if not request.user.is_authenticated:
        return
    event = Event.objects.get(pk=event_id)

    event_org = EventOrganiser.objects.filter(user=request.user, event=event)

    if len(event_org) == 0:
        return

    if ticket_id == 'placeholder':
        return JsonResponse({
            "recordsTotal": 0,
            "recordsFiltered": 0,
            "data": []
        })

    if ticket_id == 'guest_ticket':
        records = SoldTicket.objects.filter(event=event,  is_guest_ticket=True).order_by('-id')
    elif ticket_id == 'special_guest_ticket':
        records = SoldTicket.objects.filter(event=event, is_special_guest_ticket=True).order_by('-id')
    elif ticket_id == 'all':
        guests_records = SoldTicket.objects.filter(event=event, is_guest_ticket=True).order_by('-id')
        special_guests_records = SoldTicket.objects.filter(event=event, is_special_guest_ticket=True).order_by('-id')
        records = SoldTicket.objects.filter(event=event,  order_nr__order_paid=True,is_subticket=False ).order_by('-id')
        records = records.union(guests_records,special_guests_records).order_by('-id')
    else:
        ticket = Ticket.objects.filter(pk=ticket_id)

        if len(ticket) == 0:
            return JsonResponse({
                "recordsTotal": 0,
                "recordsFiltered": 0,
                "data": []
            })
        else:
            ticket = ticket.first()

        # if the ticket doesnt belong to this user just skip all
        event_org_check2 = EventOrganiser.objects.filter(user=request.user, event=ticket.event)

        if len(event_org_check2) == 0:
            return

        records = SoldTicket.objects.filter(ticket_type=ticket, order_nr__order_paid=True,is_subticket=False).order_by('-id')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="visitors.csv"'
    writer = csv.writer(response)
    writer.writerow(["voornaam", "achternaam", "emailadres", "geslacht", "geboortedetum"])
    
    for visitor in records:
        writer.writerow([
            visitor.first_name,
            visitor.last_name,
            visitor.email  if visitor.user is None  else visitor.user.email,
            visitor.sex,
            visitor.birth_date,
                ])
    return response


def downloadVisitorlog(request, event_id):
    querysetf = EventOrganiser.objects.filter(user=request.user, event__id=event_id).order_by('-pk')
    event = querysetf.first().event
    visitors = SoldTicket.objects.filter(event=event, order_nr__order_paid=True).order_by('-id')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="visitors.csv"'
    writer = csv.writer(response)
    writer.writerow(["voornaam","achternaam","emailadres","geslacht","geboortedetum", "Toestemming voor marketing","order id"])
    for visitor in visitors:
        writer.writerow([
            visitor.first_name,
            visitor.last_name,
            visitor.user.email,
            visitor.sex, visitor.birth_date,
            visitor.email_allowed,
            visitor.order_nr.id+1000])
    return response

@csrf_exempt
def ajax_delete_ticket(request, ticket_id):
    if not request.user.is_authenticated:
        return

    ticket = SoldTicket.objects.filter(pk=ticket_id)

    if len(ticket) == 0:
        return
    else:
        ticket = ticket.first()

    # if the ticket doesnt belong to this user just skip all
    event_org_check2 = EventOrganiser.objects.filter(user=request.user, event=ticket.event)

    if len(event_org_check2) == 0:
        return

    GuestTickets.objects.get(pk=ticket.guest_ticket_id).delete()

    ticket.delete()

    return JsonResponse({'success': True})

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_cols():
    return [
        {"title": "Naam", "data": "name"},
        {"title": "E-mail", "data": "email"},
        {"title": "Geslacht", "data": "gender"},
        {"title": "Geboortedatum", "data": "birthdate", "renderer": "test"},
        {"title": "Email allowed", "data": "email_allowed"}
    ]


def handle_uploaded_file(f, event_id):

    file_extension = os.path.splitext(f.name)[1]

    with open(settings.TEMP_TICKET_CREATION_DIR+event_id+file_extension, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
