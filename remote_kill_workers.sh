#!/bin/bash


while read -r line
do
    array+=($line)
done < hostnames.txt

for ((i=0; i < ${#array[*]}; i++))
do
    echo "${array[i]}"
    ssh "${array[i]}"  pkill -9 -f weibo_rumor
done

