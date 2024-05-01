import json
import operator
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import (
    render
)
from django.urls import reverse
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.models import User
from functools import reduce

from ticketshop.models import UserExtra, Order, Event, SoldTicket, Ticket
from yourtickets.common import shop, ticket
from youradmin.common.datatable import build_order_args, build_search_args, get_single_dict_array
from youradmin.views.forms.orders import ResendTicketsForm
from yourtickets.tasks import (
    send_mail_order
)

def get_cols_order_list():
    return [
        {"title": "id", "data": "pk", "searchType": "exact"},
        {"title": "email", "data": "fields.email"},
        {"title": "betaald", "data": "fields.order_paid", "render": "truefalse_field_renderer"},
        {"title": "date", "data": "fields.date"},
        {"title": "mollie id", "data": "fields.mollie_id"},
        {"title": "Order price", "data": "order_price"},
        {"title": "order send", "data": "fields.mail_send", "render": "truefalse_field_renderer"},
        {"title": "email allowed", "data": "fields.email_allowed", "render": "truefalse_field_renderer"},
        {"title": "action", "data": None, "types": {
            'delete': {
                'url': reverse('youradmin_orders_send', kwargs={'order_id': '_placeholder'}),
                'iconCls': 'glyphicon-envelope',
                'modal_id': 'order_resend',
                'hover': 'Resend order',
                'action_id_property': 'pk',
                'color': '#ec971f'
            }

        }}
    ]



@staff_member_required(login_url='/youradmin/login/')
def dashboard(request):

    return render(request, 'youradmin/orders/dashboard.html', {

        # 'datatables_config': json.dumps({
        #     'pageLength': request.GET.get('pageLength', 10),
        #     'columns': get_cols_user(),
        #     'ajax': {
        #         'url': reverse('youradmin_users_getlist', kwargs={})
        #     }
        #
        # })
    })

@staff_member_required(login_url='/youradmin/login/')
def orderlist(request):
    return render(request, 'youradmin/orders/list.html', {
        'orderform': ResendTicketsForm(),
        'datatables_config': json.dumps({
            'pageLength': request.GET.get('pageLength', 10),
            'columns': get_cols_order_list(),
            "order": [[ 0, "desc" ]],
            'ajax': {
                'url': reverse('youradmin_orders_getlist', kwargs={})
            }

        })
    })

@staff_member_required(login_url='/youradmin/login/')
def getlist(request):
    source = request.POST

    page_length = int(source.get('length', 1))
    data_start = int(source.get('start', 0))

    order_args = build_order_args(request.POST, get_cols_order_list())

    postdata = request.POST.copy()

    search_dict = get_single_dict_array(postdata, 'search')

    mail_search = None
    for column_key in search_dict:
        if column_key == 1:
            mail_search = Q(user__email__icontains=search_dict[column_key])
            del postdata['search[1]']
            pass

    search_args = build_search_args(postdata, get_cols_order_list())

    if mail_search:
        search_args.append(mail_search)

    if len(order_args) == 0:
        order_args.append('date')

    if len(search_args) > 0:
        orders = Order.objects.filter(reduce(operator.or_, search_args)).order_by(*order_args)[data_start:data_start+page_length]
        total = Order.objects.filter(reduce(operator.or_, search_args)).count()
    else:
        orders = Order.objects.all().select_related('user').order_by(*order_args)[data_start:data_start+page_length]
        total = Order.objects.all().count()

    order_prices = dict()
    users_for_orders = dict()

    temp_orders = []

    for order in orders:
        # get the event

        tickets = SoldTicket.objects.filter(order_nr=order).select_related('ticket_type')

        order_price = 0
        tickets_amount = 0
        # get the price for the ticket in ticket table
        for ticket in tickets:
            order_price += float(ticket.ticket_type.price)/100
            tickets_amount += 1

        # get the price and add service costs added to it
        order_prices[order.id] = "{0:.2f}".format(order_price+shop.get_service_cost(order_price, tickets_amount, 0))

        # serialization doesnt do a good job at foreign tables so lets build it manually
        single_row = {
            'pk': order.pk,
            'mollie_id': order.mollie_id,
            'order_paid': order.order_paid,
            'date': order.date,
            'mail_send': order.mail_send,
            'email_allowed': order.email_allowed,
            'ordered_in_language': order.ordered_in_language,
            'price': order.price,
            'service_costs': order.service_costs,
            'payment_method': order.payment_method,
            'email': order.user.email,
            'order_price': "{0:.2f}".format(order.price+order.service_costs)
        }

        temp_orders.append({'fields': single_row, 'pk': order.pk, 'order_price':  "{0:.2f}".format(order.price+order.service_costs)})

        # users_for_orders[order.id] =

    # dit is de werkende
    # orders_data_json = serializers.serialize("json", orders)
    # users_data_load = json.loads(orders_data_json)
    users_data_load = temp_orders

    #test
    # users_data_load = orders.values_list('pk','mollie_id', 'order_paid', 'date', 'mail_send', 'email_allowed', 'ordered_in_language', 'price', 'service_costs', 'payment_method')

    #print(users_data_load)

    for order in users_data_load:
        #if order['pk'] in order_prices:
        #    order['order_price'] = order_prices[order['pk']]
        #else:
        #     order['order_price'] = 0

        if order['fields']['order_paid'] and order['fields']['mail_send']:
            order['finalized'] = True

        # order['user_id'] = user.pk
        order['order_id'] = order.get('pk')
        # order['email'] = 'jan@adf'

    return JsonResponse({
        "recordsTotal": total,
        "recordsFiltered": total,
        "data": users_data_load
    })

@staff_member_required(login_url='/youradmin/login/')
def delete(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        order.delete()
    except:
        return JsonResponse({"success": False, 'error': "Order not found"})

    return JsonResponse({"success": True})

@staff_member_required(login_url='/youradmin/login/')
def send(request, order_id):

    order = Order.objects.get(pk=order_id)

    try:
        form = ResendTicketsForm(request.POST)

        if form.is_valid():
            # send_mail_order.delay(order_id=order.pk, email=form.cleaned_data['email'])
            ticket.send_mail_and_create_pdfs(order, form.cleaned_data['email'])
        else:
            # send_mail_order.delay(order_id=order.pk, email=None)
            ticket.send_mail_and_create_pdfs(order)
            order.mail_send = True
            order.save()

    except Exception as e:

        return JsonResponse({"success": False, 'error': "Error sending ticket ("+str(e)+")"})

    return JsonResponse({"success": True})

from django.db.models import Q

def test(request):

    event = Event.objects.get(pk=142)
    querysetf = Ticket.objects.filter(event=event)
    resultlist = []
    for item in querysetf:
        resultlist.append(item.id)

    a = SoldTicket.objects.filter(Q(event=event), Q(ticket_type__in=resultlist) | Q(is_guest_ticket=True) | Q(is_special_guest_ticket=True))
    print(a)
    return
