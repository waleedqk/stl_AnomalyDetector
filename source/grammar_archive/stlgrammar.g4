/** Grammars always start with a grammar header. This grammar is called
 */
grammar stlgrammar;
// parser rules start with lowercase letters, lexer rules with uppercase


prog: (stlFormula EOF) ; // + // (temporalLogic NL)+ ;

stlFormula:
        stlFormula implies stlFormula                   # stlFormulaImplies
        | stlFormula andorOp stlFormula                 # stlconjdisjFormula
        | stlFormula 'U' timeslice stlFormula           # stluntilFormula
        | NOT '(' stlFormula ')'                        # stlnotFormula
        | 'G' timeslice? stlFormula                     # stlglobalFormula
        | 'F' timeslice? stlFormula                     # stleventualFormula
        | signalComp                                    # stlsignalComp
        | signal                                        # stlsignal
        | Bool                                          # stlprop
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


timeslice:
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
      'True' | 'False'
 ;

signalID: ID;

start_t: INT;
end_t: INT | 'INF';


/*STL KEYWORDS*/
ALWAYS      :   'G';
EVENTUALLY  :   'F';

MUL :   '*' ; // assigns token name to '*' used above in grammar
DIV :   '/' ;
ADD :   '+' ;
SUB :   '-' ;

OP_EE : '==' ;
OP_NE : '!=' ;
OP_LT : '<' ;
OP_LEQ : '<=' ;
OP_GT : '>' ;
OP_GEQ : '>=' ;

NOT :   'not';

ID  :   [a-zA-Z]+ ;      // match identifiers
INT :   [0-9]+ ;         // Define token INT as one or more digits
NL  :   '\r'? '\n' ;     // return newlines to parser (is end-statement signal)
WS  :   [ \t]+ -> skip ; // Define whitespace rule, toss it out