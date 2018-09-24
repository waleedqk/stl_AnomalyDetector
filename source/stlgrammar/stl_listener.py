import os
import subprocess

from stlgrammarLexer import stlgrammarLexer
from stlgrammarParser import stlgrammarParser
from stlgrammarListener import stlgrammarListener


'''
The functionality is based on extending the listener since it visits all the nodes on its own

The 'stl_expression.py' adds all the functionality related to just processing the expression portion of the stl rule
'''
from stl_expression import stl_listener

class stl_listener(stl_listener):

    def __init__(self):
        self.stack = {}

        '''
        keeps a unique list of all the signals being used in the stl rules
        '''
        self.signals = []

        self.expr = {}

        '''
        The code that is being generated is appended to the string
        '''
        self.code = ""

    # Exit a parse tree produced by stlgrammarParser#Gcall.
    def exitGcall(self, ctx:stlgrammarParser.GcallContext):
        code = ""

        # get the parsed expression that is generated for this node
        expr = self.getExpr(ctx.formula())

        code += "\ncheck=True"

        # does this call have an associated timeslice with it
        if (ctx.timeslice() == None):
            code += "\nfor i in range(signal_length):"
        else:
            start_t = ctx.timeslice().start_t().getText().strip()
            end_t = ctx.timeslice().end_t().getText().strip()
            code += "\nfor i in range({}, {}):".format(start_t, end_t)

        code += "\nif(not({})):".format(expr)
        code += "\ncheck=False"

        self.code = code

    # Exit a parse tree produced by stlgrammarParser#prog.
    def exitProg(self, ctx:stlgrammarParser.ProgContext):
        with open("code.py", "w") as code_output:
            code_output.write("\nx = [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1]")
            code_output.write("\nif __name__ == '__main__':")
            code_output.write(self.code)
            code_output.write('\nprint("{}".format(check))')

        proc = subprocess.Popen(
        ['chmod', '+x', 'code.py'],
        stdout=subprocess.PIPE)
        (stdoutdata, stderrdata) = proc.communicate()
        print(stdoutdata)

        proc = subprocess.Popen(
        ['autopep8', '--in-place', '--aggressive', '--aggressive', 'code.py'],
        stdout=subprocess.PIPE)
        (stdoutdata, stderrdata) = proc.communicate()
        print(stdoutdata)