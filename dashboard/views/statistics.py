import json

from django.contrib.auth.decorators import login_required
from ticketshop.models import (
    Event, EventOrganiser,
    Ticket, SoldTicket,

)
from django.shortcuts import render
from datetime import date

import datetime
from django.utils import timezone
from django.db.models import F, Sum, Count

from django.http import JsonResponse

from youradmin.common.decorators import is_event_from_user

from dashboard.common.base_vars import base_vars


# @is_organizer(login_url='login')
@is_event_from_user(login_url='login', shared_events=True)
@login_required(login_url='login')
def index(request, event_id):

    event = Event.objects.filter(pk=event_id).first()

    today_date = request.GET.get('date', date.today())

    # totaal aantal tickets
    total_tickets_sold = SoldTicket.objects.filter(event=event, order_nr__order_paid=True, is_subticket=False).count()
    total_tickets_sold_m = SoldTicket.objects.filter(event=event, order_nr__order_paid=True, sex='M').count()
    total_tickets_sold_f = SoldTicket.objects.filter(event=event, order_nr__order_paid=True, sex='F').count()
    # vandaag verkocht
    total_tickets_sold_today = SoldTicket.objects.filter(event=event, order_nr__order_paid=True,
                                                         sold_date__date=today_date, is_subticket=False).count()

    max_tickets = Ticket.objects.filter(event_id=event).aggregate(quantity=Sum(F('quantity')))
    max_tickets = max_tickets['quantity']
    tickets2 = []

    tickets = Ticket.objects.filter(event_id=event)

    financial_overview = []
    total_price = 0

    #@TODO get record with lowest date
    graphdata = get_graph_data(event)

    # loop over all the tickets
    for ticket in tickets:
        sold_total = SoldTicket.objects.filter(
            ticket_type=ticket, order_nr__order_paid=True,
            is_subticket=False).count()

        sold_tickets = SoldTicket.objects.filter(
            ticket_type=ticket, order_nr__order_paid=True, is_subticket=False)

        # holds prices and amount of that price
        ticket_price_types = stats_define_price(sold_tickets, ticket)

        total_ticket_price = 0

        for ticket_price_type in ticket_price_types:
            price = ticket_price_type['price']
            amount = ticket_price_type['amount']

            financial_overview.append({
                'name': ticket.name,
                'ticket_price': round(float(price), 2),
                'total_sold': amount,
                'quantity': ticket.quantity,
                'total_price': round(amount * float(price), 2),
                'id': ticket.id
            })
            total_price += round(amount * float(price), 2)

    total_100 = total_tickets_sold_m + total_tickets_sold_f

    if total_100 == 0:
        m_count = 0
        f_count = 0
    else:
        m_count = int(round(float(total_tickets_sold_m) / float(total_100) * 100, 0))
        f_count = int(round(float(total_tickets_sold_f) / float(total_100) * 100, 0))

    top10 = []
    try:
        top10 = SoldTicket.objects.filter(
            event=event, order_nr__order_paid=True,
            is_subticket=False).values('adress').annotate(count=Count('adress')).order_by('-count')[:10]
    except:
        pass
    events = EventOrganiser.objects.filter(user=request.user)

    return render(request, 'dash/event/statistics.html', base_vars(request, event_id, {
        'total_tickets_sold': total_tickets_sold,
        'max_tickets': max_tickets,
        'total_tickets_sold_today': total_tickets_sold_today,
        'male_count': m_count,
        'female_count': f_count,
        'total_price': total_price,
        'tickets_sold_male': total_tickets_sold_m,
        'tickets_sold_female': total_tickets_sold_f,
        'graphdata': graphdata,
        'financial_overview': financial_overview,
        'edit': False,
        'age_chart_data': get_age_chart_data(event=event),
        'top10': top10,
        'events': events
    }))



def get_age_chart_data(event):
    # sold_tickets = SoldTicket.objects.filter(event=event, order_nr__order_paid=True, is_subticket=False)

    age_ranges = [
        {'from': 0, 'to': 17, 'data': []},
        {'from': 18, 'to': 25, 'data': []},
        {'from': 26, 'to': 35, 'data': []},
        {'from': 36, 'to': 45, 'data': []},
        {'from': 46, 'to': 200, 'data': []}
    ]

    data = {"M": [], "F": [], "labels": []}

    i = 0
    for age_range in age_ranges:
        male = get_age_range(event, "M", age_range['from'], age_range["to"])
        female = get_age_range(event, "F", age_range['from'], age_range["to"])

        data['M'].append(male)
        data['F'].append(female)

        # first item
        if i == 0:
            data['labels'].append("< "+ str(age_range['to'] + 1))
        # last item
        elif i == (len(age_ranges)-1):
            data['labels'].append(str(age_range['from'] - 1) + " >")
        else:
            data['labels'].append(str(age_range['from']) + "-" + str(age_range['to']))

        i += 1

    no_birthdate_records_count = SoldTicket.objects.filter(
        event=event, order_nr__order_paid=True,
        is_subticket=False, birth_date__isnull=True
    ).count()

    if no_birthdate_records_count > 0:
        male = SoldTicket.objects.filter(
            event=event, order_nr__order_paid=True,
            is_subticket=False, birth_date__isnull=True,
            sex="M"
        ).count()

        female = SoldTicket.objects.filter(
            event=event, order_nr__order_paid=True,
            is_subticket=False, birth_date__isnull=True,
            sex="F"
        ).count()

        data['labels'].append('unknown')
        data['M'].append(male)
        data['F'].append(female)

    return data


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def get_age_range(event, sex, min_age, max_age):
    current = event.end_date.date()

    min_date = date(current.year - min_age, current.month, current.day)
    max_date = date(current.year - (max_age+1), current.month, current.day)

    return SoldTicket.objects.filter(birth_date__gte=max_date,
                                     birth_date__lte=min_date,
                                     sex=sex,
                                     event=event,
                                     order_nr__order_paid=True
                                     ).count()


