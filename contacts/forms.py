from django import forms
from django.utils.translation import gettext_lazy as _
from localflavor.us.forms import USZipCodeField, USStateField
from phonenumber_field.formfields import PhoneNumberField
from .models import Contact, ContactAddress, ContactEmail, ContactPhoneNumber


class ContactModelForm(forms.ModelForm):
    """ModelForm definition for Contact."""

    class Meta:
        """Meta definition for Contactform."""

        model = Contact
        fields = ('first_name','last_name','job_title', 'description')


class ContactAddressModelForm(forms.ModelForm):
    """ModelForm definition for ContactAddress."""

    class Meta:
        """Meta definition for ContactAddressModelForm."""

        model = ContactAddress
        fields = ('contact', 'building_number', 'street_name', 'unit_type','unit_number', 'city', 'state', 'zipcode')


class ContactEmailModelForm(forms.ModelForm):
    """ModelForm definition for ContactEmail."""

    class Meta:
        """Meta definition for ContactEmailModelForm."""

        model = ContactEmail
        fields = ('contact','email_address')


class ContactPhoneNumberForm(forms.ModelForm):
    """ModelForm definition for ContactPhoneNumber."""

    class Meta:
        """Meta definition for ContactPhoneNumberModelForm."""

        model = ContactPhoneNumber
        fields = ('contact','phone_number',)


class ContactFormWithAEP(forms.Form):
    """Provides a contact form including required fields for one of each:

    - email address
    - phone number
    - address

    Attributes:
        first_name (forms.CharField): contact's first name
        last_name (forms.CharField): contact's last name
        job_title (forms.CharField, optional): contact's job role or title
        contact_desc (forms.CharField, optional): additional information about the contact
        email_addr (forms.EmailField): contact's initial email address
        phone (PhoneNumberField): contact's initial phone number
        building_no (forms.CharField): address house or building number
        street_name (forms.CharField): address street name
        unit_type (forms.CharField): address unit type
        unit_no (forms.CharField, optional): address unit identifier
        city (forms.CharField): address city
        state (USStateField): address state
        zipcode (USZipCodeField): address postal code or zipcode
    """

    first_name = forms.CharField(_("first name"), max_length=50, required=True)
    last_name = forms.CharField(_("last name"), max_length=50, required=True)
    job_title = forms.CharField(_("job title"), max_length=250, required=False)
    contact_desc = forms.CharField(_("additional information about the contact"), widget=forms.Textarea, required=False)
    email_addr = forms.EmailField(_("email address"), required=True)
    phone = PhoneNumberField(_("phone number"))
    building_no = forms.CharField(_("building number"), max_length=50, required=True)
    street_name = forms.CharField(_("street name"), max_length=150, required=True)
    unit_type = forms.CharField(_("unit type"), max_length=20, required=False, help_text=_("Suite, Box, Unit, etc."))
    unit_no = forms.CharField(_("unit number"), max_length=20, required=False, help_text=_("unit identifier ex: 105"))
    city = forms.CharField(_("city"), max_length=150, required=True)
    state = USStateField(_("state"))
    zipcode = USZipCodeField(_("zipcode"))
