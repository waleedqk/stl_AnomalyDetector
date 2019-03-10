#!/bin/bash


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT_DIR=$(dirname "$SCRIPT_DIR")


FILE_LIST=(
    commit_git.bash
    README.md
    recompile_grammar.bash
    runme.bash
    CommonLexerRules.g4
    structuredEnglishSTL.g4
    stl_phrase.expr
	phrases.md
)

git add $SCRIPT_DIR/"${FILE_LIST[@]}"
git commit -m "New grammar, based on the paper: 'Real-time specification patterns'"
git push origin master	
