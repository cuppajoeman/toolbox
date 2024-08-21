#!/bin/bash
# after you've committed in your submodule:
( this=`git rev-parse --show-toplevel`
  while up=$(git -C "$this"/.. rev-parse --show-toplevel 2>&-)
  do
        cd "$this"/..
        git add ${this##*/}
        git commit -m "updating ${this#$up/}"
        this=$up
  done
)
