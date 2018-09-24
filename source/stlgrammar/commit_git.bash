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
)

git add $SCRIPT_DIR/"${FILE_LIST[@]}"
git commit -m "stl_listener class is broken down into in terms of functionality. The stl_expression handles the logic related to expression, while the stl_listener inherits that class and add the functionality needed for the rules."
git push origin master	