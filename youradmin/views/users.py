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
from yourtickets.common import shop
from youradmin.common.datatable import build_order_args, build_search_args

def get_cols_user():
    return [
        {"title": "id", "data": "pk", "searchType": "exact"},
        {"title": "firstname", "data": "fields.first_name"},
        {"title": "lastname", "data": "fields.last_name"},
        {"title": "username", "data": "fields.username"},
        {"title": "email", "data": "fields.email"},
        {"title": "superuser", "data": "fields.is_superuser",
         "render": "truefalse_field_renderer"},
        {"title": "staff", "data": "fields.is_staff", "render": "truefalse_field_renderer"},
        {"title": "active", "data": "fields.is_active", "render": "truefalse_field_renderer"},
        {"title": "action", "data": None, "types":
            {
                'linkicon': {
                    'url': reverse('youradmin_users_orders', kwargs={
                        'user_id': '_placeholder'}),
                    'hover': 'See orders',
                    'action_id_property': 'pk',
                    'iconCls': 'glyphicon-list-alt'
                },
                'delete': {
                    'url': reverse('youradmin_users_delete', kwargs={
                        'user_id': '_placeholder'}),
                    'modal_id': 'user_delete',
                    'hover': 'Delete user',
                    'action_id_property': 'pk'
                }


            }
         }
    ]



@staff_member_required(login_url='/youradmin/login/')
def index(request):

    return render(request, 'youradmin/users/list.html', {
        'datatables_config': json.dumps({
            'pageLength': request.GET.get('pageLength', 10),
            'columns': get_cols_user(),
            'ajax': {
                'url': reverse('youradmin_users_getlist', kwargs={})
            }

        })
    })



@staff_member_required(login_url='/youradmin/login/')
def getlist(request):

    source = request.POST

    page_length = int(source.get('length', 1))
    data_start = int(source.get('start', 0))

    order_args = build_order_args(request.POST, get_cols_user())

    search_args = build_search_args(request.POST, get_cols_user())

    if len(order_args) == 0:
        order_args.append('id')

    if len(search_args) > 0:
        users = User.objects.filter(reduce(operator.or_, search_args)).order_by(*order_args)[data_start:data_start+page_length]
        total = User.objects.filter(reduce(operator.or_, search_args)).count()
    else:
        users = User.objects.all().order_by(*order_args)[data_start:data_start+page_length]
        total = User.objects.all().count()

    users_data_json = serializers.serialize("json", users)

    users_data_load = json.loads(users_data_json)

    return JsonResponse({
        "recordsTotal": total,
        "recordsFiltered": total,
        "data": users_data_load
    })


