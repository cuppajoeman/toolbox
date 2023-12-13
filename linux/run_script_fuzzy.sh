#!/bin/bash


if ! command -v fzf &> /dev/null
then
    echo "fzf is not available on this system, please install it first"
    exit 1
fi

executable=$(find $(dirname -- "${BASH_SOURCE[0]}") -name "*.sh" | fzf)

echo script: $executable selected

echo -------------------------
echo ------SCRIPT-SOURCE------
echo -------------------------
echo

cat $executable

echo
echo -------------------------
echo -------------------------
echo -------------------------

echo now provide arguments

read -a input_arguments -p "args: " 

echo $executable "${input_arguments[@]}"
sh $executable "${input_arguments[@]}"
