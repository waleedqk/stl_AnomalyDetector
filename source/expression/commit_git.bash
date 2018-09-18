#!/bin/bash


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT_DIR=$(dirname "$SCRIPT_DIR")


FILE_LIST=(
    commit_git.bash
    README.md
    runme.bash
    exp_expressions.expr
    expressions.g4
    expression_visitor.py
    sample_expressions.expr
    test_expressions.py
)

git add $SCRIPT_DIR/"${FILE_LIST[@]}"
git commit -m "Initial commit to expression grammar"
git push origin master	