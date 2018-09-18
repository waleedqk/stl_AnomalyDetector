#!/bin/bash


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT_DIR=$(dirname "$SCRIPT_DIR")


FILE_LIST=(
    commit_git.bash
    README.md
    runme.bash
    expressions.g4
    expr_sample.expr
    all.expr
    main_expr.py
    expr_visitor.py
    expr_listener.py
)

git add $SCRIPT_DIR/"${FILE_LIST[@]}"
git commit -m "Initial commit to expression grammar"
git push origin master	