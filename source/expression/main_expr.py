import sys
from antlr4 import *
from antlr4.InputStream import InputStream

from expressionsLexer import expressionsLexer
from expressionsParser import expressionsParser
from expr_visitor import expr_visitor
from expr_listener import expr_listener

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1])
    else:
        # input_stream = InputStream(sys.stdin.readline())
        input_stream = FileStream("expr_sample.expr")

    lexer = expressionsLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = expressionsParser(token_stream)
    tree = parser.prog() # parse; start at prog

    # print tree as text
    lisp_tree_str = tree.toStringTree(recog=parser)
    print(lisp_tree_str)

    # visitor = expr_visitor()
    # visitor.visit(tree)

    # listener
    print("Start Walking...")
    listener = expr_listener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    # print('result_stack=', listener.stack)

    print('signal_list=', listener.signals)

    print('expression=', listener.expr)