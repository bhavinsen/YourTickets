from django.contrib import admin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from .models import (accessRequests, Event, UserExtra,
                     LineUp, UserExtraSeller, Ticket, SoldTicket,
                     EventOrganiser, TicketShopCustom, Dictionary,
                     Languages, Order, Log, GuestTickets, Orderlog, PreReg)

from advanced_filters.admin import AdminAdvancedFiltersMixin, AdvancedListFilters
from advanced_filters.models import AdvancedFilter
from ticketshop.adm.filters.orderlogs import OrderLogFilter

admin.site.register(UserExtra)
admin.site.register(UserExtraSeller)
admin.site.register(LineUp)
# admin.site.register(Ticket)

admin.site.register(EventOrganiser)
admin.site.register(TicketShopCustom)
admin.site.register(Dictionary)
admin.site.register(Languages)

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_public', 'start_date', 'end_date', 'removed')
    list_filter = ('removed', 'event_public',)

admin.site.register(Event, EventAdmin)

class LogAdmin(admin.ModelAdmin):
    list_display = ('date', 'category', 'message')

admin.site.register(Log, LogAdmin)


from django.forms import ModelForm, Form
from django.forms import DateField, CharField, ChoiceField, TextInput

class AdvancedListFiltersC(AdvancedListFilters):
    
    title = _('Advanced filters')

    parameter_name = '_afilter'

    def lookups(self, request, model_admin):
        if not model_admin:
            raise Exception('Cannot use AdvancedListFilters without a '
                            'model_admin')
        model_name = "%s.%s" % (model_admin.model._meta.app_label,
                                model_admin.model._meta.object_name)
        return AdvancedFilter.objects.filter(
            model=model_name).values_list('id', 'title')

class AdminAdvancedFiltersMixinC(AdminAdvancedFiltersMixin):
    
    original_filters = ()

    def __init__(self, *args, **kwargs):
        self.original_filters = self.list_filter

        super(AdminAdvancedFiltersMixinC, self).__init__(*args, **kwargs)
        self.list_filter = (AdvancedListFiltersC,) + tuple(self.original_filters)
    
    # def save_advanced_filter(self, request, form):
        # super(AdminAdvancedFiltersMixinC, self).save_advanced_filter(request, form)

class OrderLogAdmin(AdminAdvancedFiltersMixinC, admin.ModelAdmin):
    list_display = ('date', 'mollie_id', 'order_id', 'type')
    search_fields = ['=mollie_id', '=order_id']
    list_filter = (OrderLogFilter,)
    advanced_filter_fields = (
        'date', 'mollie_id', 'order_id', 'type'
    )

admin.site.register(Orderlog, OrderLogAdmin)

# Tickets
class SoldTicketInline(admin.TabularInline):
    model = SoldTicket
    max_num = 10

class TicketAdmin(admin.ModelAdmin):
    inlines = [SoldTicketInline]
    list_filter = ('event', )

    list_display = ('name', 'event')

    def event(self, x):
        return x.event.title

admin.site.register(Ticket, TicketAdmin)
# end tickets

# sold tickets
class SoldTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'sold_date', 'price', 'ticket_name', 'ticket_type', 'orderid')
    list_filter = ('event', )
    list_editable = ('price',)
    raw_id_fields = ('order_nr', 'event', 'ticket_type', 'primary_ticket', 'guest_ticket', 'user', )

    def ticket_name(self, x):

        if x.ticket_type:
            return x.ticket_type.name
        else:
            return ""

    def orderid(self, obj):
        return obj.order_nr

admin.site.register(SoldTicket, SoldTicketAdmin)

class GuestTicketsAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'name', 'email', 'type')
    list_filter = ('delayed_send',)

    def event(self, x):
        return x.event.title

admin.site.register(GuestTickets, GuestTicketsAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'order_paid', 'mollie_id', 'user_link', 'user_name']


    def user_link(self, obj):
        return '<a href="{user_url}">{username}</a>'.format(user_url=reverse('admin:auth_user_change', args=(obj.user.id,)), username=obj.user)

    user_link.allow_tags = True
    user_link.short_description = 'User'
    def user_name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

admin.site.register(Order, OrderAdmin)
admin.site.register(accessRequests)


class PreRegdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'country', 'notify_me']

admin.site.register(PreReg, PreRegdmin)