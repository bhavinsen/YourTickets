from dashboard.common.helpers import get_username
from ticketshop.models import (
    Event, EventOrganiser,
    TicketShopCustom,
    SharedEvents
)
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.db.models import Q


def get_events_from_user(user):
    basic_filters = [Q(
            Q(eventorganiser__admin_rights=EventOrganiser.ROLE_OWNER)
            |
            Q(eventorganiser__admin_rights=EventOrganiser.ROLE_ADMINISTRATOR)
            |
            Q(eventorganiser__admin_rights=EventOrganiser.ROLE_VIEW),
            eventorganiser__user__pk=user.pk,
            removed=False,
        )]
    
    events = Event.objects.filter(
        *basic_filters
    ).order_by('-pk')
    return events

def base_vars(request, event_id=None, new_data={}):

    events_from_user = get_events_from_user(request.user)
    
    cshop = []

    for item in events_from_user:
        cshopObj = TicketShopCustom.objects.filter(event_id=item.id).first()
        if cshopObj:
            if cshopObj.header_img:
                cshop.append(cshopObj.header_img.url)
            else:
                cshop.append("")

    event_id = int(event_id)
    event = None
    tsc = None
    event_url = ""
    event_date = ""
    event_is_shared_event = False
    if event_id > 0 :
        event = Event.objects.filter(pk=event_id).order_by('-id').first()
        
        if not event:
            event = EventOrganiser.objects.filter(user=request.user).first().event
                
        if event:
            event_id=event.pk
            event_url_str = event.event_url
            if event_url_str == "":
                event_url_str = event.title
            event_url = reverse('buy_ticket', kwargs={'event_id': event.id, 'event_name': event_url_str})

            tsc = TicketShopCustom.objects.filter(event_id=event).first()

            # this is a repitition
            #event = Event.objects.filter(pk=event_id).first()
            start = timezone.localtime(event.start_date)
            end = timezone.localtime(event.end_date)
            event_date = start.strftime("%d %B %y | %H:%M") + " - " + end.strftime("%H:%M")
    
            
            if SharedEvents.objects.filter(user=request.user, event=event.pk).exists():
                # shared_ev = SharedEvents.objects.filter(user=request.user, event=event.pk)[0]
                # ev = Event.objects.filter(event=event.pk)[0]
                try:
                    Event.objects.get(eventorganiser__user=request.user, pk=event.pk)

                except:
                    event_is_shared_event = True

    shared_events = SharedEvents.objects.filter(user=request.user).select_related('event')

    return merge_two_dicts({
        'event_is_shared_event': event_is_shared_event,
        'event_list': events_from_user,
        'cshop': cshop,
        'event_url': event_url,
        'cur_event': event,
        'username_full': get_username(request),
        'ticketshop': tsc,
        'event_date': event_date,
        'shared_events': shared_events,
        'dashboard_url': settings.DASHBOARD_URL
    }, new_data)

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z