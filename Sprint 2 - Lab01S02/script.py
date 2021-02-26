import requests
import time
import constant
from datetime import datetime
from dateutil import relativedelta
import os
import os.path


def run_github_query(query):
    request = requests.post(f'{constant.URL}', json=query, headers=constant.HEADERS)
    while request.status_code != 200:
        print("Error calling the API, processing again...")
        print(f'The query failed: {request.status_code}. {json["query"]}, {json["variables"]}')
        time.sleep(2)
        request = requests.post(f'{constant.URL}', json=query, headers=constant.HEADERS)
    return request.json()


def csv_header():
    path = os.getcwd() + "\\" + constant.PATH_CSV
    with open(path, 'w+') as csv_final:
        csv_final.write("Name" + ";"
                        + "URL" + ";"
                        + "Created At" + ";"
                        + "Repository Age" + ";"
                        + "Updated At" + ";"
                        + "Amount of stars" + ";"
                        + "Total amount of pull request(s)" + ";"
                        + "Total amount of release(s)" + ";"
                        + "Primary Language" + ";"
                        + "Total amount issues" + ";"
                        + "Total amount closed issues" + ";"
                        + "Ratio between total amount issues and total amount closed issues (%) \n")


def export_to_csv(data):
    path = os.getcwd() + "\\" + constant.PATH_CSV
    for node in data:
        if node['primaryLanguage'] is None:
            primary_language = "None"
        else:
            primary_language = str(node['primaryLanguage']['name'])

        date_pattern = "%Y-%m-%dT%H:%M:%SZ"
        datetime_now = datetime.now()
        datetime_created_at = datetime.strptime(node['createdAt'], date_pattern)
        datetime_updated_at = datetime.strptime(node['updatedAt'], date_pattern)
        repository_age = relativedelta.relativedelta(datetime_now, datetime_created_at).years

        closed_issues = node['totIssuesClosed']['totalCount']
        total_issues = node['totIssues']['totalCount']

        if total_issues == 0:
            closed_issues_ratio = "-"
        else:
            closed_issues_ratio = str("{0:.2f}".format(closed_issues / total_issues * 100))

        with open(path, 'a+') as csv_final:
            csv_final.write(node['nameWithOwner'] + ";" +
                            node['url'] + ";" +
                            datetime_created_at.strftime('%d/%m/%y %H:%M:%S') + ";" +
                            str(repository_age) + ";" +
                            datetime_updated_at.strftime('%d/%m/%y %H:%M:%S') + ";" +
                            str(node['stargazers']['totalCount']) + ";" +
                            str(node['pullRequests']['totalCount']) + ";" +
                            str(node['releases']['totalCount']) + ";" +
                            primary_language + ";" +
                            str(total_issues) + ";" +
                            str(closed_issues) + ";" +
                            str(closed_issues_ratio) + "\n")


# The flag is responsible for replacing the cursor on the next page
finalQuery = constant.QUERY.replace("{AFTER}", "")

json = {
    "query": finalQuery, "variables": {}
}

# Run application first time
total_pages = 1
print(f'Page -> {total_pages}')
response = run_github_query(json)

current_final_cursor = response["data"]["search"]["pageInfo"]["endCursor"]
has_next_page = response["data"]["search"]["pageInfo"]["hasNextPage"]
nodes = response["data"]["search"]["nodes"]

# 5 repositories * 200 pages = 1000 repositories
while total_pages < 200 and has_next_page:
    total_pages += 1
    print(f'Page -> {total_pages}')
    next_query = constant.QUERY.replace("{AFTER}", ', after: "%s"' % current_final_cursor)
    json["query"] = next_query
    response = run_github_query(json)
    # Increase the output
    nodes += response["data"]["search"]["nodes"]
    # Changes to the next page
    has_next_page = response["data"]["search"]["pageInfo"]["hasNextPage"]
    # Changes the cursor to the current
    current_final_cursor = response["data"]["search"]["pageInfo"]["endCursor"]

if __name__ == "__main__":
    csv_header()
    export_to_csv(nodes)
    print('#' * 100)
    print('\nSuccessfully generated csv file...')
