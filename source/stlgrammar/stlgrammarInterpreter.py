import os
import subprocess
import random
import numpy as np 
import pandas as pd 
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
        There is a time depth associated with operators 
        We want to keep the longest possible time depth for the a given correctness property
        '''
        self.time_depth = {}

        '''
        at any given node we want access to the entire rule being processed by that node
        in a string format - to label the curve in the final plots
        '''
        self.rule_tree = {}

        '''
        keeps a unique list of all the signals being used in the stl rules from the input data
        '''
        self.signals = ["Time"]

        '''
        list of all the columns that the final dataframe should have
        this should include the self.signals
        and all the function call columns that are going to be presented for diagnostics
        '''
        self.output_signals = []


        '''
        List of unique ID's associated with all the function calls
        '''
        self.uids = {}

        '''
        output code file name
        '''
        self.outputCode_file = "runSTLcheck.py"
        # clear contents of file
        open(self.outputCode_file, 'w').close()


        '''
        A dictionary:
        key: the function name
        value: the expression that is being processind in the function
        '''
        self.signal_dict = {}

    def appendCode(self, code, file=None):
        '''
        Appends text to a file
        :param file: the name of the file to append the text to - defaults to self.outputCode_file
        :param code: the string that needs to be appended to the file
        :return:
        '''

        if file is None:
            file = self.outputCode_file


        with open(file, "a") as code_output:
            code_output.write(str(code))


    def getUniqueId(self):
        '''
        generate a random number between 100 and 999, which has not been already generated
        :return: number

        https://stackoverflow.com/questions/9807634/find-all-occurrences-of-a-key-in-nested-python-dictionaries-and-lists

        '''
        number = str(random.sample(range(100, 999),1)[0])

        already_used_uids = []
        if self.uids:
            for key, value in self.uids.items():
                already_used_uids.append(self.uids[key]['uid'])


        while (number in already_used_uids):     # self.uids.values()
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


    def get_timeDepth(self, ctx):
        '''

        :param ctx:
        :return:
        '''
        return self.time_depth[ctx]


    def set_timeDepth(self, ctx, value):
        '''

        :param ctx:
        :param value:
        :return:
        '''
        self.time_depth[ctx] = int(value)

    def get_rule_tree(self, ctx):
        '''

        :param ctx: the node to whose contents need to be retrieved
        :return:
        '''
        return self.rule_tree[ctx]

    def set_rule_tree(self, ctx, value):
        '''

        :param ctx: the node which we need to annotate. Becomes the key to the dict value
        :param value: the value we want to annotate the node with
        :return:
        '''
        self.rule_tree[ctx] = value



    def funcUIDgen(self, func_prepend="_"):
        '''
        Generate the unique ID and the function call that will use this UID for nodes
        :param func_prepend: The function constant that will prepend the unique ID, e.g. func_prepend="StlGlobal_"
        :return: uid, func_call = 289, StlGlobal_289
        '''

        # get unique ID 
        uid = str(self.getUniqueId()).strip()

        # the function call that will be used with this UID
        func_call = func_prepend.strip() + uid.strip()

        return (uid, func_call)

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

        annotated_rule = self.get_rule_tree(ctx.stlFormula())
        print("annotated_rule: {}".format(annotated_rule))

        timeDepth = int(self.get_timeDepth(ctx.stlFormula()))
        print("Total signal length required for rule: {}".format(timeDepth))

        # add the signal list from the input data to the column names of the dataframe to be created
        self.output_signals.extend(self.signals)

        # convert the list of string in a list to a comma seperated single string variable
        input_signal_list_string = ', '.join('"{0}"'.format(signal) for signal in self.signals)
        output_signal_list_string = ', '.join('"{0}"'.format(signal) for signal in self.output_signals)


        code = ""
        code += "\nimport os, sys, random"
        code += "\nimport numpy as np"
        code += "\nimport pandas as pd"
        code += "\n\n"
        code += "\ndf = pd.DataFrame(columns=[{}])".format(output_signal_list_string)
        code += "\n\n"
        code += "\ninput_data_df = pd.read_csv('input_data.csv', sep=',', usecols=[{}])".format(input_signal_list_string)
        code += "\ninput_data_df = input_data_df.reset_index(drop=True)"
        code += "\n\nfor col in list(input_data_df.columns.values):"
        code += "\n\tdf[col] = input_data_df[col]"
        code += "\n\ndf.fillna(0, inplace=True)"
        code += "\n\ndel input_data_df"

        with open(self.outputCode_file, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(code.rstrip('\r\n') + '\n' + content)

        code = ""
        code += "\n\nif __name__ == '__main__':"
        code += "\n\tstl_rule = " + first_call + "(t=0)"
        code += "\n\tprint('Checking STL rule: {}')".format(self.stlString)
        code += "\n\tprint('STL rule was satisfied: {}'.format(stl_rule))"
        code += "\n\tdf.to_csv('dataframe_populated.csv', sep=',', index=False)"

        self.appendCode(code)

        proc = subprocess.Popen(
        ['chmod', '+x', str(self.outputCode_file)],
        stdout=subprocess.PIPE)
        (stdoutdata, stderrdata) = proc.communicate()

        # Store the rule as part of the dict - to show on the plot
        self.signal_dict['STL_rule'] = self.stlString

        # save the signal_dict to a file
        np.save('signal_dict.npy', self.signal_dict)


    # Enter a parse tree produced by stlgrammarParser#stlConjDisjFormula.
    def enterStlConjDisjFormula(self, ctx:stlgrammarParser.StlConjDisjFormulaContext):
        '''
        a or b = not(a and b)
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
        a or b = not(a and b)
        (F[5,6]((4/63) < b)) and G[3,4](a > 25)
        :param ctx:
        :param value: 
        :return:
        '''
        before = self.getExpr(ctx.stlFormula(0))
        andorOp = self.getExpr(ctx.andorOp())
        after = self.getExpr(ctx.stlFormula(1))

        conjdisjFormula = "({}(t=t) {} {}(t=t))".format(before, andorOp, after)    # due to the adition of the simplifier the andorOp will always be an 'and'
        # print(conjdisjFormula)


        self.set_rule_tree(ctx, "{} {} {}".format(
            self.get_rule_tree(ctx.stlFormula(0)),
            andorOp,
            self.get_rule_tree(ctx.stlFormula(1))
        ))

        # get the function call for this node: StlConjDisj_611
        func_call = self.getUID(ctx)["func"]

        # add the function call as a column name to be added in the dataframe
        # self.df[func_call] = 0
        self.output_signals.append(func_call)

        # update the signal dictionary with the function call 
        self.signal_dict[func_call] = self.get_rule_tree(ctx)   # "{}".format(conjdisjFormula)

        code = "\n"
        code += "\n\ndef " + str(func_call) + "(t=0):"
        code += "\n\tif({} == True):".format(conjdisjFormula)
        code += "\n\t\tdf.loc[df.Time == t, '{}'] = 1".format(func_call)
        code += "\n\t\treturn True"
        code += "\n\telse:"
        code += "\n\t\tdf.loc[df.Time == t, '{}'] = -1".format(func_call)
        code += "\n\t\treturn False"

        self.appendCode(code)

        # set the time depth for the formula
        self.set_timeDepth(ctx, max( int(self.get_timeDepth(ctx.stlFormula(0))), int(self.get_timeDepth(ctx.stlFormula(1))) )  )


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

        self.set_rule_tree(ctx, "{} U [{}, {}] {}".format(
            self.get_rule_tree(ctx.stlFormula(0)),
            start_t,
            end_t,
            self.get_rule_tree(ctx.stlFormula(1))
        ))

        # get the function call for this node: StlUntil_611
        func_call = self.getUID(ctx)["func"]

        # add the function call as a column name to be added in the dataframe
        self.output_signals.append(func_call)

        # update the signal dictionary with the function call
        self.signal_dict[func_call] = self.get_rule_tree(ctx)   # "{} U [{}, {}] {}".format(stlFormula_phi, start_t, end_t, stlFormula_phe)

        code = "\n"
        code += "\n\ndef " + str(func_call) + "(t=0):"
        code += "\n\tuntil_check = False"
        code += "\n\ttime_phe = df.loc[(df['Time'] >= (t+{})) & (df['Time'] <= (t+{})), 'Time'].values.tolist()".format(start_t, end_t)
        code += "\n\tfor i in time_phe:"
        code += "\n\t\tif ({}(t=i)):".format(stlFormula_phe)
        code += "\n\t\t\tuntil_check = True"
        code += "\n\t\t\tbreak"
        code += "\n\tif (until_check):"
        code += "\n\t\ttime_phi = [m for m in time_phe if m >= i]"
        code += "\n\t\tfor j in time_phi:"
        code += "\n\t\t\tif(not ({}(t=j))):".format(stlFormula_phi)
        code += "\n\t\t\t\tuntil_check = False"
        code += "\n\tif (until_check):"
        code += "\n\t\tdf.loc[(df['Time'] >= (t+{})) & (df['Time'] <= (t+{})), '{}'] = 1".format(start_t, end_t, func_call)
        code += "\n\t\treturn True"
        code += "\n\telse:"
        code += "\n\t\tdf.loc[(df['Time'] >= (t+{})) & (df['Time'] <= (t+{})), '{}'] = -1".format(start_t, end_t,
                                                                                                 func_call)
        code += "\n\t\treturn False"

        self.appendCode(code)

        # set the time depth for the formula
        self.set_timeDepth(ctx, int(end_t) + max( int(self.get_timeDepth(ctx.stlFormula(0))), int(self.get_timeDepth(ctx.stlFormula(1))) )  )




    # Enter a parse tree produced by stlgrammarParser#stlNotFormula.
    def enterStlNotFormula(self, ctx:stlgrammarParser.StlNotFormulaContext):
        '''
        NOT '(' stlFormula ')' 
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
        NOT '(' stlFormula ')' 
        :param ctx:
        :param value: 
        :return:
        '''
        stlFormula = self.getExpr(ctx.stlFormula())

        self.set_rule_tree(ctx, "not({})".format(
            self.get_rule_tree(ctx.stlFormula())
        ))

        # get the function call for this node: signalComp_611
        func_call = self.getUID(ctx)["func"]

        # add the function call as a column name to be added in the dataframe
        # self.df[func_call] = 0
        self.output_signals.append(func_call)

        # update the signal dictionary with the function call 
        self.signal_dict[func_call] = self.get_rule_tree(ctx)    #  "not({}[t]) == True".format(stlFormula)

        # generate code that is associated with an stlNotFormula formula: NOT '(' stlFormula ')' 
        code = "\n"
        code += "\n\ndef " + str(func_call) + "(t=0):"
        code += "\n\tif( not( {}(t=t) )):".format(stlFormula)
        code += "\n\t\tdf.loc[df.Time == t, '{}'] = 1".format(func_call)
        code += "\n\t\treturn True"
        code += "\n\telse:"
        code += "\n\t\tdf.loc[df.Time == t, '{}'] = -1".format(func_call)
        code += "\n\t\treturn False"

        self.appendCode(code)

        # set the time depth for the formula
        self.set_timeDepth(ctx, self.get_timeDepth(ctx.stlFormula()))


    # Exit a parse tree produced by stlgrammarParser#stlSignalComp.
    def exitStlSignalComp(self, ctx:stlgrammarParser.StlSignalCompContext):
        '''
        grammar:   signal relOp expr   |   signal relOp Bool
        :param ctx:
        :param value: 
        :return:
        '''

        # Get the name of the function associated with the call
        self.setExpr(ctx, self.getExpr(ctx.getChild(0)))
        # print("signalComp: {}".format(self.getExpr(ctx.getChild(0))))

        # set the time depth for the formula
        self.set_timeDepth(ctx, self.get_timeDepth(ctx.getChild(0)))

        self.set_rule_tree(ctx, self.get_rule_tree(ctx.getChild(0)))



    # Enter a parse tree produced by stlgrammarParser#stlSignal.
    def enterStlSignal(self, ctx:stlgrammarParser.StlSignalContext):
        '''
        grammar: signal = signalID
        Getting a single signal value as a formula: x | x[t]
        :param ctx:
        :return:
        '''
        signal = ctx.signal().getText().strip().replace("(","").replace(")","").replace("[t]","")

        print("signal: {}".format(signal))

        self.set_rule_tree(ctx, signal)

        # get unique ID and the function call that will use this UID for this node
        uid, func_call = self.funcUIDgen(func_prepend="StlSignal_")

        # annotate the node with the variables
        self.setUID(ctx, {"uid": uid, "func": func_call})

        # signal calls will only be referred to with their appointed function calls 
        self.setExpr(ctx, func_call)

        # add the function call as a column name to be added in the dataframe
        # self.df[func_call] = 0
        self.output_signals.append(func_call)

        # update the signal dictionary with the function call and expression string
        self.signal_dict[func_call] = "{}[t] == True".format(signal)

        code = "\n"
        code += "\n\ndef " + func_call + "(t=0):"
        code += "\n\tif(df.loc[df['Time'] == t, '{}'].iloc[0] == True):".format(signal)
        code += "\n\t\tdf.loc[df.Time == t, '{}'] = 1".format(func_call)
        code += "\n\t\treturn True"
        code += "\n\telse:"
        code += "\n\t\tdf.loc[df.Time == t, '{}'] = -1".format(func_call)
        code += "\n\t\treturn False"

        self.appendCode(code)

        # set the time depth for the formula
        self.set_timeDepth(ctx, 0)


    # Enter a parse tree produced by stlgrammarParser#stlProp.
    def enterStlProp(self, ctx:stlgrammarParser.StlPropContext):
        '''
        grammar: True | False
        Getting a single boolean prop as a formula: True
        :param ctx:
        :return:
        '''

        # Get the proposition and remove any parenthsis if it has any
        boolVal = ctx.Bool().getText().strip().replace("(","").replace(")","")

        # get unique ID and the function call that will use this UID for this node
        uid, func_call = self.funcUIDgen(func_prepend="stlProp_")

        # annotate the node with the variables
        self.setUID(ctx, {"uid": uid, "func": func_call})

        # signal calls will only be referred to with their appointed function calls 
        self.setExpr(ctx, func_call)

        self.set_rule_tree(ctx,boolVal)

        # add the function call as a column name to be added in the dataframe
        self.output_signals.append(func_call)

        # update the signal dictionary with the function call and expression string
        self.signal_dict[func_call] = "{} == True".format(boolVal)


        # generate code that is associated with an stlProp formula: True, False
        code = "\n"
        code += "\n\ndef " + func_call + "(t=0):"
        code += "\n\tif({} == True):".format(boolVal)
        code += "\n\t\tdf.loc[df.Time == t, '{}'] = 1".format(func_call)
        code += "\n\t\treturn True"
        code += "\n\telse:"
        code += "\n\t\tdf.loc[df.Time == t, '{}'] = -1".format(func_call)
        code += "\n\t\treturn False"        

        self.appendCode(code)

        # set the time depth for the formula
        self.set_timeDepth(ctx, 0)


    # Exit a parse tree produced by stlgrammarParser#stlParens.
    def exitStlParens(self, ctx:stlgrammarParser.StlParensContext):
        '''
        grammar: '(' stlFormula ')'
        :param ctx:
        :param value: 
        :return:
        '''

        stlFormula = self.getExpr(ctx.stlFormula())
        # print("stlFormula: {}".format(stlFormula))

        # set formula call to the node of the parenthesis
        self.setExpr(ctx, stlFormula)


        # set the time depth for the formula
        self.set_timeDepth(ctx, self.get_timeDepth(ctx.stlFormula()))

        self.set_rule_tree(ctx, "({})".format(self.get_rule_tree(ctx.stlFormula())))





















    # Enter a parse tree produced by stlgrammarParser#signalExpr.
    def enterSignalExpr(self, ctx:stlgrammarParser.SignalExprContext):
        '''
        grammar: signal relOp expr
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
        grammar: signal relOp expr
        parse the signalExpr: a < 54, ((4/63) < a)
        :param ctx:
        :return:
        '''

        signal = self.getExpr(ctx.signal())
        relOp = ctx.relOp().getText().strip()
        expr = self.getExpr(ctx.expr())

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
            relOp = switchCase.get(relOp,"==")


        self.set_rule_tree(ctx, "{}[t] {} {}".format(
            self.get_rule_tree(ctx.signal()),
            relOp,
            self.get_rule_tree(ctx.expr())
        ))

        # get the function call for this node: signalComp_611
        func_call = self.getUID(ctx)["func"]

        # add the function call as a column name to be added in the dataframe
        self.output_signals.append(func_call)

        # update the signal dictionary with the function call and expression string
        self.signal_dict[func_call] = "{}[t] {} {}".format(signal, relOp, expr)

        # generate code that is associated with a signalExpr expr: a < 54, ((4/63) < a)
        code = "\n"
        code += "\n\ndef " + str(func_call) + "(t=0):"
        # code += "\n\tif({}[t] {} {}):".format(signal, relOp, expr)
        code += "\n\tif(df.loc[df['Time'] == t, '{}'].iloc[0] {} {}):".format(signal, relOp, expr)
        code += "\n\t\tdf.loc[df.Time == t, '{}'] = 1".format(func_call)          
        code += "\n\t\treturn True"
        code += "\n\telse:"
        code += "\n\t\tdf.loc[df.Time == t, '{}'] = -1".format(func_call)
        code += "\n\t\treturn False"

        self.appendCode(code)

        # set the time depth for the formula
        self.set_timeDepth(ctx, 0)


    # Enter a parse tree produced by stlgrammarParser#signalBool.
    def enterSignalBool(self, ctx:stlgrammarParser.SignalBoolContext):
        '''
        grammar: Bool relOp signal
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
        grammar: Bool relOp signal
        parse the signalBool: a == True, (False != a)
        :param ctx:
        :return:
        '''

        signal = self.getExpr(ctx.signal())
        relOp = ctx.relOp().getText().strip()
        boolVal = ctx.Bool().getText().strip().replace("(","").replace(")","")

        self.set_rule_tree(ctx, "{}[t] {} {}".format(
            self.get_rule_tree(ctx.signal()),
            relOp,
            boolVal
        ))

        # print("SignalBool: {}".format(self.getExpr(ctx)))

        # get the function call for this node: signalComp_611
        func_call = self.getUID(ctx)["func"]

        # add the function call as a column name to be added in the dataframe
        self.output_signals.append(func_call)

        # update the signal dictionary with the function call and expression string
        self.signal_dict[func_call] = "{}[t] {} {}".format(signal, relOp, boolVal)

        # generate code that is associated with a signalBool expr:  a == True, (False != a)
        code = "\n"
        code += "\n\ndef " + str(func_call) + "(t=0):"
        code += "\n\tif(df.loc[df['Time'] == t, '{}'].iloc[0] {} {}):".format(signal, relOp, boolVal)
        code += "\n\t\tdf.loc[df.Time == t, '{}'] = 1".format(func_call)
        code += "\n\t\treturn True"
        code += "\n\telse:"
        code += "\n\t\tdf.loc[df.Time == t, '{}'] = -1".format(func_call)
        code += "\n\t\treturn False"
        
        
        self.appendCode(code)

        # set the time depth for the formula
        self.set_timeDepth(ctx, 0)













    # Exit a parse tree produced by stlgrammarParser#signalName.
    def exitSignalName(self, ctx:stlgrammarParser.SignalNameContext):
        '''
        grammar: signalID'[t]'  |  signalID
        Get the signal name associated with the node
        Should only have one child
        :param ctx:
        :return:
        '''

        # print("The signal name is: {}".format(self.getExpr(ctx)))
        self.setExpr(ctx, self.getExpr(ctx.signalID()))

        self.set_rule_tree(ctx, self.get_rule_tree(ctx.signalID()))

    # Exit a parse tree produced by stlgrammarParser#signalID.
    def exitSignalID(self, ctx:stlgrammarParser.SignalIDContext):
        '''
        grammar: ID
        Update the dict self.signals with unique signals used in the stl rules
        e.g. a, x, time, trigger
        :param ctx:
        :return:
        '''
        signal = ctx.getText()

        self.setExpr(ctx, signal)

        self.set_rule_tree(ctx, signal)

        # if the signal name is being seen for the first time, add to global signal list
        if signal not in self.signals:
            self.signals.append(signal)

            # update the signal dictionary with the signal call 
            self.signal_dict[signal] = "{}".format(signal)


    # Exit a parse tree produced by stlgrammarParser#MulDivExpr.
    def exitMulDivExpr(self, ctx:stlgrammarParser.MulDivExprContext):
        '''
        grammar: expr op=('*'|'/') expr
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

        self.set_rule_tree(ctx, expr)

    # Exit a parse tree produced by stlgrammarParser#AddSubExpr.
    def exitAddSubExpr(self, ctx:stlgrammarParser.AddSubExprContext):
        '''
        grammar: expr op=('+'|'-') expr
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

        self.set_rule_tree(ctx, expr)

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

        self.set_rule_tree(ctx, intExpr)

    # Exit a parse tree produced by stlgrammarParser#parensExpr.
    def exitParensExpr(self, ctx:stlgrammarParser.ParensExprContext):
        '''
        grammar: '(' expr ')' 
        get the parsed expression in the parenthesis: (4/3)
        :param ctx:
        :return:
        '''

        expr = self.getExpr(ctx.expr())
        # print(expr)

        self.setExpr(ctx, expr)

        self.set_rule_tree(ctx, expr)



    # Exit a parse tree produced by stlgrammarParser#andorOp.
    def exitAndorOp(self, ctx:stlgrammarParser.AndorOpContext):
        '''
        grammar: 'and' | 'or'
        :param ctx:
        :return:
        '''
        andor = ctx.getText().strip()
        self.setExpr(ctx, andor)


    # def stlProp_code(self, func_call="_", boolVal="True"):
    #     '''
    #     generate code that is associated with an stlProp formula: True, False
    #     '''
    #
    #     # add the function call as a column name to be added in the dataframe
    #     # self.df[func_call] = 0
    #     self.output_signals.append(func_call)
    #
    #     # update the signal dictionary with the function call and expression string
    #     self.signal_dict[func_call] = "{} == True".format(boolVal)
    # 
    #     code = "\n"
    #     code += "\n\ndef " + func_call + "(t=0):"
    #     code += "\n\tif({} == True):".format(boolVal)
    #     # code += "\n\t\tdf.loc[df.Time == t, '{}'] = 1".format(func_call)
    #     code += "\n\t\treturn True"
    #     code += "\n\telse:"
    #     # code += "\n\t\tdf.loc[df.Time == t, '{}'] = -1".format(func_call)
    #     code += "\n\t\treturn False"
    # 
    #     return code
    # 
    # 
    # def stlNotFormula_code(self, func_call="_", func_check="_"):
    #     '''
    #     generate code that is associated with an stlNotFormula formula: NOT '(' stlFormula ')' 
    #     '''        
    #     code = "\n"
    #     code += "\n\ndef " + str(func_call) + "(t=0):"
    #     code += "\n\tif( not( {}(t=t) )):".format(func_check)
    #     code += "\n\t\treturn True"
    #     code += "\n\telse:"
    #     code += "\n\t\treturn False"

    #     return code    
    # 
    # 
    # def stlUntilFormula_code(self, func_call="_", start_t="0", end_t="0", phi="_", phe="_"):
    #     '''
    #     generate code that is associated with a Until formula: x > 9 U [10, 15] y > 25
    #     '''
    #     code = "\n"
    #     code += "\n\ndef " + str(func_call) + "(t=0):"            # "(t=0, start_t={}, end_t={}):".format(start_t, end_t)
    #     code += "\n\tfor i in range(t+{}, t+{}+1+1):".format(start_t, end_t)
    #     code += "\n\t\tif ({}(t=i)):".format(phe)
    #     code += "\n\t\t\tbreak"
    #     code += "\n\tif (i > (t + {})):".format(end_t)
    #     code += "\n\t\treturn False"
    #     code += "\n\tfor j in range(t,i+1):"
    #     code += "\n\t\tif(not ({}(t=j))):".format(phi)
    #     code += "\n\t\t\treturn False"
    #     code += "\n\treturn True"
    # 
    #     return code
    # 
    #     
    # # Enter a parse tree produced by stlgrammarParser#stlFormulaImplies.
    # def enterStlFormulaImplies(self, ctx:stlgrammarParser.StlFormulaImpliesContext):
    #     '''
    #     a -> b === (not(a)) or (a and b)
    #     :param ctx:
    #     :param value:
    #     :return:
    #     '''
    #
    #     # get unique ID and the function call that will use this UID for this node
    #     uid, func_call = self.funcUIDgen(func_prepend="StlFormulaImplies_")
    #
    #     # annotate the node with the variables
    #     self.setUID(ctx, {"uid": uid, "func": func_call})
    #
    #     # signal calls will only be referred to with their appointed function calls
    #     self.setExpr(ctx, func_call)
    #
    #
    # # Exit a parse tree produced by stlgrammarParser#stlFormulaImplies.
    # def exitStlFormulaImplies(self, ctx:stlgrammarParser.StlFormulaImpliesContext):
    #     '''
    #     a -> b === not(a) or b === not(not(a) and b)
    #     :param ctx:
    #     :param value:
    #     :return:
    #     '''
    #     before = self.getExpr(ctx.stlFormula(0))
    #     after = self.getExpr(ctx.stlFormula(1))
    #
    #     impliesFormula = "(not(not({}(t=t)) and {}(t=t)))".format(before, after)
    #     # print(impliesFormula)
    #
    #     # get the function call for this node: StlFormulaImplies_611
    #     func_call = self.getUID(ctx)["func"]
    #
    #     # add the function call as a column name to be added in the dataframe
    #     # self.df[func_call] = 0
    #     self.output_signals.append(func_call)
    #
    #     # update the signal dictionary with the function call
    #     self.signal_dict[func_call] = "{}".format(impliesFormula)
    #
    #     code = "\n"
    #     code += "\n\ndef " + str(func_call) + "(t=0):"
    #     code += "\n\tif({} == True):".format(impliesFormula)
    #     code += "\n\t\tdf.loc[df.Time == t, '{}'] = 1".format(func_call)
    #     code += "\n\t\treturn True"
    #     code += "\n\telse:"
    #     code += "\n\t\tdf.loc[df.Time == t, '{}'] = -1".format(func_call)
    #     code += "\n\t\treturn False"
    #
    #     self.appendCode(code)
    #
    #
    #
    # # Enter a parse tree produced by stlgrammarParser#stlGlobalFormula.
    # def enterStlGlobalFormula(self, ctx:stlgrammarParser.StlGlobalFormulaContext):
    #     '''
    #     G[3,4](a > 25)
    #     :param ctx:
    #     :param value:
    #     :return:
    #     '''
    #
    #     # get unique ID and the function call that will use this UID for this node
    #     uid, func_call = self.funcUIDgen(func_prepend="StlGlobal_")
    #
    #     # annotate the node with the variables
    #     self.setUID(ctx, {"uid": uid, "func": func_call})
    #
    #     # signal calls will only be referred to with their appointed function calls
    #     self.setExpr(ctx, func_call)
    #
    #
    #
    # # Exit a parse tree produced by stlgrammarParser#stlGlobalFormula.
    # def exitStlGlobalFormula(self, ctx:stlgrammarParser.StlGlobalFormulaContext):
    #     '''
    #     G[3,4](a > 25)
    #     :param ctx:
    #     :param value:
    #     :return:
    #     '''
    #     timeRange = (ctx.timeSlice() != None)
    #     if timeRange:
    #         start_t = ctx.timeSlice().start_t().getText().strip()
    #         end_t = ctx.timeSlice().end_t().getText().strip()
    #     else:
    #         start_t = 0
    #         end_t = 20 # self.time_max
    #     # print("start: {} \t end: {}".format(start_t, end_t))
    #
    #     stlFormula = self.getExpr(ctx.stlFormula())
    #
    #     # get the function call for this node: StlGlobal_930
    #     func_call = self.getUID(ctx)["func"]
    #
    #     boolVal = "True"
    #     # get unique ID and the function call that will use this UID for this node
    #     uid_bool, func_call_bool = self.funcUIDgen(func_prepend="stlProp_")
    #     # stlProp formula function code generation
    #     code = self.stlProp_code(func_call=func_call_bool, boolVal=boolVal)
    #     # append code to file
    #     self.appendCode(code)
    #
    #     # get unique ID and the function call that will use this UID for this node
    #     uid_stlNot, func_call_stlNot = self.funcUIDgen(func_prepend="StlNot_")
    #     # stlNotFormula formula function code generation
    #     code = self.stlNotFormula_code(func_call=func_call_stlNot, func_check=stlFormula)
    #     # append code to file
    #     self.appendCode(code)
    #
    #
    #     # get unique ID and the function call that will use this UID for this node
    #     uid_until, func_call_until = self.funcUIDgen(func_prepend="StlUntil_")
    #
    #     code = self.stlUntilFormula_code(func_call=func_call_until, start_t=start_t, end_t=end_t, phi=func_call_bool, phe=func_call_stlNot)
    #     # append code to file
    #     self.appendCode(code)
    #
    #     code = "\n"
    #     code += "\n\ndef " + str(func_call) + "(t=0):"
    #     # code += "\n\tif(not( True U [3,4] not({}) ) ):".format(stlFormula)
    #     code += "\n\tif(not( {}(t=t)) ):".format(func_call_until)
    #     code += "\n\t\treturn True"
    #     code += "\n\telse:"
    #     code += "\n\t\treturn False"
    #
    #     self.appendCode(code)
    #
    #
    # # Enter a parse tree produced by stlgrammarParser#stlEventualFormula.
    # def enterStlEventualFormula(self, ctx:stlgrammarParser.StlEventualFormulaContext):
    #     '''
    #     F[5,6]((4/63) < b)
    #     :param ctx:
    #     :param value:
    #     :return:
    #     '''
    #
    #     # get unique ID and the function call that will use this UID for this node
    #     uid, func_call = self.funcUIDgen(func_prepend="StlEventual_")
    #
    #     # annotate the node with the variables
    #     self.setUID(ctx, {"uid": uid, "func": func_call})
    #
    #     # signal calls will only be referred to with their appointed function calls
    #     self.setExpr(ctx, func_call)
    #
    #
    # # Exit a parse tree produced by stlgrammarParser#stlEventualFormula.
    # def exitStlEventualFormula(self, ctx:stlgrammarParser.StlEventualFormulaContext):
    #     '''
    #     F[5,6]((4/63) < b)
    #     :param ctx:
    #     :param value:
    #     :return:
    #     '''
    #     timeRange = (ctx.timeSlice() != None)
    #     if timeRange:
    #         start_t = ctx.timeSlice().start_t().getText().strip()
    #         end_t = ctx.timeSlice().end_t().getText().strip()
    #     else:
    #         start_t = 0
    #         end_t = 20 # self.time_max
    #     # print("start: {} \t end: {}".format(start_t, end_t))
    #
    #     stlFormula = self.getExpr(ctx.stlFormula())
    #
    #     # get the function call for this node: signalComp_611
    #     func_call = self.getUID(ctx)["func"]
    #
    #
    #     boolVal = "True"
    #     # get unique ID and the function call that will use this UID for this node
    #     uid_bool, func_call_bool = self.funcUIDgen(func_prepend="stlProp_")
    #     # stlProp formula function code generation
    #     code = self.stlProp_code(func_call=func_call_bool, boolVal=boolVal)
    #     # append code to file
    #     self.appendCode(code)
    #
    #     # get unique ID and the function call that will use this UID for this node
    #     uid_until, func_call_until = self.funcUIDgen(func_prepend="StlUntil_")
    #
    #     code = self.stlUntilFormula_code(func_call=func_call_until, start_t=start_t, end_t=end_t, phi=func_call_bool, phe=stlFormula)
    #     # append code to file
    #     self.appendCode(code)
    #
    #     code = "\n"
    #     code += "\n\ndef " + str(func_call) + "(t=0):"
    #     code += "\n\tif({}(t=t)):".format(func_call_until)
    #     code += "\n\t\treturn True"
    #     code += "\n\telse:"
    #     code += "\n\t\treturn False"
    #
    #     self.appendCode(code)