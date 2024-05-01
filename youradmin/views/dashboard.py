import datetime
from django.http.response import JsonResponse
from ticketshop.models import SoldTicket

def soldtickets(request):

    now = datetime.datetime.now()

    total = SoldTicket.objects.filter(
        sold_date__year=now.year,
        sold_date__month=now.month,
        sold_date__day=now.day,
        guest_ticket__isnull=True
    ).count()

    return JsonResponse({'success': True, 'total': total})
