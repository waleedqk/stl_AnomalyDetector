#!/bin/bash


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT_DIR=$(dirname "$SCRIPT_DIR")


FILE_LIST=(
    commit_git.bash
    README.md
    runme.bash
    always.g4
    stl_G.expr
    test_G.py
)

git add $SCRIPT_DIR/"${FILE_LIST[@]}"
git commit -m "Initial commit to expression grammar"
git push origin master	