#!/bin/bash


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT_DIR=$(dirname "$SCRIPT_DIR")


FILE_LIST=(
    commit_git.bash
    README.md
    runme.bash
    CommonLexerRules.g4
    stlgrammar.g4
    stl.expr
    main.py
    stlgrammarInterpreter.py
)

git add $SCRIPT_DIR/"${FILE_LIST[@]}"
git commit -m "Commit before Oct 10 meeting with Sebastian. New rules added: not formula , not prop. stlgrammarInterpreter.py to parse the simple formulas "
git push origin master	