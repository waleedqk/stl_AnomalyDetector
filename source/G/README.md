# Calculator
This example shows
- 'G' - Globally rule

**How to run**

Need to have the *.g4 file that has the language specidfications

    antlr4 -Dlanguage=Python3 always.g4

OR

    antlr4py3 always.g4

**Run with visitor**

Need to have the *.g4 file that has the language specidfications

    antlr4 -Dlanguage=Python3 -visitor always.g4

OR

    antlr4py3 -visitor always.g4

**Grun with JAVA to see AST**

    antlr4 always.g4              |         antlr4 -visitor always.g4   
    javac *.java

Now grun is set up and can be used for the following cases:

**1) Parser**

Learn more about how the parser recognized the input

    pygrun always prog --tree stl_G.expr

**2) Tokens**

Print out the tokens created by the lexer

Run the command:

    pygrun always prog --tokens stl_G.expr

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

    grun always prog -gui stl_G.expr



# How to run
```
% antlr4py3 always.g4
% cat t.expr
193
a = 5
b = 6
a+b*2
(1+2)*3
```

**Run the test code**

    python calc.py t.expr

193
17
9


**Get tokens created by the lexer**

    pygrun LabeledExpr prog --tree t.expr

    pygrun LabeledExpr prog --tokens t.expr


**See the visual parse tree**

    grun LabeledExpr prog -gui t.expr

## GUI highlights the errors

    grun LabeledExpr prog -gui t_error.expr