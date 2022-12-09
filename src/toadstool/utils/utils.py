import re
from types import SimpleNamespace

class NestedNamespace(SimpleNamespace):
    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, NestedNamespace(value))
            elif isinstance(value, list):
                self.__setattr__(key, map(NestedNamespace, value))
            else:
                self.__setattr__(key, value)

def to_namespace(d):
    x = SimpleNamespace()
    _ = [setattr(x, k, to_namespace(v)) if isinstance(v, dict)
            else setattr(x, k, v) for k, v in d.items()]
    return x

def identifier(var_str):
    """Create a valid identifier from a string

    See https://stackoverflow.com/a/3305731
    """
    return re.sub(r"\W|^(?=\d)", "_", var_str)