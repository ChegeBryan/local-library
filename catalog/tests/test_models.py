from django.test import TestCase

from catalog.models import Author


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up no-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')
