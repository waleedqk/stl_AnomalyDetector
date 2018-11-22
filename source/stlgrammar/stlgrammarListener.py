# Generated from stlgrammar.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .stlgrammarParser import stlgrammarParser
else:
    from stlgrammarParser import stlgrammarParser

# This class defines a complete listener for a parse tree produced by stlgrammarParser.
class stlgrammarListener(ParseTreeListener):

    # Enter a parse tree produced by stlgrammarParser#prog.
    def enterProg(self, ctx:stlgrammarParser.ProgContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#prog.
    def exitProg(self, ctx:stlgrammarParser.ProgContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#stlGlobalFormula.
    def enterStlGlobalFormula(self, ctx:stlgrammarParser.StlGlobalFormulaContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#stlGlobalFormula.
    def exitStlGlobalFormula(self, ctx:stlgrammarParser.StlGlobalFormulaContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#stlSignal.
    def enterStlSignal(self, ctx:stlgrammarParser.StlSignalContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#stlSignal.
    def exitStlSignal(self, ctx:stlgrammarParser.StlSignalContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#stlFormulaImplies.
    def enterStlFormulaImplies(self, ctx:stlgrammarParser.StlFormulaImpliesContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#stlFormulaImplies.
    def exitStlFormulaImplies(self, ctx:stlgrammarParser.StlFormulaImpliesContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#stlEventualFormula.
    def enterStlEventualFormula(self, ctx:stlgrammarParser.StlEventualFormulaContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#stlEventualFormula.
    def exitStlEventualFormula(self, ctx:stlgrammarParser.StlEventualFormulaContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#stlParens.
    def enterStlParens(self, ctx:stlgrammarParser.StlParensContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#stlParens.
    def exitStlParens(self, ctx:stlgrammarParser.StlParensContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#stlSignalComp.
    def enterStlSignalComp(self, ctx:stlgrammarParser.StlSignalCompContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#stlSignalComp.
    def exitStlSignalComp(self, ctx:stlgrammarParser.StlSignalCompContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#stlUntilFormula.
    def enterStlUntilFormula(self, ctx:stlgrammarParser.StlUntilFormulaContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#stlUntilFormula.
    def exitStlUntilFormula(self, ctx:stlgrammarParser.StlUntilFormulaContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#stlProp.
    def enterStlProp(self, ctx:stlgrammarParser.StlPropContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#stlProp.
    def exitStlProp(self, ctx:stlgrammarParser.StlPropContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#stlConjDisjFormula.
    def enterStlConjDisjFormula(self, ctx:stlgrammarParser.StlConjDisjFormulaContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#stlConjDisjFormula.
    def exitStlConjDisjFormula(self, ctx:stlgrammarParser.StlConjDisjFormulaContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#stlNotFormula.
    def enterStlNotFormula(self, ctx:stlgrammarParser.StlNotFormulaContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#stlNotFormula.
    def exitStlNotFormula(self, ctx:stlgrammarParser.StlNotFormulaContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#signalExpr.
    def enterSignalExpr(self, ctx:stlgrammarParser.SignalExprContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#signalExpr.
    def exitSignalExpr(self, ctx:stlgrammarParser.SignalExprContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#signalBool.
    def enterSignalBool(self, ctx:stlgrammarParser.SignalBoolContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#signalBool.
    def exitSignalBool(self, ctx:stlgrammarParser.SignalBoolContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#signalName.
    def enterSignalName(self, ctx:stlgrammarParser.SignalNameContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#signalName.
    def exitSignalName(self, ctx:stlgrammarParser.SignalNameContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#timerange.
    def enterTimerange(self, ctx:stlgrammarParser.TimerangeContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#timerange.
    def exitTimerange(self, ctx:stlgrammarParser.TimerangeContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#implies.
    def enterImplies(self, ctx:stlgrammarParser.ImpliesContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#implies.
    def exitImplies(self, ctx:stlgrammarParser.ImpliesContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#intExpr.
    def enterIntExpr(self, ctx:stlgrammarParser.IntExprContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#intExpr.
    def exitIntExpr(self, ctx:stlgrammarParser.IntExprContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#MulDivExpr.
    def enterMulDivExpr(self, ctx:stlgrammarParser.MulDivExprContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#MulDivExpr.
    def exitMulDivExpr(self, ctx:stlgrammarParser.MulDivExprContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#parensExpr.
    def enterParensExpr(self, ctx:stlgrammarParser.ParensExprContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#parensExpr.
    def exitParensExpr(self, ctx:stlgrammarParser.ParensExprContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#AddSubExpr.
    def enterAddSubExpr(self, ctx:stlgrammarParser.AddSubExprContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#AddSubExpr.
    def exitAddSubExpr(self, ctx:stlgrammarParser.AddSubExprContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#signalValue.
    def enterSignalValue(self, ctx:stlgrammarParser.SignalValueContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#signalValue.
    def exitSignalValue(self, ctx:stlgrammarParser.SignalValueContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#relOp.
    def enterRelOp(self, ctx:stlgrammarParser.RelOpContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#relOp.
    def exitRelOp(self, ctx:stlgrammarParser.RelOpContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#andorOp.
    def enterAndorOp(self, ctx:stlgrammarParser.AndorOpContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#andorOp.
    def exitAndorOp(self, ctx:stlgrammarParser.AndorOpContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#signalID.
    def enterSignalID(self, ctx:stlgrammarParser.SignalIDContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#signalID.
    def exitSignalID(self, ctx:stlgrammarParser.SignalIDContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#start_t.
    def enterStart_t(self, ctx:stlgrammarParser.Start_tContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#start_t.
    def exitStart_t(self, ctx:stlgrammarParser.Start_tContext):
        pass


    # Enter a parse tree produced by stlgrammarParser#end_t.
    def enterEnd_t(self, ctx:stlgrammarParser.End_tContext):
        pass

    # Exit a parse tree produced by stlgrammarParser#end_t.
    def exitEnd_t(self, ctx:stlgrammarParser.End_tContext):
        pass


