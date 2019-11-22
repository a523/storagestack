import json
import falcon
from Agent.ops import deploy


class HelloViews:
    def on_get(self, req, resp):
        resp.body = "OK"
        resp.status = falcon.HTTP_200


class HostName:
    def on_get(self, req, resp):
        hostname = deploy.get_local_hostname()
        resp.body = hostname


class Hosts:
    def on_put(self, req, resp):
        """
        升级追加hosts文件， 该方法是幂等的，如果已经存在相同的记录不会重复新增，有冲突的记录会修改，无冲突的记录会保留
        """
        data = json.load(req.stream)
        hosts_list = data['hosts']
        ret = deploy.update_all_hosts(hosts_list)
        resp.body = json.dumps(ret)
        resp.status = falcon.HTTP_200


class SshKey:
    def on_post(self, req, resp):
        data = req.stream
        deploy.append_ssh_key(data)
