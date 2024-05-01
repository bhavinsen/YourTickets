from django.utils import timezone

from ticketshop.models import (
    Ticket
)


def get_tickets_from_event(event):
    return Ticket.objects.filter(event__pk=event['id'], deleted=False).order_by('pk')


def get_tickets_from_event_shortlist(event):
    tickets = get_tickets_from_event(event=event)
    ticket_list = list(tickets.values(
        'pk', 'name', 'description', 'price',
        'quantity', 'start_date', 'end_date',
        'max_sold', 'person_amount'
    ))

    for ticket in ticket_list:
        ticket['start_time'] = timezone.localtime(ticket['start_date']).strftime('%H:%M')
        ticket['start_date'] = ticket['start_date'].strftime('%Y-%m-%d')

        ticket['end_time'] = timezone.localtime(ticket['end_date']).strftime('%H:%M')
        ticket['end_date'] = ticket['end_date'].strftime('%Y-%m-%d')

        ticket['persons_per_ticket'] = ticket['person_amount']
        ticket['amount_per_order'] = ticket['max_sold']
        ticket['amount'] = ticket['quantity']

    return ticket_list
