#!/bin/bash

antlr4 -Dlanguage=Python3 -visitor stlgrammar.g4
antlr4 -visitor stlgrammar.g4
javac *.java