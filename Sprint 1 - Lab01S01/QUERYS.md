<h1 align="center">
    <span href="">Laboratório de Experimentação de Software</span>
</h1>

### :dart: Consultas GraphQL 

### :one: Sistemas populares são maduros/antigos?
 - Métrica: idade do repositório (calculado a partir da data de sua criação).
```sh
{
  search(query: "stars:>100", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        nameWithOwner
        url
        createdAt
      }
    }
  }
}
```

### :two: Sistemas populares recebem muita contribuição externa?
 - Métrica: total de pull requests aceitas.

```sh
{
  search(query: "stars:>100", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        nameWithOwner
        url
        pullRequests(states: MERGED) {
          totalCount
        }
      }
    }
  }
}
```

### :three: Sistemas populares lançam releases com frequência?
 - Métrica: total de releases.

```sh
{
  search(query: "stars:>100", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        nameWithOwner
        url
        releases {
          totalCount
        }
      }
    }
  }
}
```

### :four: Sistemas populares são atualizados com frequência?
 - Métrica: tempo até a última atualização (calculado a partir da data de última atualização).

```sh
{
  search(query: "stars:>100", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        nameWithOwner
        url
        updatedAt
      }
    }
  }
}
```

### :five: Sistemas populares são escritos nas linguagens mais populares (Links para um site externo.)?
 - Métrica: linguagem primária de cada um desses repositórios.

```sh
{
  search(query: "stars:>100", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        nameWithOwner
        url
       	primaryLanguage {
          name
        }
      }
    }
  }
}
```

### :six: Sistemas populares possuem um alto percentual de issues fechadas?
 - Métrica: razão entre número de issues fechadas pelo total de issues.

```sh
{
  search(query: "stars:>100", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        nameWithOwner
        url
       	totIssuesClosed: issues(states: CLOSED) {
          totalCount
        }
        totIssues: issues {
          totalCount
        }
      }
    }
  }
}
```
- Fazer a razão entre as variáveis totIssuesClosed e totIssues para sabermos se possuem alto percentual de issues fechadas.

### :seven: Sistemas escritos em linguagens mais populares recebem mais contribuição externa, lançam mais releases e são atualizados com mais frequência?

```sh
  search(query: "starts:>100", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        nameWithOwner
        url
        updatedAt
       	pullRequests(states: MERGED) {
          totalCount
        }
        releases {
          totalCount
        }
      }
    }
  }
}
```

### :busts_in_silhouette: Alunos

- Matheus Santos Rosa Carneiro.
- Raíssa Carolina Vilela da Silva.
- Vitor Augusto Alves de Jesus.

### :bust_in_silhouette: Professor responsável

- Jose Laerte Pires Xavier Junior.

<h4 align="center"> 
	🚧  Spring 1 🚀 Finalizada...  🚧
</h4>
