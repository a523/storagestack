import requests
from rest_framework.views import APIView
from ControlServer import errors, utils
from deploy import models, ops
import aiohttp


def get_node_hostname(ip):
    url = utils.gen_node_agent_url(ip, path='hostname')
    resp = requests.get(url)
    if resp.ok:
        hostname = resp.text
    else:
        raise errors.RequestAgentError(resp, 'GET')
    return hostname


def append_hosts(node, line):
    """追加hosts文件"""
    url = utils.gen_node_agent_url(node, path='hostname')
    resp = requests.put(url, data=line)
    if resp.ok:
        ret = resp.text
    else:
        raise errors.RequestAgentError(resp, 'PUT')
    return ret


def add_ssh_key(node):
    """管理节点到ceph node 的免密钥"""
    pass


class Nodes(APIView):
    def post(self, request):
        """添加节点"""
        data = request.data
        # 验证数据
        node = data['ip']
        # deploy_client = DeployClient(node)
        # deploy_client.add_ssh_key()
        # deploy_client.get_hostname()
        # hostname = ops.get_hostname(node)
        #
        # ops.append_hosts_for_all()

        # models.Nodes()

        # async with aiohttp.ClientSession() as session:
        #     async with session.get('http://127.0.0.1/hostname') as resp:
        #         print(resp.status)
        #         print(await resp.text())


        # 免密钥
        # 更改hostname
        # 写数据库

