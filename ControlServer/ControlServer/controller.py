"""连接节点，发送请求"""
from typing import List
import logging
import aiohttp
import asyncio

from . import errors
from .utils import is_ok
from django.conf import settings
from .constant import *

logger = logging.getLogger('control_server')


class AgentTask:
    path = ''
    method = None
    format_type = 'json'

    def __init__(self, raise_exc=True, **kwargs):
        self.raise_exc = raise_exc
        self.kwargs = kwargs
        self.name = None
        self.data = None
        self.params = None

    def __str__(self):
        return "name: {0}, method: {1}, path: {2}".format(self.name, self.method, self.path)


class BaseController:
    _loop = None

    def __init__(self):
        if not BaseController._loop:
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
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
        async with session.request(task.method, url=self.gen_node_agent_url(node, task.path), json=task.data,
                                   params=task.params, **task.kwargs) as resp:
            status_ok = is_ok(resp.status)
            if status_ok:
                if task.format_type == 'json':
                    val = await resp.json()
                else:
                    val = await resp.text()
                logger.debug('{0}: Request {1} agent {2} succeed'.format(resp.status, resp.method, resp.url))
            else:
                val = await resp.text()
                logger.error("{0}: Request {1} agent {2} failed, args: {4}. {3}".format(resp.status, resp.method, resp.url, val, task.data))
                if task.raise_exc:
                    raise errors.TaskException(node, task, val)
            result = Result(resp, val, status_ok, node, task)
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
    def __init__(self, node: str, return_exceptions=False):
        super().__init__()
        self.node = node
        self.return_exceptions = return_exceptions

    def run_tasks(self, request_tasks: List[AgentTask]):
        results = self.loop.run_until_complete(
            asyncio.gather(*self.make_single_node_multi_tasks(self.node, request_tasks),
                           return_exceptions=self.return_exceptions))
        multi_result = MultiTasksResult(results)
        return multi_result

    def run_task(self, request_task):
        return self.loop.run_until_complete(self.single_node_request(self.node, request_task))


class Controllers(BaseController):
    def __init__(self, nodes: List[str], return_exceptions=False):
        super().__init__()
        self.nodes = nodes
        self.return_exceptions = return_exceptions

    def make_multi_node_tasks(self, request_task):
        return [self.single_node_request(node, request_task) for node in self.nodes]

    def make_multi_node_multi_tasks(self, request_tasks: List[AgentTask]):
        tasks = []
        for node in self.nodes:
            node_tasks = self.make_single_node_multi_tasks(node, request_tasks)
            tasks += node_tasks
        return tasks

    def run_tasks(self, request_tasks: List[AgentTask]):
        return self.loop.run_until_complete(
            asyncio.gather(*self.make_multi_node_multi_tasks(request_tasks), return_exceptions=self.return_exceptions))

    def run_task(self, request_task):
        return self.loop.run_until_complete(
            asyncio.gather(*self.make_multi_node_tasks(request_task), return_exceptions=self.return_exceptions))

    def add_node(self, node):
        self.nodes.append(node)

    def add_nodes(self, nodes):
        self.nodes = self.nodes + nodes


class SingTaskResults:
    def __init__(self):
        self.succ_list = []
        self.fail_list = []


class Result:
    def __init__(self, resp: aiohttp.ClientResponse, val, ok, node, task: AgentTask):
        self.status_code = resp.status
        self.val = val
        self.node = node
        self.url = resp.url
        self.method = resp.method
        self.task = task
        self.ok = ok

    def __repr__(self):
        return "{2} {3}, result: {0} '{1}'".format(self.status_code, self.val, self.node, self.task.path)

    def __str__(self):
        return "{2} {3}, result: {0} '{1}'".format(self.status_code, self.val, self.node, self.task.path)


class SingleNodeMultiTasksResult:
    def __init__(self, is_all_succ=None):
        self.is_all_succ = is_all_succ


class MultiTasksResult:
    def __init__(self, results: List[Result]):
        self.results = results

    def _analyze_results(self):
        succ_list = []
        failed_list = []
        status = None
        for result in self.results:
            if result.ok:
                succ_list.append(result)
            else:
                failed_list.append(result)
        if succ_list == len(self.results):
            status = ALL_SUCCESS
        elif succ_list and failed_list:
            status = PART_SUCCESS
        elif failed_list == len(self.results):
            status = ALL_FAILED
        return succ_list, failed_list, status

    def __iter__(self):
        return iter(self.results)

    def __getitem__(self, item):
        return self.results[item]
