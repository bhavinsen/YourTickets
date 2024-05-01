import datetime
import bleach

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils import timezone

from youradmin.common.decorators import is_event_from_user
from ticketshop.models import (
    Event, Iframe,
    EventOrganiser)
from dashboard.forms import event as event_forms
from dashboard.common.base_vars import base_vars

@is_event_from_user(login_url='login')
@login_required(login_url='login')
def edit_algemeen(request, event_id):
    event = Event.objects.filter(pk=event_id).first()



    form = event_forms.EventForm(data={
        'start_date': event.start_date.strftime('%d-%m-%Y'),
        'start_time': timezone.localtime(event.start_date).strftime('%H:%M'),
        'end_date': event.end_date.strftime('%d-%m-%Y'),
        'end_time': timezone.localtime(event.end_date).strftime('%H:%M'),
        'description': event.description,
        'event_url': event.event_url,
        'title': event.title,
        'location': event.location,
        'show_covid19_info': event.show_covid19_info
    })

    if request.POST:
        postdata = request.POST.copy()
        form = event_forms.EventForm(postdata)

        if form.is_valid():
            start_date = datetime.datetime.strptime(request.POST['start_date'] + " " + request.POST['start_time'], '%d-%m-%Y %H:%M')

            end_date = datetime.datetime.strptime(request.POST['end_date'] + " " + request.POST['end_time'], '%d-%m-%Y %H:%M')

            if start_date > end_date:
                # pass
                form.add_error(None, 'Einddatum bevindt zich voor de startdatum')
                form.fields['start_date'].widget.attrs['class'] = ' form-error'
                form.fields['end_date'].widget.attrs['class'] = ' form-error'

            else:
                event.title = request.POST['title']
                event.location = request.POST['location']

                san = bleach.clean(request.POST['description'], tags=['b', 'p', 'br', 'strong'], strip=True)

                event.description = san
                event.event_url = request.POST['event_url']
                event.start_date = datetime.datetime.strptime(request.POST['start_date'], '%d-%m-%Y').strftime('%Y-%m-%d') + " " + request.POST['start_time']
                event.end_date = datetime.datetime.strptime(request.POST['end_date'], '%d-%m-%Y').strftime('%Y-%m-%d') + " " + request.POST['end_time']

                show_covid19_info = request.POST.get('show_covid19_info', False)

                if show_covid19_info == 'true':
                    show_covid19_info = True
                else:
                    show_covid19_info = False

                event.show_covid19_info = show_covid19_info


                event.save()

                event = Event.objects.filter(pk=event_id).first()

                # IFRAME STUFF
                iframe_urls = Iframe.objects.filter(event_id=event)

                if len(iframe_urls) > 0:
                    iframe_url = iframe_urls[0]
                    iframe_url.url = request.POST.get('iframe_redirect_url', '')
                    iframe_url.save()
                else:
                    iframe_url = Iframe(url=request.POST.get('iframe_redirect_url', ''), event_id=event)
                    iframe_url.save()

                form = event_forms.EventForm(data={
                    'start_date': event.start_date.strftime('%d-%m-%Y'),
                    'start_time': timezone.localtime(event.start_date).strftime('%H:%M'),
                    'end_date': event.end_date.strftime('%d-%m-%Y'),
                    'end_time': timezone.localtime(event.end_date).strftime('%H:%M'),
                    'description': event.description,
                    'event_url': event.event_url,
                    'title': event.title,
                    'location': event.location,
                    'show_covid19_info': event.show_covid19_info
                })
        else:
            form = event_forms.EventForm(postdata)

    iframe_urls = Iframe.objects.filter(event_id=event)

    iframe_url = ''

    if len(iframe_urls) > 0:
        iframe_url = iframe_urls[0].url

    return render(request, 'dash/event/edit/algemeen.html', base_vars(request, event_id,{
        'event_form': form,
        'curl': 'algemeen',
        'iframe_redirect_url': iframe_url
    }))


@is_event_from_user(login_url='login')
@login_required(login_url='login')
def event_delete(request, event_id):
    event = Event.objects.get(pk=event_id)

    event.removed = True
    event.save()

    return JsonResponse({'success': True})


def change_live(request, event_id):
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    event = Event.objects.filter(pk=event_id).first()
    ev_org = EventOrganiser.objects.filter(user=request.user, event_id=event).first()
    if event and ev_org:
        if event.event_public == False:
            event.event_public = True
        else:
            event.event_public = False
        event.save()
    return response