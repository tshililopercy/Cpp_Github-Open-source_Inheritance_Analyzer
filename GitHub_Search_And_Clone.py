import requests
from git import Repo
import os


def Clone():
   Repo.clone_from("https://github.com/grim-firefly/C-CPP-Project.git", "Repository", depth = 1)
   
if __name__ == '__main__':
    Clone()