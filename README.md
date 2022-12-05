# Toadstool

Python load tools -- An opinionated solution for cleanly loading files directly into Python objects.

## Modules

### GraphQL

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

>
(OperationDefinitionNode at 0:180, FragmentDefinitionNode at 182:339)
```

Also tracks all operations in a module dict as `queries.operations`