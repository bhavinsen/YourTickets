import re
import datetime

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from youradmin.common.decorators import is_event_from_user
from yourtickets.common import  shop
from dashboard.common.base_vars import base_vars
from ticketshop.models import Ticket, Event, SoldTicket


@is_event_from_user(login_url='login')
@login_required(login_url='login')
def index(request, event_id):
    event = Event.objects.filter(pk=event_id).first()

    if request.POST:
        ids = request.POST.getlist('ticket_id[]')
        names = request.POST.getlist('ticket_naam[]')
        start_dates = request.POST.getlist('ticket_begin_datum[]')
        start_times = request.POST.getlist('ticket_begin_tijd[]')
        end_dates = request.POST.getlist('ticket_eind_datum[]')
        end_times = request.POST.getlist('ticket_eind_tijd[]')
        prices = request.POST.getlist('ticket_prijs[]')
        quantitys = request.POST.getlist('ticket_aantal[]')
        maxsolds = request.POST.getlist('ticket_aantal_max[]')
        person_amount = request.POST.getlist('person_amount[]')



        x = 0
        for item in names:
            ticket_price_integer = int(re.sub("[^0-9]", "", prices[x]) )
            #ticket_price = float( ticket_price_integer ) / 100
            #ticket_service_costs_gross = shop.get_service_cost(ticket_price, 1, 0)
            #ticket_service_costs = shop.get_service_cost(ticket_price, 1, event.service_cost_discount_cents)
            #ticket_service_costs_discount = ticket_service_costs_gross - ticket_service_costs
            
            
            ticket = Ticket.objects.filter(pk=ids[x]).first()
            ticket.name = names[x]
            #ticket.price = re.sub("[^0-9]", "", prices[x])
            ticket.price = ticket_price_integer
            ticket.quantity = quantitys[x]
            ticket.max_sold = maxsolds[x]

            corrected_start_date = datetime.datetime.strptime(start_dates[x], '%d-%m-%Y').strftime('%Y-%m-%d')
            corrected_end_date = datetime.datetime.strptime(end_dates[x], '%d-%m-%Y').strftime('%Y-%m-%d')

            ticket.start_date = corrected_start_date + ' ' + start_times[x]
            ticket.end_date = corrected_end_date + ' ' + end_times[x]
            ticket.person_amount = person_amount[x]
            
            #ticket.service_costs_gross = ticket_service_costs_gross * float(quantitys[x])
            #ticket.service_costs = ticket_service_costs * float(quantitys[x])
            #ticket.service_costs_discount = ticket_service_costs_discount * float(quantitys[x])
            #ticket.total = ticket_price * float(quantitys[x])
            #ticket.total_person_amount = int(person_amount[x]) * int(quantitys[x])
            ticket.save()
            ticket.update_totals()
            x += 1

    tickets = Ticket.objects.filter(event_id=event, deleted=False).order_by('pk')

    for ticket in tickets:
        start = timezone.localtime(ticket.start_date)
        end = timezone.localtime(ticket.end_date)
        ticket.start_time = start.strftime("%H:%M")
        ticket.start_date = start.strftime("%d-%m-%Y")
        ticket.end_time = end.strftime("%H:%M")
        ticket.end_date = end.strftime("%d-%m-%Y")

    event.update_tickets_totals()

    return render(request, 'dash/event/edit/tickets.html', base_vars(request, event_id, {
        'tickets': tickets
    }))


@is_event_from_user(login_url='login')
@login_required(login_url='login')
def remove_item(request, event_id, item_id):
    ticket = Ticket.objects.get(pk=item_id)
    # if ticket is allready sold deactivate it
    sold_tickets = SoldTicket.objects.filter(ticket_type=ticket).count()
    if sold_tickets > 0:
        ticket.deleted = True
        ticket.save()
    else:
        ticket.delete()
    return HttpResponseRedirect(reverse('dashboard_event_tickets', kwargs={'event_id': event_id}))


@is_event_from_user(login_url='login')
@login_required(login_url='login')
def add_item(request, event_id):
    event = Event.objects.filter(pk=event_id).first()
    date = datetime.datetime.now()
    ticketObj = Ticket(event_id=event_id, price=0, quantity=0, start_date=date, end_date=event.start_date,
                        service_costs=0.0, service_costs_gross=0.0, service_costs_discount=0.0, total=0.0, 
                        total_person_amount =0)
    ticketObj.save()
    return HttpResponseRedirect(reverse('dashboard_event_tickets', kwargs={'event_id': event_id}))
