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
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from functools import reduce

from ticketshop.models import (
    Languages, Dictionary
)
from youradmin.views.forms import translations
from youradmin.common.datatable import build_order_args, build_search_args

def get_cols():
    return [
        # {"title": "id", "data": "id"},
        {"title": "key", "data": "fields.name"},
        {"title": "value", "data": "fields.text"},
        {"title": 'actions', "data": None, "types": {
            "delete": {
                "url": reverse("youradmin_translations_delete", kwargs={"translation_id": "_placeholder"}),
                "modal_id": "translation_delete",
                "action_id_property": "pk"
            },
            "edit": {
                "url": reverse("youradmin_translations_edit", kwargs={"translation_id": "_placeholder"}),
                "modal_id": "translation_edit",
                "action_id_property": "pk"
            }

        }}
    ]


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


@staff_member_required(login_url='/youradmin/login/')
def index(request):

    languages = Languages.objects.filter()

    with connection.cursor() as cursor:
        cursor.execute("""
        select
        distinct
        ou.name
        from ticketshop_dictionary ou
        where(
            select
        count(*)
        from ticketshop_dictionary inr
        where
        inr.name = ou.name
        AND
        inr.language_id = ou.language_id) > 1

    """)
        double_rows = dictfetchall(cursor)

    # left_language = languages[0]
    # right_language = languages[1]

    # left_translations = Dictionary.objects.filter(language=left_language)
    # right_translations = Dictionary.objects.filter(language=right_language)



    if request.POST:
        pass

    return render(request, 'youradmin/translations/index.html', {
        'double_rows': double_rows,
        'languages': Languages.objects.filter(),
        'translation_form': translations.TranslationForm(),
        'translations_form': translations.TranslationsForm(),
        'datatables_config': json.dumps({
            'pageLength': request.GET.get('pageLength', 1000),
            'columns': get_cols(),
            "order": [[ 0, "asc" ]],
            'ajax': {
                'url': reverse('youradmin_translations_getlist', kwargs={'language_id': languages.first().pk})
            }

        })
        # 'left_language': left_language,
        # 'right_language': right_language,
        # 'left_translations': left_translations,
        # 'right_translations': right_translations
    })

@staff_member_required(login_url='/youradmin/login/')
def getlist(request, language_id):
    source = request.POST

    page_length = int(source.get('length', 1000))
    data_start = int(source.get('start', 0))

    order_args = build_order_args(request.POST, get_cols())

    search_args = build_search_args(request.POST, get_cols())

    if len(order_args) == 0:
        order_args.append('name')

    # kwargs = dict()
    # Languages.objects.filter()
    # kwargs["language_id__exact"] = language_id
    # search_args.append(Q(**kwargs))

    if len(search_args) > 0:
        records = Dictionary.objects.filter(reduce(operator.or_, search_args) & Q(language_id__exact=language_id)).order_by(*order_args)[data_start:data_start+page_length]
        total = Dictionary.objects.filter(reduce(operator.or_, search_args)).count()
    else:
        records = Dictionary.objects.filter(Q(language_id__exact=language_id)).order_by(*order_args)[data_start:data_start+page_length]
        total = Dictionary.objects.filter(Q(language_id__exact=language_id)).count()

    records = serializers.serialize("json", records)
    records = json.loads(records)

    # print(records)

    return JsonResponse({
        "recordsTotal": total,
        "recordsFiltered": total,
        "data": records
    })

def create_translations(request, language_id):
    language = Languages.objects.get(pk=language_id)

    form = translations.TranslationForm(request.POST)

    if Dictionary.objects.filter(name=request.POST.get('name'), language=language).exists():
        return JsonResponse({'error': "Key name allready exists"})

    if form.is_valid():

        translation = Dictionary(name=form.cleaned_data['name'], text=form.cleaned_data['text'], language=language)
        translation.save()

        data = {'success': True}
    else:
        data = {'errors': json.loads(form.errors.as_json())}

    return JsonResponse(data)

@staff_member_required(login_url='/youradmin/login/')
def translation_edit(request, translation_id):

    translation = Dictionary.objects.get(pk=translation_id)

    if Dictionary.objects.filter(~Q(id=translation_id), name=request.POST.get('name'), language=translation.language).exists():
        return JsonResponse({'error': "Key name allready exists"})

    form = translations.TranslationForm(instance=Dictionary.objects.get(pk=translation_id))

    if request.POST:
        form = translations.TranslationForm(instance=Dictionary.objects.get(pk=translation_id), data=request.POST)
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

