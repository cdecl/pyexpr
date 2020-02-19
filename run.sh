#!/bin/bash

cat name.txt | bin/parun -p 8 venv/bin/python pyexpr.py -v -f conf/tasks.yml -n
