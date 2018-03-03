from django.shortcuts import render
from django.views.generic import DetailView, FormView, ListView, TemplateView
from django.views.generic.detail import SingleObjectMixin

from .models import Publisher, Book, BookImage


class HomeView(TemplateView):
    template_name = 'books/home.html'


class PublisherListView(ListView):
    model = Publisher
    template_name = 'books/publisher_list.html'


class PublisherDetailView(DetailView):
    model = Publisher
    template_name = 'books/publisher_detail.html'
