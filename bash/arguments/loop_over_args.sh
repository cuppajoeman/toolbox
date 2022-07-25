#!/bin/bash

# iterate over all arguments
for var in "$@"
do
  echo "$var"
done

# All but last 
for x in "${@:1:$# - 1}" ; do 
  echo do something with "$x"
done
