from contextlib import AbstractContextManager, ContextDecorator
import re
import sys
from toadstool.loaders.base_loader import Loader
from toadstool import loaded

def identifier(var_str):
    """Create a valid identifier from a string

    See https://stackoverflow.com/a/3305731
    """
    return re.sub(r"\W|^(?=\d)", "_", var_str)

class ToadContext(AbstractContextManager,ContextDecorator):
    """
    Context Manager to allow imports with toadstool loaders without permanently changing the sys.meta_path

    This context manager does not yield anything, so the proper usage is:

    with ToadContext(Loader | list(Loaders)):
        import my_module

    Reference https://docs.python.org/3/library/stdtypes.html#typecontextmanager
    """
    def __init__(self, loaders: Loader | list[Loader] = None) -> None:
        """
        Initialized the ToadContext

        Args:
            loaders (Loader | list[Loader], optional): List of Loaders or a single Loader.
                If this parameter is None, all loaders will be used. Defaults to None.
        """
        if loaders is None:
            loaders = loaded
        elif issubclass(loaders, Loader):
            loaders = [loaders]
        elif not isinstance(loaders,list):
            raise(ValueError(loaders), "Must be a list of Loaders or a Loader")
        self._loaders = loaders

    def __enter__(self):
        for loader in self._loaders:
            if loader not in sys.meta_path:
                sys.meta_path.append(loader)

    def __exit__(self,ex_type, ex_value, ex_traceback):
        sys.meta_path = [path for path in sys.meta_path if path not in self._loaders]
        return False