def get_graph_data(event):
    ticket_starts = Ticket.objects.filter(event_id=event).order_by('start_date')

    if len(ticket_starts) == 0:
        return {
            'labels': [],
            'tickets': []
        }
    ticket_starts = ticket_starts[0]
    labels = []
    tickets = Ticket.objects.filter(event_id=event)
    # only get the stuff that i need
    small_ticketlist = []

    for ticket in tickets:
        small_ticketlist.append({
            'name': ticket.name,
            'id': ticket.id,
            'graphdata': []
        })

    delta = datetime.timedelta(days=1)

    # build the labels
    d = timezone.localtime(ticket_starts.start_date)
    while d <= event.end_date+delta:
        labels.append(d.strftime("%d %B"))

        d += delta

    # get the tickets sold for this date
    for ticket in small_ticketlist:
        # print(ticket)
        d = timezone.localtime(ticket_starts.start_date)

        while d <= event.end_date+delta:
            amount_sold = SoldTicket.objects.filter(
                sold_date__date=d, event=event,
                is_subticket=False,
                ticket_type=ticket['id'], order_nr__order_paid=True
            ).count()

            ticket['graphdata'].append(amount_sold)

            d += delta

        ticket['graphdata'] = json.dumps(ticket['graphdata'])

    return {
        'labels': json.dumps(labels),
        'tickets': small_ticketlist
    }


def stats_define_price(sold_tickets, ticket):
    ticket_price_types = []

    for sold_ticket in sold_tickets:

        price = sold_ticket.price
        # als de verkochte ticket geen prijs heeft: (alleen voor dingen van het verleden)
        if sold_ticket.price == 0:
            price = float(ticket.price) / 100

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

    return ticket_price_types


def get_chart_data(event, days):
    lowest_date = Ticket.objects.filter(event=event).order_by('start_date')[0]
    start_date = lowest_date.start_date
    end_date = event.end_date

    if days != '*':
        start_date = end_date - datetime.timedelta(days=int(days))


    labels = []
    # generate bottom labels
    total_days = (end_date - start_date).days * -1
    for i in range(total_days, 0):
        labels.append(i)

    labels.append(0)

    # haal sold tickets op van bepaalde datum
    # values = gropu by
    a = SoldTicket.objects.extra({'sold_date': "date(sold_date)"}). \
        values('sold_date'). \
        annotate(count=Count('id')).filter(is_subticket=False, event_id=event, order_nr__order_paid=True)

    sum_rec = SoldTicket.objects.extra({'sold_date': "date(sold_date)"}). \
        values('sold_date'). \
        annotate(total=Sum('price')).filter(is_subticket=False, event_id=event, order_nr__order_paid=True)

    ticket_modified_records = [{rec['sold_date'].strftime("%Y-%m-%d"): rec for rec in a}][0]
    sum_records = [{rec['sold_date'].strftime("%Y-%m-%d"): rec for rec in sum_rec}][0]

    ticket_data = []
    revenue_data = []

    while start_date <= end_date:
        start_date += datetime.timedelta(days=1)
        
        if start_date.strftime("%Y-%m-%d") in ticket_modified_records:
            ticket_data.append(ticket_modified_records[start_date.strftime("%Y-%m-%d")]['count'])
        else:
            ticket_data.append(0)

        if start_date.strftime("%Y-%m-%d") in sum_records:
            revenue_data.append(sum_records[start_date.strftime("%Y-%m-%d")]['total'])
        else:
            revenue_data.append(0)

    return {
        'labels': labels,
        'revenue_data': revenue_data,
        'ticket_data': ticket_data

    }


