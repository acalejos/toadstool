from types import SimpleNamespace

def to_namespace(d):
    x = SimpleNamespace()
    _ = [setattr(x, k, to_namespace(v)) if isinstance(v, dict)
            else setattr(x, k, v) for k, v in d.items()]
    return x