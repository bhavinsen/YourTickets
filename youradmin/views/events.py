import json
import operator
from django.contrib.admin.views.decorators import staff_member_required
from youradmin.common.decorators import group_required
from django.shortcuts import (
    render
)
from django.urls import reverse
from functools import reduce
from django.http import JsonResponse
from django.core import serializers
from django.http.request import QueryDict
from youradmin.common.datatable import build_order_args, build_search_args, get_single_dict_array
from ticketshop.models import Event

def get_cols_events():
    return [
        {"title": "id", "data": "pk", "searchType": "exact"},
        {"title": "title", "data": "fields.title"},
        {"title": "start date", "data": "fields.start_date", "searchType": "range", "linked_range": 3},
        {"title": "ticket amount", "data": "fields.ticket_amount", "skipSearch": True},
        {"title": "total tickets", "data": "fields.total_tickets", "skipSearch": True},
        {"title": "total persons", "data": "fields.total_person_amount", "skipSearch": True},
        {"title": "total price", "data": "fields.total_price", "skipSearch": True},
        {"title": "total service cost", "data": "fields.total_service_costs", "skipSearch": True},
        



        {"title": "action", "data": None, "types":
            {
                'linkicon': {
                    'url': reverse('youradmin_financial:get_event_detail', kwargs={
                        'event_id': '_placeholder'}),
                    'hover': 'See orders',
                    'action_id_property': 'pk',
                    'iconCls': 'glyphicon-list-alt'
                }
            }
         }
    ]


@group_required('financial')
@staff_member_required(login_url='/youradmin/login/')
def index(request):

    data = {}
    data['from_event_id'] = 0
    data['to_event_id'] = 9999

    return render(request, 'youradmin/events/index.html', {
       
        'datatables_config': json.dumps({
            'pageLength': request.GET.get('pageLength', 20),
            'columns': get_cols_events(),
            'ajax': {
                'url': reverse('youradmin_events:list', kwargs={}),
                'data' : data,
                'action_id_property': 'pk',
            }

        })
    })



##########
@group_required('financial')
@staff_member_required(login_url='/youradmin/login/')
def update_totals(request):

    #source = json.loads(request.body.decode('utf-8'))
    source = QueryDict(request.body)
    print (source)

    from_event_id = source['from_event_id'] or 0
    to_event_id = source['to_event_id'] or 9999 




    print (from_event_id )
    print (to_event_id )
  #  events = Event.objects.filter(pk__range=(from_event_id,to_event_id))
    events = Event.objects.order_by('pk')
    
    e = 0
    t =0
    for event in events:
     #   print (event.id )
        tickets = event.get_tickets()
        for ticket in tickets:
            ticket.update_totals()
            t += 1
        event.update_tickets_totals()
        e += 1


    #return f'Events: {e}, Tickets: {t}'
    return JsonResponse({
        "Events": e,
        "Tickets": t,
        "data": "nothing"
    })    


#################
@group_required('financial')
@staff_member_required(login_url='/youradmin/login/')
def events_list(request):

    source = QueryDict(request.body)

    page_length   = int( source['length'] or 100 )
    data_start    = int( source['start'] or 0 )
    from_event_id = int( source['from_event_id'] or 0 )
    to_event_id   = int( source['to_event_id'] or 9999 )

    order_args = build_order_args(request.POST, get_cols_events())


    records = Event.objects.filter(pk__range=(from_event_id,to_event_id)).order_by(*order_args)
    total = Event.objects.filter(pk__range=(from_event_id,to_event_id)).count()

    events_data_json = serializers.serialize("json", records[data_start:data_start+page_length])

    events_data_load = json.loads(events_data_json)


    return JsonResponse({
        "recordsTotal": total,
        "recordsFiltered": total,
        "data": events_data_load

    })    