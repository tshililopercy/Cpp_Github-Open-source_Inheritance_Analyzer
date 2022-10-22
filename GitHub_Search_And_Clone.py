import requests
from git import Repo
import os

def SearchForOpenSourceProjects():
    response = requests.get('https://api.github.com/search/repositories?q=language:Cpp')
    if response.status_code == 200:
        response_dict = response.json()
        CloneRepos(response_dict)
    else:
       print("The Search URL is Invalid")

def CloneRepos(response_dict):
    repos_dicts = response_dict['items']
    for repo in repos_dicts:
        name = repo['name']
        if name != "tensorflow":
          dir = ( "../Repository", name)
          Repositories = os.path.join(dir[0], dir[1])
          print(Repositories)
          Repo.clone_from(
          repo["clone_url"],
          Repositories,
          depth = 1
          )
    print("Done Cloning...")

if __name__ == '__main__':
    SearchForOpenSourceProjects()
    
