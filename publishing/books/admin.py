from django.contrib import admin

from .models import Publisher, Book, BookImage


class BookImageInline(admin.TabularInline):
    model = BookImage
    extra = 1


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'publisher')
    list_display_links = ('title',)

    inlines = (BookImageInline,)
