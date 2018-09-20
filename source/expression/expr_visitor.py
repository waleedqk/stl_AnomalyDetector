from expressionsVisitor import expressionsVisitor
from expressionsParser import expressionsParser

class expr_visitor(expressionsVisitor):
    def __init__(self):
        self.signals = {}
        self.rule_expression = []

    def visitInt(self, ctx):

        # evaluate the expr child
        value = ctx.INT().getText()
        return value

    def visitId(self, ctx):
        # evaluate the expr child
        name = ctx.ID().getText()
        return name

    def visitParensExpr(self, ctx):
        # return child expr's value
        return self.visit(ctx.signalComp())

    # expr 'U' '[' INT ',' INT ']' expr
    def visitUntilExpr(self, ctx):
        # print("{}".format(ctx.getText()))
        return self.visit(ctx.untilTL())

    def visitUntil(self, ctx):
        # get value of left subexpression
        left = self.visit(ctx.signalComp(0))

        # get value of right subexpression
        right = self.visit(ctx.signalComp(1))

        # get the time range for the until expression
        time = self.visit(ctx.timeslice())

    def visitTimerange(self, ctx):

        from_time = ctx.INT(0).getText()

        till_time = ctx.INT(1).getText()

        print("Until time range({} - {})".format(from_time, till_time))

    # x[t] > 10
    def visitSignalExpr(self, ctx):
        # print("{}".format(ctx.getText()))

        return self.visit(ctx.signalComp())


    # x[t] > 10
    def visitSignalBrakedown(self, ctx):

        name = ctx.signal().getText()
        print("{}".format(name))     # x[t]

        operator = ctx.relOp().getText()
        print("{}".format(operator))     # >

        value = ctx.INT().getText()
        print("{}".format(value))  # 10

        print("ParentRuleIndex: {} \n"
              "CurrentRuleIndex: {}"
              .format(ctx.parentCtx.getRuleIndex(), ctx.getRuleIndex()))

        # if ctx.relOp.type == expressionsParser.OP_GT:
        #     print("Operator check passed")