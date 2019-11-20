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


class Hostname(AgentTask):
    path = 'hostname'

    def get(self):
        self.method = 'get'
        self.format_type = 'text'
        self.name = 'get hostname'


class SSHKey(AgentTask):
    path = 'ssh-key'

    def generate(self):
        self.method = 'post'
        self.format_type = 'text'
        self.name = 'generate ssh key'


class Hosts(AgentTask):
    path = 'hosts'

    def update(self, data):
        # 追加hostname 如果有， 不追加，幂等性
        self.method = 'put'
        self.format_type = 'text'
        self.name = 'update hosts'
        self.data = data

