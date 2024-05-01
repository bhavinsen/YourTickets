from datetime import date
import datetime
from datetime import timedelta

from django.http import JsonResponse
from django.db.models import Count, Sum, F, Case, When
from dateutil.relativedelta import relativedelta

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, api_view, permission_classes

from ticketshop.models import (Ticket, Event, SoldTicket, PageViews)
from yt_dashboard.common import event_utils
from yt_dashboard.common.stats_utils import get_visitors


# ik vermoed dat dit bestand weg kan

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def sold_ticket_amount(request, id, date_from=None, date_till=None):
    user = request.user

    # events_from_user = Event.objects.filter(eventorganiser__user__pk=user.pk, removed=False, pk=id).first()
    event_from_user = event_utils.get_user_event(request.user, event_id=id, include_shared_event=True)
    if not event_from_user:
        return JsonResponse({'success': False}, safe=False)

    filters = {
        'event': event_from_user,
        'order_nr__order_paid': True,
        'is_subticket': False,
        'guest_ticket__isnull': True
    }
    if date_from and date_till:
        filters['sold_date__range'] = (date_from, date_till)

    total = SoldTicket.objects.filter(
        **filters
    ).count()

    return JsonResponse({'total': total})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def revenue(request, id, date_from=None, date_till=None):

    event_from_user = event_utils.get_user_event(request.user, event_id=id, include_shared_event=True)
    if not event_from_user:
        return JsonResponse({'success': False}, safe=False)

    filters = {
        'event': event_from_user,
        'order_nr__order_paid': True,
    }

    if date_from and date_till:
        filters['sold_date__range'] = (date_from, date_till)

    price = SoldTicket.objects.filter(
        **filters
    ).aggregate(price=Sum(F('price')))
    price = price['price'] or 0
    return JsonResponse({'total': price})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def visitors(request, id, date_from=None, date_till=None):

    event_from_user = event_utils.get_user_event(request.user, event_id=id, include_shared_event=True)
    if not event_from_user:
        return JsonResponse({'success': False}, safe=False)

    visitors = get_visitors(user=request.user, event=event_from_user)

    return JsonResponse({'total': visitors}, safe=False)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def conversion_rate(request, id, date_from=None, date_till=None):
    user = request.user

    event_from_user = event_utils.get_user_event(request.user, event_id=id, include_shared_event=True)
    if not event_from_user:
        return JsonResponse({'success': False}, safe=False)

    event_views = get_visitors(
        user=request.user, 
        event=event_from_user, 
        date_from=date_from,
        date_till=date_till
    )

    events_from_user = Event.objects.filter(eventorganiser__user__pk=user.pk, removed=False).order_by('-pk')

    filters = {
        'event__in': events_from_user,
        'order_nr__order_paid': True,
        'is_subticket': False,
        'guest_ticket__isnull': True
    }
    if date_from and date_till:
        filters['sold_date__range'] = (date_from, date_till)

    total_orders = SoldTicket.objects.filter(**filters).annotate(dcount=Count('order_nr__pk')).order_by().count()

    total = 0
    if total_orders > 0:
        try:
            total = round((total_orders / event_views )*100, 2)
        except ZeroDivisionError:
            total = 0
    return JsonResponse({'total': total})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def gender_chart(request, id, date_from=None, date_till=None):

    event_from_user = event_utils.get_user_event(request.user, event_id=id, include_shared_event=True)
    if not event_from_user:
        return JsonResponse({'success': False}, safe=False)

    filters = {
        'event': event_from_user,
        'order_nr__order_paid': True,
        'sex': 'M'
    }
    if date_from and date_till:
        filters['sold_date__range'] = (date_from, date_till)

    total_tickets_sold_m = SoldTicket.objects.filter(**filters).count()
    filters['sex'] = 'F'
    total_tickets_sold_f = SoldTicket.objects.filter(**filters).count()

    del filters['sex']
    total_tickets_sold = SoldTicket.objects.filter(**filters).count()

    unknown = total_tickets_sold - (total_tickets_sold_m + total_tickets_sold_f)

    data = [
        total_tickets_sold_f,
        total_tickets_sold_m,
        # unknown
    ]
    # for debugging
    # data = [
    #     10,
    #     20,
    # ]

    # if total_tickets_sold_m < 1 and total_tickets_sold_f < 1 and unknown < 1:
    #     data = [0, 0, 1]

    return JsonResponse(data, safe=False)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ticketscount(request, id, date_from=None, date_till=None):
    event_from_user = event_utils.get_user_event(request.user, event_id=id, include_shared_event=True)
    if not event_from_user:
        return JsonResponse({'success': False}, safe=False)

    filters = {
        'event': event_from_user,
        'order_nr__order_paid': True,
        'is_subticket': False,
    }
    if date_from and date_till:
        filters['sold_date__range'] = (date_from, date_till)

    result = list(SoldTicket.objects.filter(**filters)
                  .values('ticket_type__name')
                  .annotate(the_count=Count('ticket_type__pk')).order_by('-the_count'))[:4]

    data = {
        'labels': [res['ticket_type__name'] for res in result],
        'data': [res['the_count'] for res in result]
    }

    return JsonResponse(data, safe=False)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def total_sold_of(request, id, date_from=None, date_till=None):
    event_from_user = event_utils.get_user_event(request.user, event_id=id, include_shared_event=True)
    if not event_from_user:
        return JsonResponse({'success': False}, safe=False)

    filters = {
        'event': event_from_user,
        'order_nr__order_paid': True,
        'is_subticket': False,
        'guest_ticket__isnull': True
    }
    if date_from and date_till:
        filters['sold_date__range'] = (date_from, date_till)

    total = SoldTicket.objects.filter(**filters).count()

    available = Ticket.objects.filter(
        event=event_from_user,
    ).aggregate(quantity=Sum(F('quantity')))
    available = available['quantity'] or 0

    if available == 0:
        available = 1

    return JsonResponse({'tickets_available': available, 'tickets_sold': total}, safe=False)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def earnings_chart(request, id, date_from=None, date_till=None):
    user = request.user

    event_from_user = event_utils.get_user_event(request.user, event_id=id, include_shared_event=True)
    if not event_from_user:
        return JsonResponse({'success': False}, safe=False)

    if date_from and date_till:
        start_date_object = datetime.datetime.strptime(date_from, "%Y-%m-%d").date()
        end_date_object = datetime.datetime.strptime(date_till, "%Y-%m-%d").date()
    else:
        # dit is nog niet goed, wanneer begint de verkoop? event -> tickets -> lowest date?
        # now fixed
        start_date_object = event_from_user.start_date.date()
        end_date_object = event_from_user.end_date.date()

        first_ticket_sold = SoldTicket.objects.filter(
            event=event_from_user,
            is_subticket=False,
            order_nr__order_paid=True,
            guest_ticket__isnull=True
        ).order_by('sold_date')
        if len(first_ticket_sold) > 0:
            start_date_object = first_ticket_sold[0].sold_date.date()

    labels = get_labels(start_date_object, end_date_object)
    data = []
    for d in labels:
        # if chart_type == 'sold_tickets':
        amount_sold = SoldTicket.objects.filter(
            sold_date__date=d,
            event=event_from_user,
            is_subticket=False,
            order_nr__order_paid=True,
            guest_ticket__isnull=True
        ).count()

        data.append(amount_sold)

    result = {
        'labels': labels,
        'data': data
    }

    return JsonResponse(result, safe=False)


