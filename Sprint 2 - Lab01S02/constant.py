URL = 'https://api.github.com/graphql'
TOKEN = 'INSERT YOUR TOKEN HERE'
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'bearer {TOKEN}'
}
QUERY = """
{
    search(query:"stars:>100", type:REPOSITORY, first:5{AFTER}){
        pageInfo {
            startCursor
            endCursor
            hasNextPage
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
