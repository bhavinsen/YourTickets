from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.urls import reverse
from django.db.models import F
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

from dashboard.common.base_vars import base_vars
from ticketshop.models import EventOrganiser, Multiticketshop, DynamicUrl, MultiticketshopEvents, Event


@login_required(login_url='login')
def index(request):

    multishops = Multiticketshop.objects.filter(user=request.user).values('id', 'name')

    for shop in multishops:
        dynamic_url = DynamicUrl.objects.filter(
            type=DynamicUrl.MULTITICKETSHOP,
            multiticketshop=shop['id'],
            enabled=True
        ).first()
        shop['url'] = False
        if dynamic_url:
            shop['url'] = dynamic_url.url_name

        shop['total_events'] = MultiticketshopEvents.objects.filter(multiticketshop=shop['id']).count()


    return render(request, 'dash/multi_ticketshop.html', base_vars(request, 0, {
        'multishops': multishops

    }))


@login_required(login_url='login')
def create_ticketshop(request):

    name = request.POST.get('name', '')

    if name == '':
        return JsonResponse({'success': False})

    shop = Multiticketshop.objects.create(name=name, user=request.user)

    return JsonResponse({
        'success': True, 'url': reverse('dashboard_multiticketshop_edit', kwargs={'multishop_id':shop.pk})
    })


@login_required(login_url='login')
def update_ticketshop(request, multishop_id):
    multishop = Multiticketshop.objects.filter(user=request.user, pk=multishop_id).first()

    if not multishop:
        return JsonResponse({'success': False})

    use_in_iframe = False
    if request.POST.get('use_in_iframe') == 'true':
        use_in_iframe = True
    multishop.use_in_iframe = use_in_iframe
    multishop.save()

    item_list = request.POST.getlist('items[]')

    MultiticketshopEvents.objects.filter(multiticketshop=multishop).delete()

    for index, event_id in enumerate(item_list):
        if not event_from_user(int(event_id), request.user):
            # print('event not from user')
            return JsonResponse({'success': False})

        event = Event.objects.get(pk=int(event_id))

        MultiticketshopEvents(event=event, order=index+1, multiticketshop=multishop).save()

    return JsonResponse({'success': True, 'redirect_to': reverse('dashboard_multiticketshop')})


@login_required(login_url='login')
def edit_ticketshop(request, multishop_id):

    multishop = Multiticketshop.objects.filter(user=request.user, pk=multishop_id).first()



    if not multishop:
        return HttpResponseRedirect(reverse('login'))

    # get all the events
    # events = EventOrganiser.objects.filter(user=request.user, event__removed=False).values('event__title', 'pk')

    # get multishop events
    # multishop_events = MultiticketshopEvents.objects.filter(multiticketshop=multishop).values('event__title')
    # list_events = {multishop_event: True for multishop_event in multishop_events}
    #
    #
    # print(events)
    #
    # for event in events:
    #     pass

    return render(request, 'dash/multi_ticketshop_edit.html', base_vars(request, 0, {
        'multishop': multishop,
        # 'events': events
    }))

def events_list(request, multishop_id, list_type):
    multishop = Multiticketshop.objects.filter(user=request.user, pk=multishop_id).first()

    if not multishop:
        return HttpResponseRedirect(reverse('login'))

    if list_type == 'destination':
        multishop_events = MultiticketshopEvents.objects.filter(multiticketshop=multishop) \
            .order_by('order') \
            .values('event__title', 'event__pk')

        return JsonResponse({"success": True, "data": list(multishop_events)})
    elif list_type == 'source':
        multishop_events = MultiticketshopEvents.objects.filter(multiticketshop=multishop)
        events = EventOrganiser.objects.filter(user=request.user, event__removed=False)\
            .exclude(event__id__in=multishop_events.values_list('event__pk', flat=True)) \
            .values('event__title', 'pk', 'event__pk')

        return JsonResponse({"success": True, "data": list(events)})


