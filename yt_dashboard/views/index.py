from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token, get_token, ensure_csrf_cookie
from django.http import JsonResponse


@requires_csrf_token
def index(request):
    return render(request, 'yt_dashboard/index.html', {})


@requires_csrf_token
@ensure_csrf_cookie
def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'token': token})
