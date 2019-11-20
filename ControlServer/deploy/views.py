import requests
from rest_framework.views import APIView
from ControlServer import errors, utils
from deploy import ops


class Nodes(APIView):
    def post(self, request):
        """添加节点"""
        data = request.data
        # 验证数据
        node = data['ip']
        ops.add_new_node(node)
