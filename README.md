# Toadstool

Python load tools -- An opinionated solution for cleanly loading files directly into Python objects.

This library works by creating custom Python finders and loaders and injecting them into the Python meta search path.

The Python import system is explained in great detail [here](https://docs.python.org/3/reference/import.html#the-import-system).

## Usage

To use this module, simply `import toadstool` before any import you wish to use the included loaders for. This can be at the top of your source file or just before any imports for the supported filetypes.

## Loaders

<details>
  <summary>GraphQL</summary>

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
  <summary>JSON</summary>

Loads JSON objects using builtin `json` library. Nested JSON objects are converted to a namespace so that they can be retrieved using JavaScriopt-like dot (`.`) notation. For example, the following file `sample.json`

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

print(sample.employee.name)
> 'sonoo'
print(sample.menu.popup)
> namespace(menuitem=[{'value': 'New', 'onclick': 'CreateDoc()'}, {'value': 'Open', 'onclick': 'OpenDoc()'}, {'value': 'Save', 'onclick': 'SaveDoc()'}])
```

You also have the json root object available at `sample.json`:

```python
import toadstool
import sample

print(sample.json)
>{'employee': {'name': 'sonoo', 'salary': 56000, 'married': True}, 'menu': {'id': 'file', 'value': 'File', 'popup': {'menuitem': [{'value': 'New', 'onclick': 'CreateDoc()'}, {'value': 'Open', 'onclick': 'OpenDoc()'}, {'value': 'Save', 'onclick': 'SaveDoc()'}]}}}
```

</details>