@is_event_from_user(login_url='login')
@login_required(login_url='login')
def chart_revenue(request, event_id):

    if request.GET.get('compare_to', 0) != 0:
        if not EventOrganiser.objects.filter(user=request.user, event=request.GET.get('compare_to')).exists():
            return JsonResponse({'success': False})

    event = Event.objects.get(id=event_id)

    chart_data = get_chart_data(event, request.GET.get('date', 30))

    labels = chart_data['labels']

    compare_ticket_data = []
    compare_revenue_data = []
    if request.GET.get('compare_to', 0) != 0:
        event = Event.objects.get(id=request.GET.get('compare_to'))

        chart_data_compare = get_chart_data(event, request.GET.get('date', 30))
        compare_ticket_data = chart_data_compare['ticket_data']
        compare_revenue_data = chart_data_compare['revenue_data']

        # if the labels are bigger then other labels use the other one
        if len(labels) < len(chart_data_compare['labels']):
            labels = chart_data_compare['labels']

        if len(chart_data['ticket_data']) > len(compare_ticket_data):
            diff = len(chart_data['ticket_data']) - len(compare_ticket_data)

            for i in range(diff):
                compare_ticket_data.insert(0, 0)

        elif len(compare_ticket_data) > len(chart_data['ticket_data']):
            diff = len(compare_ticket_data) - len(chart_data['ticket_data'])

            for i in range(diff):
                chart_data['ticket_data'].insert(0, 0)



    return JsonResponse({
        'success': True,
        'labels': labels,
        'tickets': chart_data['ticket_data'],
        'revenue': chart_data['revenue_data'],
        'compare_tickets': compare_ticket_data,
        'compare_revenue': compare_revenue_data
    })


def get_chart_data2(event, days):
    lowest_date = Ticket.objects.filter(event=event).order_by('start_date')[0]
    start_date = lowest_date.start_date
    end_date = event.end_date

    print(start_date)
    print(end_date)
    print('-------')

    # if days != '*':
    #     start_date = end_date - datetime.timedelta(days=int(days))


    labels = []
    # generate bottom labels
    total_days = (end_date - start_date).days + 2
    for i in range(0, total_days):
        labels.append(str(i * -1))

    # labels.append(0)

    # haal sold tickets op van bepaalde datum
    # values = gropu by
    a = SoldTicket.objects.extra({'sold_date': "date(sold_date)"}). \
        values('sold_date'). \
        annotate(count=Count('id')).filter(is_subticket=False, event_id=event, order_nr__order_paid=True)

    sum_rec = SoldTicket.objects.extra({'sold_date': "date(sold_date)"}). \
        values('sold_date'). \
        annotate(total=Sum('price')).filter(is_subticket=False, event_id=event, order_nr__order_paid=True)

    ticket_modified_records = [{rec['sold_date'].strftime("%Y-%m-%d"): rec for rec in a}][0]
    sum_records = [{rec['sold_date'].strftime("%Y-%m-%d"): rec for rec in sum_rec}][0]

    # ticket_data = []
    # revenue_data = []

    loop_start_date = end_date
    loop_start_date += datetime.timedelta(days=1)
    loop_end_date = start_date

    data_object = []

    last_inserted = {
        "soldtickets": 0,
        "revenue": 0
    }

    while loop_start_date >= loop_end_date:
        loop_start_date_date = loop_start_date.strftime("%Y-%m-%d")

        data = {}

        if loop_start_date_date in ticket_modified_records:
            data['soldtickets'] = ticket_modified_records[loop_start_date_date]['count'] + last_inserted['soldtickets']
        else:
            data['soldtickets'] = last_inserted['soldtickets']

        if loop_start_date_date in sum_records:
            data['revenue'] = sum_records[loop_start_date_date]['total'] + last_inserted['revenue']
        else:
            data['revenue'] = last_inserted['revenue']

        loop_start_date -= datetime.timedelta(days=1)

        last_inserted = data

        data_object.append(data)

    return {'data': data_object, 'labels': labels}


# @is_event_from_user(login_url='login')
@login_required(login_url='login')
def chart_data(request, event_id):
    # a = {
    #     'label': 0,
    #     'soldtickets': 0,
    #     'profit': 0,
    # }
    event = Event.objects.get(id=event_id)

    chart_data = get_chart_data2(event, request.GET.get('date', 30))

    labels = chart_data['labels']
    chart_data_compare = {'data': [], 'labels': []}

    if request.GET.get('compare_to', 0) != 0:
        event = Event.objects.get(id=request.GET.get('compare_to'))

        chart_data_compare = get_chart_data2(event, request.GET.get('date', 30))
        # compare_ticket_data = chart_data_compare['ticket_data']
        # compare_revenue_data = chart_data_compare['revenue_data']

        # if the labels are bigger then other labels use the other one
        if len(chart_data['data']) < len(chart_data_compare['data']):
            labels = chart_data_compare['labels']
        #
        # if len(chart_data['ticket_data']) > len(compare_ticket_data):
        #     diff = len(chart_data['ticket_data']) - len(compare_ticket_data)
        #
        #     for i in range(diff):
        #         compare_ticket_data.insert(0, 0)
        #
        # elif len(compare_ticket_data) > len(chart_data['ticket_data']):
        #     diff = len(compare_ticket_data) - len(chart_data['ticket_data'])
        #
        #     for i in range(diff):
        #         chart_data['ticket_data'].insert(0, 0)

    # print(chart_data)

    return JsonResponse({
        'orriginal': chart_data['data'],
        "compare": chart_data_compare['data'],
        "labels": labels
    })