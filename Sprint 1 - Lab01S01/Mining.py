import requests


def get_query():
    query = """
     query github {
        search (query: "starts:>100", type:REPOSITORY, first:100) {
            nodes {
              ... on Repository {
                nameWithOwner
                url
                createdAt
              }
            }
        }
    }
    """
    return query


class Mining:
    def __init__(self, token):
        self.token = token
    
    def run_github_query(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'bearer {self.token}'
        }
        url = 'https://api.github.com/graphql'
        query = get_query()
        request = requests.post(f'{url}', json={'query': query}, headers=headers)
        if request.status_code == 200: # return valid json request
            return request.json()
        elif request.status_code == 502: # reprocessing bad request
            return self.run_github_query()
        else:
            raise Exception(f'The query failed: {request.status_code}. {query}')