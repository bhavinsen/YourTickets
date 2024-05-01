from functools import wraps
from urllib import parse
from urllib.parse import urlparse

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import resolve_url

from ticketshop.models import UserExtra, EventOrganiser, SharedEvents
from yourtickets import settings


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)):
                return True
        return False

    return user_passes_test(in_groups, login_url='login')


def is_organizer(login_url=None, raise_exception=False):
    def check_perms(user, **kwargs):
        if not user.is_authenticated:
            return False
        user_extra = UserExtra.objects.get(user=user)

        if user.is_superuser:
            return True

        return user_extra.is_organizer

    return user_passes_test(check_perms, login_url=login_url)


def is_visitor(login_url=None, raise_exception=False):
    def check_perms(user):
        if not user.is_authenticated:
            return False
        user_extra = UserExtra.objects.get(user=user)
        return user_extra.is_visitor
    return user_passes_test(check_perms, login_url=login_url)


def is_event_from_user(login_url=None, shared_events=False, raise_exception=False):

    def check_perms(user, **kwargs):
        if not user.is_authenticated:
            return False
        if shared_events:
            if EventOrganiser.objects.filter(user=user, event=kwargs.get('event_id')).exists() or SharedEvents.objects.filter(user=user, event=kwargs.get('event_id')).exists():
                return True

            return False
        else:
            return EventOrganiser.objects.filter(user=user, event=kwargs.get('event_id')).exists()

    return user_passes_test2(check_perms, login_url=login_url)


def user_passes_test2(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user, **kwargs):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator
