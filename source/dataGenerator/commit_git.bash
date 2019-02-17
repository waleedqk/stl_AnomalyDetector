#!/bin/bash


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT_DIR=$(dirname "$SCRIPT_DIR")


FILE_LIST=(
    commit_git.bash
    README.md
    dataGen.ipynb
    input_data.csv
)


git add $SCRIPT_DIR/"${FILE_LIST[@]}"
git commit -m "Generating data files with signal values for testing"
git push origin master	
