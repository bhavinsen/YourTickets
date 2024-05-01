def is_field_clearablefileinput(formField):
    return formField.widget.__class__.__name__ == 'ClearableFileInput'


def is_field_dateinput(formField):
    return formField.widget.__class__.__name__ == 'DateInput'


def is_field_checkbox(formField):
    return formField.widget.__class__.__name__ == 'CheckboxInput'


def is_field_hidden(formField):
    return formField.widget.__class__.__name__ == 'HiddenInput'


def is_field_imagefield(formField):
    return formField.__class__.__name__ == 'ImageField'


def is_field_radioselect(formField):
    return formField.widget.__class__.__name__ == 'RadioSelect'
