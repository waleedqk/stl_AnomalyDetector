# stlgrammar.g4
This is the stlgrammar

**How to run**

Need to have the *.g4 file that has the language specidfications

    antlr4 -Dlanguage=Python3 -visitor stlgrammar.g4

OR

    antlr4py3 -visitor stlgrammar.g4

**Run with visitor**

Need to have the *.g4 file that has the language specidfications

    antlr4 -Dlanguage=Python3 -visitor stlgrammar.g4

OR

    antlr4py3 -visitor stlgrammar.g4

**Grun with JAVA to see AST**

    antlr4 stlgrammar.g4              |         antlr4 -visitor stlgrammar.g4
    javac *.java

Now grun is set up and can be used for the following cases:

**1) Parser**

Learn more about how the parser recognized the input

    pygrun stlgrammar prog --tree stl.expr

**2) Tokens**

Print out the tokens created by the lexer

Run the command:

    pygrun stlgrammar prog --tokens stl.expr

Each line of the output represents a single token and shows everything we know about the token

    token at index tokenIndex (indexed from 0),
    goes from character position start (inclusive starting from 0)
    goes to character position stop
    has text text
    has token type type
    is on line line (from 1)
    is at character position column (starting from zero and counting tabs as a single character)

**3) GUI**

See the visual parse tree

    grun stlgrammar prog -gui stl.expr


**File Description**

The code from the stlTest folder has just been ported over to this folder and the grammar has been updated as during the meeting discussions. The grammar file *.g4 has already been compiled using the instructions stated above. To generate code for a STL formula write it to a file and pass that along as an argument to ```main.py```. By default the file to be looked up is: ```stl.expr```

```stlgrammarSimplifier.py``` does some preprocessing on the stl property specified. It transforms the rules to its basic properties. G, F, implies, or are all transformed into their equivalent base components of the grammar, that uses not, and, until. The resultant rule is the same but uses the base temporal logic and operators.

The main curx of the code resides in ```stlgrammarInterpreter.py```. The class housed here is an extension of the ```**stlgrammarListener** ```, which goes through the entry and exit functions of each of the nodes. The logic here generates the output that can be used to check the STL expression provided against a csv dataset.

The ```signal_dict.npy``` is a numpy dictionary generated while running ```stlgrammarInterpreter.py```. Its a dictionary with the key being the function call name and the value being the expression that is being processind in the function.



**Run the test code**

    python main.py stl.expr

The resultant of this script creates two files:
    1) runSTLcheck.py
    2) signal_dict.npy

```runSTLcheck.py``` is a script that can be run to see the validity of the rule on a given signal. This includes all the function calls and code associated with the STL formula provided. The code only requires a CSV file that has the data needed to check the rule with the respective column with name of the signal to check.

For checks and plotting a csv file is created for holding the state of the checked data after ```runSTLcheck.py``` has been run: ```dataframe_populated.csv```, it has the updated values of the function calls w.r.t time as the code was being run.

```signal_dict.npy``` is a dictionary, with the key being the function calls and the value being the expression being checked in that function. It is used to update the graph labels when the data is being plotted.

Run the following to see if the STL rule was satisfied:

    python runSTLcheck.py

The resultant of this script creates a file:
    1) dataframe_populated.csv

```dataframe_populated.csv``` has the updated values of the function calls w.r.t time as the code was being run.


**Legacy Code**
The extensive code from the grammar one version prior can be found in the file ```stl_expression.py``` and is going to be kept till that functionality has been ported over but the code is outdated as of today and will not work.