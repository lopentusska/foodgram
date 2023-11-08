from django.contrib.auth import get_user_model
from django.test import TestCase


class UserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            email='testuser@email.com',
            username='testuser',
            first_name='testuserfrname',
            last_name='testuserlsname',
            password='testpass123',
        )

    def test_user_model(self):
        self.assertEqual(self.user.email, 'testuser@email.com')
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.first_name, 'testuserfrname')
        self.assertEqual(self.user.last_name, 'testuserlsname')

    def test_superuser_model(self):
        self.user.is_superuser = True
        self.user.is_staff = True
        self.assertTrue(self.user.is_superuser)
        self.assertTrue(self.user.is_staff)
        self.assertEqual(self.user.email, 'testuser@email.com')
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.first_name, 'testuserfrname')
        self.assertEqual(self.user.last_name, 'testuserlsname')
