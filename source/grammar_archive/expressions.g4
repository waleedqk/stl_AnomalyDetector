/** Grammars always start with a grammar header. This grammar is called
 */
grammar expressions;

// parser rules start with lowercase letters, lexer rules with uppercase
prog: (formula NL) ; // +


//formula:   expr (andorOp expr)*                   # regExpr
//     //|   expr (andorOp expr)* NEWLINE            # andorExpr
//     |   NL                                        # blank
//     ;


formula :

        formula 'U' timeslice formula                   # untilFormula
        | formula andorOp formula                       # conjdisjFormula
        | signalComp                                    # signalFormula
        | '(' signalComp ')'                            # parensSignalFormula
        | Bool                                          # propFormula
    ;


//untilTL :
//        signalComp 'U' timeslice signalComp             # until
//        ;

signalComp:
        NOT? signal relOp signalValue                           # signalBrakedown
        ;

signal:
        signalID'[t]'                                         # signalName
        | signalID                                            # signalName
        ;


timeslice:
        '[' start_t ',' end_t ']'                             # timerange
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


signalID: ID;

start_t: INT;
end_t: INT;


Bool:
      'True'
      | 'False'
 ;

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