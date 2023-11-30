#!/bin/bash

get_current_script_path_bash_source() {
  MY_PATH="$(dirname -- "${BASH_SOURCE[0]}")"            # relative
  MY_PATH="$(cd -- "$MY_PATH" && pwd)"    # absolutized and normalized
  if [[ -z "$MY_PATH" ]] ; then
    # error; for some reason, the path is not accessible
    # to the script (e.g. permissions re-evaled after suid)
    exit 1  # fail
  fi
  return "$MY_PATH"
}

get_current_script_path_first_arg() {
  echo "The script you are running has:"
  echo "basename: [$(basename "$0")]"
  echo "dirname : [$(dirname "$0")]"
  echo "pwd     : [$(pwd)]"
}

get_current_script_path_bash_source
get_current_script_path_first_arg
