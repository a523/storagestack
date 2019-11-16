"""连接节点，发送请求"""
from typing import List
from .utils import is_ok
from django.conf import settings
import aiohttp
import asyncio


class AgentTask:
    path = ''
    method = None
    format_type = 'json'

    def __init__(self, task_key=None, **kwargs):
        self.task_key = task_key
        self.kwargs = kwargs


class Hostname(AgentTask):
    path = 'hostname'


class GetHostname(Hostname):
    method = 'get'
    format_type = 'text'


class BaseController:
    _loop = None

    def __init__(self):
        if not BaseController._loop:
            BaseController._loop = asyncio.get_event_loop()
        self.loop = BaseController._loop

    @staticmethod
    def gen_node_agent_url(ip, path):
        try:
            scheme = settings.AGENT_SCHEME
            port = settings.AGENT_PORT
        except AttributeError:
            scheme = 'http'
            port = '8600'
        url = "{scheme}://{ip}:{port}/{path}".format(scheme=scheme, ip=ip, port=port, path=path)
        return url

    async def _request(self, session, node, task):
        async with session.request(task.method, url=self.gen_node_agent_url(node, task.path),
                                   **task.kwargs) as resp:
            status_ok = is_ok(resp.status)
            if status_ok and task.format_type == 'json':
                val = await resp.json()
            else:
                val = await resp.text()
            result = Result(resp, val, status_ok, node, task.path)
            return result

    async def single_node_request(self, node, request_task):
        async with aiohttp.ClientSession() as session:
            result = await self._request(session, node, request_task)
            return result

    def make_single_node_multi_tasks(self, node, request_tasks):
        tasks = []
        for task in request_tasks:
            tasks.append(self.single_node_request(node, task))
        return tasks


class Controller(BaseController):
    def __init__(self, node: str):
        super().__init__()
        self.node = node

    def run_tasks(self, request_tasks: List[AgentTask]):
        return self.loop.run_until_complete(
            asyncio.gather(*self.make_single_node_multi_tasks(self.node, request_tasks)))

    def run_task(self, request_task):
        return self.loop.run_until_complete(self.single_node_request(self.node, request_task))


class Controllers(BaseController):
    def __init__(self, nodes: List[str]):
        super().__init__()
        self.nodes = nodes

    def make_multi_node_tasks(self, request_task):
        return [self.single_node_request(node, request_task) for node in self.nodes]

    def make_multi_node_multi_tasks(self, request_tasks: List[AgentTask]):
        tasks = []
        for node in self.nodes:
            node_tasks = self.make_single_node_multi_tasks(node, request_tasks)
            tasks += node_tasks
        return tasks

    def run_tasks(self, request_tasks: List[AgentTask]):
        return self.loop.run_until_complete(asyncio.gather(*self.make_multi_node_multi_tasks(request_tasks)))

    def run_task(self, request_task):
        return self.loop.run_until_complete(asyncio.gather(*self.make_multi_node_tasks(request_task)))


class SingTaskResults:
    def __init__(self):
        self.succ_list = []
        self.fail_list = []


class Result:
    def __init__(self, resp: aiohttp.ClientResponse, val, is_ok, node=None, path=None):
        self.status_code = resp.status
        self.val = val
        self.node = node
        self.path = path
        self.url = resp.url
        self.is_ok = is_ok

    def __repr__(self):
        return "{2} {3}, result: {0} '{1}'".format(self.status_code, self.val, self.node, self.path)

    def __str__(self):
        return "{2} {3}, result: {0} '{1}'".format(self.status_code, self.val, self.node, self.path)
