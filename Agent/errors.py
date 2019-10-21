import subprocess
import signal


class AgentError(Exception):
    pass


class ExecuteCommandError(AgentError):
    pass


class CalledProcessError(subprocess.CalledProcessError, ExecuteCommandError):
    """
    更详细的错误输出
    """
    def __str__(self):
        if self.returncode and self.returncode < 0:
            try:
                return "Command '%s' died with %r." % (
                    self.cmd, signal.Signals(-self.returncode))
            except ValueError:
                return "Command '%s' died with unknown signal %d." % (
                    self.cmd, -self.returncode)
        else:
            return "Command '%s' returned non-zero exit status %d. Detail: %s" % (
                self.cmd, self.returncode, self.stderr)


class TimeoutExpired(subprocess.TimeoutExpired, ExecuteCommandError):
    pass
