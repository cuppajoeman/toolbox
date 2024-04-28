#!/bin/bash
if ! command -v $1 &> /dev/null
then
    echo $1 " is not available on this system, please install it first"
    exit 1
fi
