import json

from django.http import JsonResponse
from django.conf import settings
from ticketshop.models import Event, Multiticketshop, DynamicUrl, MultiticketshopEvents, EventOrganiser
from django.core.mail import EmailMessage


from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, api_view, permission_classes


def getUser(request):
    return request.user
    # return get_user_model().objects.filter(pk=271).first()


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getall(request):
    user = getUser(request)

    multishops = list(Multiticketshop.objects.filter(user=user).order_by('id').values('id', 'name'))

    for shop in multishops:
        dynamic_url = DynamicUrl.objects.filter(
            type=DynamicUrl.MULTITICKETSHOP,
            multiticketshop=shop['id'],
            enabled=True
        ).first()
        shop['url'] = False
        if dynamic_url:
            shop['url'] = dynamic_url.url_name
            shop['full_url'] = settings.HOSTNAME + '/' + dynamic_url.url_name

        events = list(MultiticketshopEvents.objects.filter(multiticketshop=shop['id']).values('event__title'))
        shop['events'] = events

        shop['total_events'] = MultiticketshopEvents.objects.filter(multiticketshop=shop['id']).count()

    return JsonResponse({'multishops': multishops})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create(request):

    user = getUser(request)

    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)

    name = data.get('name', '')

    if name == '':
        return JsonResponse({'success': False})

    multishop = Multiticketshop.objects.create(name=name, user=user)

    item_list = data.get('events', [])

    MultiticketshopEvents.objects.filter(multiticketshop=multishop).delete()

    for index, event in enumerate(item_list):
        if not event_from_user(int(event['pk']), user):
            return JsonResponse({'success': False})

        event = Event.objects.get(pk=int(event['pk']))
        MultiticketshopEvents(event=event, order=index + 1, multiticketshop=multishop).save()

    return JsonResponse({'success': True})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_events_for_shop(request, multiticketshop_id):

    user = getUser(request)
    shop = Multiticketshop.objects.filter(user=user, pk=multiticketshop_id).first()

    if not shop:
        return JsonResponse({'success': False})

    events = list(MultiticketshopEvents.objects.filter(multiticketshop=shop).order_by('order').values('event__title', 'event__pk'))
    # final_list = []
    for e in events:
        e['title'] = e['event__title']
        del e['event__title']
        e['id'] = e['event__pk']
        del e['event__pk']
        # final_list.append(e['id'])

    return JsonResponse({'events': events})


def event_from_user(event_id, user):

    event = Event.objects.get(pk=event_id)

    user_event = EventOrganiser.objects.filter(user=user, event=event).first()

    if user_event:
        return True

    return False


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_events_from_user(request):
    user = getUser(request)

    events = list(Event.objects.filter(eventorganiser__user__pk=user.pk, removed=False).values('id', 'title'))

    return JsonResponse({'events': events})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update(request, multiticketshop_id):

    user = getUser(request)

    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)

    multishop = Multiticketshop.objects.filter(user=user, pk=multiticketshop_id).first()

    if not multishop:
        return JsonResponse({'success': False})

    multishop.name = data.get('name')
    multishop.save()

    item_list = data.get('events', [])

    MultiticketshopEvents.objects.filter(multiticketshop=multishop).delete()

    for index, event in enumerate(item_list):
        if not event_from_user(int(event['pk']), user):
            # print('event not from user')
            return JsonResponse({'success': False})

        event = Event.objects.get(pk=int(event['pk']))

        MultiticketshopEvents(event=event, order=index + 1, multiticketshop=multishop).save()

    return JsonResponse({'success': True})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete(request, multiticketshop_id):
    user = getUser(request)
    if not multishop_is_from_user(multiticketshop_id, user):
        return JsonResponse({'success': False})

    shop = Multiticketshop.objects.get(pk=multiticketshop_id)

    shop.delete()

    return JsonResponse({'success': True})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def request_short_url(request, multiticketshop_id):
    user = getUser(request)

    if not multishop_is_from_user(multiticketshop_id, user):
        return JsonResponse({'success': False})

    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)

    multishop = Multiticketshop.objects.filter(pk=multiticketshop_id).first()

    email_message = 'Requested for multishop ' + multishop.name + '( id:' + str(multiticketshop_id) + ') \n'
    email_message += 'The url they wanted is "'+ data.get('url_name') + '" \n'
    email_message += 'https://yourtickets.nl/youradmin'

    msg = EmailMessage('Short url requested for multiticketshop', email_message,
                       'noreply@yourtickets.nl', ['info@yourtickets.nl', 'almerelc@gmail.com'])
    msg.send()

    return JsonResponse({'success': True})


def multishop_is_from_user(multiticketshop_id, user):
    multishop = Multiticketshop.objects.filter(user=user, pk=multiticketshop_id).first()

    if multishop:
        return True

    return False