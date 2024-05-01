from django import template
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.safestring import mark_safe

from ticketshop.models import Dictionary, Languages
register = template.Library()


@register.filter
def index(l, i):
    return l[int(i)]


@register.filter
def indexMin(l, i):
    return l[int(i-1)]


@register.simple_tag(takes_context=True, name='getWord')
# @register.simple_tag
def getWord(context, lc, nm, defaultText=''):

    request_object = None
    if 'request' in context:
        request_object = context['request']



    debug = False
    if 'user' not in request_object:
        request_object.user = None 
        
    if request_object and request_object.user:
        is_super_user = request_object.user.is_superuser
        showdebug = request_object.GET.get('showerrors', False)

        # import pdb;pdb.set_trace()
        if is_super_user and showdebug is not False:
            print('-------- jaaaa')
            debug = True

    lcd = "NL"
    try:
        lcd = Languages.objects.get(language_code=lcd)
        lc = Languages.objects.get(language_code=lc)
    except:
        return 'language not found'
    dicti = Dictionary.objects.filter(language=lc, name=nm).count()

    if debug:
        if dicti > 0:
            dicti = Dictionary.objects.get(language=lc, name=nm)
            helper_text = dicti.text
        else:
            helper_text = defaultText or "Text not found"

        return render_to_string('youradmin/partials/translation_helper.html',
                                translation_helper_context(translation_name=nm, current_text=helper_text)
                                )

    if dicti > 0:

        dicti = Dictionary.objects.get(language=lc, name=nm)

        return mark_safe(dicti.text)
    else:
        dicti = Dictionary.objects.filter(language=lcd, name=nm).count()
        if dicti > 0:
            dicti = Dictionary.objects.get(language=lcd, name=nm)
            return dicti.text
        else:
            text_prefix = "##! "
            # if lcd is not "NL":
            #     text_prefix

            if debug:
                return text_prefix + "value: '" +defaultText + "' - key: "+nm
            else:
                return defaultText or "Text not found"




def translation_helper_context(translation_name, current_text=''):
    translations = Dictionary.objects.filter(name=translation_name).order_by('language')

    return {
        'domId': get_random_string(),
        'translations': translations,
        'current_text': current_text,
        'languages': Languages.objects.all(),
        'translation_key': translation_name
    }

