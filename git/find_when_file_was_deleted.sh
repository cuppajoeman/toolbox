#!/bin/bash
# https://stackoverflow.com/questions/6839398/find-when-a-file-was-deleted-in-git
git log --diff-filter=D --summary | grep delete