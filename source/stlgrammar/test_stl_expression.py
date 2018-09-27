import sys
from antlr4 import *
from antlr4.InputStream import InputStream

from stlgrammarLexer import stlgrammarLexer
from stlgrammarParser import stlgrammarParser
from stl_expression import stl_expression


if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1])
    else:
        # input_stream = InputStream(sys.stdin.readline())
        input_stream = FileStream("stl.expr")

    lexer = stlgrammarLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = stlgrammarParser(token_stream)
    tree = parser.prog() # parse; start at prog

    # print tree as text
    lisp_tree_str = tree.toStringTree(recog=parser)
    print(lisp_tree_str)


    # expression
    print("Start Walking...")
    expressions = stl_expression()
    walker = ParseTreeWalker()
    walker.walk(expressions, tree)
    # print('result_stack=', listener.stack)
    print('signal_list=', expressions.signals)
