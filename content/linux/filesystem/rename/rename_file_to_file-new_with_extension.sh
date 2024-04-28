#!/bin/bash
# renames a.x, b.y, c.z  to a-new.x, b-new.y, c-new.y
for i in ?.?; 
do
  p="${i%%.*}"; 
  s="${i##*.}"; 
  mv -n "$i" "$p-new.$s"; 
done 
