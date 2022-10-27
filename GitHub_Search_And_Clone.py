import requests
from git import Repo, rmtree
import os

class Cloner:
    def __init__(self):
        #rmtree("../Repository")
        response = requests.get('https://api.github.com/search/repositories?q=language:Cpp')
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
    # repos_info = cloner.get_repos_info()
    # for repo in repos_info:
    #     # clear text
    #     # print clone status
    #     print_str = ""
    #     before_current = True
    #     for repo2 in repos_info:
    #         if (repo.name == repo2.name):
    #             print_str += "Repo: " + repo.name + " cloning...."
    #             before_current = False
    #         elif before_current:
    #             print_str += "Repo: " + repo.name + " clone complete"
    #         else:
    #             print_str += "Repo: " + repo.name + " waiting...."
    #         cloner.cloneARepo(repo)
        
    #     # setText(print_str)  