URL = 'https://api.github.com/graphql'
TOKEN = '8905a6d054459aed74c71e71ec640e0251f21269'
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'bearer {TOKEN}'
}
QUERY = """
{
    search(query:"stars:>100", type:REPOSITORY, first:10 {AFTER}){
        pageInfo {
            hasNextPage
            endCursor
        }
        nodes {
        ... on Repository {
                nameWithOwner
                url
                createdAt 
                updatedAt
                stargazers { totalCount }
                pullRequests(states: MERGED){ totalCount } 
                releases{ totalCount } 
                primaryLanguage{ name } 
                totIssues: issues{ totalCount } 
                totIssuesClosed: issues(states: CLOSED){ totalCount } 
            } 
        } 
    }
}
"""
PATH_CSV = 'output_github.csv'
