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
        fields = ('contact','email_address', 'email_label')


class ContactPhoneNumberForm(forms.ModelForm):
    """ModelForm definition for ContactPhoneNumber."""

    class Meta:
        """Meta definition for ContactPhoneNumberModelForm."""

        model = ContactPhoneNumber
        fields = ('contact','phone_number','phone_number_label',)


class ContactFormWithAEP(forms.Form):
    """Provides a contact form including required fields for one of each:
    - email address
    - phone number
    - address
    """

    first_name = forms.CharField(_("first name"), max_length=50, required=True)
    """contact's first name - 50 chars, required"""
    last_name = forms.CharField(_("last name"), max_length=50, required=True)
    """contact's last name - 50 chars, required"""
    job_title = forms.CharField(_("job title"), max_length=250, required=False)
    """contact's job role or title - 50 chars, not required"""
    contact_desc = forms.CharField(_("additional information about the contact"), widget=forms.Textarea, required=False)
    """additional information about the contact - not required"""
    email_addr = forms.EmailField(_("email address"), required=True)
    """contact's initial email address - required"""
    email_label = forms.CharField(_("email address name"), max_length=25, required=True, help_text="a memberable name for the email address, such as work or personal")
    """a label for the contact's initial email - 25 chars, required"""
    phone = PhoneNumberField(_("phone number"))
    """contact's initial phone number - required"""
    phone_label = forms.CharField(_("phone number name"), max_length=25, required=True, help_text=_("a memberable name for the phone number such as mobile or office"))
    """a label for the contact's initial phone number - 25 chars, required"""
    address_label = forms.CharField(_("address name"), max_length=50, required=True)
    """a label for the contact's initial address - 50 chars, required"""
    building_no = forms.CharField(_("building number"), max_length=50, required=True)
    """address house or building number - 50 chars, required"""
    street_name = forms.CharField(_("street name"), max_length=150, required=True)
    """address street name - 150 chars - required"""
    unit_type = forms.CharField(_("unit type"), max_length=20, required=False, help_text=_("Suite, Box, Unit, etc."))
    """address unit type - 20 chars, not required"""
    unit_no = forms.CharField(_("unit number"), max_length=20, required=False, help_text=_("unit identifier ex: 105"))
    """address unit identifier - 20 chars, not required"""
    city = forms.CharField(_("city"), max_length=150, required=True)
    """address city - 150 chars, required"""
    state = USStateField(_("state"))
    """address state - required"""
    zipcode = USZipCodeField(_("zipcode"))
    """address postal code or zipcode - required"""
