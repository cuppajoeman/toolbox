#!/usr/bin/env bash
echo "Enter a command"
while true; do
    read -p "`echo $'> '`" c
    case $c in
        "quit" ) exit;;
        * ) convert guide_blank.png -gravity North -pointsize 80 -annotate +0+200 "$c" guide_text.png ;;
    esac
done

