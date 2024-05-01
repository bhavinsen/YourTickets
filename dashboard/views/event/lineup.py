from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from youradmin.common.decorators import is_event_from_user
from dashboard.common.base_vars import base_vars
from ticketshop.models import LineUp, Event


@is_event_from_user(login_url='login')
@login_required(login_url='login')
def index(request, event_id):
    event = Event.objects.filter(pk=event_id).first()
    lineup = LineUp.objects.filter(event_id=event).order_by('pk')

    artists = request.POST.getlist('artiest_naam[]')
    ids = request.POST.getlist('artiest_id[]')
    x = 0
    for item in artists:
        if x <= len(ids):
            lu = LineUp.objects.filter(pk=ids[x]).first()
            lu.artist = item
            lu.save()
        else:
            lu = LineUp(event_id=event, artist=item)
            lu.save()
        x += 1


    return render(request, 'dash/event/edit/lineup.html', base_vars(request, event_id, {
        'lineup': lineup,
        'curl': 'lineup'
    }))


@is_event_from_user(login_url='login')
@login_required(login_url='login')
def remove_item(request, event_id, item_id):
    event = Event.objects.filter(pk=event_id).first()
    LineUp.objects.get(event_id=event, pk=item_id).delete()
    return HttpResponseRedirect(reverse('dashboard_event_lineup', kwargs={'event_id': event_id}))


@is_event_from_user(login_url='login')
@login_required(login_url='login')
def add_item(request, event_id):
    event = Event.objects.filter(pk=event_id).first()
    lineUpObj = LineUp(event_id=event, artist="", url="")
    lineUpObj.save()
    return HttpResponseRedirect(reverse('dashboard_event_lineup', kwargs={'event_id': event_id}))