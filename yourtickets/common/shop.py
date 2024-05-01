from random import randint
import mollie.api.client
from math import ceil
from django.conf import settings
from django.urls import reverse

from yourtickets.common import utils
from ticketshop.models import (
    Event,
    SoldTicket,
    LineUp,
    TicketShopCustom
)

# amount is order price total
def get_service_cost(order_price, tickets_amount, service_cost_discount_cents=0):
    service_cost = (1.45 * tickets_amount) + (0.025 * order_price)

    service_cost = ceil(service_cost * 100) / 100.0

    service_cost_discount = service_cost_discount_cents /100
    service_cost = service_cost - (service_cost_discount  * tickets_amount)

    if service_cost < 0:
        service_cost = 0

    return service_cost

def random_ticket_gen():
    n = 18
    range_start = 10**(n-1)
    range_end = (10**n)-1
    gen_id = randint(range_start, range_end)
    sold = SoldTicket.objects.filter(ticket_gen_id=gen_id)
    if sold:
        return random_ticket_gen()
    return gen_id

def payment_custom(amount, desc, event, order_id):
    molliee = mollie.api.client.Client()

    molliee.set_api_key(settings.MOLLIE_API_KEY)

    url = settings.HOSTNAME + reverse(settings.MOLLIE_REDIRECT_URL, kwargs={
        'order_id': order_id,
        'event_id': event.id
    })

    payment_object = {
        'amount':      {'currency':'EUR','value': str(format(amount, '.2f'))},
        'description': desc,
        'redirectUrl': url,
        'metadata': {'test': 'false'}
    }

    payment_object['webhookUrl'] = settings.HOSTNAME + reverse('mollie_webhook')

    payment = molliee.payments.create(payment_object)
    return payment

def get_price_and_ticket_amount(ticket_key_amount_list, tickets):

    total = 0
    tickets_amount = 0
    tickets_amount_for_service_costs = 0

    for ticket in tickets:
        amount = int(ticket_key_amount_list[str(ticket.pk)])
        ticket_price = float(ticket.price)

        # price.append(ticket_price * amount/100 )
        total += (ticket_price * amount / 100)
        tickets_amount += amount

        if ticket.price != 0:
            tickets_amount_for_service_costs += amount

    return {
        # total amount of tickets
        'tickets_amount': tickets_amount,
        # order price
        'price': total,
        # count the tickets which apply for service costs
        'tickets_amount_for_service_costs': tickets_amount_for_service_costs
    }
