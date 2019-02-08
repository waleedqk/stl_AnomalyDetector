import os
import subprocess
import random
import numpy as np
import pandas as pd
import antlr4
from stlgrammarLexer import stlgrammarLexer
from stlgrammarParser import stlgrammarParser
from stlgrammarListener import stlgrammarListener

class stlgrammarSimplifier(stlgrammarListener):
    def __init__(self):
        '''
        The original STL rule stored as a string value
        '''
        self.stlOrigRule = ""

        '''
        The new STL rule 
        that has the transformation for implies, F, G to the basic operators
        stored as a string value
        '''
        self.stlNewRule = ""

        '''
        a dict to annotate the nodes with the required content
        the key is the unique ctx made by antlr during the parsing
        '''
        self.stack = {}

        '''
        The maximum time range that can be put to a STL rule
        '''
        self.time_max = 20



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
        self.stlOrigRule = ctx.stlFormula().getText().strip()

    # Exit a parse tree produced by stlgrammarParser#prog.
    def exitProg(self, ctx:stlgrammarParser.ProgContext):
        '''

        :param ctx:
        :param value:
        :return:
        '''
        self.stlNewRule = self.getExpr(ctx.stlFormula())
        print("Final Updated rule: {}".format(self.stlNewRule))


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
            timeSlice = ctx.timeSlice().getText().strip()
        else:
            timeSlice = "[0, {}]".format(self.time_max)

        stlFormula = self.getExpr(ctx.stlFormula())

        stlGlobalFormula = "not( True U {} (not({})))".format(timeSlice, stlFormula)

        self.setExpr(ctx, stlGlobalFormula)

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
            timeSlice = ctx.timeSlice().getText().strip()
        else:
            timeSlice = "[0, {}]".format(self.time_max)

        stlFormula = self.getExpr(ctx.stlFormula())

        stlEventualFormula = "True U {} ({})".format(timeSlice, stlFormula)

        self.setExpr(ctx, stlEventualFormula)


    # Exit a parse tree produced by stlgrammarParser#stlFormulaImplies.
    def exitStlFormulaImplies(self, ctx:stlgrammarParser.StlFormulaImpliesContext):
        '''
        a -> b === not(a) or b === not(not(a) and b)
        :param ctx:
        :param value:
        :return:
        '''

        stlFormula_phi = self.getExpr(ctx.stlFormula(0))
        stlFormula_phe = self.getExpr(ctx.stlFormula(1))

        stlFormulaImplies = "not(not({}) and {})".format(stlFormula_phi, stlFormula_phe)

        self.setExpr(ctx, stlFormulaImplies)

    # Exit a parse tree produced by stlgrammarParser#stlConjDisjFormula.
    def exitStlConjDisjFormula(self, ctx:stlgrammarParser.StlConjDisjFormulaContext):
        '''
        a or b = not(a and b)
        :param ctx:
        :return:
        '''

        stlFormula_phi = self.getExpr(ctx.stlFormula(0))
        andorOp = ctx.andorOp().getText().strip()
        stlFormula_phe = self.getExpr(ctx.stlFormula(1))

        if andorOp == 'or':
            stlConjDisjFormula = "not ({} and {})".format(stlFormula_phi, stlFormula_phe)
        else:
            stlConjDisjFormula = "{} {} {}".format(stlFormula_phi, andorOp, stlFormula_phe)

        self.setExpr(ctx, stlConjDisjFormula)

    # Exit a parse tree produced by stlgrammarParser#stlUntilFormula.
    def exitStlUntilFormula(self, ctx:stlgrammarParser.StlUntilFormulaContext):
        '''

        :param ctx:
        :return:
        '''

        timeSlice = ctx.timeSlice().getText().strip()
        stlFormula_phi = self.getExpr(ctx.stlFormula(0))
        stlFormula_phe = self.getExpr(ctx.stlFormula(1))

        stlUntilFormula = "{} U {} {}".format(stlFormula_phi, timeSlice, stlFormula_phe)
        self.setExpr(ctx, stlUntilFormula)


    # Exit a parse tree produced by stlgrammarParser#stlNotFormula.
    def exitStlNotFormula(self, ctx:stlgrammarParser.StlNotFormulaContext):
        '''

        :param ctx:
        :param value:
        :return:
        '''

        stlFormula = self.getExpr(ctx.stlFormula())

        stlNotFormula = "not ({})".format(stlFormula)
        self.setExpr(ctx, stlNotFormula)


    # Exit a parse tree produced by stlgrammarParser#stlSignalComp.
    def exitStlSignalComp(self, ctx:stlgrammarParser.StlSignalCompContext):
        '''

        :param ctx:
        :param value:
        :return:
        '''

        # Get the name of the function associated with the call
        self.setExpr(ctx, self.getExpr(ctx.getChild(0)))

    # Exit a parse tree produced by stlgrammarParser#stlSignal.
    def exitStlSignal(self, ctx:stlgrammarParser.StlSignalContext):
        '''

        :param ctx:
        :return:
        '''
        self.setExpr(ctx, ctx.signalID().getText().strip())


    # Exit a parse tree produced by stlgrammarParser#stlProp.
    def exitStlProp(self, ctx:stlgrammarParser.StlPropContext):
        '''

        :param ctx:
        :return:
        '''
        boolVal = ctx.getText().strip()
        self.setExpr(ctx, boolVal)

    # Exit a parse tree produced by stlgrammarParser#stlParens.
    def exitStlParens(self, ctx:stlgrammarParser.StlParensContext):
        '''

        :param ctx:
        :param value:
        :return:
        '''

        stlFormula = "({})".format(self.getExpr(ctx.stlFormula()))
        # print("stlFormula: {}".format(stlFormula))

        self.setExpr(ctx, stlFormula)

    # Exit a parse tree produced by stlgrammarParser#signalExpr.
    def exitSignalExpr(self, ctx:stlgrammarParser.SignalExprContext):
        '''
        parse the signalExpr: a < 54, ((4/63) < a)
        :param ctx:
        :return:
        '''

        signal = self.getExpr(ctx.signal())
        relOp = ctx.relOp().getText().strip()
        expr = ctx.expr().getText().strip()

        '''
        the rule matches both  a > 5 && 5 < a, since the rule is: 
        signal relOp expr                             # signalExpr
        | expr relOp signal                           # signalExpr

        to change it to an the standard expression being used here need to find out which child is the expr child
        It can either be the first or the last (0 or 2), so we start of with the only wrong value of 1
        '''
        expr_loc = 1
        if (ctx.getChild(0).getRuleIndex() == stlgrammarParser.RULE_signal):
            expr_loc = 0

        if (ctx.getChild(2).getRuleIndex() == stlgrammarParser.RULE_signal):
            expr_loc = 2

        '''
        if the expression is the second value, we will change the orientation to match the style of:
        signal relOp expr 
        '''
        if (expr_loc == 2):
            switchCase = {
                '<': '>',
                '>': '<',
                '>=': '<=',
                '<=': '>='
            }
            relOp = switchCase.get(relOp, "==")

        expr = "{} {} {}".format(signal, relOp, expr)
        # print("SignalExpr: {}".format(expr))

        self.setExpr(ctx, expr)



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

        expr = "{} {} {}".format(signal, relOp, boolVal)
        print("SignalBool: {}".format(expr))

        self.setExpr(ctx, expr)

    # Exit a parse tree produced by stlgrammarParser#signalName.
    def exitSignalName(self, ctx:stlgrammarParser.SignalNameContext):
        '''
        Get the signal name associated with the node
        Should only have one child
        :param ctx:
        :return:
        '''

        # print("The signal name is: {}".format(self.getExpr(ctx)))
        self.setExpr(ctx, ctx.signalID().getText().strip())
