"""连接节点，发送请求"""
from typing import List
from ControlServer.utils import is_ok
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


class Controller:
    _loop = None

    def __init__(self):
        if not Controller._loop:
            Controller._loop = asyncio.get_event_loop()
        self.loop = Controller._loop

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


class SingTaskResults:
    def __init__(self):
        self.succ_list = []
        self.fail_list = []


class Result:
    def __init__(self, status, val, error, node=None):
        self.status = status
        self.val = val
        self.error = error
        self.node = node


class MulController(Controller):
    def __init__(self, nodes):
        super().__init__()
        self.nodes = nodes

    async def _request(self, session, node, task, ):
        async with session.request(task.method, url=self.gen_node_agent_url(node, task.path),
                                   **task.kwargs) as resp:
            if task.task_key:
                task_result.setdefault(task.task_key, ([], []))
            if is_ok(resp.status):
                val = await resp.json()
                if task.task_key:
                    task_result[task.task_key][0].append({node: val})
            else:
                val = await resp.text()
                if task.task_key:
                    task_result[task.task_key][1].append({node: val})

    async def mul_tasks(self, *request_tasks):
        tasks = []
        for node in self.nodes:
            async with aiohttp.ClientSession() as session:
                for task in request_tasks:
                     tasks.append(self._request(session, node, task))
        return tasks


    async def _run_task(self, task):
        res = ([], [])
        for node in self.nodes:
            async with aiohttp.ClientSession() as session:

                async with session.request(task.method, url=self.gen_node_agent_url(node, task.path),
                                           **task.kwargs) as resp:
                    if is_ok(resp.status):
                        val = await resp.json()
                        if task.task_key:
                            res[0].append({node: val})
                    else:
                        val = await resp.text()
                        if task.task_key:
                            res[1].append({node: val})
        return res

    def mul_async_request(self, *request_tasks):
        self.loop.run_until_complete(asyncio.gather(self.mul_tasks(*request_tasks)))


result = {
    "hostname": ([
                     {"192.168.0.1": 'ceph-node1'},
                     {"192.168.0.2": 'ceph-node2'},
                 ],
                 [{"192.168.0.3": 'ceph-node3'}]
    ),
    "other_task": ([], [])
}