def get_labels(start_date, end_date):

    date_modified = start_date
    list = [start_date]

    while date_modified < end_date:
        date_modified += timedelta(days=1)
        list.append(date_modified)

    return list


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_residence(request, id, date_from=None, date_till=None):

    event_from_user = event_utils.get_user_event(request.user, event_id=id, include_shared_event=True)
    if not event_from_user:
        return JsonResponse({'success': False}, safe=False)

    filters = {
        'event': event_from_user,
        'order_nr__order_paid': True
    }
    if date_from and date_till:
        filters['sold_date__range'] = (date_from, date_till)

    result = list(SoldTicket.objects.filter(**filters).values('adress').annotate(value=F('adress'),total=Count('id')).order_by('-total'))[:10]

    return JsonResponse(result, safe=False)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def new_vs_returning_visitors(request, id, date_from=None, date_till=None):
    event_from_user = event_utils.get_user_event(request.user, event_id=id, include_shared_event=True)
    if not event_from_user:
        return JsonResponse({'success': False}, safe=False)

    filters = {
        'event_id': event_from_user.pk,
        'id__count__gt': 1
    }
    if date_from and date_till:
        filters['date__range'] = (date_from, date_till)
    returning_visitors = PageViews.objects.values('uuid').annotate(Count('id')).filter(**filters).count()

    filters2 = {
        'event_id': event_from_user.pk,
        'id__count': 1
    }
    if date_from and date_till:
        filters2['date__range'] = (date_from, date_till)

    new_visitors = PageViews.objects.values('uuid').annotate(Count('id')).filter(**filters2).count()

    data = [new_visitors, returning_visitors]

    return JsonResponse(data, safe=False)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def age_and_gender(request, id, date_from=None, date_till=None):

    event_from_user = event_utils.get_user_event(request.user, event_id=id, include_shared_event=True)
    if not event_from_user:
        return JsonResponse({'success': False}, safe=False)

    current_date = event_from_user.start_date

    range_ages = (
        {"lookup": "gte", "label": "-17", "age": [18]},
        {"lookup": "range", "label": "18-25", "age": [18, 26]},
        {"lookup": "range", "label": "25-35", "age": [26, 36]},
        {"lookup": "range", "label": "36-45", "age": [36, 46]},
        {"lookup": "lt", "label": "46+", "age": [46]},
    )

    aggr_query = {}
    for item in range_ages:
        age = item.get("age")
        lookup = item.get("lookup")
        label = item.get("label")
        # calculate start_date an end_date
        end_date = current_date - relativedelta(years=age[0])
        start_date = current_date - relativedelta(years=age[-1], days=-1)
        f_value = start_date if len(age) == 1 else (start_date, end_date)
        if lookup == "gte":
            aggr_query[label] = Count(Case(When(birth_date__gte=f_value, then=1)))
        elif lookup == "lt":
            aggr_query[label] = Count(Case(When(birth_date__lt=f_value, then=1)))
        else:
            aggr_query[label] = Count(Case(When(birth_date__range=f_value, then=1)))

    filters = {
        'event': event_from_user,
        'order_nr__order_paid': True,
        'sex': 'M'
    }
    if date_from and date_till:
        filters['sold_date__range'] = (date_from, date_till)
    # Aggregate values
    male_values = list(SoldTicket.objects.filter(**filters).aggregate(**aggr_query).values())
    # male_values = [10,20,5,0,5]
    filters['sex'] = 'F'
    female_values = list(SoldTicket.objects.filter(**filters).aggregate(**aggr_query).values())
    # female_values = [10,0,5,0,5]

    highest_value = max(male_values + female_values)

    new_array = []
    for i in range(len(male_values)):
        if male_values[i] == 0 and female_values[i] == 0:
            
            new_array.append(highest_value)
        else:
            new_array.append(0)


    data = {
        'male': male_values, # [10,20,5,10,5],
        'female': female_values, # [10,20,5,10,5]
        'max': new_array
        # 'male':[10,20,5,0,5],
        # 'female': [10,0,5,0,5],
        # 'max': [0,0,0,20,0],
    }

    return JsonResponse(data, safe=False)