#!/bin/bash

antlr4 -Dlanguage=Python3 -visitor always.g4
antlr4 -visitor always.g4 
javac *.java