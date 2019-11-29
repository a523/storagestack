class ControlServerError(Exception):
    """ControlServer 自定义错误基类"""
    pass


class RequestAgentError(ControlServerError):
    """转发请求给Agent时发生错误"""

    def __init__(self, node, task):
        super().__init__(node, task)
        self.node = node
        self.task = task

    def __str__(self):
        return "Failed to request {} agent for task '{}'.".format(self.node, self.task.name or self.task.path)


class TaskException(Exception):
    """任务在Node上执行时出错"""

    def __init__(self, node, task, raw_err=''):
        super().__init__(node, task)
        self.node = node
        self.task = task
        self.raw_err = raw_err  # 异常信息

    def __str__(self):
        return "Failed to execute task '{0}' on node {1}.{2}".format(self.task, self.node, " " + self.raw_err)
