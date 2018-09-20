


antlr4 -Dlanguage=Python3 -visitor expressions.g4
antlr4 -visitor expressions.g4
javac *.java


**1) Parser**

Learn more about how the parser recognized the input

    pygrun expressions prog --tree expr_sample.expr


**2) Tokens**

Print out the tokens created by the lexer

Run the command:

    pygrun expressions prog --tokens expr_sample.expr

**3) GUI**

See the visual parse tree

    grun expressions prog -gui expr_sample.expr