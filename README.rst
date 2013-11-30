=================
django_dirty_bits
=================

Dirty tracking for Django models

django_dirty_bits is a library that tracks model's modification state. Ths lets you find out if you need to call save on a model
or add it to post processing.

Requirements
------------

* Django 1.2+


Examples
--------

1. Registering your models

  ::
  
    import dirty_bits

    class Author(models.Model):
        name = models.TextField()

    dirty_bits.register(Author)

2. Registering all of your models

  ::
  
    dirty_bits.register_all()

3. Checking dirtiness

  ::

    author = Author.objects.get(pj=3)
    author.is_dirty()


Running Tests
-------------

Running the tests requires you to either configure an environment with all the parts installed
that are required in requirements/requirements.txt, or follow the following steps


1. Create a sandbox

::

  virtualenv {% virtual_env_name %}
  {% path to virtual_env_name %}/bin/activate

2. Set the django settings to be test_settings

::

  export DJANGO_SETTINGS_MODULE=test_settings

3. Install requirements

::

  pip install -r -U requirements/requirements.txt

4. Running tests

::

  python manage.py test
