import os
import subprocess
import random
import antlr4
from stlgrammarLexer import stlgrammarLexer
from stlgrammarParser import stlgrammarParser
from stlgrammarListener import stlgrammarListener

class stlgrammarInterpreter(stlgrammarListener):
    def __init__(self):

        '''
        The code that is being generated is appended to the string
        '''
        self.code = ""

        '''
        a dict to annotate the nodes with the required content
        the key is the unique ctx made by antlr during the parsing
        '''
        self.stack = {}

        '''
        keeps a unique list of all the signals being used in the stl rules
        '''
        self.signals = []


        '''
        List of unique ID's associated with all the function calls
        '''
        self.uids = {}

        '''
        The maximum time range that can be put to a STL rule
        '''
        self.time_max = 1000

        '''
        Index for beginning of all type of stl rules 
        '''
        # self.ruleBegin = [stlgrammarParser.RULE_globallyeventuallyCall, stlgrammarParser.RULE_eventuallygloballyCall, stlgrammarParser.RULE_globallyCall, stlgrammarParser.RULE_eventuallyCall]

        with open("runSTLcheck.py", "w") as code_output:
            code_output.write("\nfrom data import *")
            code_output.write("\nimport os, sys, random")
            code_output.write("\n\nfrom functions import *")
            code_output.write("\n\nif __name__ == '__main__':")

        with open("functions.py", "w") as code_output:
            code_output.write("\nfrom data import *")

    def appendCode(self, file, code):
        '''
        Appends text to a file
        :param file: the name of the file to append the text to
        :param code: the string that needs to be appended to the file
        :return:
        '''
        with open(file, "a") as code_output:
            code_output.write(str(code))


    def getUniqueId(self):
        '''
        generate a random number between 100 and 999, which has not been already generated
        :return: number
        '''
        number = str(random.sample(range(100, 999),1)[0])

        while (number in self.uids.values()):
            number = str(random.sample(range(100, 999),1)[0])

        return number


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


    def getUID(self, ctx):
        '''

        :param ctx:
        :return: get the UID and function call associated with the ctx
        '''
        return self.uids[ctx]

    def setUID(self, ctx, value):
        '''

        :param ctx:
        :param value: set UID and function call associated with each node
        :return:
        '''
        self.uids[ctx] = value

    # Enter a parse tree produced by stlgrammarParser#prog.
    def enterProg(self, ctx:stlgrammarParser.ProgContext):
        '''
        Initialization steps at the beginning of the file
        :param ctx:
        :return:
        '''
        pass


    # Exit a parse tree produced by stlgrammarParser#prog.
    def exitProg(self, ctx:stlgrammarParser.ProgContext):

        first_call = self.getExpr(ctx.stlFormula())
        # print("first_call: {}".format(first_call))

        code = "\n\tstl_rule = " + first_call
        code += "\n\tprint('STL rule was satisfied: {}'.format(stl_rule))"

        self.appendCode("runSTLcheck.py", code)

        proc = subprocess.Popen(
        ['chmod', '+x', 'functions.py', 'runSTLcheck.py'],
        stdout=subprocess.PIPE)
        (stdoutdata, stderrdata) = proc.communicate()


    # Exit a parse tree produced by stlgrammarParser#stlSignalComp.
    def exitStlSignalComp(self, ctx:stlgrammarParser.StlSignalCompContext):

        # Get the name of the function associated with the call
        signalComp = self.setExpr(ctx, self.getExpr(ctx.getChild(0)))
        # print("signalComp: {}".format(self.getExpr(ctx.getChild(0))))


    # Enter a parse tree produced by stlgrammarParser#stlSignal.
    def enterStlSignal(self, ctx:stlgrammarParser.StlSignalContext):
        '''
        Getting a single signal value as a formula: x
        :param ctx:
        :return:
        '''
        signal = ctx.signal().getText().strip().replace("(","").replace(")","")
        print("signal: {}".format(signal))

        # get unique ID for this node
        uid = str(self.getUniqueId())

        # the function call that will use this UID
        func_call = "StlSignal_" + uid

        # annotate the node with the variables
        self.setUID(ctx, {"uid": uid, "func": func_call})

        # signal calls will only be referred to with their appointed function calls 
        self.setExpr(ctx, func_call+"(t={})")

        code = "\n"
        code += "\n\ndef " + func_call + "():"
        code += "\n\tif({}[t] == True):".format(signal)
        code += "\n\t\treturn True"
        code += "\n\telse:"
        code += "\n\t\treturn False"

        self.appendCode("functions.py", code)


    # Enter a parse tree produced by stlgrammarParser#stlProp.
    def enterStlProp(self, ctx:stlgrammarParser.StlPropContext):
        '''
        Getting a single boolean prop as a formula: True
        :param ctx:
        :return:
        '''

        boolVal = ctx.Bool().getText().strip().replace("(","").replace(")","")

        # get unique ID for this node
        uid = str(self.getUniqueId())

        # the function call that will use this UID
        func_call = "stlProp_" + uid

        # annotate the node with the variables
        self.setUID(ctx, {"uid": uid, "func": func_call})

        # signal calls will only be referred to with their appointed function calls 
        self.setExpr(ctx, func_call+"()")

        code = "\n"
        code += "\n\ndef " + func_call + "():"
        code += "\n\tif({} == True):".format(boolVal)
        code += "\n\t\treturn True"
        code += "\n\telse:"
        code += "\n\t\treturn False"

        self.appendCode("functions.py", code)


    # Exit a parse tree produced by stlgrammarParser#stlParens.
    def exitStlParens(self, ctx:stlgrammarParser.StlParensContext):
        
        stlFormula = self.getExpr(ctx.stlFormula())
        # print("stlFormula: {}".format(stlFormula))

        signalComp = self.setExpr(ctx, stlFormula)


    # Enter a parse tree produced by stlgrammarParser#signalExpr.
    def enterSignalExpr(self, ctx:stlgrammarParser.SignalExprContext):
        '''
        :param ctx:
        :return:
        '''
        # get unique ID for this node
        uid = str(self.getUniqueId())

        # the function call that will use this UID
        func_call = "signalComp_" + uid

        # annotate the node with the variables
        self.setUID(ctx, {"uid": uid, "func": func_call})

        # signal calls will only be referred to with their appointed function calls 
        self.setExpr(ctx, func_call+"(t={})")

    # Exit a parse tree produced by stlgrammarParser#signalExpr.
    def exitSignalExpr(self, ctx:stlgrammarParser.SignalExprContext):
        '''
        parse the signalExpr: a < 54, ((4/63) < a)
        :param ctx:
        :return:
        '''

        signal = self.getExpr(ctx.signal())
        relOp = ctx.relOp().getText().strip()
        expr = self.getExpr(ctx.expr())

        # get the function call for this node: signalComp_611
        func_call = self.getUID(ctx)["func"] + "(t=t)"

        code = "\n"
        code += "\n\ndef " + str(self.getUID(ctx)["func"]) + "(t):"
        code += "\n\tif({}[t] {} {}):".format(signal, relOp, expr)
        code += "\n\t\treturn True"
        code += "\n\telse:"
        code += "\n\t\treturn False"

        self.appendCode("functions.py", code)


    # Enter a parse tree produced by stlgrammarParser#signalBool.
    def enterSignalBool(self, ctx:stlgrammarParser.SignalBoolContext):
        '''
        :param ctx:
        :return:
        '''
        # get unique ID for this node
        uid = str(self.getUniqueId())

        # the function call that will use this UID
        func_call = "signalComp_" + uid

        # annotate the node with the variables
        self.setUID(ctx, {"uid": uid, "func": func_call})

        # signal calls will only be referred to with their appointed function calls 
        self.setExpr(ctx, func_call+"(t={})")

    # Exit a parse tree produced by stlgrammarParser#signalBool.
    def exitSignalBool(self, ctx:stlgrammarParser.SignalBoolContext):
        '''
        parse the signalBool: a == True, (False != a)
        :param ctx:
        :return:
        '''

        signal = self.getExpr(ctx.signal())
        relOp = ctx.relOp().getText().strip()
        boolVal = ctx.Bool().getText().strip().replace("(","").replace(")","")

        # print("SignalBool: {}".format(self.getExpr(ctx)))

        # get the function call for this node: signalComp_611
        func_call = self.getUID(ctx)["func"] + "(t=t)"

        code = "\n"
        code += "\n\ndef " + str(self.getUID(ctx)["func"]) + "(t):"
        code += "\n\tif({}[t] {} {}):".format(signal, relOp, boolVal)
        code += "\n\t\treturn True"
        code += "\n\telse:"
        code += "\n\t\treturn False"

        self.appendCode("functions.py", code)

    # Exit a parse tree produced by stlgrammarParser#signalName.
    def exitSignalName(self, ctx:stlgrammarParser.SignalNameContext):
        '''
        Get the signal name associated with the node
        Should only have one child
        :param ctx:
        :return:
        '''

        # print("The signal name is: {}".format(self.getExpr(ctx)))
        self.setExpr(ctx, self.getExpr(ctx.signalID()))   

    # Exit a parse tree produced by stlgrammarParser#signalID.
    def exitSignalID(self, ctx:stlgrammarParser.SignalIDContext):
        '''
        Update the dict self.signals with unique signals used in the stl rules
        e.g. a, x, time, trigger
        :param ctx:
        :return:
        '''
        signal = ctx.getText()

        self.setExpr(ctx, signal)

        # if the signal name is being seen for the first time, add to global signal list
        if signal not in self.signals:
            self.signals.append(signal)


    # Exit a parse tree produced by stlgrammarParser#MulDivExpr.
    def exitMulDivExpr(self, ctx:stlgrammarParser.MulDivExprContext):
        '''
        4 / 63
        :param ctx:
        :return:
        '''
        first = self.getExpr(ctx.expr(0))
        operator = str(ctx.op.text).strip()
        second = self.getExpr(ctx.expr(1))

        expr = "({} {} {})".format(first, operator, second)
        # print(expr)

        self.setExpr(ctx, expr)

    # Exit a parse tree produced by stlgrammarParser#AddSubExpr.
    def exitAddSubExpr(self, ctx:stlgrammarParser.AddSubExprContext):
        '''
        4 + 63
        :param ctx:
        :return:
        '''
        first = self.getExpr(ctx.expr(0))
        operator = str(ctx.op.text).strip()
        second = self.getExpr(ctx.expr(1))

        expr = "({} {} {})".format(first, operator, second)
        # print(expr)

        self.setExpr(ctx, expr)  

    # Exit a parse tree produced by stlgrammarParser#intExpr.
    def exitIntExpr(self, ctx:stlgrammarParser.IntExprContext):
        '''
        Get the integer value of the expression: 4
        :param ctx:
        :return:
        '''
        intExpr = ctx.INT().getText().strip()
        # print("intExpr: {}".format(intExpr))

        self.setExpr(ctx, intExpr)

    # Exit a parse tree produced by stlgrammarParser#parensExpr.
    def exitParensExpr(self, ctx:stlgrammarParser.ParensExprContext):
        '''
        get the parsed expression in the parenthesis: (4/3)
        :param ctx:
        :return:
        '''

        expr = self.getExpr(ctx.expr())
        # print(expr)

        self.setExpr(ctx, expr) 