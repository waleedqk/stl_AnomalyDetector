#!/bin/bash


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT_DIR=$(dirname "$SCRIPT_DIR")


FILE_LIST=(
    commit_git.bash
    README.md
    runme.bash
    CommonLexerRules.g4
    stlgrammar.g4
    all_expr.expr
    expr_sample.expr
    stl.expr
    stl_checks.expr
    main.py
    grammarvisitor.py
    stl_expression.py
    stl_listener.py
    test_stl_expression.py
    data.py
)

git add $SCRIPT_DIR/"${FILE_LIST[@]}"
git commit -m "Committing stlgrammar folder before merging code from stlTest to this folder and updating the grammar"
git push origin master	