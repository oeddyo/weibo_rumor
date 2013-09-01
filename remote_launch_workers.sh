#!/bin/bash


while read -r line
do
    array+=($line)
done < hostnames.txt

for ((i=0; i < ${#array[*]}; i++))
do
    echo "${array[i]}"
    ssh "${array[i]}"  nohup /.autofs/grad/grad_users/kx19/virtual_env/virtualenv-1.9.1/new_env/bin/python /grad/users/kx19/weibo_rumor/run_crawl_worker.py > /.freespace/rumor.log & 
done

