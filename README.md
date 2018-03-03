# Django nested inline formsets example

This Django project is purely to demonstrate an example of how to create a form that contains [inline formsets][if] that each contains its own inline formset.

I'm indebted to [this blogpost][post] by Ravi Kumar Gadila for helping me figure this out.

[if]: https://docs.djangoproject.com/en/2.0/topics/forms/modelforms/#inline-formsets
[post]: https://micropyramid.com/blog/how-to-use-nested-formsets-in-django/

## The situation

We have a model describing Publishers. Each Publisher can have a number of Books. Each Book can have a number of BookImages (e.g. its cover, back cover, illustrations, etc):

    Publisher #1
      |-Book
      |   |-BookImage
      |   |-BookImage
      |
      |-Book
          |-BookImage

    Publisher #2
      |-Book
      |
      |-Book

Using an inline formset we could display a single form that would let the user edit all of the Books belonging to a single Publisher.

Using another inline formset we could display another form that would let the user edit all of the BookImages belonging to a single Book.

It becomes trickier if we want to combine these two forms into one: displaying all of the Books for a Publisher, and for each Book, all of its BookImages.

## Solution

You can see in [`forms.py`][forms] how we construct an inline formset, `BookImageFormset` for editing the `BookImage`s belonging to a single `Book`.

And then we create a custom `BaseBooksWithImagesFormset` that has a custom `nested` property. This contains our `BookImageFormset`. We add custom methods for `is_valid()` and `save()` to ensure the data in these nested formsets are validated and saved.

Finally we create our `PublisherBooksWithImagesFormset` which is for editing all the `Book`s belonging to a `Publisher`... and we pass it this argument: `formset=BaseBooksWithImagesFormset` so it knows how to handle each of the `Book`s' `BookImage`s.

See [`views.py`][views] for how we use this in a class-based view to create the page. This expects the `id` of a `Publisher`. And see the [`books/publisher_update.html`][template] template for how the outer form, and its `Book` formsets, and their nested `BookImage` formsets, are rendered.

[forms]: publishing/books/forms.py
[views]: publishing/books/views.py
[template]: publishing/books/templates/books/publisher_update.html

Here's an image showing how that page looks:


## Set-up

If you want to get this project running to see how it works...

1. Download or clone the repository.

2. Install Django and [Pillow](https://pillow.readthedocs.io/en/latest/) (required for the `ImageField`). For example, using pip with the `requirements.txt` file:

		pip install -r requirements.txt

3. Run the migrations:

		./manage.py migrate

4. Create a superuser to use the Django Admin:

		./manage.py createsuperuser

5. Run the development server:

		./manage.py runserver

6. Log in to the Django Admin at http://127.0.0.1:8000/admin/ and add at least one Publisher.

7. Then view the site http://127.0.0.1:8000/ You can follow the links to see all your Publishers, then choose a Publisher, then click the link to add or edit some Books. You'll then be on a page like http://127.0.0.1:8000/publishers/1/edit/ which is the form with its inline formsets.
