#!/bin/bash
# Back up current directory
DATE=$(date +"%d-%b-%Y")
tar -zcvf BACKUP-$DATE.tgz .
