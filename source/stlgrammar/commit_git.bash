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
git commit -m "Single pass using 'python stl_expression.py stl.expr'. Creates the file 'runSTLcheck.py' and 'functions.py' with relevant code. Run final code using: 'python runSTLcheck.py'"
git push origin master	