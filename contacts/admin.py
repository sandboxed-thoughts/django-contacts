"""contacts.admin

Django admin models for the contacts app
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Contact, ContactAddress, ContactEmail, ContactPhoneNumber


# Inlines

class ContactAddressInline(admin.StackedInline):
    '''Stacked Inline View for ContactAddress'''

    model = ContactAddress
    min_num = 0
    extra = 0
    classes = ['collapse']
    fieldsets = (
        (None, {
            "fields": (
                'street',
                ('city','state','zipcode',),
            ),
        }),
    )


class ContactEmailInline(admin.StackedInline):
    '''Stacked Inline View for ContactEmail'''

    model = ContactEmail
    min_num = 0
    extra = 0
    classes = ['collapse']
    fieldsets = (
        (None, {
            "fields": (
                'email_address',
            ),
        }),
    )


class ContactPhoneNumberInline(admin.StackedInline):
    '''Stacked Inline View for ContactPhoneNumber'''

    model = ContactPhoneNumber
    min_num = 0
    extra = 0
    classes = ['collapse']
    fieldsets = (
        (None, {
            "fields": (
                "phone_number",
            ),
        }),
    )


# Models

class BaseAdmin(admin.ModelAdmin):
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


class ContactAddressAdmin(BaseAdmin):
    '''Admin View for ContactAddress'''

    class HasUnitFilter(admin.SimpleListFilter):
        # Human-readable title which will be displayed in the
        # right admin sidebar just above the filter options.
        title = _("has unit")

        # Parameter for the filter that will be used in the URL query.
        parameter_name = "has_unit"

        def lookups(self, request, model_admin):
            """
            Returns a list of tuples. The first element in each
            tuple is the coded value for the option that will
            appear in the URL query. The second element is the
            human-readable name for the option that will appear
            in the right sidebar.
            """
            return [
                (True, True),
                (False, False),
            ]

        def queryset(self, request, queryset):
            """
            Returns the filtered queryset based on the value
            provided in the query string and retrievable via
            `self.value()`.
            """
            if self.value() == True:
                return queryset.filter(
                    has_unit=True
                )
            if self.value() == False:
                return queryset.filter(
                    has_unit=False
                )

    list_display = (
        'short_address',
        'contact',
        'street',
        'has_unit',
        'city',
        'state',
        'zipcode',
    )
    list_filter = (
        'contact',
        HasUnitFilter,
        'city',
        'state',
    )
    search_fields = (
        'name',
        'street',
        'city',
        'state',
        'zipcode',
    )
    ordering = (
        'contact',
        'state',
        'city',
        'street',
    )
    fieldsets = (
        (None, {
            "fields": (
                'contact',
                'name',
            ),
        }),
        ("Address", {
            "fields": (
                'street',
                ('city','state','zipcode',),
            ),
        }),
    )


class ContactEmailAdmin(BaseAdmin):
    '''Admin View for ContactEmail'''

    list_display = ('email_address','name','contact')
    list_filter = ('name','contact',)
    search_fields = ('name','email_address','contact',)
    ordering = ('contact','email_address',)
    fieldsets = (
        (None, {
            "fields": (
                'contact',
            ),
        }),
        ("Email Address", {
            "fields": (
                'email_address',
            )
        })
    )


class ContactPhoneNumberAdmin(BaseAdmin):
    '''Admin View for ContactPhoneNumber'''

    list_display = ('email_address','name','contact')
    list_filter = ('name','contact',)
    search_fields = ('name','email_address','contact',)
    ordering = ('contact','email_address',)
    fieldsets = (
        (None, {
            "fields": (
                'contact',
            ),
        }),
        ("Email Address", {
            "fields": (
                'email_address',
            )
        })
    )
