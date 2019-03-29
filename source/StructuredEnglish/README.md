# stlgrammar.g4
This is the stlgrammar

**How to run**

Need to have the *.g4 file that has the language specidfications

    antlr4 -Dlanguage=Python3 structuredEnglishSTL.g4

OR

    antlr4py3 structuredEnglishSTL.g4

**Run with visitor**

Need to have the *.g4 file that has the language specidfications

    antlr4 -Dlanguage=Python3 -visitor structuredEnglishSTL.g4

OR

    antlr4py3 -visitor structuredEnglishSTL.g4

**Grun with JAVA to see AST**

    antlr4 structuredEnglishSTL.g4              |         antlr4 -visitor structuredEnglishSTL.g4
    javac *.java

Now grun is set up and can be used for the following cases:

**1) Parser**

Learn more about how the parser recognized the input

    pygrun structuredEnglishSTL prog --tree stl_phrase.expr

**2) Tokens**

Print out the tokens created by the lexer

Run the command:

    pygrun structuredEnglishSTL prog --tokens stl_phrase.expr

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

    grun structuredEnglishSTL prog -gui stl_phrase.expr