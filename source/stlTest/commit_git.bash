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
)

git add $SCRIPT_DIR/"${FILE_LIST[@]}"
git commit -m "Test bed for stl grammar, to create the appropriate AST tree"
git push origin master	