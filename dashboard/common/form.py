from django import forms

class Form(forms.Form):
    def is_valid(self):
        ret = forms.Form.is_valid(self)
        for f_name in self.errors:
            classes = self.fields[f_name].widget.attrs.get('class', '')
            classes += ' form-error'
            self.fields[f_name].widget.attrs['class'] = classes
        return ret

class ModelForm(forms.ModelForm):
    def is_valid(self):
        ret = forms.ModelForm.is_valid(self)
        for f_name in self.errors:
            classes = self.fields[f_name].widget.attrs.get('class', '')
            classes += ' form-error'
            self.fields[f_name].widget.attrs['class'] = classes
        return ret

class Form(forms.Form):
    def is_valid(self):
        ret = forms.Form.is_valid(self)
        for f_name in self.errors:
            classes = self.fields[f_name].widget.attrs.get('class', '')
            classes += ' form-error'
            self.fields[f_name].widget.attrs['class'] = classes
        return ret

