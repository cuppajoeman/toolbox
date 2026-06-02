#!/bin/bash

path_to_search=$1
search_query=$2

grep --color=always -Rn "$path_to_search" -e "$search_query"
