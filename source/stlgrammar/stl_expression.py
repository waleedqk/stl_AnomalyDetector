import os
import subprocess

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
        
        self.expr = {}


    def getExpr(self, ctx):
        return self.stack[ctx]

    def setExpr(self, ctx, value):
        self.stack[ctx] = value

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

        if signal not in self.signals:
            self.signals.append(signal)


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
            
        expr = "({}({}[i] {} {}))".format(negation, signal, relOp, value)

        # print(expr)
        self.setExpr(ctx, expr)


    # Exit a parse tree produced by stlgrammarParser#parensSignalFormula.
    def exitParensSignalFormula(self, ctx:stlgrammarParser.ParensSignalFormulaContext):
        # print("{}".format(self.getExpr(ctx.getChild(1))))
        self.setExpr(ctx, self.getExpr(ctx.getChild(1)))


    # Exit a parse tree produced by stlgrammarParser#signalFormula.
    def exitSignalFormula(self, ctx: stlgrammarParser.SignalFormulaContext):
        # print("{}".format(self.getExpr(ctx.getChild(0))))
        self.setExpr(ctx, self.getExpr(ctx.getChild(0)))

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

        if theta not in ["True", "False"]:
            theta_NOT = ""
            theta_signal = ctx.formula(0).signalComp().signal().signalID().getText().strip()
            theta_relOp = ctx.formula(0).signalComp().relOp().getText().strip()
            theta_signalValue = ctx.formula(0).signalComp().signalValue().getText().strip()
            if (ctx.formula(0).signalComp().NOT() != None):
                theta_NOT = ctx.formula(0).signalComp().NOT().getText().strip()

            # print("({}({} {} {}))".format(theta_NOT, theta_signal, theta_relOp, theta_signalValue))

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
