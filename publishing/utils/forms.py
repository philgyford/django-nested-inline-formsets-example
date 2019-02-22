def is_empty_form(form):
    return form.is_valid() and not form.cleaned_data


def is_form_persisted(form):
    return form.instance and not form.instance._state.adding
