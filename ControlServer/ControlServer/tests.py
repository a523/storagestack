from django.test import TestCase, override_settings
from ControlServer import exe
from ControlServer.controller import *
from ControlServer.errors import RequestAgentError, TaskException
from deploy import tasks
from unittest.mock import patch, create_autospec
from aiohttp.test_utils import make_mocked_coro
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


def modify_setting_permission():
    rest_setting = settings.REST_FRAMEWORK
    del rest_setting['DEFAULT_PERMISSION_CLASSES']
    return rest_setting


class RunExeTestCase(TestCase):
    def test_run_cmd(self):
        ret = exe.run_cmd('echo hello')
        self.assertEqual(ret.returncode, 0)
        self.assertEqual(ret.stdout.strip(), 'hello')


class MultiTasksResultTestCase(TestCase):
    def setUp(self) -> None:
        self.mock_result_1 = create_autospec(Result)
        self.mock_result_2 = create_autospec(Result)
        self.mul_r = MultiTasksResult([self.mock_result_1, self.mock_result_2])

    def test_getitem_as_list(self):
        self.assertEqual(self.mul_r[1], self.mock_result_2)

    def test_loop_as_list(self):
        i = 0
        for result in self.mul_r:
            self.assertIs(result, self.mul_r[i])
            i += 1


class ControllerTestCase(TestCase):
    def setUp(self) -> None:
        self.agent = Controller(node='127.0.0.1')

    def test_single_task(self):
        with patch.object(BaseController, '_request', make_mocked_coro()) as request:
            self.agent.run_task(tasks.Hostname().get())
            request.assert_called()


@override_settings(REST_FRAMEWORK=modify_setting_permission())
class CustomExceptionMiddlewareTestCase(TestCase):
    def setUp(self) -> None:
        superuser = User.objects.create_superuser(username='super', password='superuser')
        self.client.force_login(superuser)

    def test_task_exception_can_return_409(self):
        with patch('deploy.views.Nodes.post') as mock_post:
            node = '127.0.0.1',
            mock_post.side_effect = TaskException(node, 'test_task_exception')
            resp = self.client.post('/deploy/nodes/', {'ip': node})
            self.assertContains(resp, '执行任务时出错', status_code=409, msg_prefix=str(resp.content))

    def test_request_exception_can_return_409(self):
        with patch('deploy.views.Nodes.post') as mock_post:
            node = '127.0.0.1',
            mock_post.side_effect = RequestAgentError(node, tasks.Hostname().get())
            resp = self.client.post('/deploy/nodes/', {'ip': node})
            self.assertContains(resp, '联系节点', status_code=409)

    def test_other_exception_can_return_500(self):
        with patch('deploy.views.Nodes.post') as mock_post:
            mock_post.side_effect = Exception('测试用未知错误')
            resp = self.client.post('/deploy/nodes/', )
            self.assertContains(resp, '未知错误', status_code=500)

    def test_assertException_can_return_400(self):
        with patch('deploy.views.Nodes.post') as mock_post:
            mock_post.side_effect = AssertionError('测试用断言错误')
            resp = self.client.post('/deploy/nodes/', )
            self.assertContains(resp, '断言错误', status_code=400)
