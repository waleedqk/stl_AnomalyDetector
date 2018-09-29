import os
import subprocess
import random

from stlgrammarLexer import stlgrammarLexer
from stlgrammarParser import stlgrammarParser
from stlgrammarListener import stlgrammarListener


class stl_listener(stlgrammarListener):

    def __init__(self):
        self.stack = {}

        '''
        keeps a unique list of all the signals being used in the stl rules
        '''
        self.signals = []

        '''
        The code that is being generated is appended to the string
        '''
        self.code = ""


    def getExpr(self, ctx):
        '''

        :param ctx: the node to whose contents need to be retrieved
        :return:
        '''
        return self.stack[ctx]

    def setExpr(self, ctx, value):
        '''

        :param ctx: the node which we need to annotate. Becomes the key to the dict value
        :param value: the value we want to annotate the node with
        :return:
        '''
        self.stack[ctx] = value

    # Enter a parse tree produced by stlgrammarParser#Gcall.
    def enterGcall(self, ctx:stlgrammarParser.GcallContext):
        code = ""

        code += "\nGcall_check=True"

        # does this call have an associated timeslice with it
        if (ctx.timeslice() == None):
            code += "\nfor i in range(signal_length):"
        else:
            start_t = ctx.timeslice().start_t().getText().strip()
            end_t = ctx.timeslice().end_t().getText().strip()
            code += "\nfor i in range({}, {}):".format(start_t, end_t)

        # get the parsed expression that is generated for this node
        expr = self.getExpr(ctx.formula())

        code += "\nif(({})):\npass".format(expr)

        self.code += code


    # Exit a parse tree produced by stlgrammarParser#Gcall.
    def exitGcall(self, ctx:stlgrammarParser.GcallContext):
        code = ""

        code += "\nelse:"
        code += "\nGcall_check=False"

        self.code += code

    # Exit a parse tree produced by stlgrammarParser#prog.
    def exitProg(self, ctx:stlgrammarParser.ProgContext):
        with open("functions.py", "w") as code_output:
            code_output.write("\nimport * from functions")
            code_output.write("\nx = [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1]")
            code_output.write("\nif __name__ == '__main__':")
            code_output.write(self.code)
            code_output.write('\nprint("{}".format(Gcall_check))')

        proc = subprocess.Popen(
        ['chmod', '+x', 'functions.py'],
        stdout=subprocess.PIPE)
        (stdoutdata, stderrdata) = proc.communicate()
        print(stdoutdata)

        proc = subprocess.Popen(
        ['autopep8', '--in-place', '--aggressive', '--aggressive', '--select=E11,E101,E121', 'functions.py'],
        #     ['autopep8', 'functions.py', '--select=E11,E101,E121', '--in-place'],
        stdout=subprocess.PIPE)
        (stdoutdata, stderrdata) = proc.communicate()
        print(stdoutdata)