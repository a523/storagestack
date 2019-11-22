from ControlServer.controller import AgentTask


class Hostname(AgentTask):
    path = 'hostname'

    def get(self):
        self.method = 'get'
        self.format_type = 'text'
        self.name = 'get hostname'
        return self


class SSHKey(AgentTask):
    path = 'ssh-key'

    def append(self, data):
        self.method = 'post'
        self.format_type = 'text'
        self.name = 'generate ssh key'
        self.data = data
        return self


class Hosts(AgentTask):
    path = 'hosts'

    def update(self, data):
        # 追加hostname 如果有， 不追加，幂等性
        self.method = 'put'
        self.format_type = 'text'
        self.name = 'update hosts'
        self.data = data
        return self