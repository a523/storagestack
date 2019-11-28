from django.test import TestCase
from ControlServer import exe
from ControlServer.controller import *
from deploy import tasks
from unittest import mock
from aiohttp.test_utils import make_mocked_coro, make_mocked_request, TestClient, ClientSession


class RunExeTestCase(TestCase):
    def test_run_cmd(self):
        ret = exe.run_cmd('pwd', cwd='/tmp')
        self.assertEqual(ret.returncode, 0)
        self.assertEqual(ret.stdout.strip(), '/tmp')


class MultiTasksResultTestCase(TestCase):
    def setUp(self) -> None:
        self.mock_result_1 = mock.create_autospec(Result)
        self.mock_result_2 = mock.create_autospec(Result)
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
        with mock.patch.object(BaseController, '_request', make_mocked_coro()) as request:
            self.agent.run_task(tasks.Hostname().get())
            request.assert_called()
