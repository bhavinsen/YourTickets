import json

from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.encoding import iri_to_uri

from dashboard.common.base_vars import base_vars
from dashboard.forms.shared_events import SharedEventsForm, TempSharedEventsForm
from youradmin.common.decorators import is_event_from_user
from ticketshop.models import TempSharedEvents, SharedEvents, Event, SoldTicket,TicketShopCustom
from yourtickets.common.mail import create_mail
from django.template.loader import render_to_string



@is_event_from_user(login_url='login')
def index(request, event_id):

    event = Event.objects.get(pk=event_id)

    users = SharedEvents.objects.filter(event=event).select_related('user')
    temp_users = TempSharedEvents.objects.filter(event=event)

    # print(users[0].username)

    return render(request, 'dash/event/share_event/index.html', base_vars(request, event_id, {
        'users': users,
        'temp_users': temp_users,
        'form': TempSharedEventsForm(),
        'hostname': settings.HOSTNAME
    }))


@is_event_from_user(login_url='login')
def create(request, event_id):

    if request.POST:
        data = request.POST.copy()
        data['event'] = Event.objects.get(pk=event_id)

        # if user exist in the db share right away!
        if User.objects.filter(username=data['user_email']).exists():
            form = SharedEventsForm(data=data)
            data['user'] = User.objects.get(username=data['user_email']).pk
            if form.is_valid():
                SharedEvents.objects.create(event=Event.objects.get(pk=event_id), user=User.objects.get(username=data['user_email']))
        else:
            # data['user_email'] = data['email']
            form = TempSharedEventsForm(data=data)
            if form.is_valid():
                event = Event.objects.get(pk=event_id)
                cshop = TicketShopCustom.objects.filter(event_id=event.id).first()
                TempSharedEvents.objects.create(event=event,
                                                user_email=data['user_email'])
                url = settings.HOSTNAME + reverse('register')
                content = render_to_string('emails/shared_events.html', {
                    'event_name': event.title,
                    'button_link': url
                })

                create_mail({
                    'content': content
                }, 'Er is via Yourtickets een event met je gedeeld!', data['user_email'],
                banner=cshop.header_img.url)

        if form.is_valid():
            data = {'success': True}
        else:
            data = {'errors': json.loads(form.errors.as_json())}
    else:
        data = {'success': False}

    return JsonResponse(data)


@is_event_from_user(login_url='login')
def delete(request, event_id, id, type):

    if type == 'temp':
        TempSharedEvents.objects.get(pk=id).delete()
    else:
        SharedEvents.objects.get(pk=id).delete()


    return redirect(reverse('dashboard_event:share_event:index', kwargs={'event_id': event_id}))