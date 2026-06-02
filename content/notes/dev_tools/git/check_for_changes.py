import os
from git import Repo

root_search_path = os.getcwd()

for rec_root, dirs, files in os.walk(root_search_path):

    if ".git" in dirs:
        rec_repo = Repo(rec_root)
        changed_files = [item.a_path for item in rec_repo.index.diff(None)]
        if changed_files != []:
            print("has changes: ", rec_root)

    path = rec_root.split(os.sep)
