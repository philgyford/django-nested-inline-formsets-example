from django.db import models


class Publisher(models.Model):

    name = models.CharField(null=False, blank=False, max_length=255)


class Book(models.Model):

    title = models.CharField(null=False, blank=False, max_length=255)

    publisher = models.ForeignKey('Publisher', null=False, blank=False,
                                                    on_delete=models.CASCADE)


class BookImage(models.Model):
    "e.g. image of the cover, backcover, etc."

    book = models.ForeignKey('Book', null=False, blank=False,
                                                    on_delete=models.CASCADE)

    image = models.ImageField(null=False, blank=False, max_length=255)

    alt_text = models.CharField(null=False, blank=True, max_length=255)
