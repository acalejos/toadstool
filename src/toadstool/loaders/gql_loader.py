import pathlib
import re
import sys
from importlib.machinery import ModuleSpec
from graphql import Source, parse
from graphql.utilities import separate_operations

class GqlLoader():
    """
    Used to import GraphQL Query Files stored as .gql or .graphql files

    Adds all operations from the imported file into its namespace and
    adds a dict of operations to operation names. Each operation is
    mapped to its corresponding graphql.language.ast.DocumentNode

    Not to be used with schema files!
    """
    def __init__(self, gql_path):
        """Store path to GraphQL file"""
        self.gql_path = gql_path

    @classmethod
    def find_spec(cls, name, path, target=None):
        """Look for GQL file"""
        print(name)
        package, _, module_name = name.rpartition(".")
        gql_file_names = [f"{module_name}.gql",f"{module_name}.graphql"]
        directories = sys.path if path is None else path
        for filename in gql_file_names:
            for directory in directories:
                gql_path = pathlib.Path(directory) / filename
                if gql_path.exists():
                    return ModuleSpec(name, cls(gql_path))

    def create_module(self, spec):
        """Returning None uses the standard machinery for creating modules"""
        return None

    def exec_module(self, module):
        """Executing the module means reading the gql file"""
        with self.gql_path.open() as f:
            source = Source(f.read(), "GraphQL request")
        ast = parse(source)
        operations = separate_operations(ast)
        fieldnames = tuple(_identifier(key) for key in operations.keys())
        fields = dict(zip(fieldnames, operations.values()))
        module.__dict__.update(fields)
        module.__dict__["operations"] = operations
        module.__file__ = str(self.gql_path)

    def __repr__(self):
        """Nice representation of the class"""
        return f"{self.__class__.__name__}({str(self.gql_path)!r})"

def _identifier(var_str):
    """Create a valid identifier from a string

    See https://stackoverflow.com/a/3305731
    """
    return re.sub(r"\W|^(?=\d)", "_", var_str)
