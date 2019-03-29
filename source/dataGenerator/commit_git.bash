#!/bin/bash


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT_DIR=$(dirname "$SCRIPT_DIR")


FILE_LIST=(
    commit_git.bash
    README.md
    dataGen.ipynb
    dataGenerator.py
    timing_result.py
    plot_results.py
    input_data_1000.csv
    input_data.csv
    timing_results.csv
    requirements.txt
    runme.bash
    py_venv.md
)


git add $SCRIPT_DIR/"${FILE_LIST[@]}"
git commit -m "Plotting experimental results"
git push origin master	
