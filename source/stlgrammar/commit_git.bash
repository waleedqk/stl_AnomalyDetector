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
    stl.expr
    main.py
    stlgrammarInterpreter.py
    grammarvisitor.py
    stl_expression.py
    stl_listener.py
    test_stl_expression.py
    data.py
)

git add $SCRIPT_DIR/"${FILE_LIST[@]}"
git commit -m "Full working STL code generater. Commit after meeting with Sebastian on 06 Nov 2018 10 AM. See meeting notes for details."
git push origin master	