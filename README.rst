===============
django-contacts
===============

django-contacts is a Django app to provide a directory of
people including their contact information such as email addresses, phone numbers, and physical addresses.


Quick start
-----------

1. Add "simple_history" and "contacts" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "simple_history",
        "contacts",
    ]

2. Run ``python manage.py migrate`` to create the models.

3. Start the development server and visit the admin to create a contact.
