#!/bin/bash

cd "$(dirname "$0")"

current_date=$(date +%Y-%m-%d)

array=(office garage upstairs basement livingroom)

for i in "${array[@]}"
do
    ### Check if a directory does not exist ###
    if [ ! -d "./$i" ] 
    then
        echo "Directory ./$i DOES NOT exists." 
        mkdir $i
    fi
    curl http://$i.temp.lan/history > ./$i/$current_date.json
    sleep 10
done
