from django.urls import path

from . import views


app_name = 'books'

urlpatterns = [

    path('',
        views.HomeView.as_view(),
        name='home'),

    path('publishers/',
        views.PublisherListView.as_view(),
        name='publisher_list'),

    path('publishers/<int:pk>/',
        views.PublisherDetailView.as_view(),
        name='publisher_detail'),

    path('publishers/<int:pk>/edit/',
        views.PublisherUpdateView.as_view(),
        name='publisher_update'),

]
