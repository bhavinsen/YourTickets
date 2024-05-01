import json
import csv
import operator
import os.path
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import (
    render
)
from django.db.models import ObjectDoesNotExist, Q
from django.urls import reverse
from django.http import JsonResponse
from django.core import serializers
from django.db import connection
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime
from django.utils import timezone
from functools import reduce

from ticketshop.models import Event, EventOrganiser, EventPayments, UserExtraSeller, SoldTicket
from youradmin.common.datatable import build_order_args, build_search_args
from youradmin.common.decorators import group_required
from youradmin.views.forms.financial_payments import FinancialPaymentsForm


def get_cols_events():
    return [
        {"title": "id", "data": "pk", "searchType": "exact"},
        {"title": "title", "data": "fields.title"},
        {"title": "start date", "data": "fields.start_date", "searchType": "range", "linked_range": 3},
        {"title": "tickets sold", "data": "fields.tickets_sold", "skipSearch": True},
        {"title": "YT income", "data": "fields.yt_income", "skipSearch": True},
        {"title": "inkomsten", "data": "fields.income"},
        {"title": "uitbetalingen", "data": "fields.payout"},

        {"title": "saldo", "data": "fields.saldo"},
        {"title": "marked", "data": "fields.marked", "render": "truefalse_field_renderer_marker"},
        {"title": "action", "data": None, "types":
            {
                'linkicon': {
                    'url': reverse('youradmin_financial:get_event_detail', kwargs={
                        'event_id': '_placeholder'}),
                    'hover': 'See orders',
                    'action_id_property': 'pk',
                    'iconCls': 'glyphicon-list-alt'
                }
            }
         }
    ]

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_income(start_date=None, end_date=None, title=None, event_id=None):

    # //1 aug tot vandaag
    # Total
    # order
    # amount: 20505.00
    # Total
    # service
    # costs: 2718.50

    query = """
        SELECT 
          DISTINCT 
          orderr.*, 
          ticketshop_soldticket.event_id as event_id
        FROM 
          ticketshop_order as orderr
        INNER JOIN ticketshop_soldticket ON (orderr.id = ticketshop_soldticket.order_nr_id)
          
        AND orderr.order_paid = TRUE
    """

    params = []

    sold_tickets_arguments = {
        'order_nr__order_paid': True,
        'is_subticket': False
    }
    sold_tickets_q = []

    if start_date and end_date:

        query += """
            AND orderr.date >= %s
            AND orderr.date <= %s
        """

        params.append(timezone.make_aware(datetime.strptime(start_date + ' 00:00:00', '%Y-%m-%d %H:%M:%S'), timezone.get_current_timezone()))
        params.append(timezone.make_aware(datetime.strptime(end_date + ' 23:59:59', '%Y-%m-%d %H:%M:%S'), timezone.get_current_timezone()))

        startdate = timezone.make_aware(datetime.strptime(start_date + ' 00:00:00', '%Y-%m-%d %H:%M:%S'), timezone.get_current_timezone())
        enddate = timezone.make_aware(datetime.strptime(end_date + ' 23:59:59', '%Y-%m-%d %H:%M:%S'), timezone.get_current_timezone())

        kwargs = {
            'order_nr__date__range': (startdate, enddate)
        }

        sold_tickets_q.append(Q(**kwargs))
    if event_id:
        query += """
        AND ticketshop_soldticket.event_id = %s
        """
        params.append(event_id)
        sold_tickets_arguments['event'] = event_id


    with connection.cursor() as cursor:
        cursor.execute(query, params)
        orders = dictfetchall(cursor)

    # AND ticketshop_soldticket.event_id = 177

    total_orders_amount = 0
    service_costs = 0

    eventIDS = []

    for order in orders:
        total_orders_amount += order['price']
        service_costs += order['service_costs']
        eventIDS.append(order['event_id'])

    total_payout = EventPayments.objects.filter(event_id__in=eventIDS).aggregate(Sum('amount'))
    total_tickets_sold = 0



    if len(sold_tickets_q) > 0:
        # print(SoldTicket.objects.filter(**sold_tickets_arguments).filter(reduce(operator.or_, sold_tickets_q)).query)
        total_tickets_sold = SoldTicket.objects.filter(**sold_tickets_arguments).filter(reduce(operator.or_, sold_tickets_q)).count()
    else:
        total_tickets_sold = SoldTicket.objects.filter(**sold_tickets_arguments).count()

    if not total_payout['amount__sum']:
        total_payout = 0
    else:
        total_payout = total_payout['amount__sum']

    return {
        'total_service_costs': service_costs,
        'total_orders_amount': total_orders_amount,
        'total_payd': total_payout,
        'total_still_to_pay': total_orders_amount - total_payout,
        'total_tickets_sold': total_tickets_sold
    }

