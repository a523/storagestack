class AgentError(Exception):
    pass


class ExecuteCommandError(AgentError):
    pass


class ScriptConfigError(ExecuteCommandError):
    pass
