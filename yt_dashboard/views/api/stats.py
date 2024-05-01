import datetime
from datetime import timedelta

from django.http import JsonResponse
from django.db.models import Count, Sum, F, Case, When
from dateutil.relativedelta import relativedelta

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, api_view, permission_classes

from ticketshop.models import (
    Event,
    SoldTicket,
    PageViews
)
from yt_dashboard.common.event_utils import get_events_from_user


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_gender_chart(request, date_from, date_till):

    events_from_user = get_events_from_user(user=request.user)

    total_tickets_sold_m = SoldTicket.objects.filter(
        event__in=events_from_user, order_nr__order_paid=True,
        sex='M',
        sold_date__range=(date_from, date_till),
    ).count()
    total_tickets_sold_f = SoldTicket.objects.filter(event__in=events_from_user, order_nr__order_paid=True,
                                                     sex='F', sold_date__range=(date_from, date_till),).count()
    total_tickets_sold = SoldTicket.objects.filter(event__in=events_from_user, order_nr__order_paid=True,
                                                   sold_date__range=(date_from, date_till),
                                                   ).count()

    data = [total_tickets_sold_m, total_tickets_sold_f,
            total_tickets_sold - (total_tickets_sold_m + total_tickets_sold_f)]

    return JsonResponse(data, safe=False)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_ticketscount(request, date_from, date_till):
    events_from_user = get_events_from_user(user=request.user)

    result = list(SoldTicket.objects.filter(
        event__in=events_from_user,
        order_nr__order_paid=True,
        is_subticket=False,
        sold_date__range=(date_from, date_till),
    )
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
def get_earnings_chart(request, chart_type, date_from, date_till):
    events_from_user = get_events_from_user(user=request.user)

    start_date_object = datetime.datetime.strptime(date_from, "%Y-%m-%d").date()
    end_date_object = datetime.datetime.strptime(date_till, "%Y-%m-%d").date()
    labels = get_labels(start_date_object, end_date_object)

    # print(labels)


    # prijs per datum per dag, nu nog niet nodig maar die hebben we alvast
    #result = SoldTicket.objects.filter(event__in=events_from_user).order_by('sold_date').values('sold_date').annotate(price=Sum('price'))

    # SoldTicket.objects.filter(
    #     event__in=events_from_user,
    #     # sold_date__year=now.year,
    #     # sold_date__month=now.month,
    #     # sold_date__day=now.day,
    #     order_nr__order_paid=True,
    #     is_subticket=False,
    #     guest_ticket__isnull=True
    # ).count()

    # ok ik ben er bijna maar werkt nog niet

    # from django.db.models.functions import TruncMonth, TruncDay, TruncYear, TruncDate
    # result = SoldTicket.objects.filter(event__in=events_from_user).annotate(date=TruncDate('sold_date')).order_by('sold_date').values('date').annotate(amount=Count('date'))
    # print(result.query)
    # for res in result:
    #     print(res['amount'])
    #     print(res['date'])
    # import random
    data = []
    for d in labels:
        if chart_type == 'sold_tickets':
            amount_sold = SoldTicket.objects.filter(
                sold_date__date=d,
                event__in=events_from_user,
                is_subticket=False,
                order_nr__order_paid=True,
                guest_ticket__isnull=True
            ).count()
            
        elif chart_type == 'revenue':
            amount_sold = SoldTicket.objects.filter(
                sold_date__date=d,
                # pk=11173,
                event__in=events_from_user,
                is_subticket=False,
                order_nr__order_paid=True,
                guest_ticket__isnull=True
            ).annotate(total_price=Sum('price')).first()
            
            if amount_sold:
                amount_sold = amount_sold.total
            else:
                amount_sold = 0
        # amount_sold = random.randint(10, 200)
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
def get_top_5_chart(request, chart_type, date_from, date_till):
    result = ''

    events = get_events_from_user(user=request.user)

    if chart_type == 'sold_tickets':

        result = list(SoldTicket.objects.filter(
            event__in=events,
            order_nr__order_paid=True,
            is_subticket=False,
            # voor result dit tijdelijk uitgezet
            sold_date__range=(date_from, date_till),
        )
            .values('event__title')
            .annotate(value=F('event__title'), total=Count('event')).order_by('-total'))[:5]

    elif chart_type == 'visitors':
        events_ids = events.values_list('id', flat=True)
        filters = {
            'event_id__in': [str(x) for x in events_ids],
            'date__range': (date_from, date_till),
        }
        topviews = PageViews.objects.values('event_id').annotate(total=Count('event_id')).filter(**filters).order_by('-total')[:5]
        if topviews:
            result = []
        for topview in topviews:
            event = Event.objects.get(id=topview['event_id'])
            result.append({'value': event.title, 'total': topview['total']})
        

    elif chart_type == 'profit':

        result = list(SoldTicket.objects.filter(
            event__in=events,
            order_nr__order_paid=True,
            is_subticket=False,
            sold_date__range=(date_from, date_till),
        ).values('event__title')
            .annotate(value=F('event__title'), total=Sum(F('price'))).order_by('-total'))[:5]


    return JsonResponse(result, safe=False)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def new_vs_returning_visitors(request, date_from, date_till):
    user = request.user

    event_from_user = list(Event.objects.filter(eventorganiser__user__pk=user.pk, removed=False).values('pk'))
    # event_from_user.pk
    filters = {
        'event_id__in': event_from_user,
        'id__count__gt': 1
    }
    if date_from and date_till:
        filters['date__range'] = (date_from, date_till)
    returning_visitors = PageViews.objects.values('uuid').annotate(Count('id')).filter(**filters).count()

    filters2 = {
        'event_id__in': event_from_user,
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
def list_residence(request, date_from, date_till):
    events_from_user = get_events_from_user(user=request.user)

    filters = {
        'event__in': events_from_user,
        'order_nr__order_paid': True
    }
    if date_from and date_till:
        filters['sold_date__range'] = (date_from, date_till)

    result = list(SoldTicket.objects.filter(**filters).values('adress').annotate(value=F('adress'), total=Count('id')).order_by('-total'))[
             :10]

    return JsonResponse(result, safe=False)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def age_gender(request, date_from, date_till):

    events_from_user = get_events_from_user(user=request.user)

    male_list = []
    female_list = []

    for event in events_from_user:
        current_date = event.start_date

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
            'event__in': events_from_user,
            'order_nr__order_paid': True,
            'sex': 'M'
        }
        if date_from and date_till:
            filters['sold_date__range'] = (date_from, date_till)
        # Aggregate values
        male_list.append(list(SoldTicket.objects.filter(**filters).aggregate(**aggr_query).values()))
        filters['sex'] = 'F'
        female_list.append(list(SoldTicket.objects.filter(**filters).aggregate(**aggr_query).values()))

    data = {
        'male':  [sum(x) for x in zip(*male_list)],  # [10,20,5,10,5], #
        'female':   [sum(x) for x in zip(*female_list)],  # [10,20,5,10,5] #
    }

    return JsonResponse(data, safe=False)