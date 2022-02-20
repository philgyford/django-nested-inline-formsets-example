from django.urls import path

from . import views


app_name = "books"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("publishers/", views.PublisherListView.as_view(), name="publisher_list"),
    path(
        "publishers/<int:pk>/",
        views.PublisherDetailView.as_view(),
        name="publisher_detail",
    ),
    path(
        "publishers/add/", views.PublisherCreateView.as_view(), name="publisher_create"
    ),
    path(
        "publishers/<int:pk>/books/edit/",
        views.PublisherBooksUpdateView.as_view(),
        name="publisher_books_update",
    ),
]
