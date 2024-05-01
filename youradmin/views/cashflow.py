import json
import csv
import operator
import os.path
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import (
    render
)
from django.db.models import  ObjectDoesNotExist
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.models import User

from ticketshop.models import UserExtra, Order, Event, SoldTicket, Ticket, EventOrganiser
from yourtickets.common import shop, ticket
from youradmin.common.datatable import build_order_args, build_search_args
from youradmin.views.forms.orders import ResendTicketsForm
from django.conf import settings
from yourtickets.common.shop import get_service_cost, get_price_and_ticket_amount
from youradmin.views.forms.cashflow import UploadCsvForm


@staff_member_required(login_url='/youradmin/login/')
def cashflow(request):


    file = settings.BASE_DIR + '/youradmin/payment_import/data.csv'

    # print(os.path.isfile(file))

    # reader = csv.reader(open(file, 'r'))
    # t = 'PLEASURE, Order nr: 2098'
    #
    # print(t[t.index('Order nr:')+len('Order nr:'):])

    total_orders = 0
    total_orders_parsed = 0
    total_tickets = 0
    inkomsten_van_mollie = 0.0
    inkomsten_van_yourtickets = 0.0
    inkomsten_incorrecte_orders = 0.0
    first_ticket_sold_date = False
    last_ticket_sold_date = False
    service_kosten = 0.0

    a = {
        'BIC consument': 'INGBNL2A',
        'Naam consument': 'MW T C I Vyent',
        'Datum': '2017-06-01 11:55:58',
        'Rekening consument': 'NL10INGB0750870729',
        'Bedrag': '16.83',
        'ID': 'tr_rNNbnpwaN7',
        'Betaalmethode': 'ideal',
        'Omschrijving': 'PLEASURE, Order nr: 2098'
     }

    csv_records = {}

    logs = []

    order_ids = []

    # get the order_ids and get the csv records
    with open(file, mode='r') as infile:
        reader = csv.DictReader(infile)

        # print(reader)

        for row in reader:
            total_orders += 1
            details = row['Omschrijving']
            order_id = details[details.index('Order nr:')+len('Order nr:'):].strip()

            # get the order for this order_id
            try:
                order = Order.objects.get(pk=order_id)
                total_orders_parsed += 1
                order_ids.append(order_id)

                inkomsten_van_mollie += float(row['Bedrag'])

                if last_ticket_sold_date == False:
                    last_ticket_sold_date = row['Datum']

                if first_ticket_sold_date == False:
                    first_ticket_sold_date = row['Datum']

                if row['Datum'] > last_ticket_sold_date:
                    last_ticket_sold_date = row['Datum']

                if row['Datum'] < first_ticket_sold_date:
                    first_ticket_sold_date = row['Datum']

                csv_records[order_id] = row
            except ObjectDoesNotExist as e:
                inkomsten_incorrecte_orders += float(row['Bedrag'])
                logs.append({
                    'payment_object': row,
                    'message': 'Order not found in yt database, order_id='+ order_id
                })
                continue

    #get all the orders in 1 query
    orders = Order.objects.prefetch_related('soldticket_set','soldticket_set__event').filter(pk__in=order_ids)

    data_per_user = {
        'user_id': {
            'user_model': 'usermodel',
            # 'mollie_row': 'mollierow',
            'events': {
                'event_id': {
                    'event_model': 'model',
                    'amount_sold': 0,
                    'price_amount_sold': 0,
                    'tickets': {
                        'ticketid': {
                            'ticket_model': 'model',
                            'amount_sold': 5,
                            'price_amount_sold': '50'

                        }
                    }
                }

            }
        }
    }

    data_per_user = {}

    for order in orders:
        # service_kosten += float(order.service_costs)

        t = 0
        for soldticket in order.soldticket_set.all():
            if soldticket.price != 0:
                t += 1
        service_kosten += get_service_cost(float(order.price), t , 0)

        for soldticket in order.soldticket_set.all():
            # print(soldticket.event.title)
            # print(soldticket.event.title)
            total_tickets += 1
            event_for_user = EventOrganiser.objects.filter(event=soldticket.event).first()
            user = event_for_user.user

            if not event_for_user:
                logs.append({
                    'payment_object': {},
                    'message': 'Event not found for user, event_id: '+ soldticket.event.id
                })
                continue

            # create the user if not exists
            if str(user.pk) not in data_per_user:

                data_per_user[str(user.pk)] = {
                    'user_model': user,
                    # 'mollie_row': '',#csv_records[order.pk]
                    'events': {}
                }

            # if event doesnt exists
            if 'events' not in data_per_user[str(user.pk)]:
                data_per_user[str(user.pk)]['events'] = {}

            if str(soldticket.event.id) not in data_per_user[str(user.pk)]['events']:

                data_per_user[str(user.pk)]['events'][str(soldticket.event.id)] = {
                    'event_model': soldticket.event,
                    'tickets': {},
                    'amount_sold': 0,
                    'price_amount_sold': 0.0,
                }


            price = soldticket.price

            if price == 0:
                price = soldticket.ticket_type.price/100

            data_per_user[str(user.pk)]['events'][str(soldticket.event.id)]['amount_sold'] += 1
            data_per_user[str(user.pk)]['events'][str(soldticket.event.id)]['price_amount_sold'] += float(price)
            # end event

            # if the ticket doesnt exists for this event
            if 'tickets' not in data_per_user[str(user.pk)]['events'][str(soldticket.event.id)]:
                data_per_user[str(user.pk)]['events'][str(soldticket.event.id)]['tickets'] = {}

            if str(soldticket.ticket_type.id) not in data_per_user[str(user.pk)]['events'][str(soldticket.event.id)]['tickets']:
                print(soldticket.ticket_type.id)
                # print('create '+str(soldticket.event.id))

                data_per_user[str(user.pk)]['events'][str(soldticket.event.id)]['tickets'][str(soldticket.ticket_type.id)] = {
                    'ticket_model': soldticket.ticket_type,
                    'amount_sold': 0,
                    'price_amount_sold': 0.0
                }
                # print(data_per_user)
                # print('-----------------------------')
            # print('add one')
            data_per_user[str(user.pk)]['events'][str(soldticket.event.id)]['tickets'][str(soldticket.ticket_type.id)]['amount_sold'] += 1
            data_per_user[str(user.pk)]['events'][str(soldticket.event.id)]['tickets'][str(soldticket.ticket_type.id)]['price_amount_sold'] += float(price)

            inkomsten_van_yourtickets += float(price)

    return render(request, 'youradmin/cashflow/index.html', {
        'logs': logs,
        'total_orders': total_orders,
        'total_orders_parsed': total_orders_parsed,
        'inkomsten_van_mollie': inkomsten_van_mollie,
        'last_ticket_sold_date': last_ticket_sold_date,
        'first_ticket_sold_date': first_ticket_sold_date,
        'inkomsten_van_yourtickets': inkomsten_van_yourtickets+service_kosten,  # calculated based on soldticket.price or ticket.price
        'inkomsten_zonder_service_kosten_yourtickets': inkomsten_van_yourtickets,
        'inkomsten_incorrecte_orders': inkomsten_incorrecte_orders,  # inkomsten van orders die niet teruggevonden konden worden
        'service_kosten': service_kosten,
        'data_per_user': data_per_user,
        'total_tickets': total_tickets,

        'form': UploadCsvForm(),

    })

def upload_csv(request):

    if request.method == 'POST':
        form = UploadCsvForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': True})

def handle_uploaded_file(f):
    with open(settings.YOURADMIN_CASHFLOW_UPLOAD_DIR+'data.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
