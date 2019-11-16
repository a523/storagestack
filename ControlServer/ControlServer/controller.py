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
            result = await resp.text()
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
        return self.loop.run_until_complete(asyncio.gather(*self.make_single_node_multi_tasks(self.node, request_tasks)))

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


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class SingTaskResults:
    def __init__(self):
        self.succ_list = []
        self.fail_list = []


class Result:
    def __init__(self, status_code, val, error, node=None):
        self.status_code = status_code
        self.val = val
        self.error = error
        self.node = node

    @property
    def status(self):
        return is_ok(self.status_code)




result = {
    "hostname": ([
                     {"192.168.0.1": 'ceph-node1'},
                     {"192.168.0.2": 'ceph-node2'},
                 ],
                 [{"192.168.0.3": 'ceph-node3'}]
    ),
    "other_task": ([], [])
}
