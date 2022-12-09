from dotenv import load_dotenv
import os
import requests
import read_nodes

load_dotenv()

TOKEN = os.getenv('GITHUB_TOKEN')

headers = {'Authorization': 'bearer {}'.format(TOKEN)}


def run_query(query):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed to run by returning code of {}. {}'.format(request.status_code, query))


query = '''
{{
    search(query: "{queryString}", type: REPOSITORY, first: 100) {{
        pageInfo {{
            startCursor
            hasNextPage
            endCursor
        }}
        repositoryCount
        nodes {{
            ... on Repository {{
                id
                nameWithOwner
                createdAt
                isPrivate
                primaryLanguage {{
                    name
                }}
            }}
        }}
    }}
}}
'''

afterQuery = '''
{{
    search(query: "{queryString}", type: REPOSITORY, first: 100, after: "{afterString}") {{
        pageInfo {{
            startCursor
            hasNextPage
            endCursor
        }}
        repositoryCount
        nodes {{
            ... on Repository {{
                id
                nameWithOwner
                createdAt
                isPrivate
                primaryLanguage {{
                    name
                }}
            }}
        }}
    }}
}}
'''

nodes = []

for year in range(2008, 2025):
    variables = {
        'queryString': 'language:ada created:{}'.format(year)
    }
    result = run_query(query.format(**variables))['data']['search']
    print(result)
    nodes.extend(result['nodes'])
    while result['pageInfo']['hasNextPage']:
        variables = {
            'queryString': 'language:ada created:{}'.format(year),
            'afterString': result['pageInfo']['endCursor']
        }
        result = run_query(afterQuery.format(**variables))['data']['search']
        print(result)
        nodes.extend(result['nodes'])

read_nodes.write_nodes(nodes)

print(len(nodes))
