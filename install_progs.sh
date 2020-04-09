#!/usr/bin/env bash

progs=`cat progs.txt`
for prog in $progs;
do
	if [[ $(apt-cache search $prog) ]]; then
		echo "installing $prog"
		sudo apt install $prog
	else
		echo "wasn't able to find $prog"	
	fi
done

