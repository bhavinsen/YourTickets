from django.db.models import Count

from ticketshop.models import (Event, PageViews)

from yt_dashboard.common.event_utils import get_events_from_user


def get_visitors(user, date_from=None, date_till=None, event=None, unique=False):

    event_filter = {
        'eventorganiser__user__pk':user.pk,
        'removed':False
    }
    if event:
        event_filter['id']=event.id
    events_ids_user = Event.objects.filter(**event_filter).values_list('id', flat=True)

    filters = {
        'event_id__in': [str(x) for x in events_ids_user]
    }

    if date_from and date_till:
        filters['date__range'] = (date_from, date_till)
    
    if unique:
        visitors = PageViews.objects.values('uuid').annotate(Count('id')).filter(**filters).count()
    else:
        visitors = PageViews.objects.annotate(Count('id')).filter(**filters).count()

    return visitors
