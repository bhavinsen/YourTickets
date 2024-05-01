import json

from django.http import JsonResponse
from django.utils.encoding import iri_to_uri
from django.forms.models import model_to_dict
from django.conf import settings
from django.urls import reverse

from dashboard.forms.sales_channels import SalesChannelForm
from ticketshop.models import Saleschannel, Event, SoldTicket

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, api_view, permission_classes
from django.db.models import Sum, F

def getUser(request):
    return request.user
    # return get_user_model().objects.filter(pk=271).first()


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getall(request, id):
    user = getUser(request)

    try:
        event = Event.objects.get(eventorganiser__user__pk=user.pk, pk=id, removed=False)
    except:
        return JsonResponse({'success': False}, safe=False)

    channels = list(Saleschannel.objects.filter(event=event, deleted=False).values('id', 'name', 'url_name'))

    for channel in channels:
        filters = {
            'event': event,
            'order_nr__order_paid': True,
            'order_nr__sale_channel__pk': channel['id']
        }

        price = SoldTicket.objects.filter(
            **filters
        ).aggregate(price=Sum(F('price')))
        revenue = price['price'] or 0
        channel['revenue'] = revenue
        event_url_str = event.event_url
        if event_url_str == "":
            if event.title == "":
                event.title = 'LEEG'
            event_url_str = event.title
        url = settings.HOSTNAME + reverse('buy_ticket', kwargs={'event_id': event.pk, 'event_name': event_url_str}) + channel['url_name']

        channel['url_name'] = url

    # total_revenue
    total = 0


    return JsonResponse({
        'channels': channels,
        'total': total
    })



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def stats_define_price(sold_tickets):
    ticket_price_types = []

    for sold_ticket in sold_tickets:

        price = sold_ticket.price
        # als de verkochte ticket geen prijs heeft: (alleen voor dingen van het verleden)
        if sold_ticket.price == 0:
            if not sold_ticket.ticket_type:
                pass
            else:
                # print(sold_ticket.ticket_type)
                price = float(sold_ticket.ticket_type.price) / 100

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


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create(request, id):
    user = getUser(request)

    try:
        event = Event.objects.get(eventorganiser__user__pk=user.pk, pk=id, removed=False)
    except:
        return JsonResponse({'success': False}, safe=False)

    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)

    form = SalesChannelForm(data=data)
    if form.is_valid():
        data = form.cleaned_data
        # event = Event.objects.get(pk=event_id)
        sc = Saleschannel(name=data['name'], event=event)
        sc.url_name = iri_to_uri(data['name'])
        sc.save()
        rec = model_to_dict(sc)
        rec['total'] = 0
        data = {'success': True, 'saleschannel': rec}
    else:
        data = {'errors': json.loads(form.errors.as_json())}

    return JsonResponse(data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update(request, id, saleschannel_id):
    user = getUser(request)

    try:
        event = Event.objects.get(eventorganiser__user__pk=user.pk, pk=id, removed=False)
    except:
        return JsonResponse({'success': False}, safe=False)

    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)

    form = SalesChannelForm(data=data)
    if form.is_valid():
        data = form.cleaned_data

        sc = Saleschannel.objects.get(pk=saleschannel_id, event=event)
        sc.name = data['name']
        sc.url_name = iri_to_uri(data['name'])

        sc.save()
        return JsonResponse({'success': True})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete(request, id, saleschannel_id):
    user = getUser(request)
    try:
        event = Event.objects.get(eventorganiser__user__pk=user.pk, pk=id, removed=False)
    except:
        return JsonResponse({'success': False}, safe=False)

    channel = Saleschannel.objects.get(pk=saleschannel_id, event=event)

    channel.deleted = True
    channel.save()

    return JsonResponse({'success': True})