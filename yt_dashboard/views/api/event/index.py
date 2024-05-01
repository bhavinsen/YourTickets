import json

from django.conf import settings
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.db.models import CharField, Value

from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from ticketshop.models import (
    Event,
    EventOrganiser,
    TicketShopCustom,
    Ticket,
    LineUp,
    SharedEvents
)
from yt_dashboard.forms.event import (EventGeneralForm)
from yt_dashboard.forms.lineup import LineupForm
from yt_dashboard.forms.ticket import TicketForm
from yt_dashboard.forms.ticketshop_custom import TicketShopCustomFormNew
from yt_dashboard.common.event_utils import (
    get_user_event,
    get_events_from_user_shortlist,
    get_event_url,
)
from yt_dashboard.common.ticket_utils import (
    get_tickets_from_event_shortlist
)



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete(request, id):
    event_from_user = get_user_event(user=request.user, event_id=id)
    event_from_user.removed = True
    event_from_user.save()
    return JsonResponse({'success': True})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getall(request):
    user = request.user
    events = get_events_from_user_shortlist(user=user, include_shared_events=True)
    return JsonResponse(events, safe=False)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def search(request, title_filter=''):
    events = get_events_from_user_shortlist(user=request.user, include_shared_events=True, title_filter=title_filter)
    return JsonResponse(events, safe=False)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get(request, id):
    event = get_user_event(request.user, event_id=id, include_shared_event=True)
    if not event:
        return JsonResponse({'success': False}, safe=False)

    return JsonResponse(get_event_data(id, request.user), safe=False)


def get_event_data(id, user):

    event = get_user_event(user, event_id=id, include_shared_event=True)
    if not event:
        return JsonResponse({'success': False}, safe=False)

    shared_event = getattr(event, 'shared_event', False)

    event = model_to_dict(event)

    event['pk'] = event['id']
    event['shared_event'] = shared_event
    event['start_time'] = timezone.localtime(event['start_date']).strftime('%H:%M')
    event['start_date'] = event['start_date'].strftime('%Y-%m-%d')
    event['end_time'] = timezone.localtime(event['end_date']).strftime('%H:%M')
    event['end_date'] = event['end_date'].strftime('%Y-%m-%d')
    event['primary_color'] = None
    event['secondary_color'] = None
    event['header_img'] = None
    event['bg_img'] = None
    event['can_be_published'] = can_be_published(event)
    event['name'] = event['title']
    event['url'] = get_event_url(event)

    shop_design = TicketShopCustom.objects.filter(event_id=event['id']).first()

    if shop_design:
        shop_design = model_to_dict(shop_design)
        if shop_design.get('header_img'):
            from django.templatetags.static import static
            event['header_img'] = static(shop_design.get('header_img').url)
        if shop_design['bg_img']:
            event['bg_img'] = shop_design.get('bg_img').url

        event['primary_color'] = shop_design['primary_color']
        event['secondary_color'] = shop_design['secondary_color']

    ticket_list = get_tickets_from_event_shortlist(event=event)

    # lineup
    lineups = LineUp.objects.filter(event_id__pk=event['id'])
    lineups_list = list(lineups.values('id', 'artist'))

    return {
        'event': event,
        'tickets': ticket_list,
        'lineups': lineups_list
    }


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_publish(request, id):

    event = get_user_event(request.user, event_id=id)
    if not event:
        return JsonResponse({'success': False}, safe=False)

    can_be = can_be_published(event)

    return JsonResponse({
        'success': True,
        'tab': can_be['tab'],
        'can_be_published': can_be['status']

    })


def can_be_published(event):
    general_form = EventGeneralForm(data=event)

    tickets = Ticket.objects.filter(event_id=event['id'], deleted=False).count()
    tab = 0
    if not general_form.is_valid():
        tab = 2
    elif tickets == 0:
        tab = 4

    return {
        'tab': tab,
        'status': general_form.is_valid() and tickets > 0
    }