@staff_member_required(login_url='/youradmin/login/')
def delete(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user.delete()
    except:
        return JsonResponse({"success": False, 'error': "User not found"})

    return JsonResponse({"success": True})

@staff_member_required(login_url='/youradmin/login/')
def orders(request, user_id):

    user = User.objects.get(pk=user_id)

    # aantal tickets , # order totaal bedrag
    return render(request, 'youradmin/users/orders.html', {
        'user': user,
        'datatables_config': json.dumps({
            'pageLength': request.GET.get('pageLength', 10),
            'columns': [
                        {"title": "id", "data": "pk"},
                        {"title": "betaald", "data": "fields.order_paid", "render": "truefalse_field_renderer"},
                        {"title": "date", "data": "fields.date"},
                        {"title": "mollie id", "data": "fields.mollie_id"},
                        {"title": "Order price", "data": "order_price"},
                        {"title": "order send", "data": "fields.mail_send", "render": "truefalse_field_renderer"},
                        {"title": "email allowed", "data": "fields.email_allowed", "render": "truefalse_field_renderer"},
                        {"title": "action", "data": None, "types": {
                            'linkicon': {
                                'url': reverse('youradmin_users_orders_tickets', kwargs={
                                    'user_id': '_placeholder1',
                                    'order_id': '_placeholder2'
                                }),
                                'urlbuild': {
                                    '_placeholder1': 'user_id',
                                    '_placeholder2': 'pk',
                                    # example keep it
                                    # '_placeholder2': [
                                    #     'fields',
                                    #     'pk'
                                    # ]

                                },
                                'hover': 'See orders',
                                'action_id_property': 'pk',
                                'iconCls': 'glyphicon-list-alt'
                            },
                            'delete': {
                                'url': reverse('youradmin_orders_delete', kwargs={
                                    'order_id': '_placeholder'}),
                                'modal_id': 'order_delete',
                                'hover': 'Delete order',
                                'action_id_property': 'pk'
                            },
                            'delete': {
                                'url': reverse('youradmin_orders_send', kwargs={
                                    'order_id': '_placeholder'}),
                                'iconCls': 'glyphicon-envelope',
                                'modal_id': 'order_resend',
                                'hover': 'Resend order',
                                'action_id_property': 'pk',
                                'color': '#ec971f'
                            },

                        }}],
            'highlight_row': {
                'data': 'finalized', 'comparator': '==', 'value': True
            },
            'ajax': {
                'url': reverse('youradmin_users_orders_getlist', kwargs={'user_id': user.id})
            }

        })
    })


@staff_member_required(login_url='/youradmin/login/')
def get_orders_list(request, user_id):

    user = User.objects.get(pk=user_id)

    source = request.POST
    page_length = int(source.get('length', 1))
    data_start = int(source.get('start', 0))

    user_orders = Order.objects.filter(user=user).order_by('id')[data_start:data_start+page_length]
    total = Order.objects.filter(user=user).count()

    # per verkochte ticket is er een soldticket record

    order_prices = dict()

    for order in user_orders:
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

    data_json = serializers.serialize("json", user_orders)

    data_load = json.loads(data_json)

    for order in data_load:
        if order['pk'] in order_prices:
            order['order_price'] = order_prices[order['pk']]
        else:
            order['order_price'] = 0

        if order['fields']['order_paid'] and order['fields']['mail_send']:
            order['finalized'] = True

        order['user_id'] = user.pk
        order['order_id'] = order.get('pk')

    return JsonResponse({
        "recordsTotal": total,
        "recordsFiltered": total,
        "data": data_load
    })

@staff_member_required(login_url='/youradmin/login/')
def get_tickets_for_order(request, user_id, order_id):

    user = User.objects.get(pk=user_id)
    order = Order.objects.get(pk=order_id)

    return render(request, 'youradmin/users/tickets_for_order.html', {
        'user': user,
        'order': order,
        'datatables_config': json.dumps({
            'pageLength': request.GET.get('pageLength', 10),
            'columns': [
                {"title": "id", "data": "id"},
                {"title": "ticket name", "data": "ticketname"},
                {"title": "event", "data": "eventname"},
                {"title": "event location", "data": "eventlocation"},
                {"title": "price", "data": "price"},
                {"title": "checked", "data": "checked", "render": "truefalse_field_renderer"},
            ],

            'ajax': {
                'url': reverse('youradmin_users_orders_tickets_getlist', kwargs={'user_id': user.id, 'order_id': order.pk})
            }

        })
    })

@staff_member_required(login_url='/youradmin/login/')
def get_tickets_for_order_list(request, user_id, order_id):

    order = Order.objects.get(pk=order_id)
    source = request.POST
    page_length = int(source.get('length', 1))
    data_start = int(source.get('start', 0))

    soldTickets = SoldTicket.objects.filter(order_nr=order).select_related('ticket_type')[data_start:data_start+page_length]
    total = SoldTicket.objects.filter(order_nr=order).count()
    data = list()

    for ticket in soldTickets:
        ticketref = ticket.ticket_type
        event = ticketref.event

        ticket_price = ticket.price
        if ticket_price == 0:
            ticket_price = "{0:.2f}".format(ticketref.price / 100) + '!'

        data.append({
            'id': ticket.id,
            'ticketname': ticket.ticket_type.name,
            'eventname': event.title,
            'eventlocation': event.location,
            'price': ticket_price,
            'checked': ticket.checked
        })

    return JsonResponse({

        "recordsTotal": total,
        "recordsFiltered": total,
        "data": data
    })
