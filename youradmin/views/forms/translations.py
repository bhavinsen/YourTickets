from django import forms
from ticketshop.models import Dictionary, Languages

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Languages
        fields = ('language_code', 'language_name')

    based_values = forms.ChoiceField(label="Based on language", choices=(), required=True)

    def __init__(self, *args, **kwargs):
        languages = kwargs.pop('languages', None)

        if languages:
            languages_tuple = ()

            for language in languages:
                languages_tuple = ((language.id, language.language_code),) + languages_tuple

        super(LanguageForm, self).__init__(*args, **kwargs)

        if languages:
            self.fields['based_values'].choices = languages_tuple
        else:
            del self.fields['based_values']


class TranslationForm(forms.ModelForm):
    # name = forms.CharField(max_length=100, required=True)
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Dictionary
        fields = ('name', 'text')

class TranslationsForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    # text = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(TranslationsForm, self).__init__(*args, **kwargs)
        languages = Languages.objects.all()

        for language in languages:
            self.fields[language.language_code+'_text'] = forms.CharField(max_length=100, required=True)
