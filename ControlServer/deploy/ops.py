"""一些复杂的业务逻辑"""
from ControlServer.controller import Controllers, Controller
from . import tasks, models


def add_new_node(new_node):
    """
    把新的节点添加到管理系统中，需要做一些初始化操作，如添加密钥和同步hosts
    :return:
    """
    agent = Controller(new_node)
    # 免密钥 & 获取新节点hostname
    results = agent.run_tasks([tasks.Hostname().get(), tasks.SSHKey().generate()])

    new_node_hostname = results[0].val

    # 追加hostname
    all_nodes = models.Nodes.objects.values('ip').all()
    nodes_agents = Controllers([node['ip'] for node in all_nodes])
    results = nodes_agents.run_task(tasks.Hostname().get())

    hosts = [{'ip': new_node, 'hostname': new_node_hostname}]
    for result in results:
        if result.ok:
            hosts.append({'ip': result.node, 'hostname': result.val})

    nodes_agents.add_node(new_node)
    nodes_agents.run_task(tasks.Hosts().update(data=hosts))

    models.Nodes(ip=new_node).save()
