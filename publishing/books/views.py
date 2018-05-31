from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import (
    CreateView, DetailView, FormView, ListView, TemplateView
)
from django.views.generic.detail import SingleObjectMixin

from .forms import PublisherBooksWithImagesFormset
from .models import Publisher, Book, BookImage


class HomeView(TemplateView):
    template_name = 'books/home.html'


class PublisherListView(ListView):
    model = Publisher
    template_name = 'books/publisher_list.html'


class PublisherDetailView(DetailView):
    model = Publisher
    template_name = 'books/publisher_detail.html'


class PublisherCreateView(CreateView):
    """
    Only for creating a new publisher. Adding books to it is done in the
    PublisherBooksUpdateView().
    """
    model = Publisher
    template_name = 'books/publisher_create.html'
    fields = ['name',]

    def form_valid(self, form):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'The publisher was added.'
        )

        return super().form_valid(form)


class PublisherBooksUpdateView(SingleObjectMixin, FormView):
    """
    For adding books to a Publisher.
    """

    model = Publisher
    template_name = 'books/publisher_books_update.html'

    def get(self, request, *args, **kwargs):
        # The Publisher we're editing:
        self.object = self.get_object(queryset=Publisher.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # The Publisher we're uploading for:
        self.object = self.get_object(queryset=Publisher.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        """
        Use our big formset of formsets, and pass in the Publisher object.
        """
        return PublisherBooksWithImagesFormset(
                            **self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        form.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Changes were saved.'
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('books:publisher_detail', kwargs={'pk': self.object.pk})
