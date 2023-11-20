#!/bin/bash

sh ../bash/cd_to_script_path.sh

if ! command -v fzf &> /dev/null
then
    echo "fzf is not avaible on this system, please install it first"
    exit 1
fi

executable=$(find -name "*.sh" | fzf)

echo $executable selected, now provide arguments

read -p "args: " input_arguments

eval $executable "${input_arguments[@]}"
