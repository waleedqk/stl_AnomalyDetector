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
    stl_checks.expr
    main.py
    grammarvisitor.py
    stl_listener.py
)

git add $SCRIPT_DIR/"${FILE_LIST[@]}"
git commit -m "STL grammar looks parses global stl expressions and output code.py (still needs to be tabulated properly)"
git push origin master	