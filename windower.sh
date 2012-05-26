#!/bin/sh

sleep 20 # wait until desktop shows

cd ./windower
python windower.py > log_windower.txt 2>&1
