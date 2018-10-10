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
        Index for beginning of all type of stl rules 
        '''
        # self.ruleBegin = [stlgrammarParser.RULE_globallyeventuallyCall, stlgrammarParser.RULE_eventuallygloballyCall, stlgrammarParser.RULE_globallyCall, stlgrammarParser.RULE_eventuallyCall]

        with open("runSTLcheck.py", "w") as code_output:
            code_output.write("\nfrom data import *")

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


    # Enter a parse tree produced by stlgrammarParser#prog.
    def enterProg(self, ctx:stlgrammarParser.ProgContext):
        '''
        Initialization steps at the beginning of the file
        :param ctx:
        :return:
        '''
        with open("runSTLcheck.py", "a") as code_output:
            code_output.write("\nimport os, sys, random")
            code_output.write("\n\nfrom functions import *")
            code_output.write("\n\nif __name__ == '__main__':")


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

    # Exit a parse tree produced by stlgrammarParser#intExpr.
    def exitIntExpr(self, ctx:stlgrammarParser.IntExprContext):
        '''
        Get the integer value of the expression: 4
        :param ctx:
        :return:
        '''
        integer_val = ctx.INT().getText().strip()
        # print(integer_val)

        self.setExpr(ctx, integer_val)


    # Exit a parse tree produced by stlgrammarParser#andorOp.
    def exitAndorOp(self, ctx:stlgrammarParser.AndorOpContext):
        '''

        :param ctx:
        :return:
        '''
        andor = ctx.getText().strip()
        self.setExpr(ctx, andor)

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

        SignalExpr = "({} {} {})".format(signal, relOp, expr)
        # print(SignalExpr)

        self.setExpr(ctx, SignalExpr)

    # Exit a parse tree produced by stlgrammarParser#signalBool.
    def exitSignalBool(self, ctx:stlgrammarParser.SignalBoolContext):
        '''
        parse the signalBool: a == True, (False != a)
        :param ctx:
        :return:
        '''

        signal = self.getExpr(ctx.signal())
        relOp = ctx.relOp().getText().strip()
        boolVal = ctx.Bool().getText().strip()

        SignalBool = "({} {} {})".format(signal, relOp, boolVal)
        # print(SignalBool)

        self.setExpr(ctx, SignalBool)

    # Exit a parse tree produced by stlgrammarParser#parensFormula.
    def exitParensFormula(self, ctx:stlgrammarParser.ParensFormulaContext):
        '''
        get the formula stored in the parenthesis
        :param ctx:
        :return:
        '''
        # print("The SignalFormula in parens is: {}".format(self.getExpr(ctx.formula())))
        self.setExpr(ctx, self.getExpr(ctx.formula()))

    # Exit a parse tree produced by stlgrammarParser#signalNegFormula.
    def exitSignalNegFormula(self, ctx:stlgrammarParser.SignalNegFormulaContext):
        '''
        process the negation of a formula: will only have a single formula child associated with it
        :param ctx:
        :return:
        '''

        SignalFormula = "(not({}))".format(self.getExpr(ctx.formula()))
        # print("The signalNegFormula is: {}".format(SignalFormula))

        self.setExpr(ctx, SignalFormula)

    # Exit a parse tree produced by stlgrammarParser#propFormula.
    def exitPropFormula(self, ctx:stlgrammarParser.PropFormulaContext):
        '''
        stand alone boolean expression: True or False
        :param ctx:
        :return:
        '''
        # print(ctx.Bool().getText().strip())
        self.setExpr(ctx, ctx.Bool().getText().strip())

    # Exit a parse tree produced by stlgrammarParser#signalProp.
    def exitSignalProp(self, ctx:stlgrammarParser.SignalPropContext):
        '''
        process 'not(a)', '(a)' type
        :param ctx:
        :return:
        '''

        negation = ''
        if (ctx.NOT() != None):
            negation = ctx.NOT().getText().strip()

        signal = self.getExpr(ctx.signal())
        signalProp = "({}({}))".format(negation, signal)

        # print("The signalProp is: {}".format(signalProp))
        self.setExpr(ctx, signalProp)

    # Exit a parse tree produced by stlgrammarParser#signalFormula.
    def exitSignalFormula(self, ctx:stlgrammarParser.SignalFormulaContext):
        '''
        signalFormula has signalComp as a child which can be either signalBool or signalExpr
        :param ctx:
        :return:
        '''

        # print("The SignalFormula is: {}".format(self.getExpr(ctx.signalComp())))
        self.setExpr(ctx, self.getExpr(ctx.signalComp()))


    # Exit a parse tree produced by stlgrammarParser#conjdisjFormula.
    def exitConjdisjFormula(self, ctx:stlgrammarParser.ConjdisjFormulaContext):
        '''
        parse: formula and formula
        :param ctx:
        :return:
        '''
        before = self.getExpr(ctx.formula(0))
        andorOp = self.getExpr(ctx.andorOp())
        after = self.getExpr(ctx.formula(1))

        conjdisjFormula = "({} {} {})".format(before, andorOp, after)
        # print(conjdisjFormula)

        self.setExpr(ctx, conjdisjFormula)

    # Exit a parse tree produced by stlgrammarParser#untilFormula.
    def exitUntilFormula(self, ctx:stlgrammarParser.UntilFormulaContext):
        '''

        :param ctx:
        :return:
        '''
        theta = self.getExpr(ctx.formula(0))
        phi = self.getExpr(ctx.formula(1))


        start_t = ctx.timeslice().start_t().getText().strip()
        end_t = ctx.timeslice().end_t().getText().strip()

        formula = "{}-{}".format(end_t, start_t)
        self.setExpr(ctx, formula)






    # Exit a parse tree produced by stlgrammarParser#stlFormula.
    def exitStlFormula(self, ctx:stlgrammarParser.StlFormulaContext):
        '''

        :param ctx:
        :return:
        '''

        self.setExpr(ctx, self.getExpr(ctx.formula()))

    # Exit a parse tree produced by stlgrammarParser#prog.
    def exitProg(self, ctx:stlgrammarParser.ProgContext):
        '''

        :param ctx:
        :return:
        '''

        formula = self.getExpr(ctx.stl())
        self.finalProg = formula
        # print("The final formula is: {}".format(formula))