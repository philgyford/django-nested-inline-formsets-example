def is_empty_form(form):
    """
    Is this form valid (has no errors) and contains no data?
    """
    if form.is_valid() and not form.cleaned_data:
        return True
    else:
        # Either the form has errors (isn't valid) or
        # it doesn't have errors and contains data.
        return False


def is_form_persisted(form):
    """
    Does the form have a model instance attached and it's not being added?
    e.g. The form is about an existing Book whose data is being edited.
    """
    if form.instance and not form.instance._state.adding:
        return True
    else:
        # Either the form has no instance attached or
        # it has an instance that is being added.
        return False
