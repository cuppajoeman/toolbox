#!/bin/bash
find "." -name "*.tex" | xargs sed -e "s/\documentclass\[preview\]{standalone}/\documentclass{standalone}/g" 
