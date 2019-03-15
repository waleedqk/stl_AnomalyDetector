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
    stlgrammarSimplifier.py
    stlgrammarInterpreter_plot.py
    input_data.csv
)

LEGACY_FILES=(
    grammarvisitor.py
    stl_expression.py
    stl_listener.py
    test_stl_expression.py
)

# Files created by compiling the grammar *.g4 file with ANTLR
STATIC_FILES=(
    stlgrammarLexer.py
    stlgrammarListener.py
    stlgrammarParser.py
)

git add $SCRIPT_DIR/"${FILE_LIST[@]}"
git add $SCRIPT_DIR/"${LEGACY_FILES[@]}"
git add $SCRIPT_DIR/"${STATIC_FILES[@]}"
git commit -m "Print execution run time information"
git push origin master	