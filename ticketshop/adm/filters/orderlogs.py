from django.contrib.admin import SimpleListFilter
from ticketshop.models import(
    Orderlog
)

class OrderLogFilter(SimpleListFilter):
    title = 'preset filters' # or use _('country') for translated title
    parameter_name = 'status'

    model = None

    def __init__(self, request, params, model, model_admin):
        super(OrderLogFilter, self).__init__(request, params, model, model_admin)
        self.model = model

    def lookups(self, request, model_admin):
        # countries = set([c.country for c in model_admin.model.objects.all()])
        # return [(c.id, c.name) for c in countries] + [
        #   ('AFRICA', 'AFRICA - ALL')]

        return (
            ('BEFORE_MOLLIE_AANVRAAG', 'ERRORS ONLY'),
            ('SMART_CHECK', 'SMART CHECK')
        )

    def queryset(self, request, queryset):
        # if self.value() == 'AFRICA':
        #     return queryset.filter(country__continent='Africa')
        if self.value():
            print(self.value())
            if self.value() == 'SMART_CHECK':

                return queryset
                
            else:

                return queryset.filter(type__in=[
                        Orderlog.TYPE_WEBHOOK_MOLLIE_API_ERROR,
                        Orderlog.TYPE_WEBHOOK_MOLLIE_EXCEPTION,
                        Orderlog.TYPE_MAIL_PDF_ERROR
                    ])
        else:
            return queryset