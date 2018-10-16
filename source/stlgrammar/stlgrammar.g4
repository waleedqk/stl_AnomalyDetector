/** Grammars always start with a grammar header. This grammar is called
 */
grammar stlgrammar;
import CommonLexerRules; // includes all rules from CommonLexerRules.g4

// parser rules start with lowercase letters, lexer rules with uppercase


prog: (stlFormula EOF) ; // + // (temporalLogic NL)+ ;

stlFormula:
        stlFormula implies stlFormula                   # stlFormulaImplies
        | stlFormula andorOp stlFormula                 # stlConjDisjFormula
        | stlFormula 'U' timeSlice stlFormula           # stlUntilFormula
        | NOT '(' stlFormula ')'                        # stlNotFormula
        | 'G' timeSlice? stlFormula                     # stlGlobalFormula
        | 'F' timeSlice? stlFormula                     # stlEventualFormula
        | signalComp                                    # stlSignalComp
        | signal                                        # stlSignal
        | Bool                                          # stlProp
        | '(' stlFormula ')'                            # stlParens
      ;


signalComp:
          signal relOp expr                             # signalExpr
        | expr relOp signal                             # signalExpr
        | Bool relOp signal                             # signalBool
        | signal relOp Bool                             # signalBool
        ;

signal:
        signalID'[t]'                                   # signalName
        | signalID                                      # signalName
        ;


timeSlice:
        '[' start_t ',' end_t ']'                       # timerange
        ;

implies:
        '->'
        ;

expr:   expr op=('*'|'/') expr                          # MulDivExpr
    |   expr op=('+'|'-') expr                          # AddSubExpr
    |   INT                                             # intExpr
//    |   ID                          # id
    |   '(' expr ')'                                    # parensExpr
    ;

signalValue:
        INT | Bool
        ;



relOp:
      OP_EE | OP_NE | OP_GT | OP_LEQ | OP_LT | OP_GEQ
      ;

andorOp:
      'and' | 'or'
      ;

Bool:
      'True' | 'False' | '(' Bool ')'
 ;

signalID: ID;

start_t: INT;
end_t: INT | 'INF';