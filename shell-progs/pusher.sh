#!/usr/bin/env bash
# Declare an array of string with type
declare -a StringArray=("~/knowledge-book" "~/basic-system" )
 
# Iterate the string array using for loop
for val in ${StringArray[@]}; do
   cd $val
   git add -A && git commit -m "this was an automated push" && git push
done

#cd ~/knowledge-book
#git add -A && git commit -m "this was an automated push" && git push
