"""contacts.utils.mixins

General model mixin objects used to provide common fields
and functionality for the contacts app's models.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from localflavor.us.models import USZipCodeField, USStateField
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

from contacts.utils import normalize_email


USER_MODEL: str = settings.AUTH_USER_MODEL
"""Reference to the project's user model as defined in the settings module.
"""


class ObjectTrackingMixin(models.Model):
    """supplies standard create/update tracking fields

    Attributes:
        created_on (models.DateTimeField): datetime the instance was created
        updated_on (models.DateTimeField): datetime the instance was last updated
        created_by (models.ForeignKey): the user that created the instance
        updated_by (models.ForeignKey): the user that last updated the instances
    """

    created_on: models.DateTimeField = models.DateTimeField(_("created on"), auto_now_add=True, auto_now=False, editable=False)
    updated_on: models.DateTimeField = models.DateTimeField(_("last updated"), auto_now_add=False, auto_now=True, editable=False)
    created_by: models.ForeignKey = models.ForeignKey(USER_MODEL, related_name='created_%(class)s', on_delete=models.SET_NULL, blank=True, null=True, editable=False)
    updated_by: models.ForeignKey = models.ForeignKey(USER_MODEL, related_name='edited_%(class)s', on_delete=models.SET_NULL, blank=True, null=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class USAddressMixin(models.Model):
    """A django model mixin for adding address information.

    Attributes:
        name (models.CharField, optional): A reference name for the address
        street (models.CharField): The buiding number and street name for the address
        unit_type (models.CharField): The designated unit type.
            Examples incude Unit, Suite, PO Box, etc. Defaults to `"unit"`.
        unit_number(models.CharField, optional): The identification number for the provided unit.
        city (models.CharField): The address' city
        state (USStateField): The address' state
        zipcode (USZipCodeField): The address' zipcode
    """

    street: models.CharField = models.CharField(_("street"), max_length=150, help_text=_("building number and street name"))
    unit_type: models.CharField = models.CharField(_("unit type"), max_length=20, help_text=_("P.O. Box, Unit, Suite, etc."), default="unit")
    unit_number: models.CharField = models.CharField(_("Unit number"), max_length=20, help_text=_("The assigned unit reference. This is typically a number"), blank=True, null=True)
    city: models.CharField = models.CharField(_("city"), max_length=150)
    state: USStateField = USStateField()
    zipcode: USZipCodeField = USZipCodeField()

    @property
    def line1(self) -> str:
        """Defines the full first line of the address.
        """
        return self.street

    @property
    def line2(self) -> str | None:
        """Defines the full second line of the address.
        """
        if self.has_unit:
            return self.unit()

    @property
    def line3(self) -> str:
        """Defines the full third line of the address.
        """
        return f"{self.region()} {self.zipcode}"

    @property
    def has_unit(self) -> bool:
        """A check to determine if a unit number exists.

        Returns:
            bool: `self.unit_number is not None`
        """
        return self.unit_number is not None

    class Meta:
        abstract = True

    def unit(self) -> str:
        """A full unit line including the unit type and identification.

        Returns:
            str: `f"{self.unit_type} {self.unit_number}"`
        """
        return f"{self.unit_type} {self.unit_number}"

    def region(self) -> str:
        """Compiles the instance's city and street into one string.

        Returns:
            str: `f"{self.city}, {self.state}`
        """
        return f"{self.city}, {self.state}"

    def _full_address(self) -> list[str]:
        """Compiles a list of formatted address lines.

        Returns:
            list[str]: `[self.street, self.line2, self.line3]` or `[self.street, self.line3]`
        """
        lines: list[str] = [self.street, self.line3]
        if self.has_unit:
            lines.insert(1, self.line2)
        return lines

    def _short_address(self) -> list[str]:
        """Compiles a small-format list of address lines.

        Returns:
            list[str]: `[self.line1, self.region()]`
        """
        return [
            self.line1,
            self.region(),
        ]

    def single_line_address(self, named: bool = False) -> str:
        """Compiles a single string intended for single-line printing from
        `self._full_address()`.

        Args:
            named (bool, optional): Add the address name. Defaults to False.

        Returns:
            str: `f"{self.name}: {", ".join(self._full_address())}"` or `", ".join(self._full_address())`
        """
        addr: str = ", ".join(self._full_address())
        if named:
            return f"{self.name}: {addr}"
        return addr

    def multi_line_address(self, named: bool = False) -> str:
        addr: str = "\n".join(self._full_address())
        if named:
            return f"{self.name}\n{addr}"
        return addr

    def short_address(self, named: bool = False) -> str:
        addr: str = ", ".join(self._short_address())
        if named:
            return f"{self.name}: {addr}"
        return addr

    def __str__(self) -> str:
        """String representation of model instances.
        """
        return self.short_address()


class PersonMixin(models.Model):
    """A model mixin for adding identification of an individual.

    Attributes:
        first_name (models.CharField): the person's first name
        last_name (models.CharField): the person's last name
        job_title (models.CharField, optional): an optional field to identify the person's
            role within a company
        description (models.TextField, optional): an optional block of text providing
            additional information about the person.
    """

    first_name: models.CharField = models.CharField(_("first name"), max_length=50)
    last_name: models.CharField = models.CharField(_("last name"), max_length=50)
    job_title: models.CharField = models.CharField(_("role / title"), max_length=50, blank=True, null=True)
    description: models.TextField = models.TextField(_("about the person"), blank=True, null=True)

    def full_name(self) -> str:
        """Generates a single string including the instance's first and last names.

        Returns:
            str: `f"{self.first_name} {self.last_name}"`
        """
        return f"{self.first_name} {self.last_name}"

    def short_name(self) -> str:
        """Generates a single string of the instance's first initial of the first name
        and full last name.

        Returns:
            str: `f"{self.first_name[0]}. {self.last_name}"`
        """
        return f"{self.first_name[0]}. {self.last_name}"

    def clean(self):
        """Format and sanitize submitted data.
        """
        super().clean()
        if self.job_title:
            self.job_title = self.job_title.title()

    class Meta:
        abstract = True


class EmailMixin(models.Model):
    """A model mixin providing email information.

    The intention of this mixin is to provide defaults for models
    that will be used to relate multiple email addresses to other models.

    Attributes:
        email_address (models.EmailField): the email address to store
        email_label (models.CharField, optional): an optional label for identifying the email address
    """

    email_address: models.EmailField = models.EmailField(_("email address"), max_length=254, unique=True)

    class Meta:
        abstract = True

    def clean(self):
        """Format and sanitize submitted data.
        """
        super().clean()
        self.email_address = normalize_email(self.email_address)

    def __str__(self):
        return self.email_address


class PhoneNumberMixin(models.Model):
    """A model mixin providing phone number information.

    The intention of this mixin is to provide defaults for models
    that will be used to relate multiple phone numbers to other models.

    Attributes:
        phone_number (PhoneNumberField): the phone number
    """
    phone_number: PhoneNumberField = PhoneNumberField()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.phone_number




class AbstractContact(ObjectTrackingMixin, PersonMixin):
    """An abstract Contact model for importing into other pacakges.
    """

    class Meta:
        abstract: bool = True
        verbose_name: str = _("contact")
        verbose_name_plural: str = _("contacts")

    def __str__(self):
        return self.full_name()
