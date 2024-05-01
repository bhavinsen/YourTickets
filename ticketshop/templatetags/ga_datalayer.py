import json
from django.template.defaulttags import register
from django.utils.safestring import mark_safe
from django.utils.html import escapejs
from ticketshop.models import SoldTicket

@register.simple_tag(name='ga_datalayer')
def ga_datalayer(event, page_type, order):

    if page_type == 'Success page':

        tickets = SoldTicket.objects.filter(order_nr=order.id)

        product_list = []

        for ticket in tickets:
            ticket_type = ticket.ticket_type

            product_found = False

            for product in product_list:
                if product['name'] == ticket_type.name:
                    product_found = product

            if product_found != False:
                product_found['quantity'] = product_found['quantity'] + 1
            else:
                product_list.append({
                    'name': ticket_type.name,
                    'id': ticket_type.id,
                    'price': str(ticket.price),
                    'quantity': 1
                })

        return mark_safe("<script>dataLayer =" + json.dumps(
            [{
                'eventName': escapejs(event.title + ' - ' + str(event.pk)),
                'pageType': page_type,
                'ecommerce': {
                    'purchase': {
                        'actionField': {
                            'id': str(order.id),  # Order ID
                            'affiliation': 'Yourtickets',  # Affiliatie(niet verplicht)
                            'revenue': float(order.price+order.service_costs),  # Incl.btw en verzendkosten
                            # 'tax': '5.84',  # BTW(niet verplicht)
                            'shipping': float(order.service_costs)  # Verzendkosten
                        },
                        'products': product_list
                    }
                }
            }]
        ) + ';</script>')
    else:
        return mark_safe("<script>dataLayer ="+ json.dumps(
            [{
                'eventName': escapejs(event.title+' - '+str(event.pk)),
                'pageType': page_type
            }]
        ) + ';</script>')
