import sys
active_loaders = []
try:
    from gql_loader import GqlLoader
except ImportError:
    print("GQL Not Supported")
else:
    active_loaders.append(GqlLoader)

sys.meta_path += active_loaders