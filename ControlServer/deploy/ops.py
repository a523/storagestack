"""一些复杂的业务逻辑"""
import os
from ControlServer.controller import Controllers, Controller
from ControlServer import exe
from ControlServer.constant import *
from . import tasks, models


def add_new_node(new_node):
    """
    把新的节点添加到管理系统中，需要做一些初始化操作，如添加密钥和同步hosts
    :return:
    """
    agent = Controller(new_node)
    # 免密钥 & 获取新节点hostname
    pub_key = get_pub_key()
    results = agent.run_tasks([tasks.Hostname().get(), tasks.SSHKey().append(pub_key)])

    new_node_hostname = results[0].val
    append_known_hosts(new_node)

    # 追加hostname
    all_nodes = models.Nodes.objects.values('ip').all()
    nodes_agents = Controllers([node['ip'] for node in all_nodes])
    results = nodes_agents.run_task(tasks.Hostname().get())

    hosts = [{'ip': new_node, 'hostname': new_node_hostname}]
    for result in results:
        if result.ok:
            hosts.append({'ip': result.node, 'hostname': result.val})

    nodes_agents.add_node(new_node)
    nodes_agents.run_task(tasks.Hosts().update(data={"hosts": hosts}))

    models.Nodes(ip=new_node).save()


def read_pub_key(file=PUB_KEY_FILE):
    if os.path.isfile(file):
        with open(file, 'r') as f:
            data = f.read()
            return data


def gen_pub_key():
    cmd = """ssh-keygen -t rsa -P "" -f ~/.ssh/id_rsa"""
    exe.run_cmd(cmd)


def get_pub_key():
    """如果有公钥读取， 没有生成"""
    key = read_pub_key()
    if key:
        return key
    else:
        gen_pub_key()
        return read_pub_key()


def append_known_hosts(ip):
    """
    把指定主机ip和公钥添加到known_hosts
    :param ip:
    :return:
    """
    exe.run_cmd("ssh-keygen -R {}".format(ip))
    exe.run_cmd("ssh-keyscan -t ecdsa {} >> {}".format(ip, KNOWN_HOSTS))