@group_required('financial')
@staff_member_required(login_url='/youradmin/login/')
def list_events(request):

    return render(request, 'youradmin/financial/index.html', {
        # 'income_data': get_income(),
        'datatables_config': json.dumps({
            'pageLength': request.GET.get('pageLength', 20),
            'columns': get_cols_events(),
            'ajax': {
                'url': reverse('youradmin_financial:list', kwargs={})
            }

        })
    })

@group_required('financial')
@staff_member_required(login_url='/youradmin/login/')
def get_total_income(request):

    success = True
    try:
        data = get_income(
            request.POST.get('start_date', None),
            request.POST.get('end_date', None),
            request.POST.get('title', None),
            request.POST.get('event_id', None)
        )
    except Exception as e:
        data = ''
        success = False

    return JsonResponse({'data':data, 'success': success})

@group_required('financial')
@staff_member_required(login_url='/youradmin/login/')
def events_list(request):

    source = request.POST

    page_length = int(source.get('length', 1))
    data_start = int(source.get('start', 0))

    order_args = build_order_args(request.POST, get_cols_events())

    search_args = build_search_args(request.POST, get_cols_events())

    # exclude income, payout, saldo that will be a manual order

    try:
        order_args.remove('income')
    except:
        pass
    try:
        order_args.remove('-income')
    except:
        pass
    try:
        order_args.remove('payout')
    except:
        pass
    try:
        order_args.remove('-payout')
    except:
        pass
    try:
        order_args.remove('saldo')
    except:
        pass
    try:
        order_args.remove('-saldo')
    except:
        pass


    if len(order_args) == 0:
        order_args.append('id')

    total_tickets_sold = 0

    if len(search_args) > 0:
        records = Event.objects.filter(reduce(operator.or_, search_args)).order_by(*order_args)[data_start:data_start+page_length]
        total = Event.objects.filter(reduce(operator.or_, search_args)).count()
    else:
        records = Event.objects.all().order_by(*order_args)[data_start:int(data_start)+int(page_length)]
        total = Event.objects.all().count()

    events_data_json = serializers.serialize("json", records)

    events_data_load = json.loads(events_data_json)

    for record in events_data_load:
        record['fields']['start_date'] = record['fields']['start_date'][:10]
        record['fields']['end_date'] = record['fields']['end_date'][:10]

        fin_data = get_income(event_id=record['pk'])

        record['fields']['income'] = fin_data['total_orders_amount']
        record['fields']['payout'] = fin_data['total_payd']
        record['fields']['saldo'] = fin_data['total_still_to_pay']

        fin_data = get_income_per_event(event_id=record['pk'])
        record['fields']['yt_income'] = fin_data['total_service_costs']
        record['fields']['tickets_sold'] = SoldTicket.objects.filter(event_id=record['pk'], order_nr__order_paid=True, is_subticket=False).count()







    # newlist = sorted(list_to_be_sorted, key=lambda k: k['name'])

    return JsonResponse({
        "recordsTotal": total,
        "recordsFiltered": total,
        "data": events_data_load,
        "total_sold": total_tickets_sold
    })


