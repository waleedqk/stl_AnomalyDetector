/** Grammars always start with a grammar header. This grammar is called
 */
grammar stlgrammar;
import CommonLexerRules; // includes all rules from CommonLexerRules.g4

// parser rules start with lowercase letters, lexer rules with uppercase


prog: (stl EOF) ; // + // (temporalLogic NL)+ ;

stl:

        modifier '(' stl implies stl ')'        # stlModImplies
      |  stl implies stl                        # stlImplies
      | modifier '(' stl ')'                    # stlSingular
//      | '(' modifier  '(' stl ')' ')'           # stlSingular
//      | modifier '(' '(' stl ')' ')'            # stlSingular
      | stl andorOp stl                         # stlConjstl
//      | '(' stl andorOp stl   ')'               # stlConjstl
      | formula                                 # stlFormula
      | '(' stl ')'                             # stlParens
//       |   NL       # blank
      ;


modifier:
//        ALWAYS timeslice? EVENTUALLY timeslice?             # GFcall
//      | EVENTUALLY timeslice? ALWAYS timeslice?             # FGcall
        ALWAYS timeslice?                                   # Gcall
      | EVENTUALLY timeslice?                               # Fcall
      ;


formula :
          formula  implies formula                      # impliesFormula
        | formula 'U' timeslice formula                 # untilFormula
        | formula andorOp formula                       # conjdisjFormula
        | signalComp                                    # signalFormula
        | NOT '(' formula ')'                           # signalNegFormula
        | NOT? '(' signal ')'                           # signalProp
        | '(' formula ')'                               # parensFormula
        | Bool                                          # propFormula
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


timeslice:
        '[' start_t ',' end_t ']'                             # timerange
        ;

implies:
        '->'
        ;

expr:   expr op=('*'|'/') expr      # MulDivExpr
    |   expr op=('+'|'-') expr      # AddSubExpr
    |   INT                         # intExpr
//    |   ID                          # id
    |   '(' expr ')'                # parensExpr
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
      'True' | 'False'
 ;

signalID: ID;

start_t: INT;
end_t: INT | 'INF';