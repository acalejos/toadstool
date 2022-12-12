import re
import sys
from toadstool.loaders.base_loader import Loader

def identifier(var_str):
    """Create a valid identifier from a string

    See https://stackoverflow.com/a/3305731
    """
    return re.sub(r"\W|^(?=\d)", "_", var_str)

class ToadContext:
    """
    Context Manager to allow imports with toadstool loaders without permanently changing the sys.meta_path

    This context manager does not yield anything, so the proper usage is:

    with ToadContext(Loader | list(Loaders)):
        import my_module
    """
    def __init__(self, loaders: Loader | list[Loader] = None) -> None:
        if loaders is None:
            loaders = []
        elif issubclass(loaders, Loader):
            print("Is subclass")
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