#!/bin/bash

antlr4 -Dlanguage=Python3 structuredEnglishSTL.g4
antlr4 structuredEnglishSTL.g4
javac *.java
