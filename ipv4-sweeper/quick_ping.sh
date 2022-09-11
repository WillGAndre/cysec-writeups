#!/bin/bash

IFCFG=$(ifconfig $1 | grep -w 'inet')
ADDR=$(echo $IFCFG | awk '{print $2}' | awk -F '.' '{print $1,$2,$3"."}' OFS='.')

for host in $(eval echo {$2..$3});
do
    f=""$ADDR$host
    if ping -t 1 -c 1 $f | grep "from" >/dev/null; then
        echo $f" active"
    fi
done

