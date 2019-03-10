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
git commit -m "Fixed minor space issue"
git push origin master	
