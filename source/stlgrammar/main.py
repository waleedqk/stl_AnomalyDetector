import sys
from antlr4 import *
from antlr4.InputStream import InputStream

from stlgrammarLexer import stlgrammarLexer
from stlgrammarParser import stlgrammarParser
from stlgrammarInterpreter import stlgrammarInterpreter


if __name__ == '__main__':
    if len(sys.argv) > 1:
        stlFile = open(sys.argv[1], 'r')
    else:
        # input_stream = InputStream(sys.stdin.readline())
        stlFile = open('stl.expr','r')

    with open("temp_expr_parser.txt", "w") as code_output:
        code_output.write("\n")

    for line in stlFile.readlines():
        stlRule = line.strip()

        lexer = stlgrammarLexer(InputStream(stlRule))
        token_stream = CommonTokenStream(lexer)
        parser = stlgrammarParser(token_stream)
        tree = parser.prog() # parse; start at prog

        # print tree as text
        lisp_tree_str = tree.toStringTree(recog=parser)
        print(lisp_tree_str)


        # stlgrammarInterpreter
        # print("Start Walking...")
        interpreter = stlgrammarInterpreter()
        walker = ParseTreeWalker()
        walker.walk(interpreter, tree)
        # print('signal_list=', interpreter.signals)

        # with open("temp_expr_parser.txt", "a") as code_output:
        #     code_output.write("\n"+str(interpreter.finalProg))


    stlFile.close()