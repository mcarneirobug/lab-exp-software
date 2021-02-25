import requests
import time
import constant
from datetime import datetime
from dateutil import relativedelta
import os
import os.path


def run_github_query(query):
    request = requests.post(f'{constant.URL}', json={'query': query}, headers=constant.HEADERS)
    while request.status_code == 502:  # reprocessing bad request
        time.sleep(2)
        return run_github_query(query)
    if request.status_code == 200:  # return valid json request
        return request.json()
    else:
        raise Exception(f'The query failed: {request.status_code}. {query}')


def export_to_csv(data):
    path = os.getcwd() + "\\" + constant.PATH_CSV
    with open(path, 'a+') as csv_final:
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

            with open(path, 'a+') as final_csv:
                final_csv.write(node['nameWithOwner'] + ";" +
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
initial_query = constant.QUERY.replace("{AFTER}", "")

# Run application first time
response = run_github_query(initial_query)
total_pages = 1

current_final_cursor = response["data"]["search"]["pageInfo"]["endCursor"]
has_next_page = response["data"]["search"]["pageInfo"]["hasNextPage"]
nodes = response["data"]["search"]["nodes"]

print("Page: ", total_pages)

while total_pages < 100 and has_next_page:
    total_pages += 1
    print("Page: ", total_pages)
    finalQuery = constant.QUERY.replace("{AFTER}", ', after: "%s"' % current_final_cursor)

    response = run_github_query(finalQuery)
    # Increase the output
    nodes += response["data"]["search"]["nodes"]
    # Changes to the next page
    has_next_page = response["data"]["search"]["pageInfo"]["hasNextPage"]
    # Changes the cursor to the current
    current_final_cursor = response["data"]["search"]["pageInfo"]["endCursor"]


export_to_csv(nodes)
print('#' * 50)
print('\nSuccessfully generated csv file...')
