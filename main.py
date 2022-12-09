from github import Github
from dotenv import load_dotenv
import time
import os
from tqdm import tqdm
from read_nodes import read_nodes

load_dotenv()

TOKEN = os.getenv('GITHUB_TOKEN')

g = Github(TOKEN, per_page=100, retry=1000)


def search_repositories(language):
    return g.search_repositories(query='language:{}'.format(language))


def search_commits(repository, keyword):
    return g.search_commits(query='repo:{} {}'.format(repository, keyword))


keywords = [      # from https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/kim-tse-2014.pdf
    'refactor',
    'clean-up',
    'rewrite',
    'restructure',
    'redesign',
    'move',
    'extract',
    'improve',
    'split',
    'reorganize',
    'rename'
]

repositories = [repository['nameWithOwner'] for repository in read_nodes()]

for keyword in tqdm(keywords):
    f = open('{}.csv'.format(keyword), 'a')
    for repo in tqdm(repositories, total=len(repositories)):
        print('searching {} for commits...'.format(repo))
        f.write('{}'.format(repo))
        commits = search_commits(repo, keyword)
        print('found {} total commits.'.format(commits.totalCount))
        for commit in commits:
            f.write(',{}'.format(commit.sha))
        f.write('\n')
        while g.get_rate_limit().search.remaining < 5:
            time.sleep(1)
    f.close()
