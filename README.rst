django_dirty_bits
=================
Dirty tracking for Django models

django_dirty_bits is a library that tracks model's modification state. Ths lets you find out if you need to call save on a model
or add it to post processing.


Examples
========

Registering your models::

    import dirty_bits

    class Author(models.Model):
        name = models.TextField()

    dirty_bits.register(Author)

Registering all of your models::

    dirty_bits.register_all()

Checking dirtiness::

    author = Author.objects.get(pj=3)
    author.is_dirty()
