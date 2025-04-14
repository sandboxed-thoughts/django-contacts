"""contacts.tests

Automated test modules for the contacts app.
"""

from django.test import TestCase
from django.db.utils import IntegrityError
from .models import Contact, ContactAddress, ContactEmail, ContactPhoneNumber


class TestClassDocstrExist(TestCase):
    """Ensure that each of the contacts-defined objects has a docstring.
    """

    def setUp(self):
        """Provides a default list of objects for testing as `self.class_list`.
        """
        self.class_list = [
            Contact, ContactAddress, ContactEmail, ContactPhoneNumber
        ]
        return super().setUp()

    def test_docstrings(self):
        """iterate over the objects in `self.class_list` to ensure each object has
        a docstring.
        """
        for obj in self.class_list:
            self.assertIsNotNone(
                obj.__doc__,
                f"{obj.__name__} missing docstring",
            )
            self.assertNotEqual(
                obj.__doc__,
                "",
                f"{obj.__name__} blank docstring",
            )

class TestContactModel(TestCase):
    """A test suite to test `contacts.models.Contact`
    """
    def setUp(self):
        """provide basic contact information and a base `Contact` instance for testing.

        Attributes:
            self.fn (str): first_name
            self.ln (str): last_name
            self.jt (str): job_title
            self.desc (str): description
            self.test_contact (Contact): a contact instance
        """
        self.fn: str = "jack"
        self.ln: str = "hoff"
        self.jt: str = "generic employee"
        self.desc: str = "a general office worker"
        self.test_contact: Contact = Contact.objects.create(first_name=self.fn, last_name=self.ln, job_title=self.jt, description=self.desc)
        return super().setUp()

    def test_contact_is_instance(self):
        "test that the test contact is an instance of `Contact`"
        self.assertIsInstance(self.test_contact, Contact)

    def test_contact_first_name_required(self):
        """test that the test contact cannot have a blank or null first_name.
        """
        with self.assertRaises(IntegrityError):
            Contact.objects.create(first_name="", last_name="ln", job_title="job thing", description=None)
            Contact.objects.create(first_name=None, last_name="ln", job_title="job thing", description=None)

    def test_contact_last_name_required(self):
        """test that the test contact cannot have a null last_name.
        """
        with self.assertRaises(IntegrityError):
            Contact.objects.create(first_name="firstname", last_name="", job_title="job thing", description=None)
            Contact.objects.create(first_name="firstname", last_name=None, job_title="job thing", description=None)

    def test_contact_fields(self):
        """test that the test contact has no null fields"""
        self.assertIsNotNone(
            self.test_contact.first_name
        )
        self.assertIsNotNone(
            self.test_contact.last_name
        )
        self.assertIsNotNone(
            self.test_contact.job_title
        )
        self.assertIsNotNone(
            self.test_contact.description
        )



