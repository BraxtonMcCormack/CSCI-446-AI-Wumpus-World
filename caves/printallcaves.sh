#! /bin/bash

for cave in *.cave;
    do python print-cave.py -c $cave -f ${cave%.cave}.png -g 'True' -s 'True';
done;