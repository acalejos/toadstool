from graphql import Source, parse
from graphql.utilities import separate_operations

from toadstool.utils.utils import identifier
from toadstool.loaders.base_loader import Loader

class GqlLoader(Loader):
    """
    Used to import GraphQL Query Files stored as .gql or .graphql files

    Adds all operations from the imported file into its namespace and
    adds a dict of operations to operation names. Each operation is
    mapped to its corresponding graphql.language.ast.DocumentNode

    Not to be used with schema files!
    """
    @classmethod
    def find_spec(cls, name, path, target=None):
        """Look for GQL file"""
        return super().find_spec(name,path,target,file_exts=["gql","graphql"])

    def exec_module(self, module):
        """Executing the module means reading the gql file"""
        with self.path.open() as f:
            source = Source(f.read(), "GraphQL request")
        ast = parse(source)
        operations = separate_operations(ast)
        fieldnames = tuple(identifier(key) for key in operations.keys())
        fields = dict(zip(fieldnames, operations.values()))
        module.__dict__.update(fields)
        module.__dict__["operations"] = operations
        super().exec_module(module)
