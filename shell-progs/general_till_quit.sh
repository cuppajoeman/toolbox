#!/usr/bin/env bash
echo "Enter a command"
while true; do
    read -p "`echo $'> '`" c
    case $c in
        "quit" ) exit;;
        * ) echo "Process command $c";;
    esac
done

