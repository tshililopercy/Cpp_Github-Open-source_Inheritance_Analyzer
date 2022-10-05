import requests
from git import Repo
import os

def Clone(Repository_URL):
   Response = requests.get(Repository_URL)
   if Response.status_code == 200:
        Repo.clone_from(Repository_URL, "../Repository", depth = 1)
   else:
       print("Invalid Repo URL")
if __name__ == '__main__':
    Clone("https://github.com/Frkncln/Cpp-Inheritance-.git")
    