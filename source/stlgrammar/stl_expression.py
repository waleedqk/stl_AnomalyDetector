import os
import subprocess
import random
import antlr4
from stlgrammarLexer import stlgrammarLexer
from stlgrammarParser import stlgrammarParser
from stlgrammarListener import stlgrammarListener



class stl_expression(stlgrammarListener):
    def __init__(self):

        '''
        The code that is being generated is appended to the string
        '''
        self.code = ""

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
        Index for beginning of all type of stl rules 
        '''
        self.ruleBegin = [stlgrammarParser.RULE_globallyeventuallyCall, stlgrammarParser.RULE_eventuallygloballyCall, stlgrammarParser.RULE_globallyCall, stlgrammarParser.RULE_eventuallyCall]

        with open("runSTLcheck.py", "w") as code_output:
            code_output.write("\nfrom data import *")

        with open("functions.py", "w") as code_output:
            code_output.write("\nfrom data import *")


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
        return self.uids[ctx]

    def setUID(self, ctx, value):
        self.uids[ctx] = value


    def appendCode(self, file, code):
        with open(file, "a") as code_output:
            code_output.write(str(code))

    # Enter a parse tree produced by stlgrammarParser#prog.
    def enterProg(self, ctx:stlgrammarParser.ProgContext):

        with open("runSTLcheck.py", "a") as code_output:
            code_output.write("\nimport os, sys, random")
            # code_output.write("\n\nx = [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1]")
            # code_output.write("\ny = [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1]")
            code_output.write("\n\nfrom functions import *")
            code_output.write("\n\nif __name__ == '__main__':")


    # Enter a parse tree produced by stlgrammarParser#Gcall.
    def enterGcall(self, ctx:stlgrammarParser.GcallContext):
        # get unique ID for this node
        uid = str(self.getUniqueId())
        # the function call that will use this UID
        func_call = "G_"+uid
        # boolean value associated with the satisfiability of this rule
        property_check = "G_"+uid+"_bool"

        # annotate the node with the vaeiables
        self.setUID(ctx, {"uid": uid, "func": func_call})

        implies = (ctx.implies() != None)         # ctx.globallyCall().implies()
        print("Implies G: {}".format(implies))


    # Exit a parse tree produced by stlgrammarParser#Gcall.
    def exitGcall(self, ctx:stlgrammarParser.GcallContext):
        code = "\n"

        code += "\n\ndef " + str(self.getUID(ctx)["func"]) + "(t):"

        code += "\n\tG_check_" + str(self.getUID(ctx)["uid"]) + "=True"

        # does this call have an associated timeslice with it
        if (ctx.timeslice() == None):
            code += "\n\tfor i in range(signal_length):"
        else:
            start_t = ctx.timeslice().start_t().getText().strip()
            end_t = ctx.timeslice().end_t().getText().strip()
            code += "\n\tfor t in range({}, {}):".format(start_t, end_t)

        # does the rule have implies
        implies = (ctx.implies() != None)

        before_check_call = self.getUID(ctx.stl(0))["func"] + "(t=t)"

        if not implies:
            code += "\n\t\tG_check_" + str(self.getUID(ctx)["uid"]) + " = " + before_check_call
            code += "\n\n\t\tif (G_check_" + str(self.getUID(ctx)["uid"]) + ") == False:"
            code += "\n\t\t\tbreak"

            code += "\n\n\t\telse:"
            code += "\n\t\t\tpass"

        code += "\n\treturn G_check_" +  str(self.getUID(ctx)["uid"])

        self.appendCode("functions.py", code)


    # Exit a parse tree produced by stlgrammarParser#GLOBALLY.
    def exitGLOBALLY(self, ctx:stlgrammarParser.GLOBALLYContext):
        self.setUID(ctx,self.getUID(ctx.getChild(0)))



        # Enter a parse tree produced by stlgrammarParser#STLFORMULA.
    def enterSTLFORMULA(self, ctx:stlgrammarParser.STLFORMULAContext):
        uid = str(self.getUniqueId())
        func_call = "Phi_" + uid
        self.setUID(ctx, {"uid": uid, "func": func_call})

        print("ParentRuleIndex: {} \n"
              "CurrentRuleIndex: {}"
              .format(ctx.parentCtx.getRuleIndex(), ctx.getRuleIndex()))


    # Exit a parse tree produced by stlgrammarParser#STLFORMULA.
    def exitSTLFORMULA(self, ctx:stlgrammarParser.STLFORMULAContext):

        child_list = list(ctx.getChildren())
        expr = self.getExpr(child_list[0])
        self.setExpr(ctx, expr)
        # print("Length of children: {}\n"
        #       "{}"
        #       .format(len(child_list), child_list))
        # print("Exp: {}" .format(self.getExpr(child_list[0])))

        code = ""
        code += "\n\ndef "+ str(self.getUID(ctx)["func"]) + "(t):"
        code += "\n\tif(" + expr + "):"
        code += "\n\t\treturn t"
        code += "\n\telse:"
        code += "\n\t\t return False"


        self.appendCode("functions.py", code)



    # Exit a parse tree produced by stlgrammarParser#propFormula.
    def exitPropFormula(self, ctx:stlgrammarParser.PropFormulaContext):
        self.setExpr(ctx, ctx.getText())

    # Exit a parse tree produced by stlgrammarParser#signalID.
    def exitSignalID(self, ctx: stlgrammarParser.SignalIDContext):
        '''

        :param ctx:
        :return:
        computes the signal value and appends to a unique list of all the signals used till now
        '''
        signal = ctx.getText()

        # if the signal name is being seen for the first time, add to global signal list
        if signal not in self.signals:
            self.signals.append(signal)

    # Exit a parse tree produced by stlgrammarParser#relOp.
    def exitRelOp(self, ctx:stlgrammarParser.RelOpContext):
        pass
        # print("RelOP: {} \t relopRuleIdx: {} \t relOPIdx: {} symbolicNames: {}".format(ctx.getText().strip(), ctx.getRuleIndex(), ctx.children[0].symbol.type, stlgrammarParser.symbolicNames[ctx.children[0].symbol.type]))

    # Exit a parse tree produced by stlgrammarParser#signalBrakedown.
    def exitSignalBrakedown(self, ctx:stlgrammarParser.SignalBrakedownContext):
        '''

        :param ctx:
        :return:
        for an input of
        ( NOT z[t] >= 25) should output: NOT (z[t] >= 25)
        x[t] > 12 should output:  x[t] > 12
        '''
        signal = ctx.signal().signalID().getText().strip()
        relOp = ctx.relOp().getText().strip()
        value = ctx.signalValue().getText().strip()
        expr = ''
        negation = ''

        if (ctx.NOT() != None):
            negation = ctx.NOT().getText().strip()
            
        expr = "({}({}[t] {} {}))".format(negation, signal, relOp, value)

        self.setExpr(ctx, expr)



    # Exit a parse tree produced by stlgrammarParser#signalFormula.
    def exitSignalFormula(self, ctx: stlgrammarParser.SignalFormulaContext):
        # print("{}".format(self.getExpr(ctx.signalComp())))
        self.setExpr(ctx, self.getExpr(ctx.signalComp()))

    # Exit a parse tree produced by stlgrammarParser#conjdisjFormula.
    def exitConjdisjFormula(self, ctx:stlgrammarParser.ConjdisjFormulaContext):
        before = self.getExpr(ctx.formula(0))
        andor = ctx.andorOp().getText().strip()
        after = self.getExpr(ctx.formula(1))

        expr = "({} {} {})".format(before, andor, after)
        # print("{}".format(expr))
        self.setExpr(ctx, expr)

    def exitUntilFormula(self, ctx: stlgrammarParser.UntilFormulaContext):
        theta = ctx.formula(0).getText().strip()
        phi = ctx.formula(1).getText().strip()
        time = ctx.timeslice().getText().strip()

        # expr = "({} {} {})".format(theta, time, phi)
        # print(expr)
        #
        # child_list = list(ctx.getChildren())
        # print("Length of children: {}\n"
        #       "{}"
        #       .format(len(child_list), child_list))
        #
        # formulas = list(ctx.formula())
        # print(formulas)
        #
        # print("Contents: \n1 - {} \n2 - {}".format(self.getExpr(formulas[0]), self.getExpr(formulas[1])))
        # print("Types: \n1 - {} \n2 - {}".format(formulas[0].getRuleIndex(), formulas[1].getRuleIndex()))

        expr = ''

        # check if the formula is simply a true false statement
        if theta not in ["True", "False"]:
            theta_NOT = ""
            theta_signal = ctx.formula(0).signalComp().signal().signalID().getText().strip()
            theta_relOp = ctx.formula(0).signalComp().relOp().getText().strip()
            theta_signalValue = ctx.formula(0).signalComp().signalValue().getText().strip()
            if (ctx.formula(0).signalComp().NOT() != None):
                theta_NOT = ctx.formula(0).signalComp().NOT().getText().strip()

            # print("({}({} {} {}))".format(theta_NOT, theta_signal, theta_relOp, theta_signalValue))

        # check if the formula is simply a true false statement
        if phi not in ["True", "False"]:
            phi_NOT = ""
            phi_signal = ctx.formula(1).signalComp().signal().signalID().getText().strip()
            phi_relOp = ctx.formula(1).signalComp().relOp().getText().strip()
            phi_signalValue = ctx.formula(1).signalComp().signalValue().getText().strip()
            if (ctx.formula(1).signalComp().NOT() != None):
                phi_NOT = ctx.formula(1).signalComp().NOT().getText().strip()

            # print("({}({} {} {}))".format(phi_NOT, phi_signal, phi_relOp, phi_signalValue))

        start_t = ctx.timeslice().start_t().getText().strip()
        end_t = ctx.timeslice().end_t().getText().strip()
        # print("From: {} - {}".format(start_t, end_t))

        if (phi not in ["True", "False"]) and (theta not in ["True", "False"]):
            expr = "(True if True in [True if (all({}(i {} {}) for i in {}[0:val])) else False for idx, val in enumerate([i for i in range({},{}) if ({}({}[i]{}{}))])] else False)".format(theta_NOT, theta_relOp, theta_signalValue, theta_signal, start_t, end_t, phi_NOT, phi_signal, phi_relOp, phi_signalValue)

        self.setExpr(ctx, expr)


    # Exit a parse tree produced by stlgrammarParser#prog.
    def exitProg(self, ctx:stlgrammarParser.ProgContext):
        tree_root = list(ctx.getChildren())                  # .getRuleIndex()   .children[0].symbol.type
        print("first_call: {}".format(tree_root))

        if (isinstance(tree_root[1] , antlr4.tree.Tree.TerminalNodeImpl)):
            print("Terminal node Reached")

        code = "\n\tstl_rule = " + str(self.getUID(tree_root[0].getChild(0))["func"]) + "(t=0)"

        code += "\n\tprint('STL rule was satisfied: {}'.format(stl_rule))"

        self.appendCode("runSTLcheck.py", code)


        proc = subprocess.Popen(
        ['chmod', '+x', 'functions.py', 'runSTLcheck.py'],
        stdout=subprocess.PIPE)
        (stdoutdata, stderrdata) = proc.communicate()