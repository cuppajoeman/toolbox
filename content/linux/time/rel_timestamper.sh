#!/usr/bin/env bash
# REL_TIMESTAMPER
# bookmarks times relative to the start of this program
echo " Starting timestamp/bookmark session === $(date) ===" > timestamps.txt
SECONDS=0
while true; do
    read -p "Enter a command `echo $'\n> '`" c
    case $c in
        [h]* ) duration=$SECONDS ; echo "Bookmarked at: $(($duration / 60)) minutes and $(($duration % 60)) seconds" | tee -a timestamps.txt;;
        [q]* ) exit;;
        * ) echo "Invalid command";;
    esac
done
