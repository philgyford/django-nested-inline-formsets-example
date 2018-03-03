from django.db import models
from django.urls import reverse


class Publisher(models.Model):

    name = models.CharField(null=False, blank=False, max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('books:publisher_detail', kwargs={'pk': self.pk})


class Book(models.Model):

    title = models.CharField(null=False, blank=False, max_length=255)

    publisher = models.ForeignKey('Publisher', null=False, blank=False,
                            on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title


class BookImage(models.Model):
    "e.g. image of the cover, backcover, etc."

    book = models.ForeignKey('Book', null=False, blank=False,
                            on_delete=models.CASCADE, related_name='images')

    image = models.ImageField(null=False, blank=False, max_length=255)

    alt_text = models.CharField(null=False, blank=True, max_length=255)
