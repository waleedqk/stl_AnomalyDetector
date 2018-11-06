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
        The STL rule stored as a string value
        '''
        self.stlString = ""

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

    def funcUIDgen(self, func_prepend="_"):
        '''
        Generate the unique ID and the function call that will use this UID for nodes
        :param func_prepend: The function constant that will prepend the unique ID
        :return:
        '''

        # get unique ID 
        uid = str(self.getUniqueId()).strip()

        # the function call that will be used with this UID
        func_call = func_prepend.strip() + uid.strip()

        return (uid, func_call)

    def signalComp_boolCode(self, func_call="_", signal="x", relOp="==", boolVal="True"):
        '''
        generate code that is associated with a signalBool expr:  a == True, (False != a)

        '''
        code = "\n"
        code += "\n\ndef " + str(func_call) + "(t=0):"
        code += "\n\tif({}[t] {} {}):".format(signal, relOp, boolVal)
        code += "\n\t\treturn True"
        code += "\n\telse:"
        code += "\n\t\treturn False"

        return code

    def signalComp_exprCode(self, func_call="_", signal="x", relOp="==", expr="0"):
        '''
        generate code that is associated with a signalExpr expr:  a < 54, ((4/63) < a)

        '''
        code = "\n"
        code += "\n\ndef " + str(func_call) + "(t=0):"
        code += "\n\tif({}[t] {} {}):".format(signal, relOp, expr)
        code += "\n\t\treturn True"
        code += "\n\telse:"
        code += "\n\t\treturn False"

        return code

    def stlProp_code(self, func_call="_", boolVal="True"):
        '''
        generate code that is associated with an stlProp formula: True, False
        '''
        
        code = "\n"
        code += "\n\ndef " + func_call + "(t=0):"
        code += "\n\tif({} == True):".format(boolVal)
        code += "\n\t\treturn True"
        code += "\n\telse:"
        code += "\n\t\treturn False"

        return code



    def stlNotFormula_code(self, func_call="_", func_check="_"):
        '''
        generate code that is associated with an stlProp formula: True, False
        '''        
        code = "\n"
        code += "\n\ndef " + str(func_call) + "(t=0):"
        code += "\n\tif( not( {}(t=t) )):".format(func_check)
        code += "\n\t\treturn True"
        code += "\n\telse:"
        code += "\n\t\treturn False"

        return code


    def stlUntilFormula_code(self, func_call="_", start_t="0", end_t="0", phi="_", phe="_"):
        '''
        generate code that is associated with a Until formula: x > 9 U [10, 15] y > 25
        '''
        code = "\n"
        code += "\n\ndef " + str(func_call) + "(t=0):"            # "(t=0, start_t={}, end_t={}):".format(start_t, end_t)
        code += "\n\tfor i in range(t+{}, t+{}+1+1):".format(start_t, end_t)
        code += "\n\t\tif ({}(t=i)):".format(phe)
        code += "\n\t\t\tbreak"
        code += "\n\tif (i > (t + {})):".format(end_t)
        code += "\n\t\treturn False"
        code += "\n\tfor j in range(t,i):"
        code += "\n\t\tif(not ({}(t=j))):".format(phi)
        code += "\n\t\t\treturn False"
        code += "\n\treturn True"

        return code

    # Enter a parse tree produced by stlgrammarParser#prog.
    def enterProg(self, ctx:stlgrammarParser.ProgContext):
        '''
        Initialization steps at the beginning of the file
        :param ctx:
        :return:
        '''
        self.stlString = ctx.stlFormula().getText().strip()


    # Exit a parse tree produced by stlgrammarParser#prog.
    def exitProg(self, ctx:stlgrammarParser.ProgContext):
        '''

        :param ctx:
        :param value: 
        :return:
        '''
        first_call = self.getExpr(ctx.stlFormula())
        # print("first_call: {}".format(first_call))

        code = "\n\tstl_rule = " + first_call + "(t=0)"
        code += "\n\tprint('Checking STL rule: {}')".format(self.stlString)
        code += "\n\tprint('STL rule was satisfied: {}'.format(stl_rule))"

        self.appendCode("runSTLcheck.py", code)

        proc = subprocess.Popen(
        ['chmod', '+x', 'functions.py', 'runSTLcheck.py'],
        stdout=subprocess.PIPE)
        (stdoutdata, stderrdata) = proc.communicate()

    # Enter a parse tree produced by stlgrammarParser#stlGlobalFormula.
    def enterStlGlobalFormula(self, ctx:stlgrammarParser.StlGlobalFormulaContext):
        '''
        G[3,4](a > 25)
        :param ctx:
        :param value: 
        :return:
        '''

        # get unique ID and the function call that will use this UID for this node
        uid, func_call = self.funcUIDgen(func_prepend="StlGlobal_")

        # annotate the node with the variables
        self.setUID(ctx, {"uid": uid, "func": func_call})

        # signal calls will only be referred to with their appointed function calls 
        self.setExpr(ctx, func_call)



    # Exit a parse tree produced by stlgrammarParser#stlGlobalFormula.
    def exitStlGlobalFormula(self, ctx:stlgrammarParser.StlGlobalFormulaContext):
        '''
        G[3,4](a > 25)
        :param ctx:
        :param value: 
        :return:
        '''
        timeRange = (ctx.timeSlice() != None)
        if timeRange:
            start_t = ctx.timeSlice().start_t().getText().strip()
            end_t = ctx.timeSlice().end_t().getText().strip()
        else:
            start_t = 0
            end_t = self.time_max
        # print("start: {} \t end: {}".format(start_t, end_t))

        stlFormula = self.getExpr(ctx.stlFormula())

        # get the function call for this node: StlGlobal_930
        func_call = self.getUID(ctx)["func"]




        boolVal = "True"
        # get unique ID and the function call that will use this UID for this node
        uid_bool, func_call_bool = self.funcUIDgen(func_prepend="stlProp_")
        # stlProp formula function code generation
        code = self.stlProp_code(func_call=func_call_bool, boolVal=boolVal)
        # append code to file
        self.appendCode("functions.py", code)

        # get unique ID and the function call that will use this UID for this node
        uid_stlNot, func_call_stlNot = self.funcUIDgen(func_prepend="StlNot_")
        # stlNotFormula formula function code generation
        code = self.stlNotFormula_code(func_call=func_call_stlNot, func_check=stlFormula)
        # append code to file
        self.appendCode("functions.py", code)


        # get unique ID and the function call that will use this UID for this node
        uid_until, func_call_until = self.funcUIDgen(func_prepend="StlUntil_")

        code = self.stlUntilFormula_code(func_call=func_call_until, start_t=start_t, end_t=end_t, phi=func_call_bool, phe=func_call_stlNot)
        # append code to file
        self.appendCode("functions.py", code)



        code = "\n"
        code += "\n\ndef " + str(func_call) + "(t=0):"
        # code += "\n\tif(not( True U [3,4] not({}) ) ):".format(stlFormula)
        code += "\n\tif(not( {}(t=t)) ):".format(func_call_until)
        code += "\n\t\treturn True"
        code += "\n\telse:"
        code += "\n\t\treturn False"

        self.appendCode("functions.py", code)


    # Enter a parse tree produced by stlgrammarParser#stlEventualFormula.
    def enterStlEventualFormula(self, ctx:stlgrammarParser.StlEventualFormulaContext):
        '''
        F[5,6]((4/63) < b)
        :param ctx:
        :param value: 
        :return:
        '''

        # get unique ID and the function call that will use this UID for this node
        uid, func_call = self.funcUIDgen(func_prepend="StlEventual_")

        # annotate the node with the variables
        self.setUID(ctx, {"uid": uid, "func": func_call})

        # signal calls will only be referred to with their appointed function calls 
        self.setExpr(ctx, func_call)


    # Exit a parse tree produced by stlgrammarParser#stlEventualFormula.
    def exitStlEventualFormula(self, ctx:stlgrammarParser.StlEventualFormulaContext):
        '''
        F[5,6]((4/63) < b)
        :param ctx:
        :param value: 
        :return:
        '''
        timeRange = (ctx.timeSlice() != None)
        if timeRange:
            start_t = ctx.timeSlice().start_t().getText().strip()
            end_t = ctx.timeSlice().end_t().getText().strip()
        else:
            start_t = 0
            end_t = self.time_max
        # print("start: {} \t end: {}".format(start_t, end_t))

        stlFormula = self.getExpr(ctx.stlFormula())

        # get the function call for this node: signalComp_611
        func_call = self.getUID(ctx)["func"]


        boolVal = "True"
        # get unique ID and the function call that will use this UID for this node
        uid_bool, func_call_bool = self.funcUIDgen(func_prepend="stlProp_")
        # stlProp formula function code generation
        code = self.stlProp_code(func_call=func_call_bool, boolVal=boolVal)
        # append code to file
        self.appendCode("functions.py", code)

        # get unique ID and the function call that will use this UID for this node
        uid_until, func_call_until = self.funcUIDgen(func_prepend="StlUntil_")

        code = self.stlUntilFormula_code(func_call=func_call_until, start_t=start_t, end_t=end_t, phi=func_call_bool, phe=stlFormula)
        # append code to file
        self.appendCode("functions.py", code)

        code = "\n"
        code += "\n\ndef " + str(func_call) + "(t=0):"
        code += "\n\tif({}(t=t)):".format(func_call_until)
        code += "\n\t\treturn True"
        code += "\n\telse:"
        code += "\n\t\treturn False"

        self.appendCode("functions.py", code)


    # Exit a parse tree produced by stlgrammarParser#stlSignalComp.
    def exitStlSignalComp(self, ctx:stlgrammarParser.StlSignalCompContext):
        '''

        :param ctx:
        :param value: 
        :return:
        '''

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

        # get unique ID and the function call that will use this UID for this node
        uid, func_call = self.funcUIDgen(func_prepend="StlSignal_")

        # annotate the node with the variables
        self.setUID(ctx, {"uid": uid, "func": func_call})

        # signal calls will only be referred to with their appointed function calls 
        self.setExpr(ctx, func_call)

        code = "\n"
        code += "\n\ndef " + func_call + "(t=0):"
        code += "\n\tif({}[t] == True):".format(signal)
        code += "\n\t\treturn True"
        code += "\n\telse:"
        code += "\n\t\treturn False"

        self.appendCode("functions.py", code)

    # Enter a parse tree produced by stlgrammarParser#stlUntilFormula.
    def enterStlUntilFormula(self, ctx:stlgrammarParser.StlUntilFormulaContext):
        '''

        '''

        # get unique ID and the function call that will use this UID for this node
        uid, func_call = self.funcUIDgen(func_prepend="StlUntil_")

        # annotate the node with the variables
        self.setUID(ctx, {"uid": uid, "func": func_call})

        # signal calls will only be referred to with their appointed function calls 
        self.setExpr(ctx, func_call)


    # Exit a parse tree produced by stlgrammarParser#stlUntilFormula.
    def exitStlUntilFormula(self, ctx:stlgrammarParser.StlUntilFormulaContext):
        '''
        
        '''

        start_t = ctx.timeSlice().start_t().getText().strip()
        end_t = ctx.timeSlice().end_t().getText().strip()
        # print("start: {} \t end: {}".format(start_t, end_t))

        stlFormula_phi = self.getExpr(ctx.stlFormula(0))
        stlFormula_phe = self.getExpr(ctx.stlFormula(1))

        # get the function call for this node: StlUntil_611
        func_call = self.getUID(ctx)["func"]

        code = self.stlUntilFormula_code(func_call=func_call, start_t=start_t, end_t=end_t, phi=stlFormula_phi, phe=stlFormula_phe)

        self.appendCode("functions.py", code)



    # Enter a parse tree produced by stlgrammarParser#stlProp.
    def enterStlProp(self, ctx:stlgrammarParser.StlPropContext):
        '''
        Getting a single boolean prop as a formula: True
        :param ctx:
        :return:
        '''

        boolVal = ctx.Bool().getText().strip().replace("(","").replace(")","")

        # get unique ID and the function call that will use this UID for this node
        uid, func_call = self.funcUIDgen(func_prepend="stlProp_")

        # annotate the node with the variables
        self.setUID(ctx, {"uid": uid, "func": func_call})

        # signal calls will only be referred to with their appointed function calls 
        self.setExpr(ctx, func_call)

        code = self.stlProp_code(func_call=func_call, boolVal=boolVal)

        self.appendCode("functions.py", code)

    # Enter a parse tree produced by stlgrammarParser#stlConjDisjFormula.
    def enterStlConjDisjFormula(self, ctx:stlgrammarParser.StlConjDisjFormulaContext):
        '''
        (F[5,6]((4/63) < b)) and G[3,4](a > 25)
        :param ctx:
        :param value: 
        :return:
        '''

        # get unique ID and the function call that will use this UID for this node
        uid, func_call = self.funcUIDgen(func_prepend="StlConjDisj_")

        # annotate the node with the variables
        self.setUID(ctx, {"uid": uid, "func": func_call})

        # signal calls will only be referred to with their appointed function calls 
        self.setExpr(ctx, func_call)


    # Exit a parse tree produced by stlgrammarParser#stlConjDisjFormula.
    def exitStlConjDisjFormula(self, ctx:stlgrammarParser.StlConjDisjFormulaContext):
        '''
        (F[5,6]((4/63) < b)) and G[3,4](a > 25)
        :param ctx:
        :param value: 
        :return:
        '''
        before = self.getExpr(ctx.stlFormula(0))
        andorOp = self.getExpr(ctx.andorOp())
        after = self.getExpr(ctx.stlFormula(1))

        conjdisjFormula = "({}(t=t) {} {}(t=t))".format(before, andorOp, after)
        # print(conjdisjFormula)

        # get the function call for this node: signalComp_611
        func_call = self.getUID(ctx)["func"]

        code = "\n"
        code += "\n\ndef " + str(func_call) + "(t=0):"
        code += "\n\tif({} == True):".format(conjdisjFormula)
        code += "\n\t\treturn True"
        code += "\n\telse:"
        code += "\n\t\treturn False"

        self.appendCode("functions.py", code)


    # Enter a parse tree produced by stlgrammarParser#stlFormulaImplies.
    def enterStlFormulaImplies(self, ctx:stlgrammarParser.StlFormulaImpliesContext):
        '''
        F[5,6](4/63 < b) -> G[3,4](a > 25)
        :param ctx:
        :param value: 
        :return:
        '''

        # get unique ID and the function call that will use this UID for this node
        uid, func_call = self.funcUIDgen(func_prepend="StlFormulaImplies_")

        # annotate the node with the variables
        self.setUID(ctx, {"uid": uid, "func": func_call})

        # signal calls will only be referred to with their appointed function calls 
        self.setExpr(ctx, func_call)


    # Exit a parse tree produced by stlgrammarParser#stlFormulaImplies.
    def exitStlFormulaImplies(self, ctx:stlgrammarParser.StlFormulaImpliesContext):
        '''
        (F[5,6]((4/63) < b)) and G[3,4](a > 25)
        :param ctx:
        :param value: 
        :return:
        '''
        before = self.getExpr(ctx.stlFormula(0))
        after = self.getExpr(ctx.stlFormula(1))

        conjdisjFormula = "((not ({}(t=t))) or ({}(t=t) and {}(t=t)))".format(before, before, after)
        # print(conjdisjFormula)

        # get the function call for this node: signalComp_611
        func_call = self.getUID(ctx)["func"]

        code = "\n"
        code += "\n\ndef " + str(func_call) + "(t=0):"
        code += "\n\tif({} == True):".format(conjdisjFormula)
        code += "\n\t\treturn True"
        code += "\n\telse:"
        code += "\n\t\treturn False"

        self.appendCode("functions.py", code)


    # Enter a parse tree produced by stlgrammarParser#stlNotFormula.
    def enterStlNotFormula(self, ctx:stlgrammarParser.StlNotFormulaContext):
        '''

        :param ctx:
        :param value: 
        :return:
        '''

        # get unique ID and the function call that will use this UID for this node
        uid, func_call = self.funcUIDgen(func_prepend="StlNot_")

        # annotate the node with the variables
        self.setUID(ctx, {"uid": uid, "func": func_call})

        # signal calls will only be referred to with their appointed function calls 
        self.setExpr(ctx, func_call)


    # Exit a parse tree produced by stlgrammarParser#stlNotFormula.
    def exitStlNotFormula(self, ctx:stlgrammarParser.StlNotFormulaContext):
        '''

        :param ctx:
        :param value: 
        :return:
        '''
        stlFormula = self.getExpr(ctx.stlFormula())

        # get the function call for this node: signalComp_611
        func_call = self.getUID(ctx)["func"]

        code = self.stlNotFormula_code(func_call=func_call, func_check=stlFormula)

        self.appendCode("functions.py", code)

    # Exit a parse tree produced by stlgrammarParser#stlParens.
    def exitStlParens(self, ctx:stlgrammarParser.StlParensContext):
        '''

        :param ctx:
        :param value: 
        :return:
        '''

        stlFormula = self.getExpr(ctx.stlFormula())
        # print("stlFormula: {}".format(stlFormula))

        signalComp = self.setExpr(ctx, stlFormula)


    # Enter a parse tree produced by stlgrammarParser#signalExpr.
    def enterSignalExpr(self, ctx:stlgrammarParser.SignalExprContext):
        '''
        :param ctx:
        :return:
        '''

        # get unique ID and the function call that will use this UID for this node
        uid, func_call = self.funcUIDgen(func_prepend="signalComp_")

        # annotate the node with the variables
        self.setUID(ctx, {"uid": uid, "func": func_call})

        # signal calls will only be referred to with their appointed function calls 
        self.setExpr(ctx, func_call)

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
        func_call = self.getUID(ctx)["func"]

        # generate code that is associated with a signalBool expr:  a == True, (False != a)
        code = self.signalComp_exprCode(func_call=func_call, signal=signal, relOp=relOp, expr=expr)

        self.appendCode("functions.py", code)


    # Enter a parse tree produced by stlgrammarParser#signalBool.
    def enterSignalBool(self, ctx:stlgrammarParser.SignalBoolContext):
        '''
        :param ctx:
        :return:
        '''

        # get unique ID and the function call that will use this UID for this node
        uid, func_call = self.funcUIDgen(func_prepend="signalComp_")

        # annotate the node with the variables
        self.setUID(ctx, {"uid": uid, "func": func_call})

        # signal calls will only be referred to with their appointed function calls 
        self.setExpr(ctx, func_call)

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
        func_call = self.getUID(ctx)["func"]

        # generate code that is associated with a signalBool expr:  a == True, (False != a)
        code = self.signalComp_boolCode(func_call=func_call, signal=signal, relOp=relOp, boolVal=boolVal)

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

    # Exit a parse tree produced by stlgrammarParser#andorOp.
    def exitAndorOp(self, ctx:stlgrammarParser.AndorOpContext):
        '''

        :param ctx:
        :return:
        '''
        andor = ctx.getText().strip()
        self.setExpr(ctx, andor)