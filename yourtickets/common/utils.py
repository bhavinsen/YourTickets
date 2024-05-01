from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.translation import get_language

from ticketshop.models import (
    Languages,
    Dictionary
)

from django.utils.translation import get_language_from_request

def getCurrentLanguage(request):

    language_from_request = get_language_from_request(request)
    use_language = 'nl'

    if is_valid_language(language_from_request):
        use_language = language_from_request

    # print(request.COOKIES.get('language', 'uhmm... ok'))
    # print(request.COOKIES)

    # cookie_language = request.COOKIES.get('language', use_language).lower()

    # if not is_valid_language(cookie_language):
    #     cookie_language = 'nl'

    # from django.utils.translation import get_language
    #
    # print get_language()

    return get_language().upper()

def is_valid_language(language):

    return Languages.objects.filter(language_code=language.upper()).exists()


def getLanguagesList():
    language_list = []

    languages = Languages.objects.filter()
    for lg in languages:
        language_list.append([lg.language_code, lg.language_name])
    return language_list

def getWord(lc, nm, defaultText='', request_object=None):

    debug = False
    if request_object and request_object.user:
        is_super_user = request_object.user.is_superuser
        showdebug = request_object.GET.get('showerrors', False)

        # import pdb;pdb.set_trace()
        if is_super_user and showdebug is not False:
            debug = True


    # print defaultText
    # print showdebug

    lcd = "NL"
    lcd = Languages.objects.filter(language_code=lcd).first()
    lc = Languages.objects.filter(language_code=lc).first()
    dicti = Dictionary.objects.filter(language=lc, name=nm)

    # print('')
    # print(lcd)
    # print(lc)

    if dicti.exists():

        dicti = Dictionary.objects.get(language=lc, name=nm)
        return dicti.text
    else:
        dicti = Dictionary.objects.filter(language=lcd, name=nm)
        if dicti.exists():
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

def currency(dollars):
    dollars = round(float(dollars), 2)
    return "%s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])
