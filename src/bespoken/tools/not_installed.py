"""Helper class for optional dependencies."""


class NotInstalled:
    """
    This object is used for optional dependencies. If a dependency is not installed we
    replace the tool with this object. This allows us to give a friendly
    message to the user that they need to install extra dependencies.
    """

    def __init__(self, tool, dep, extra_instructions=""):
        self.tool = tool
        self.dep = dep

        msg = f"In order to use {self.tool} you'll need to install via:\n\n"
        msg += f"pip install 'bespoken[{self.dep}]' or uv pip install 'bespoken[{self.dep}]'\n"
        if extra_instructions:
            msg += f"\n{extra_instructions}"
        self.msg = msg

    def __getattr__(self, *args, **kwargs):
        raise ModuleNotFoundError(self.msg)

    def __call__(self, *args, **kwargs):
        raise ModuleNotFoundError(self.msg)