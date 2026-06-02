#!/bin/bash
for fullfile in *.pdf; do 
	filename=$(basename -- "$fullfile")
	extension="${filename##*.}"
	filename="${filename%.*}"
	pdftoppm "$fullfile" "$filename" -png
done
