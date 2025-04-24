from django.db import models
from django.utils.translation import gettext_lazy as _
from .mixins import (
    ObjectTrackingMixin, USAddressMixin, PersonMixin,
    EmailMixin, PhoneNumberMixin, AbstractContact
)



class Contact(AbstractContact):
    """Provides a default Contact model"""
    class meta:
        abstract: bool = False



class ContactAddress(ObjectTrackingMixin, USAddressMixin):
    """Model definition for assigning addresses to a Contact
    """

    contact = models.ForeignKey(Contact, related_name='contact_addresses', on_delete=models.CASCADE)
    """the assigned contact for the address"""

    class Meta:
        verbose_name: str = _("contact address")
        verbose_name_plural: str = _("contact addresses")


class ContactPhoneNumber(ObjectTrackingMixin, PhoneNumberMixin):
    """Model definition for assigning phone numbers to a Contact
    """

    contact = models.ForeignKey(Contact, related_name='contact_phone_numbers', on_delete=models.CASCADE)
    """the assigned contact for the phone number"""

    def __str__(self):
        return self.phone_number.as_national


class ContactEmail(ObjectTrackingMixin, EmailMixin):
    """Model definition for assinging emails to a Contact"""

    contact = models.ForeignKey(Contact, related_name='contact_email_addresses', on_delete=models.CASCADE)
    """the assigned contact"""

    def __str__(self):
        return self.email_address
