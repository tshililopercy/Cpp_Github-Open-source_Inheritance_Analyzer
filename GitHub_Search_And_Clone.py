import requests
from git import Repo
import os


def Clone(Repository_URL):
   Repo.clone_from(Repository_URL, "Repository", depth = 1)
   
if __name__ == '__main__':
    Clone()