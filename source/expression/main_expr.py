import sys
from antlr4 import *
from antlr4.InputStream import InputStream

from expressionsLexer import expressionsLexer
from expressionsParser import expressionsParser
from expression_visitor import expression_visitor


if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1])
    else:
        # input_stream = InputStream(sys.stdin.readline())
        input_stream = FileStream("exp_expressions.expr")

    lexer = expressionsLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = expressionsParser(token_stream)
    tree = parser.prog() # parse; start at prog

    # print tree as text
    lisp_tree_str = tree.toStringTree(recog=parser)
    print(lisp_tree_str)

    visitor = expression_visitor()
    visitor.visit(tree)