#!/bin/bash


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT_DIR=$(dirname "$SCRIPT_DIR")

git add $SCRIPT_DIR/*
git commit -m "Commiting miscellaneous items to repo"
git push origin master	