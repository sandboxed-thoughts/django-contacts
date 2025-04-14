"""contacts.admin

Django admin models for the contacts app
"""

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Contact, ContactAddress, ContactEmail, ContactPhoneNumber


# Inlines

class ContactAddressInline(admin.StackedInline):
    '''Stacked Inline View for ContactAddress'''

    model = ContactAddress
    min_num = 0
    extra = 0
    classes = ['collapse']


class ContactEmailInline(admin.StackedInline):
    '''Stacked Inline View for ContactEmail'''

    model = ContactEmail
    min_num = 0
    extra = 0
    classes = ['collapse']


class ContactPhoneNumberInline(admin.StackedInline):
    '''Stacked Inline View for ContactPhoneNumber'''

    model = ContactPhoneNumber
    min_num = 0
    extra = 0
    classes = ['collapse']


# Models

class BaseAdmin(SimpleHistoryAdmin):
    """Provides standard save methods for the tracking fields `created_by` and `updated_by`
    """
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if not change:  #: new instance
                instance.created_by = request.user
            instance.updated_by = request.user
            instance.save()
        formset.save_m2m()

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Contact)
class ContactAdmin(BaseAdmin):
    list_display = ('full_name','job_title','created_on',)
    list_filter = ('job_title','created_on',)
    search_fields = ('first_name','last_name','job_title',)
    inlines = (ContactEmailInline, ContactPhoneNumberInline, ContactAddressInline)

    fieldsets = (
        (None, {
            "fields": (
                ("first_name", "last_name",),
                "job_title",
                "description",
            ),
        }),
    )
