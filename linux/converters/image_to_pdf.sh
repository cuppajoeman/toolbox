#!/bin/bash
if [ "$1" == "-h" ]; then
  echo "Usage: `basename $0` [input-file(s)] [output-file]"
  exit 0
fi
convert $1 -auto-orient $2