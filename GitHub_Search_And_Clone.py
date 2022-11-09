import requests
from git import Repo, rmtree
import os

class Cloner:
    def __init__(self):
        response = requests.get('https://api.github.com/search/repositories?q=language:Cpp&&per_page=100&page='+ str(1))
        self.repos_info = {}
        if response.status_code == 200:
            response_dict = response.json()
            self.repos_info = response_dict['items']
        else:
            raise Exception("Connection failed!")

    def get_repos_info(self):
        return self.repos_info

    def cloneARepo(self, repo):
        name = repo['name']
        dir = ( "../Repository", name)
        Repositories = os.path.join(dir[0], dir[1])
        print(Repositories)
        Repo.clone_from(
        repo["clone_url"],
        Repositories,
        depth = 1
        )

if __name__ == '__main__':
    cloner = Cloner()