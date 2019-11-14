class ControlServerError(Exception):
    """ControlServer 自定义错误基类"""
    pass


class RequestAgentError(ControlServerError):
    def __init__(self, resp, method, args=None):
        super().__init__(resp, method, args)
        self.resp = resp
        self.method = method
        self.args = args

    def __str__(self):
        return "Failed to request agent ({0}: {1}), code: {2}, message: {3}, args: {4}".format(self.method
                                                                                               , self.resp.url,
                                                                                               self.resp.status_code,
                                                                                               self.resp.text,
                                                                                               self.args)