def event_position(request, multishop_id, position, linked_event_id):
    if not multishop_is_from_user(multishop_id, request.user):
        return JsonResponse({'success': False})

    multishop = Multiticketshop.objects.filter(user=request.user, pk=multishop_id).first()

    linked_event = MultiticketshopEvents.objects.get(pk=linked_event_id)

    # linked_event.order = position
    # linked_event.save()


    # events = MultiticketshopEvents.objects.filter(multiticketshop=multishop).order_by('order')

    if int(position) > int(linked_event.order):
        events = MultiticketshopEvents.objects.filter(
            multiticketshop=multishop,
            order__lte=position,
            order__gt=linked_event.order
        ).order_by('order')
        events.update(order=F('order') - 1)

    else:
        events = MultiticketshopEvents.objects.filter(
            multiticketshop=multishop,
            order__gte=position,
            order__lt=linked_event.order
        ).order_by('-order')
        events.update(order=F('order') + 1)

    linked_event.order = position
    linked_event.save()

    return JsonResponse({'success': True})


def add_event(request, multishop_id, event_id, position):

    if not multishop_is_from_user(multishop_id, request.user):
        return JsonResponse({'success': False})

    # later on if we want to have different events linked from other organisations we need to remove this
    if not event_from_user(event_id, request.user):
        return JsonResponse({'success': False})

    multishop = Multiticketshop.objects.filter(user=request.user, pk=multishop_id).first()
    # multishop_events = MultiticketshopEvents.objects.filter(multiticketshop=multishop)
    events_with_equal_or_bigger_pos = MultiticketshopEvents.objects.filter(multiticketshop=multishop, order__gte=position).order_by('order')

    for event in events_with_equal_or_bigger_pos:
        event.order = event.order+1
        event.save()

    event = Event.objects.get(pk=event_id)
    MultiticketshopEvents(event=event, order=position, multiticketshop=multishop).save()

    return JsonResponse({'success':True})


def delete_event(request, multishop_id, linked_event_id):
    if not multishop_is_from_user(multishop_id, request.user):
        return JsonResponse({'success': False})

    multishop = Multiticketshop.objects.filter(user=request.user, pk=multishop_id).first()
    multishop_event = MultiticketshopEvents.objects.get(multiticketshop=multishop, pk=linked_event_id)
    multishop_event.delete()

    # multishop_event = MultiticketshopEvents.objects.get(multiticketshop=multishop, pk=linked_event_id)

    events_with_equal_or_bigger_pos = MultiticketshopEvents.objects.filter(multiticketshop=multishop).order_by('order')
    i=1
    for event in events_with_equal_or_bigger_pos:
        event.order = i
        event.save()
        i += 1

    return JsonResponse({'success': True})


def delete_ticketshop(request, multishop_id):
    if not multishop_is_from_user(multishop_id, request.user):
        return HttpResponseRedirect(reverse('login'))

    shop = Multiticketshop.objects.get(pk=multishop_id)

    shop.delete()

    return HttpResponseRedirect(reverse('dashboard_multiticketshop'))


def multishop_is_from_user(multiticketshop_id, user):
    multishop = Multiticketshop.objects.filter(user=user, pk=multiticketshop_id).first()

    if multishop:
        return True

    return False

def request_short_url(request, multishop_id):

    if not multishop_is_from_user(multishop_id, request.user):
        return HttpResponseRedirect(reverse('login'))

    multishop = Multiticketshop.objects.filter(pk=multishop_id).first()

    email_message = 'Requested for multishop ' + multishop.name + '( id:' + multishop_id + ') \n'
    email_message += 'The url they wanted is "'+ request.POST.get('url_name') + '" \n'
    email_message += 'https://yourtickets.nl/youradmin'

    msg = EmailMessage('Short url requested for multiticketshop', email_message,
                       'noreply@yourtickets.nl', ['info@yourtickets.nl', 'almerelc@gmail.com'])
    msg.send()

    return JsonResponse({'success': True})


def event_from_user(event_id, user):

    event = Event.objects.get(pk=event_id)

    user_event = EventOrganiser.objects.filter(user=user, event=event).first()

    if user_event:
        return True

    return False

