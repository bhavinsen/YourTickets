import json

from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.utils.encoding import iri_to_uri

from dashboard.common.base_vars import base_vars
from dashboard.forms.sales_channels import SalesChannelForm
from youradmin.common.decorators import is_event_from_user
from ticketshop.models import Saleschannel, Event, SoldTicket




@is_event_from_user(login_url='login')
def index(request, event_id):

    event = Event.objects.get(pk=event_id)

    channels = Saleschannel.objects.filter(event=event, deleted=False).values('pk', 'id', 'name', 'url_name')

    # total_revenue_
    total = 0

    for channel in channels:
        sold_tickets = SoldTicket.objects.filter(
            order_nr__sale_channel=channel['pk'],
            order_nr__order_paid=True,
            is_subticket=False
        )

        channel_total = 0

        prices = stats_define_price(sold_tickets)
        # print(prices)
        # print(prices)
        for price in prices:
            # print(float(str(price['price']))
            p = price['price']
            amount = price['amount']

            channel_total += round(amount * float(p), 2)

        total += channel_total
        channel['total'] = channel_total

    # if request.POST:
    #     form = SalesChannelForm(data=request.POST, event_id=event_id)
    #     if form.is_valid():
    #         data = form.cleaned_data
    #         event = Event.objects.get(pk=event_id)
    #         sc = Saleschannel(name=data['name'], url_name=data['url_name'], event=event)
    #         sc.save()
    #         return redirect(reverse('dashboard_event:sales_channels:index', kwargs={'event_id': event_id}))
    # else:


    return render(request, 'dash/event/sales_channels/index.html', base_vars(request, event_id, {
        'channels': channels,
        'total': total,
        'form': SalesChannelForm(),
        'hostname': settings.HOSTNAME
    }))

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


@is_event_from_user(login_url='login')
def create(request, event_id):

    if request.POST:
        form = SalesChannelForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            event = Event.objects.get(pk=event_id)
            sc = Saleschannel(name=data['name'], event=event)
            sc.url_name = iri_to_uri(data['name'])
            sc.save()
            data = {'success': True}
        else:
            data = {'errors': json.loads(form.errors.as_json())}
    else:
        data = {'success': False}

    return JsonResponse(data)


@is_event_from_user(login_url='login')
def edit(request, event_id, channel_id):
    if request.POST:
        form = SalesChannelForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data

            sc = Saleschannel.objects.get(pk=channel_id)
            sc.name = data['name']
            sc.url_name = iri_to_uri(data['name'])

            sc.save()
            return redirect(reverse('dashboard_event:sales_channels:index', kwargs={'event_id': event_id}))
    else:
        channel = Saleschannel.objects.filter(pk=channel_id).values().first()
        form = SalesChannelForm(initial=channel)


    return render(request, 'dash/event/sales_channels/edit.html', base_vars(request, event_id, {
        'form': form

    }))


@is_event_from_user(login_url='login')
def delete(request, event_id, channel_id):
    channel = Saleschannel.objects.get(pk=channel_id, event_id=event_id)

    channel.deleted = True
    channel.save()

    return redirect(reverse('dashboard_event:sales_channels:index', kwargs={'event_id': event_id}))