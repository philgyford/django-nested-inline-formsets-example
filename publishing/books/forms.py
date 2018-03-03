from django import forms
from django.forms.models import BaseInlineFormSet, inlineformset_factory

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
