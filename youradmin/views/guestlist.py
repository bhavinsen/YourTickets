import json
import csv
import operator
import os.path

import datetime
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import (
    render
)
from django.db.models import  ObjectDoesNotExist
from django.urls import reverse
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
from django.template import loader

from yourtickets.common import shop
from yourtickets.common.ticket import send_mail_and_create_pdf_for_ticket

from ticketshop.models import GuestTickets, SoldTicket, Event
from yourtickets.common.mail import create_mail



def get_cols_list():
    # hash = id_generator(30),
    # name = rec_name,
    # email = rec_mail,
    # event = event,
    # delayed_send = True,
    # type = ticket_type

    return [
        {"title": "id", "data": "pk"},
        {"title": "Naam", "data": "fields.name"},
        {"title": "email", "data": "fields.email"},
        {"title": "Event", "data": "fields.event"},
        {"title": "Type", "data": "fields.type"},
        # {"title": "order send", "data": "fields.mail_send", "render": "truefalse_field_renderer"},
        # {"title": "email allowed", "data": "fields.email_allowed", "render": "truefalse_field_renderer"},
        {"title": "action", "data": None, "types": {
            'delete': {
                'url': reverse('youradmin_guestlist:send', kwargs={'id': '_placeholder'}),
                'iconCls': 'glyphicon-envelope',
                'modal_id': 'send_mail',
                'hover': 'Resend order',
                'action_id_property': 'pk',
                'color': '#ec971f'
            }

        }}
    ]


@staff_member_required(login_url='/youradmin/login/')
def index(request):
    return render(request, 'youradmin/guestlist/list.html', {
        'datatables_config': json.dumps({
            'pageLength': request.GET.get('pageLength', 50000),
            'ordering': False,
            'serverSide': False,
            'columns': get_cols_list(),
            'rowId': 'pk',
            'ajax': {
                'url': reverse('youradmin_guestlist:list', kwargs={})
            }

        })
    })


@staff_member_required(login_url='/youradmin/login/')
def send(request, id):

    guest_ticket = GuestTickets.objects.get(pk=id)

    try:
        if guest_ticket.type == 'with':
            send_direct_ticket(event=guest_ticket.event, name=guest_ticket.name, email=guest_ticket.email, hash=guest_ticket.hash)

        elif guest_ticket.type == 'without':
            event = Event.objects.filter(pk=guest_ticket.event.id).first()

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
                price=0,  # ticket price is in cents bah!
                email=guest_ticket.email,
                # is_subticket=is_subticket,
                primary_ticket=None,
                is_special_guest_ticket=True,
                guest_ticket=guest_ticket
            )

            t.save()

            send_mail_and_create_pdf_for_ticket(t, 'ticket_mail_without_data')

        guest_ticket.delayed_send = False
        guest_ticket.save()
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': True})


@staff_member_required(login_url='/youradmin/login/')
def getlist(request):

    records = GuestTickets.objects.filter(delayed_send=True)
    total = GuestTickets.objects.filter(delayed_send=True).count()

    # for testing:
    # for r in records:
    #     if r.pk > 688:
    #         r.delayed_send = True
    #         r.type = 'with'
    #         r.save()

    records_data_json = serializers.serialize("json", records)

    records_data_load = json.loads(records_data_json)

    return JsonResponse({
        "recordsTotal": total,
        "recordsFiltered": total,
        "data": records_data_load
    })


def send_direct_ticket(event, name, hash, email):

    url = settings.HOSTNAME + reverse('guestlist_profile', kwargs={'hash': hash})

    content = loader.render_to_string('emails/content_guestlist.html', {
        'event': event,
        'name': name,
        'url': url
    })

    create_mail({
        'content': content
    }, 'Hello there!', email)
