import json, datetime
import csv
import string
import random
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.db.models import F, Sum, Count
from django.core.mail import EmailMessage
from django.urls import reverse
from django.template.loader import render_to_string

import pyexcel as pe
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, api_view, permission_classes

from ticketshop.models import (
    Event,
    Ticket,
    SoldTicket,
    EventOrganiser,
    GuestTickets
)
from dashboard.forms.visitors import GuestlistUploadForm, SendticketForm
from yourtickets.common.ticket import send_mail_and_create_pdf_for_ticket
from yourtickets.common import shop
from yourtickets.common.mail import create_mail


def getUser(request):

    return request.user
    # return get_user_model().objects.filter(pk=271).first()


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_event_tickets(request, id):
    user = request.user
    # eventorganiser__user__pk=user.pk, 201
    event = Event.objects.filter(eventorganiser__user__pk=user.pk, pk=id, removed=False).first()

    event_tickets = Ticket.objects.filter(event_id=event)

    result_tickets = []

    total_tickets_sold = 0
    total_amount = 0

    for ticket in event_tickets:
        sold_tickets_for_ticket = SoldTicket.objects.filter(
            ticket_type=ticket, order_nr__order_paid=True,
            is_subticket=False, is_guest_ticket=False,
            is_special_guest_ticket=False
        )
        amount_sold = sold_tickets_for_ticket.count()
        total_amount_price = round(amount_sold * float(ticket.price / 100), 2)

        total_amount += total_amount_price
        total_tickets_sold += amount_sold

        result_tickets.append({
            'name': ticket.name,
            'amount_sold': amount_sold,
            'amount_available': ticket.quantity,
            'ticket_price': ticket.price / 100,
            'total_amount_price': total_amount_price,
            'id': ticket.pk
        })

    guestlist_count = SoldTicket.objects.filter(event=event, is_special_guest_ticket=True).count()

    # add the guestlist manually
    result_tickets.append({
        'name': 'Gastenlijst',
        'amount_sold': guestlist_count,
        'amount_available': 0,
        'ticket_price': 0,
        'total_amount_price': 0,
        'id': 'guest_ticket'
    })

    return JsonResponse({
        'tickets': result_tickets,

        'total_tickets_sold': total_tickets_sold,
        'total_amount': total_amount+guestlist_count

    })


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_single_ticket(request, id):
    user = getUser(request)
    try:
        event = Event.objects.get(eventorganiser__user__pk=user.pk, pk=id, removed=False)
    except:
        return JsonResponse({'success': False}, safe=False)

    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)

    form_without_data = SendticketForm(data)
    if form_without_data.is_valid():
        form_data = form_without_data.cleaned_data

        guest_ticket = GuestTickets(
            hash=id_generator(30),
            name=form_data['name'],
            email=form_data['email'],
            event=event,
            type='without'
        )
        guest_ticket.save()

        gender = data.get('gender', 'N')
        if gender == 'M':
            gender = 'M'
        elif gender == 'F':
            gender = 'F'

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
            sex=gender,
            adress='',
            email_allowed=False,
            price=0,
            email=guest_ticket.email,
            # is_subticket=is_subticket,
            primary_ticket=None,
            is_special_guest_ticket=True,
            guest_ticket=guest_ticket
        )

        t.save()

        send_mail_and_create_pdf_for_ticket(t, 'ticket_mail_without_data')

    return JsonResponse({'success': True})


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


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_ticket(request, id):
    user = getUser(request)
    try:
        event = Event.objects.get(eventorganiser__user__pk=user.pk, pk=id, removed=False)
    except:
        return JsonResponse({'success': False}, safe=False)

    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)

    sold_ticket = SoldTicket.objects.filter(pk=data.get('ticket_id'), event=event, is_subticket=False, is_guest_ticket=False,
                              is_special_guest_ticket=True).first()
    if not sold_ticket:
        return JsonResponse({'success': False}, safe=False)


    sold_ticket.guest_ticket.delete()
    return JsonResponse({'success': True}, safe=False)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def visitors_send(request, id):
    user = getUser(request)
    try:
        event = Event.objects.get(eventorganiser__user__pk=user.pk, pk=id, removed=False)
    except:
        return JsonResponse({'success': False}, safe=False)

    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)

    ticket_type = data.get('ticket_type')
    name = data.get('name', False)
    email = data.get('email', False)

    if email is False or name is False:
        return JsonResponse({'success': False, 'errors': 'Email or name not selected' })

    file_name = settings.TEMP_TICKET_CREATION_DIR + str(event.pk) + '.xlsx'

    sheet = pe.get_sheet(file_name=file_name, name_columns_by_row=0)

    records = sheet.to_records()

    for record in records:
        # OrderedDict([(u'naam', u'martijn'), (u'email', u'almerelc@gmail.com')])
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
    email_message += 'organisator email: ' + str(user.email) + ' \n'
    email_message += 'https://yourtickets.nl/youradmin'

    msg = EmailMessage('New guestlist batch ready (total tickets:'+str(len(records))+') ' + event.title, email_message,
                           'noreply@yourtickets.nl', ['info@yourtickets.nl', 'almerelc@gmail.com'])
    msg.send()

    return JsonResponse({'success': True})


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# @is_event_from_user(login_url='login')
# @login_required(login_url='login')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def visitors_upload(request, id):
    if request.method == 'POST':
        form = GuestlistUploadForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['importfile'], id)
            file_name = settings.TEMP_TICKET_CREATION_DIR + id + '.xlsx'
            # request.session['filename'] = event_id + os.path.splitext(request.FILES['importfile'].name)[1]
            sheet = pe.get_sheet(file_name=file_name, name_columns_by_row=0)
            return JsonResponse({'success': True, 'sheet': sheet.to_dict()})
        else:
            pass
        return JsonResponse({'success': False, 'errors': str(form.errors) })


