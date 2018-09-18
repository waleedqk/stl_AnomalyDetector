


antlr4 -Dlanguage=Python3 -visitor expressions.g4
antlr4 -visitor expressions.g4
javac *.java


**1) Parser**

Learn more about how the parser recognized the input

    pygrun expressions prog --tree exp_expressions.expr


**2) Tokens**

Print out the tokens created by the lexer

Run the command:

    pygrun expressions prog --tokens exp_expressions.expr

**3) GUI**

See the visual parse tree

    grun expressions prog -gui exp_expressions.expr