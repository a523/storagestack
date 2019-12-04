from django.test import TestCase
from django.urls import reverse


class UserTestCase(TestCase):
    def test_get_user_list(self):
        resp = self.client.get(reverse('user_admin:users_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(isinstance(resp.json(), list))
