from django.test import modify_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status


User = get_user_model()


@modify_settings(MIDDLEWARE={
    'remove': 'ControlServer.middleware.CustomExceptionMiddleware',
})
class UserTestCase(APITestCase):
    def setUp(self) -> None:
        self.superuser = User.objects.create_superuser(username='super', password='superuser')
        self.client.force_login(self.superuser)

    def create_user(self):
        user_info = {'username': 'xin', 'password': 'test_a!'}
        resp = self.client.post(reverse('user_admin:users_list'), user_info, format='json')
        self.assertEqual(resp.status_code, 201, resp.data)
        return resp

    def test_create_user(self):
        resp = self.create_user()
        new_user_info = resp.json()
        user_id = new_user_info['id']
        self.assertTrue(isinstance(new_user_info, dict))
        self.assertTrue(isinstance(user_id, int))
        self.assertFalse(new_user_info['is_superuser'], "设计应不能通过web创建超级用户")

    def test_get_user_list(self):
        resp = self.client.get(reverse('user_admin:users_list'))
        self.assertEqual(resp.status_code, 200, resp.data)
        self.assertTrue(isinstance(resp.json(), list))

    def test_get_user_detail(self):
        user = self.create_user()
        resp = self.client.get(reverse('user_admin:user_detail', kwargs={'pk': user.json()['id']}))
        self.assertEqual(resp.status_code, 200, resp.data)
        self.assertEqual(resp.json()['id'], user.json()['id'])
        self.assertEqual(resp.json()['username'], 'xin')

    def test_update_user(self):
        user = self.create_user()
        data = {'username': 'newname', 'first_name': 'lei', 'last_name': 'xin', 'email': 'test@qq.com',
                'is_active': False, 'password': 'new_password'}
        resp = self.client.put(reverse('user_admin:user_detail', kwargs={'pk': user.json()['id']}), data=data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.data)
        user = resp.json()
        self.assertEqual(user['first_name'], data['first_name'])
        self.assertEqual(user['last_name'], data['last_name'])
        self.assertEqual(user['email'], data['email'])
        self.assertEqual(user['is_active'], data['is_active'])
        self.assertEqual(user['username'], data['username'])
        u = User.objects.get(id=user['id'])
        self.assertTrue(u.check_password(data['password']))

    def test_update_user_no_password(self):
        general_user = User.objects.create_user(username='user', password='general_user_password')
        url = reverse('user_admin:user_detail', kwargs={'pk': general_user.id})
        new_data_no_pw = {'username': 'new_name'}
        response = self.client.put(url, data=new_data_no_pw)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('username'), new_data_no_pw['username'])

    def test_delete_user(self):
        user = self.create_user()
        resp = self.client.delete(reverse('user_admin:user_detail', kwargs={'pk': user.json()['id']}))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)


# 测试自定义用户修改权限验证
class UserModifyPermissionTestCase(APITestCase):
    def setUp(self) -> None:
        # 创建超级用户和管理员用户
        self.superuser = User.objects.create_superuser(username='superuser', password='superuser_password')
        self.staff_user = User.objects.create_user(username='staff_user', is_staff=True, password='staff_user_password')
        self.general_user = User.objects.create_user(username='user', password='general_user_password')

    def test_cannot_delete_superuser(self):
        url = reverse('user_admin:user_detail', kwargs={'pk': self.superuser.id})
        self.client.login(username='superuser', password='superuser_password')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_admin_can_delete_general_user(self):
        general_user = User.objects.create_user(username='user_temp', password='general_user_password')
        url = reverse('user_admin:user_detail', kwargs={'pk': general_user.id})
        self.client.login(username='staff_user', password='staff_user_password')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_general_user_cannot_delete_admin(self):
        url = reverse('user_admin:user_detail', kwargs={'pk': self.staff_user.id})
        self.client.login(username='user', password='general_user_password')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_super_can_delete_admin_user(self):
        url = reverse('user_admin:user_detail', kwargs={'pk': self.staff_user.id})
        self.client.login(username='superuser', password='superuser_password')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
