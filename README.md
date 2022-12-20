# Toadstool

Python load tools -- An opinionated solution for cleanly loading files directly into Python objects.

This library works by creating custom Python finders and loaders and injecting them into the Python meta search path.

The Python import system is explained in great detail [here](https://docs.python.org/3/reference/import.html#the-import-system).

Consider a `json` file `sample.json`

```json
{
    "employee": {
        "name":       "sonoo",
        "salary":      56000,
        "married":    true
    },
    "menu": {
        "id": "file",
        "value": "File",
        "popup": {
          "menuitem": [
            {"value": "New", "onclick": "CreateDoc()"},
            {"value": "Open", "onclick": "OpenDoc()"},
            {"value": "Save", "onclick": "SaveDoc()"}
          ]
        }
      }
}
```

can be loaded and used in the following way:

```python
import toadstool
import sample

# Or import using ToadContext
from toadstool.utils.utils import ToadContext
from toadstool.loaders.json_loader import JsonLoader
with ToadContext(JsonLoader):
  import sample

>>> sample.
sample.employee  sample.json      sample.menu
print(sample.menu)
> {'id': 'file', 'value': 'File', 'popup': {'menuitem': [{'value': 'New', 'onclick': 'CreateDoc()'}, {'value': 'Open', 'onclick': 'OpenDoc()'}, {'value': 'Save', 'onclick': 'SaveDoc()'}]}}
```

## Requirements

Requires Python 3.10

## Install

### Basic Install

`$ python3 -m pip install toadstool`

### Advanced Install

`$ python3 -m pip install toadstool[options]`
Where `options` are any of the following (or combinations thereof):

* `toml` For `.toml` support using `toml` library for Python versions prior to `Python 3.11`, which introduced `tomllib` into the standard library
* `yaml` For `.yaml` support using `PyYaml`
* `gql` For `.gql` or `.graphql` query support using `graphql-core` library

## Usage

To use this module, simply `import toadstool` before any import you wish to use the included loaders for. This can be at the top of your source file or just before any imports for the supported filetypes.

## Loaders

<details>
  <summary>GraphQL (.gql | .graphql)</summary>

Load graphql queries directly as graphql.language.ast.DocumentNode objects from the [GraphQL Core Library](https://github.com/graphql-python/graphql-core/tree/main/src/graphql).  Allows direct importing of queries/mutations/subscriptions/fragments (aka GraphQL operations).

Example:

Given a GraphQL query file names `queries.graphl` or `queries.gql` with the following contents:

```graphql
query HeroComparison($first: Int = 3) {
  leftComparison: hero(episode: EMPIRE) {
    ...comparisonFields
  }
  rightComparison: hero(episode: JEDI) {
    ...comparisonFields
  }
}

fragment comparisonFields on Character {
  name
  friendsConnection(first: $first) {
    totalCount
    edges {
      node {
        name
      }
    }
  }
}

mutation CreateReviewForEpisode($ep: Episode!, $review: ReviewInput!) {
  createReview(episode: $ep, review: $review) {
    stars
    commentary
  }
}
```

then you can import the contents of the file either as a whole module:

```python
import queries
print(queries.__dict__)

>
{'__name__': 'queries', '__doc__': None, '__package__': '', '__loader__': GqlImporter('queries.gql'), '__spec__': ModuleSpec(name='queries', loader=GqlImporter('queries.gql')), 'HeroComparison': DocumentNode, 'operations': {'HeroComparison': DocumentNode}, '__file__': 'queries.gql'}
```

or using specific query names:

```python
from queries import HeroComparison
print(HeroComparison.definitions)

> (OperationDefinitionNode at 0:180, FragmentDefinitionNode at 182:339)
```

Also tracks all operations in a module dict as `queries.operations`

</details>

<details>
  <summary>JSON (.json)</summary>

Loads JSON objects using builtin `json` library. The top-level JSON keys are stored as attirbutes for the module and the whole `json` converted `dict` is stored as `imported_name.json` For example, the following file `sample.json`

```json
{
    "employee": {
        "name":       "sonoo",
        "salary":      56000,
        "married":    true
    },
    "menu": {
        "id": "file",
        "value": "File",
        "popup": {
          "menuitem": [
            {"value": "New", "onclick": "CreateDoc()"},
            {"value": "Open", "onclick": "OpenDoc()"},
            {"value": "Save", "onclick": "SaveDoc()"}
          ]
        }
      }
}
```

can be loaded and used in the following way:

```python
import toadstool
import sample

>>> sample.
sample.employee  sample.json      sample.menu
print(sample.menu)
> {'id': 'file', 'value': 'File', 'popup': {'menuitem': [{'value': 'New', 'onclick': 'CreateDoc()'}, {'value': 'Open', 'onclick': 'OpenDoc()'}, {'value': 'Save', 'onclick': 'SaveDoc()'}]}}
```

You also have the json root object available at `sample.json`:

```python
import toadstool
import sample

print(sample.json)
>{'employee': {'name': 'sonoo', 'salary': 56000, 'married': True}, 'menu': {'id': 'file', 'value': 'File', 'popup': {'menuitem': [{'value': 'New', 'onclick': 'CreateDoc()'}, {'value': 'Open', 'onclick': 'OpenDoc()'}, {'value': 'Save', 'onclick': 'SaveDoc()'}]}}}
```

</details>

<details>
  <summary>TOML (.toml)</summary>

  Loads TOML files such that each top-level table becomes an attribute of the imported module. Also loads the whole TOML file as a dictionary under the `toml` attirbute (which will overwrite any table from the file with the name `toml` as well). For example, if you have `example.toml` with the following contents:

  ```toml
  [project]
  name = 'Toadstool'
  description = 'Python Load Tools Suite'
  readme = 'README.md'
  requires-python = "~=3.10"
  license = { file = 'LICENSE' }
  version = '0.1.0'
  authors = [{ name = 'Andrés Alejos', email = 'acalejos@proton.me' }]
  classifiers = [
      'License :: OSI Approved :: MIT Licens',
      'Programming Language :: Python :: 3',
      'Topic :: Software Development',
      'Topic :: Utilities',
  ]
  keywords = ["import", "loader", "meta", "sys"]
  urls = { Home = "https://github.com/acalejos/toadstool" }

  [project.optional-dependencies]
  gql = ['graphql_core>=3.2.3']
  yaml = ['pyyaml >= 5.3.1']
  toml = ['toml >= 0.10.2;python_version < "3.11"']
  all = ['toadstool[gql]', 'toadstool[yaml]', 'toadstool[toml]']

  [sample]
  name = 'Sample'

  [[Root]]
  name = 'Root'
  ```

  can be loaded and used in the following way:

```python
import toadstool
import example

>>> example.
example.Root     example.project  example.sample   example.toml
```

</details>

<details>
  <summary>YAML (.yaml | .yml)</summary>

  Loads a YAML file, assigning each top-level key as a module attribute (similar to the JSON loader). Also loads the whole YAML definition as a `dict` into the `yaml` attirbute. If the YAML file has more than 1 YAML definition (which is legal within the YAML definition), then only the `yaml` attribute is set, and is a `list[dict]`. Suppose you have a YAML file called `sample.yaml` with the following contents:

```yaml
document: 1
name: 'erik'
```

then you could do the following:

```python
import toadstool
import sample

>>> sample.
sample.document sample.name sample.yaml
```

and suppose you had a similar multifile YAML file:

```yaml
document: 1
name: 'erik'
---
document: 2
name: 'config'
```

then you could do the following:

```python
import toadstool
import sample

>>> sample.
sample.yaml
```

</details>

<details>
  <summary>Config (.ini | .cfg | .config)</summary>

  Uses the `configparser` package from the standard library to load the file and assign any top-level key to the module's attribute, and the entire `ConfigParser` object to the `config` attribute. Suppose you have the following config file `sample.ini`:

  ```ini
  [http]
  port=8080
  username=httpuser
  [https]
  port=8043
  username=httpsuser
  [FTP]
  port=8043
  username=ftpuser
  [database]
  driverclass   = com.mysql.jdbc.Driver
  dbName        = mydatabase
  port          = 3306
  username      = root
  ```

  then you could do the following

  ```python
  import toadstool
  import sample

  >>> sample.
  sample.http  sample.https sample.FTP sample.database sample.config
  ```
</details>

<details>
  <summary>CSV (.csv)</summary>

Loads a CSV file and loads the contents into `rows` and `columns` attributes as `list[list[str]]`.  This will attempt to determine if the CSV contains a header as the first row, and will do the following according to that determination:

If Header:

* Creates attributes `named_rows` and `named_columns`
  * `named_columns`: Each column is a `dict` keyed on the column header and contains the whole column
  * `named_rows`: Each row contains a `dict` with each column entry keyed from its header to the value at that row.
* Populates each column name as an attribute name that will correspond to its respective column
* Populates an attribute `fieldnames` with the header values.

For any CSV:

* Creates a `rows` attirbute which contains a `list[list[str]]` with the CSV content rows (skips header if exists)
* Creates a `columns` attirbute which contains a `list[list[str]]` with the CSV content columns

Suppose you have a file called `sample.csv` with the following contents:

```csv
Index,Customer Id,First Name
1,DD37Cf93aecA6Dc,Sheryl
2,1Ef7b82A4CAAD10,Preston
3,6F94879bDAfE5a6,Roy
4,5Cef8BFA16c5e3c,Linda
5,053d585Ab6b3159,Joanna
```

then you can do the following:

```python
import toadstool
import sample

>>> sample.
sample.First_Name         sample.named_rows         sample.rows
sample.Index              sample.columns            sample.named_columns
sample.Customer_Id        sample.fieldnames
```

</details>

## ToadContext

Located in `toadstool.utils.utils`, ToadContext is a Context Manager to allow imports with `toadstool` loaders without permanently changing the `sys.meta_path`.  Using this, you can import your files the same way as you would using `import toadstool` from within a context without having to actually import `toadstool`. You must explicitly pass loaders you wish to use as arguments.

This context manager does not yield anything, so the proper usage is:

```python
with ToadContext(Loader | list(Loaders)):
    import my_module
```

## Limitations

Toadstool works by injecting the supported `Loader`s into the `sys.meta_path` during Toadstool's module init. The `sys.meta_path` is a list of class instances that contain the `find_spec` and `exec_module` methods. This occurs the first time that Toadstool is imported (upon `init` of Toadstool), after which `toadstool` is cached in the `sys.modules` data structure, which is what is checked when any module is referenced before deferring to the loaders in `sys.meta_path` and searching for the module. Therefore, after the first `import toadstool` that occurs per Python interpreter session, the module `__init__.py` might not be run again and thus if you do anything to alter the `sys.meta_path` after `import toadstool` then the `Loader`s may no longer be in the search path.

One possible solution is to use `importlib.reload(toadstool)` which reruns the module `__init__.py` code (only code not contained in `if __name__ == '__main__'` block).

Another possible solution is to use the `ToadContext` when you wish to import using the Toadstool `Loader`s, This could prove to be redundant, but it also ensures that the `sys.meta_path` is only altered while importing the modules that require `toadstool` and removes the `Loader`s upon existing the context.

## Contributing

Feel free to open feature requests for new features or simply supported file extensions. If you feel so inclined, you can also open up a pull request to merge in your own loader. Creating a new loader is very straight forwards and can be accomplished by:

* Creating a file in `toadstool/loaders` with the name `{filetype}_loader.py`
* Implementing a class that inherits from the `Loader` class located in `toadstool/loaders/base_loader`. Your class must implement the following:

  * Add a class attribute `file_exts` specifying your file extension(s) either as a `str` for a single extension or `list[str]` for multiple extensions. For example:

  ```python
  class CsvLoader(Loader):
    file_exts="csv"
  ```

  ```python
  class GqlLoader(Loader):
    file_exts=["gql","graphql"]
  ```

  * Define `def exec_module(self, module):` where your functionality will be implemented. This will typically look like updating the `module.__dict__` with values according to how you load the file
* If your loader has dependencies:
  * Specify a new optional dependency in `pyrpoject.toml` under `[project.optional-dependencies]`
  * Add your dependency to the `all` optional dependency by adding it as `toadstool[your_dep]`
* Add your loader to the list `all_loaders` in the root `__init__.py` file as a 3-tuple with:
  * Path to your module in dotted notation
  * Name of your loader class
  * Name of dependency from `pyrpoject.toml` if it exists or `None`

Refer to any of the existing loaders in `toadstool/loaders` for examples
