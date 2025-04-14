===============
django-contacts
===============

django-contacts is a Django app to provide a directory of
people including their contact information such as email addresses, phone numbers, and physical addresses.


Quick start
-----------

1. Add "contacts" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "contacts",
    ]

2. Include the contacts URLconf in your project urls.py like this::

    path("contacts/", include("contacts.urls")),

3. Run ``python manage.py migrate`` to create the models.

4. Start the development server and visit the admin to create a contact.
