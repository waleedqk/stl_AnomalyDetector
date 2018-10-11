#!/bin/bash


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT_DIR=$(dirname "$SCRIPT_DIR")


FILE_LIST=(
    commit_git.bash
    README.md
    always.g4
    expressions.g4
    stlgrammar.g4
)

git add $SCRIPT_DIR/"${FILE_LIST[@]}"
git commit -m "stlgrammar.g4 first commit, New AST strategy for Until only tree"
git push origin master	