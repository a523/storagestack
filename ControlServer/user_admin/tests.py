from django.test import modify_settings
from django.urls import reverse
from rest_framework.test import APITestCase


@modify_settings(MIDDLEWARE={
    'remove': 'ControlServer.middleware.CustomExceptionMiddleware',
})
class UserTestCase(APITestCase):
    def test_get_user_list(self):
        resp = self.client.get(reverse('user_admin:users_list'))
        self.assertEqual(resp.status_code, 200, resp.data)
        self.assertTrue(isinstance(resp.json(), list))

    def test_create_user(self):
        user_info = {'username': 'xin', 'password': 'test_a!'}
        resp = self.client.post(reverse('user_admin:users_list'), user_info, format='json')
        self.assertEqual(resp.status_code, 201, resp.data)
        new_user_info = resp.json()
        user_id = new_user_info['id']
        self.assertTrue(isinstance(new_user_info, dict))
        self.assertTrue(isinstance(user_id, int))
        self.assertFalse(new_user_info['is_superuser'], "设计应不能通过web创建超级用户")

    def test_get_user_detail(self):
        pass

    def test_update_user(self):
        pass

    def delete_user(self):
        pass