def handle_uploaded_file(f, event_id):
    # file_extension = os.path.splitext(f.name)[1]
    with open(settings.TEMP_TICKET_CREATION_DIR+event_id+'.xlsx', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_visitors_for_ticket(request, id, ticket_id):

    user = getUser(request)

    try:
        # eventorganiser__user__pk=user.pk 201
        event = Event.objects.get(eventorganiser__user__pk=user.pk, pk=id, removed=False)
    except:
        return JsonResponse({'success': False}, safe=False)

    # now every guest_ticket is a special_guest ticket
    # we sturen alleen nog direct tickets zonder dataverzameling
    # en dat is dan een special_guest_ticket
    if ticket_id == 'guest_ticket':

        records = SoldTicket.objects.filter(event=event, is_subticket=False, is_guest_ticket=False,
                        is_special_guest_ticket=True).order_by('-id')
        # total = SoldTicket.objects.filter(event=event, is_subticket=False, is_guest_ticket=True,
        #                 is_special_guest_ticket=False).order_by('-id').count()

    # elif ticket_id == 'special_guest_ticket':
    #     # event = Event.objects.filter(pk=event_id)
    #     records = SoldTicket.objects.filter(event=event, is_subticket=False, is_guest_ticket=False,
    #                     is_special_guest_ticket=True).order_by('-id')
    #     # total = SoldTicket.objects.filter(event=event, is_subticket=False, is_guest_ticket=False,
    #     #                 is_special_guest_ticket=True).order_by('-id').count()
    elif ticket_id == 'all':
        # event = Event.objects.filter(pk=event_id)
        records = SoldTicket.objects.filter(event=event, order_nr__order_paid=True, is_subticket=False,
                                            is_guest_ticket=False,
                                            is_special_guest_ticket=False).order_by('-id')
        # total = SoldTicket.objects.filter(event=event,order_nr__order_paid=True, is_subticket=False,
        #                                   is_guest_ticket=False,
        #                                   is_special_guest_ticket=False).order_by('-id').count()
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
        event_org_check2 = EventOrganiser.objects.filter(user=user, event=ticket.event)

        if len(event_org_check2) == 0:
            return

        records = SoldTicket.objects.filter(ticket_type=ticket, order_nr__order_paid=True,is_subticket=False, is_guest_ticket=False,
                        is_special_guest_ticket=False).order_by('-id')
        # total = SoldTicket.objects.filter(ticket_type=ticket, order_nr__order_paid=True,is_subticket=False, is_guest_ticket=False,
        #                 is_special_guest_ticket=False).order_by('-id').count()

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
        # "recordsTotal": total,
        # "recordsFiltered": total,
        "data": final_data
    })



@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def downloadVisitors(request, id):
    user = getUser(request)

    try:
        event = Event.objects.get(eventorganiser__user__pk=request.user.pk, pk=id, removed=False)

    except:
        return JsonResponse({'success': False}, safe=False)



    visitors = SoldTicket.objects.filter(event=event, order_nr__order_paid=True,
            is_subticket=False, is_guest_ticket=False,
            is_special_guest_ticket=False).order_by('-id')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="visitors.csv"'
    writer = csv.writer(response)
    writer.writerow(["voornaam","achternaam","emailadres","geslacht","geboortedetum", "Toestemming voor marketing"])
    for visitor in visitors:
        writer.writerow([
            visitor.first_name,
            visitor.last_name,
            visitor.user.email,
            visitor.sex,
            visitor.birth_date,
            'ja' if visitor.email_allowed else 'nee',
            ])

    # add the guest tickets
    visitors = SoldTicket.objects.filter(event=event, is_subticket=False, is_guest_ticket=False,
                                         is_special_guest_ticket=True).order_by('-id')
    for visitor in visitors:
        writer.writerow([
            visitor.first_name,
            visitor.last_name,
            visitor.email,
            visitor.sex,
            visitor.birth_date,
            'ja' if visitor.email_allowed else 'nee',
            ])
    return response


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def downloadVisitorsPerTicket(request, id, ticket_id):
    user = getUser(request)

    try:
        event = Event.objects.get(eventorganiser__user__pk=user.pk, pk=id, removed=False)
    except:
        return JsonResponse({'success': False}, safe=False)


    if ticket_id == 'guest_ticket':
        visitors = SoldTicket.objects.filter(event=event, is_subticket=False, is_guest_ticket=False,
                                             is_special_guest_ticket=True).order_by('-id')
    else:
        ticket = Ticket.objects.get(event=event, pk=ticket_id)
        visitors = SoldTicket.objects.filter(event=event, ticket_type=ticket, order_nr__order_paid=True,
                is_subticket=False, is_guest_ticket=False,
                is_special_guest_ticket=False).order_by('-id')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="visitors.csv"'
    writer = csv.writer(response)
    writer.writerow(["voornaam","achternaam","emailadres","geslacht","geboortedetum", "Toestemming voor marketing"])
    for visitor in visitors:
        writer.writerow([
            visitor.first_name,
            visitor.last_name,
            visitor.email,
            visitor.sex,
            visitor.birth_date,
            'ja' if visitor.email_allowed else 'nee',
            ])


    return response