def get_income_per_event(event_id):
    with connection.cursor() as cursor:

        cursor.execute("""
        SELECT 
          orderr.*
          
        FROM 
          ticketshop_order as orderr

        INNER JOIN ticketshop_soldticket ON (orderr.id = ticketshop_soldticket.order_nr_id)

        AND orderr.order_paid = TRUE

        AND ticketshop_soldticket.event_id = %s
        
        GROUP BY orderr.id

    """, [event_id])
        orders = dictfetchall(cursor)

    # AND ticketshop_soldticket.event_id = 177

    total_orders_amount = 0
    service_costs = 0
    for order in orders:
        # print(order['ticketshop_soldticket'])
        total_orders_amount += order['price']



        # print(str(service_costs) + ' + ' + str(order['service_costs']) + ' = ' + str(service_costs + order['service_costs']))

        service_costs += order['service_costs']


    return {
        'total_service_costs': service_costs,
        'total_orders_amount': total_orders_amount

    }

@group_required('financial')
def get_event_details(request, event_id):

    event = Event.objects.filter(pk=event_id)[0]

    event_organizer = EventOrganiser.objects.filter(event_id = event_id)[0]
    organizer = User.objects.filter(pk = event_organizer.user_id)[0]

    totals = get_income_per_event(event.pk)

    payments = EventPayments.objects.filter(event=event)

    total_payout = 0
    for payment in payments:
        total_payout += payment.amount

    total_still_to_pay = totals['total_orders_amount'] - total_payout

    account = {}

    if UserExtraSeller.objects.filter(event_id=event.id).exists():
        account = UserExtraSeller.objects.filter(event_id=event.id)[0]

    total_tickets_sold = SoldTicket.objects.filter(event=event, order_nr__order_paid=True, is_subticket=False).count()



    return render(request, 'youradmin/financial/event.html', {
        'total_still_to_pay': total_still_to_pay,
        'total_payout': total_payout,
        'form': FinancialPaymentsForm(),
        'payments': payments,
        'event': event,
        'organizer': organizer,
        'totals': totals,
        'account': account,
        'total_tickets_sold': total_tickets_sold

    })

def create_event_payment(request, event_id):
    event = Event.objects.get(pk=event_id)

    form = FinancialPaymentsForm(request.POST)

    if form.is_valid():

        payment = EventPayments(
            amount=form.cleaned_data['amount'],
            payout_date=form.cleaned_data['payout_date'],
            description=form.cleaned_data['description'],
            type=form.cleaned_data['type'],
            approved=True,
            event=event)
        payment.save()

        data = {'success': True, 'redirect': True}
    else:
        data = {'errors': json.loads(form.errors.as_json())}

    return JsonResponse(data)


@group_required('financial')
@staff_member_required(login_url='/youradmin/login/')
def edit_event_payment(request, payment_id):

    form = FinancialPaymentsForm(instance=EventPayments.objects.get(pk=payment_id))

    if request.POST:
        form = FinancialPaymentsForm(instance=EventPayments.objects.get(pk=payment_id), data=request.POST)
        if form.is_valid():
            form.save()
            data = {'success': True, 'redirect': True}
        else:
            data = {'errors': json.loads(form.errors.as_json())}
    else:
        return render(request, 'youradmin/partials/formdecorator_renderer.html', {
            "form": form
        })
    return JsonResponse(data)

@group_required('financial')
@staff_member_required(login_url='/youradmin/login/')
def payment_delete(request, payment_id):
    EventPayments.objects.get(pk=payment_id).delete()
    return JsonResponse({'success': True, 'redirect': True})

@group_required('financial')
@staff_member_required(login_url='/youradmin/login/')
def mark_event(request, event_id):
    event = Event.objects.get(pk=event_id)

    mark = request.POST.get('mark', False)

    if mark == 'true':
        mark = True
    else:
        mark = False

    event.marked = mark
    event.save()
    return JsonResponse({'success':True})
