#!/usr/bin/env bash
# Declare an array of string with type
declare -a StringArray=("$HOME/knowledge-book" "$HOME/basic-system" )
 
# Iterate the string array using for loop
for val in ${StringArray[@]}; do
   cd $val
   git pull
done

#cd ~/knowledge-book
#git add -A && git commit -m "this was an automated push" && git push
