from datetime import date
import datetime

from django.http import JsonResponse
from django.db.models import Count, Sum, F

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, api_view, permission_classes

from ticketshop.models import (Ticket, Event, SoldTicket, Order, PageViews)

from yt_dashboard.common.stats_utils import get_visitors

# verkochte tickets aantal

# /api/account/aggregate/tickets?from=132&till=543
# /api/account/aggregate/visitors?from=132&till=543
# /api/account/aggregate/revenue?from=132&till=543
# /api/account/aggregate/genders?from=132&till=543
# /api/account/aggregate/conversion?from=132&till=543

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def sold_ticket_amount(request, date_from, date_till):

    user = request.user

    events_from_user = Event.objects.filter(eventorganiser__user__pk=user.pk, removed=False).order_by('-pk')

    total = SoldTicket.objects.filter(
        event__in=events_from_user,
        sold_date__range=(date_from, date_till),
        order_nr__order_paid=True,
        is_subticket=False,
        guest_ticket__isnull=True
    ).count()

    return JsonResponse({'total': total})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def revenue(request, date_from, date_till):
    user = request.user
    events_from_user = Event.objects.filter(
        eventorganiser__user__pk=user.pk, removed=False,

    )

    price = SoldTicket.objects.filter(
        event__in=events_from_user,
        sold_date__range=(date_from, date_till),
    ).aggregate(price=Sum(F('price')))
    price = price['price'] or 0
    return JsonResponse({'total': price})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def visitors(request, date_from, date_till):
    visitors = get_visitors(
        user=request.user,
        date_from=date_from,
        date_till=date_till
    )
    return JsonResponse({'total': visitors})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def conversion_rate(request, date_from, date_till):
    user = request.user

    visitors = get_visitors(
        user=request.user,
        date_from=date_from,
        date_till=date_till
    )

    events_from_user = Event.objects.filter(eventorganiser__user__pk=user.pk, removed=False).order_by('-pk')

    total_orders = SoldTicket.objects.filter(
        event__in=events_from_user,
        sold_date__range=(date_from, date_till),
        order_nr__order_paid=True,
        is_subticket=False,
        guest_ticket__isnull=True
    ).annotate(dcount=Count('order_nr__pk')).order_by().count()

    total = 0
    if total_orders > 0:
        total = round((total_orders/visitors)*100, 2)

    return JsonResponse({'total': total})

