
import sys
from antlr4 import *
from alwaysLexer import alwaysLexer
from alwaysParser import alwaysParser
from alwaysListener import alwaysListener

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1])
    else:
        # input_stream = InputStream(sys.stdin.readline())
        input_stream = FileStream("stl_G.expr")

    lexer = alwaysLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = alwaysParser(token_stream)
    tree = parser.prog() # parse; start at prog

    # print tree as text
    lisp_tree_str = tree.toStringTree(recog=parser)
    print(lisp_tree_str)

    my_tokens = token_stream.getTokens(0, 100)
    print(' '.join(str(tkn) for tkn in my_tokens))
    for tkn in my_tokens:
        print("[@{},{}:{}='{}',<{}>,{}:{}]".format(
            tkn.tokenIndex,  # token at index tokenIndex (indexed from 0),
            tkn.start,       # goes from character position start (inclusive starting from 0)
            tkn.stop,        # goes to character position stop
            tkn.text,        # has text text
            tkn.type,        # has token type type
            tkn.line,        # is on line line (from 1)
            tkn.column       # is at character position column (starting from zero and counting tabs as a single character)
        ))