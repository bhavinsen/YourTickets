from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from rest_framework import routers
from ticketshop import views
from yourtickets import views as yourticketsviews
from django.conf.urls.static import static

from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.views.static import serve
from django.conf import settings
from django.views.generic import RedirectView
from django.views.generic.base import TemplateView
from django.contrib.sitemaps.views import sitemap


from ticketshop.views import mollie_webhook
from yourtickets.viewss import index


handler404 = 'yourtickets.views.handler404'
handler500 = 'yourtickets.views.handler500'



# @login_required
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
patterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^advanced_filters/', include('advanced_filters.urls')),
    url(r'^static/tickets/gen/(?P<ticket_id>.+)', yourticketsviews.login_func, name='get_ticket_login'),
    url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], protected_serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^ticketshop/', include('ticketshop.urls')),
    url(r'^profiel/$', yourticketsviews.profiel, name='profiel'),
    # url(r'^mol/verify$', mollie_webhook, name='mollie_webhook'),
    url(r'^contact/$', yourticketsviews.contact, name='contact'),
    url(r'^$', index.index, name='index'),
    url(r'^login/$', yourticketsviews.login_req, name='login'),
    url(r'^login_func/$', yourticketsviews.login_func, name='login_func'),
    url(r'^logout/$', yourticketsviews.logout_req, name='logout'),
    url(r'^register/$', yourticketsviews.register_req, name='register'),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^youradmin/', include('youradmin.urls')),

    url(r'^pre-reg/rauw_alejandro$', index.pre_reg, name='pre_reg'),
    url(r'^pre-reg/succes_page$', index.pre_reg_succes, name='pre_reg_succes'),

    url('^usercheck/(?P<user>.+)/$', yourticketsviews.usernameExists, name='usercheck'),

    url(r'^iframe/(?P<event_id>[-\w\.]+)', yourticketsviews.iframe, name='iframe'),
    url(r'^iframe_redirect', yourticketsviews.iframe_redirect, name='iframe_redirect'),
    url(r'^account/activate/(?P<token>[-\w\.]+)', yourticketsviews.account_activate, name='account_activate'),


    url(r'^account/reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', yourticketsviews.PasswordResetConfirmView.as_view(),name='reset_password_confirm'),
    url(r'^account/reset_password', yourticketsviews.ResetPasswordRequestView.as_view(), name="reset_password"),

    url(r'^error/(?P<error_id>.+)/', yourticketsviews.error_page, name="error_page"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls import include, url



urlpatterns = i18n_patterns(*patterns) + patterns

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'events', views.EventViewSet, 'Events')

urlpatterns += [
    url(r'^admin$', RedirectView.as_view(url = '/admin/')),
    url(r'^login$', RedirectView.as_view(url = '/login/')),
    url(r'^logout$', RedirectView.as_view(url = '/logout/')),
    url(r'^register$', RedirectView.as_view(url = '/register/')),
    url(r'^dashboard$', RedirectView.as_view(url = '/dashboard/')),
    url(r'^youradmin$', RedirectView.as_view(url = '/youradmin/')),
    url(r'^contact$', RedirectView.as_view(url = '/contact/')),

    url(r'^mol/verify$', mollie_webhook, name='mollie_webhook'),

    url(r'^robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('^tickets/(?P<event>.+)/$', views.TicketList.as_view({'get': 'list'})),
	url('^ticketcheck/(?P<gen_id>.+)/$', views.TicketCheck.as_view({'get': 'list'})),
	url('^ticketcheckget/(?P<gen_id>.+)/$', views.TicketCheckGet.as_view({'get': 'list'})),
    url(r'^ticketkwijt/download/(?P<description>.+)/all/$', yourticketsviews.download_all, name='lost_download_all'),
    url(r'^ticketkwijt/download/(?P<description>.+)/(?P<ticket_id>.+)/$', yourticketsviews.download_ticket, name='lost_download_ticket'),
    url(r'^ticketkwijt$', yourticketsviews.lost_tickets, name='lost'),

    url(r'^dashboard2/api/', include('yt_dashboard.urls_api')),
    url(r'^dashboard2/', include('yt_dashboard.urls')),
    # url(r'^dashboard2', include('yt_dashboard.urls')),
    url(r'^t$', yourticketsviews.track, name='track_url'),

    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^$', index.index, name='index'),
    url(r'^', include(router.urls)),



    # event specifics
    url(r'^(?P<event_name>[-\w\.]+)$', yourticketsviews.custom_event_url, name='event_url'),




]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
