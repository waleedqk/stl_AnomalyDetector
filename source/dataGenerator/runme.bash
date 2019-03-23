#!/bin/bash


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT_DIR=$(dirname "$SCRIPT_DIR")

DATA_FILES=(
    input_data_1000.csv
    input_data_10000.csv
    input_data_100000.csv
    input_data_1000000.csv
    input_data_10000000.csv
)


#for j in "${DATA_FILES[@]}"
#do
#

cp input_data_10000000.csv input_data.csv
for i in {1..10}; do python3 runSTLcheck.py; done
# python3 stlgrammarInterpreter_plot.py

#done