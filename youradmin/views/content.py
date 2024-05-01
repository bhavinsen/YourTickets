import json
import operator
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import (
    render
)
from django.db.models import Q
from django.urls import reverse
from django.http import JsonResponse
from django.core import serializers

from ticketshop.models import (
    DynamicUrl
)
from youradmin.views.forms.content import EventUrlForm

def get_cols():
    return [
        # {"title": "id", "data": "id"},
        {"title": "event", "data": "fields.event"},
        {"title": "url name", "data": "fields.url_name"},
        {"title": "enabled", "data": "fields.enabled",
         "render": "truefalse_field_renderer"},
        {"title": 'actions', "data": None, "types": {
            "delete": {
                "url": reverse("youradmin_content_eventurls_delete", kwargs={"dynamicurl_id": "_placeholder"}),
                "modal_id": "event_url_delete",
                "action_id_property": "pk"
            },
            "edit": {
                "url": reverse("youradmin_content_eventurls_edit", kwargs={"dynamicurl_id": "_placeholder"}),
                "modal_id": "event_url_edit",
                "action_id_property": "pk"
            }

        }}
    ]

@staff_member_required(login_url='/youradmin/login/')
def event_urls_index(request):

    return render(request, 'youradmin/content/event_urls.html', {
        'event_url_form': EventUrlForm(),
        # 'translations_form': translations.TranslationsForm(),
        'datatables_config': json.dumps({
            'columns': get_cols(),
            'ajax': {
                'url': reverse('youradmin_content_eventurls_getlist')
            }

        })
    })


@staff_member_required(login_url='/youradmin/login/')
def event_urls_getlist(request):
    source = request.POST

    page_length = int(source.get('length', 100))
    data_start = int(source.get('start', 0))

    records = DynamicUrl.objects.filter()[data_start:data_start+page_length]
    total = DynamicUrl.objects.filter().count()

    records = serializers.serialize("json", records)
    records = json.loads(records)

    # print(records)

    return JsonResponse({
        "recordsTotal": total,
        "recordsFiltered": total,
        "data": records
    })


@staff_member_required(login_url='/youradmin/login/')
def event_url_create(request):
    # language = DynamicUrl.objects.get(pk=language_id)

    post = request.POST.copy()

    if request.POST.get('multiticketshop'):
        post['type'] = DynamicUrl.MULTITICKETSHOP
    else:
        post['type'] = DynamicUrl.EVENT

    form = EventUrlForm(post)

    if form.is_valid():

        # translation = Dictionary(name=form.cleaned_data['name'], text=form.cleaned_data['text'], language=language)

        form.save()

        data = {'success': True}
    else:
        data = {'errors': json.loads(form.errors.as_json())}

    return JsonResponse(data)


@staff_member_required(login_url='/youradmin/login/')
def event_url_delete(request, dynamicurl_id):
    DynamicUrl.objects.get(pk=dynamicurl_id).delete()
    return JsonResponse({'success': True})


@staff_member_required(login_url='/youradmin/login/')
def event_url_edit(request, dynamicurl_id):
    form = EventUrlForm(instance=DynamicUrl.objects.get(pk=dynamicurl_id))

    if request.POST:
        form = EventUrlForm(instance=DynamicUrl.objects.get(pk=dynamicurl_id), data=request.POST)
        if form.is_valid():
            form.save()
            data = {'success': True}
        else:
            data = {'errors': json.loads(form.errors.as_json())}
    else:
        return render(request, 'youradmin/partials/formdecorator_renderer.html', {
            "form": form
        })
    return JsonResponse(data)