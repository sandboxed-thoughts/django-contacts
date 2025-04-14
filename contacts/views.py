"""contacts.views

View modules for the contacts app.
"""

from django.views.generic import DetailView, ListView
from .models import Contact


class ContactList(ListView):
    model = Contact
    context_object_name = 'objects'
    template_name='contacts/list_view.html'


class ContactDetail(DetailView):
    model = Contact
    context_object_name = 'object'
    template_name='contacts/detail_view.html'
