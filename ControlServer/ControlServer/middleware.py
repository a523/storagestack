import logging
from django.conf import settings
from ControlServer import errors
from django.http.response import HttpResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('control_server' + '.' + __name__)


class CustomExceptionMiddleware(MiddlewareMixin):
    """处理全部视图函数未处理的异常"""

    def process_exception(self, request, exception):
        """视图函数发生异常时调用"""
        if isinstance(exception, errors.TaskException):
            logger.error("Error in handle {request}, {task}".format(request=request, task=exception))
            return HttpResponse("在节点\"{}\"上执行任务时出错：{}".format(exception.node, exception.raw_err), status=409)
        elif isinstance(exception, errors.RequestAgentError):
            logger.error("Error in handle {request}, {task}".format(request=request, task=exception))
            return HttpResponse("联系节点\"{}\"时出错".format(exception.node), status=409)
        elif isinstance(exception, AssertionError):
            logger.error("Error in handle {request}, {task}".format(request=request, task=exception))
            return HttpResponse("出错，请检查输入或环境，{}".format(exception), status=400)
        else:
            if not settings.DEBUG:
                return HttpResponse("未知错误, 请查看日志或联系作者: {}".format(exception), status=500)
            else:
                raise
