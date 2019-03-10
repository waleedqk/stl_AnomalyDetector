#!/bin/bash

python3 main.py stl.expr
python3 runSTLcheck.py
python3 stlgrammarInterpreter_plot.py