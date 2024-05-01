from itertools import chain
from datetime import datetime
from django.db.models import Q
from django.db.models import CharField, Value
from django.urls import reverse
from django.conf import settings
from ticketshop.models import (
    Event,
    EventOrganiser,
    SharedEvents
)


def get_user_event(user, event_id, include_shared_event=False):
    try:
        return Event.objects.annotate(shared_event=Value('false', output_field=CharField())).get(
            Q(
                Q(eventorganiser__admin_rights=EventOrganiser.ROLE_OWNER)
                |
                Q(eventorganiser__admin_rights=EventOrganiser.ROLE_ADMINISTRATOR)
                |
                Q(eventorganiser__admin_rights=EventOrganiser.ROLE_VIEW),
                eventorganiser__user__pk=user.pk,
                pk=event_id,
                removed=False,
            )
        )
    except:
        try:
            if include_shared_event:
                shared_event = SharedEvents.objects.get(user=user, event_id=event_id)
                return Event.objects.filter(removed=False, pk=shared_event.event_id).annotate(
                    shared_event=Value('true', output_field=CharField())).first()
            else:
                return False
        except:
            return False


def get_events_from_user(user, include_shared_events=False, title_filter=None):
    basic_filters = [Q(
            Q(eventorganiser__admin_rights=EventOrganiser.ROLE_OWNER)
            |
            Q(eventorganiser__admin_rights=EventOrganiser.ROLE_ADMINISTRATOR)
            |
            Q(eventorganiser__admin_rights=EventOrganiser.ROLE_VIEW),
            eventorganiser__user__pk=user.pk,
            removed=False,
        )]
    if title_filter:
        basic_filters.append(Q(title__startswith=title_filter))

    events = Event.objects.filter(
        *basic_filters
    ).annotate(shared_event=Value('false', output_field=CharField())).order_by('-pk')

    if include_shared_events:
        shar_ev = list(SharedEvents.objects.filter(user=user).values_list('event_id', flat=True))
        basic_filters = [
            Q(removed=False),
            Q(pk__in=shar_ev)
        ]
        if title_filter:
            basic_filters.append(Q(title__startswith=title_filter))
        shared_events_from_user = Event.objects.filter(*basic_filters).annotate(
            shared_event=Value('true', output_field=CharField()))

        # events = list(chain(events, shared_events_from_user))
        events.union(shared_events_from_user)
        # events = shared_events_from_user | events
    # print(events[7].pk)
    # print(events[7].shared_event)
    return events


def get_event_url(event):
    event_url_str = event['event_url']
    if event_url_str == "":
        if event['title'] == "":
            event['title'] = 'LEEG'
        event_url_str = event['title']

    return settings.HOSTNAME + reverse('buy_ticket', kwargs={'event_id': event['pk'], 'event_name': event_url_str})


def get_events_from_user_shortlist(user, include_shared_events=False, title_filter=None):
    events = get_events_from_user(user, include_shared_events=include_shared_events, title_filter=title_filter)
    events = list(events.values('title', 'location', 'start_date', 'event_public', 'event_url', 'pk', 'shared_event'))

    for event in events:
        event['url'] = get_event_url(event)
        event['name'] = event['title']
        event['start_date'] = datetime.strftime(event['start_date'], '%d-%m-%Y')

    return events
