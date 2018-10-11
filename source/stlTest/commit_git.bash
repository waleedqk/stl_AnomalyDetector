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
    data.py
)

git add $SCRIPT_DIR/"${FILE_LIST[@]}"
git commit -m "Commit before meeting with Sebastian 11/10/2018. G(formula) generates code that can be run. "
git push origin master	