from django.http import QueryDict
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create(request):
    user = request.user

    data = request.POST.copy()
    if not bool(data) and len(data) == 0:
        data = QueryDict('', mutable=True)
        data.update(request.data)

    errors = []

    online_event = False
    if data.get('online') == 'true':
        online_event = True

    event_data = {
        'title': data.get('name', ''),
        'location': data.get('event_location', ''),
        'description': '',
        'start_date': data.get('start_date', ''),
        'end_date': data.get('end_date', ''),
        'service_cost': '100',
        'event_public': True,
        'unique_tickets': False,
        'online': online_event,
        'event_url': '',
        # nog implementeren
        # show_covid19_info
    }

    if data.get('id', False):
        event_data['pk'] = data.get('id')

    event = Event(**event_data)
    event_form = EventGeneralForm(data=event_data)

    if not event_form.is_valid():
        errors.append({
            'tab': 2,
            'errors': dict(event_form.errors)
        })

    tickets = json.loads(data.get('tickets', ''))

    someticket_form_invalid = False
    ticket_objects_to_save = []
    for ticket in tickets:
        start_date = str(ticket.get('start_date', ''))
        end_date = str(ticket.get('end_date',''))

        ticket_data = {
            'event': event,
            'name': ticket.get('name', ''),
            'description': '',
            'price': ticket.get('price',''),
            'quantity': ticket.get('amount',''),
            'start_date': start_date + " " + ticket.get('start_time', ''),
            'end_date': end_date + " " + ticket.get('end_time', ''),
            'max_sold': ticket.get('amount_per_order',''),
            'person_amount': ticket.get('persons_per_ticket', '')
        }
        ticket_obj = Ticket(**ticket_data)
        ticket_form = TicketForm(ticket_data)

        if not ticket_form.is_valid():
            someticket_form_invalid = True

        ticket_objects_to_save.append(ticket_obj)

    # if all ticket forms are fine
    # remove all tickets
    # save all ticket objects from above
    if someticket_form_invalid:
        errors.append({
            'tab': 4,
            # 'errors': dict(event_form.errors)
        })

    some_lineup_invalid = False
    lineups_to_save = []
    # save lineup
    lineup = json.loads(data.get('lineup', ''))
    for artist in lineup:
        lineup_data = {
            'artist': artist.get('artist', ''),
            'event_id': event
        }
        lineup_form = LineupForm(data=lineup_data)
        artist = LineUp(**lineup_data)

        if not lineup_form.is_valid():
            some_lineup_invalid = True

        lineups_to_save.append(artist)

    if some_lineup_invalid:
        errors.append({
            'tab': 5,
            # 'errors': dict(event_form.errors)
        })

    if len(request.FILES) > 0:

        # save design
        event.save()
        obj, created = TicketShopCustom.objects.get_or_create(event_id=event)
        data['event_id'] = event.pk
        form = TicketShopCustomFormNew(data=data, files=request.FILES, instance=obj)

        if form.is_valid():
            form.save()
        else:
            print('aaaaaahhhhhhh')
            pass

    if len(errors) == 0:
        # save all
        event.save()
        if not EventOrganiser.objects.filter(user=user, event=event).exists():
            EventOrganiser(user=user, event=event, admin_rights=2).save()

        Ticket.objects.filter(event=event.pk).delete()
        for t in ticket_objects_to_save:
            t.save()

        LineUp.objects.filter(event_id=event.pk).delete()
        for t in lineups_to_save:
            t.save()

        result = get_event_data(event.id, request.user)
        result['success'] = True

        return JsonResponse(result, safe=False)
    else:
        return JsonResponse({'success': False, 'errors': errors})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def publish(request, id):
    event = get_user_event(request.user, event_id=id)
    if not event:
        return JsonResponse({'success': False}, safe=False)

    # before publish call check_event
    _toggle_publish(event=event, event_public=True)

    return JsonResponse({'success': False}, safe=False)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def unpublish(request, id):
    event = get_user_event(request.user, event_id=id)
    if not event:
        return JsonResponse({'success': False}, safe=False)

    # before publish call check_event
    _toggle_publish(event=event, event_public=False)

    return JsonResponse({'success': False}, safe=False)


def _toggle_publish(event, event_public):
    event.event_public = event_public
    event.save()
