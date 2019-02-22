from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from publishing.utils.forms import is_empty_form, is_form_persisted
from .models import Publisher, Book, BookImage


# The formset for editing the BookImages that belong to a Book.
BookImageFormset = inlineformset_factory(
                            Book,
                            BookImage,
                            fields=('image', 'alt_text'),
                            extra=1)


class BaseBooksWithImagesFormset(BaseInlineFormSet):
    """
    The base formset for editing Books belonging to a Publisher, and the
    BookImages belonging to those Books.
    """

    def add_fields(self, form, index):
        super().add_fields(form, index)

        # Save the formset for a Book's Images in the nested property.
        form.nested = BookImageFormset(
                                instance=form.instance,
                                data=form.data if form.is_bound else None,
                                files=form.files if form.is_bound else None,
                                prefix='bookimage-%s-%s' % (
                                    form.prefix,
                                    BookImageFormset.get_default_prefix()),
                                )

    def is_valid(self):
        """
        Also validate the nested formsets.
        """
        result = super().is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()

        return result

    def clean(self):
        super().clean()

        for form in self.forms:
            if not hasattr(form, 'nested') or self._should_delete_form(form):
                continue

            if self._is_adding_nested_inlines_to_empty_form(form):
                form.add_error(
                    field=None,
                    error=_('You are trying to add Images to a Book which '
                            'does not yet exist. Please add information '
                            'about the Book.'))

    def save(self, commit=True):
        """
        Also save the nested formsets.
        """
        result = super().save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result

    def _is_adding_nested_inlines_to_empty_form(self, form):
        if not hasattr(form, 'nested'):
            return False

        if is_form_persisted(form) or not is_empty_form(form):
            return False

        non_deleted_forms = (set(form.nested.forms)
                             .difference(set(form.nested.deleted_forms)))
        return any(not is_empty_form(nested_form)
                   for nested_form in non_deleted_forms)


# This is the formset for the Books belonging to a Publisher and the
# BookImages belonging to those Books.
#
# You'd use this by passing in a Publisher:
#     PublisherBooksWithImagesFormset(**form_kwargs, instance=self.object)
PublisherBooksWithImagesFormset = inlineformset_factory(
                                Publisher,
                                Book,
                                formset=BaseBooksWithImagesFormset,
                                # We need to specify at least one Book field:
                                fields=('title',),
                                extra=1,
                                # If you don't want to be able to delete Publishers:
                                #can_delete=False
                            )
