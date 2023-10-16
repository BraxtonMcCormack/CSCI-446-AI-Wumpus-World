#! /bin/bash

for cave in *.cave;
    do python test_cave.py $cave;
done;