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



**Run the test code**

Test the expression part of the grammar. To see how a single expression is parsed and processed

    python test_stl_expression.py

Test the entire code base:

    python main.py stl.expr

Will result in an output file called 'code.py' that can be run to see the validity of the rule on a given signal