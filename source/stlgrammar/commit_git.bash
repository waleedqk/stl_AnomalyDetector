#!/bin/bash


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT_DIR=$(dirname "$SCRIPT_DIR")


FILE_LIST=(
    commit_git.bash
    README.md
    recompile_grammar.bash
    runme.bash
    CommonLexerRules.g4
    stlgrammar.g4
    all_expr.expr
    stl.expr
    main.py
    stlgrammarInterpreter.py
    stlgrammarInterpreter_plot.py
    data.csv
)

LEGACY_FILES=(
    grammarvisitor.py
    stl_expression.py
    stl_listener.py
    test_stl_expression.py
)

git add $SCRIPT_DIR/"${FILE_LIST[@]}"
git add $SCRIPT_DIR/"${LEGACY_FILES[@]}"
git commit -m "data.py replaced by data.csv. runSTLcheck now loads the data.csv for the signals. Access the value by index. Time plots now include implies and conjDisj. runme.bash runs the entire chain"
git push origin master	