#!/bin/bash
shopt -s extglob nullglob
files=(!(.git|cleaner.sh|*.tex|*.sty|*.pdf|output.txt|new.sh))

# ${#files[@]} is the number of entries in the file array
(( "${#files[@]}" > 0 )) && {
	printf 'files to be deleted:\n'
	printf '%s\n' "${files[@]}"
  # Ask for confirmation
  read -p "Are you sure? " -n 1 -r
  echo    # (optional) move to a new line
  if [[ $REPLY =~ ^[Yy]$ ]]
  then
    rm -- "${files[@]}"
  fi
}