@staff_member_required(login_url='/youradmin/login/')
@csrf_exempt
def translation_helper_edit(request):

    data = json.loads(request.POST.get('data'))

    for translation in data:
        id = translation['id']
        if not id or id == "0":
            if Dictionary.objects.filter(language=Languages.objects.get(pk=translation['languageid']), name=translation['translation_key']).exists():
                return JsonResponse({'success': False})
            record = Dictionary(
                text=translation['value'],
                language=Languages.objects.get(pk=translation['languageid']),
                name=translation['translation_key']
            )
        else:
            value = translation['value']
            record = Dictionary.objects.get(pk=id)
            record.text = value
        record.save()

    return JsonResponse({'success': True})
    # translation = Dictionary.objects.get(pk=translation_id)
    #
    # if Dictionary.objects.filter(~Q(id=translation_id), name=request.POST.get('name'), language=translation.language).exists():
    #     return JsonResponse({'error': "Key name allready exists"})
    #
    # form = translations.TranslationForm(instance=Dictionary.objects.get(pk=translation_id))
    #
    # if request.POST:
    #     form = translations.TranslationForm(instance=Dictionary.objects.get(pk=translation_id), data=request.POST)
    #     if form.is_valid():
    #         form.save()
    #         data = {'success': True}
    #     else:
    #         data = {'errors': json.loads(form.errors.as_json())}
    # else:
    #     return render(request, 'youradmin/partials/formdecorator_renderer.html', {
    #         "form": form
    #     })
    # return JsonResponse(data)

@staff_member_required(login_url='/youradmin/login/')
def translation_delete(request, translation_id):
    Dictionary.objects.get(pk=translation_id).delete()
    return JsonResponse({'success': True})


def get_cols_languages():
    return [
        {"title": "language_code", "data": "fields.language_code"},
        {"title": "language_name", "data": "fields.language_name"},
        {"title": 'actions', "data": None, "types": {
            "delete": {
                "url": reverse("youradmin_translations_languages_delete", kwargs={"language_id": "_placeholder"}),
                "modal_id": "language_delete",
                "action_id_property": "pk"
            },
            "edit": {
                "url": reverse("youradmin_translations_languages_edit", kwargs={"language_id": "_placeholder"}),
                "modal_id": "language_edit",
                "action_id_property": "pk"
            }

        }}
    ]

@staff_member_required(login_url='/youradmin/login/')
def language_index(request):

    languages = Languages.objects.filter()

    return render(request, 'youradmin/translations/languages.html', {
        # 'languages': Languages.objects.filter(),
        'language_form': translations.LanguageForm(languages=languages),
        'language_form_url': reverse('youradmin_translations_languages_create'),
        'datatables_config': json.dumps({
            'pageLength': request.GET.get('pageLength', 1000),
            'columns': get_cols_languages(),
            "order": [[ 0, "asc" ]],
            'ajax': {
                'url': reverse('youradmin_translations_languages_getlist', kwargs={})
            }

        })
        # 'left_language': left_language,
        # 'right_language': right_language,
        # 'left_translations': left_translations,
        # 'right_translations': right_translations
    })

@staff_member_required(login_url='/youradmin/login/')
def language_getlist(request):
    source = request.POST

    page_length = int(source.get('length', 1000))
    data_start = int(source.get('start', 0))

    order_args = build_order_args(request.POST, get_cols_languages())

    search_args = build_search_args(request.POST, get_cols_languages())

    if len(order_args) == 0:
        order_args.append('language_code')

    if len(search_args) > 0:
        records = Languages.objects.filter(reduce(operator.or_, search_args)).order_by(*order_args)[data_start:data_start+page_length]
        total = Languages.objects.filter(reduce(operator.or_, search_args)).count()
    else:
        records = Languages.objects.all().order_by(*order_args)[data_start:data_start+page_length]
        total = Languages.objects.all().count()

    records = serializers.serialize("json", records)
    records = json.loads(records)

    # print(records)

    return JsonResponse({
        "recordsTotal": total,
        "recordsFiltered": total,
        "data": records
    })

@staff_member_required(login_url='/youradmin/login/')
def language_edit(request, language_id):

    form = translations.LanguageForm(instance=Languages.objects.get(pk=language_id))

    if request.POST:
        form = translations.LanguageForm(instance=Languages.objects.get(pk=language_id), data=request.POST)
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


@staff_member_required(login_url='/youradmin/login/')
def language_delete(request, language_id):
    Languages.objects.get(pk=language_id).delete()
    return JsonResponse({'success': True})


@staff_member_required(login_url='/youradmin/login/')
def language_create(request):
    if request.POST:
        form = translations.LanguageForm(request.POST)
        based_on = request.POST.get('based_values')
        based_on_language = Languages.objects.filter(pk=based_on).first()

        # model.objects.bulk_create([])

        if form.is_valid():
            new_language = form.save()

            based_on_text_translations = Dictionary.objects.filter(language=based_on_language)

            for trans in based_on_text_translations:
                dic = Dictionary(name=trans.name, text="", language=new_language)
                dic.save()

            data = {'success': True}
        else:
            data = {'errors': json.loads(form.errors.as_json())}

        return JsonResponse(data)


def language_create_all(request):

    if Dictionary.objects.filter(name=request.POST.get('name')).exists():
        return JsonResponse({'error': "Key name allready exists"})

    if request.POST:
        languages = Languages.objects.all()
        form = translations.TranslationsForm(request.POST)

        if form.is_valid():

            data = form.cleaned_data

            for language in languages:
                dictionary = Dictionary(language=language, name=data['name'], text=data[language.language_code+'_text'])
                dictionary.save()
            data = {'success': True}
        else:
            data = {'errors': json.loads(form.errors.as_json())}

        return JsonResponse(data)
