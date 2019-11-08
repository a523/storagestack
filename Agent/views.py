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
