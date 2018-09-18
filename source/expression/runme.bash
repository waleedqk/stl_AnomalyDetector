#!/bin/bash

antlr4 -Dlanguage=Python3 -visitor expressions.g4
antlr4 -visitor expressions.g4 
javac *.java
