from django.test import TestCase
from deploy.models import Nodes


class NodesTestCase(TestCase):
    def setUp(self) -> None:
        Nodes.objects.create(ip='127.0.0.1')

    def test_nodes_have_time(self):
        node = Nodes.objects.get(ip='127.0.0.1')
        self.assertIsNotNone(node.created_time)
