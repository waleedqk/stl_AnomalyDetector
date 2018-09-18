/** Grammars always start with a grammar header. This grammar is called
 */
grammar expressions;

// parser rules start with lowercase letters, lexer rules with uppercase
prog: exprs+ ;


exprs:   expr (andorOp expr)* NEWLINE                   # regExpr
     //|   expr (andorOp expr)* NEWLINE                   # andorExpr
     |   NEWLINE                                        # blank
     ; 


expr :
      untilTL                                           # untilExpr
    | signalComp                                        # signalExpr
    | '(' signalComp ')'                                # parensExpr
    ;


untilTL :
        signalComp 'U' timeslice signalComp             # until
        ;

signal:
        ID'[t]'                                         # signalName
        ;

signalComp:
        NOT? signal relOp INT                           # signalBrakedown
        ;

timeslice:
        '[' INT ',' INT ']'                             # timerange
        ;

Bool:
      'true' 
      | 'false'
 ;


relOp:
      OP_EE | OP_NE | OP_GT | OP_LEQ | OP_LT | OP_GEQ
      ;

andorOp:
      'AND' | 'OR'
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

NOT :   'NOT';

ID  :   [a-zA-Z]+ ;      // match identifiers
INT :   [0-9]+ ;         // Define token INT as one or more digits
NEWLINE:'\r'? '\n' ;     // return newlines to parser (is end-statement signal)
WS  :   [ \t]+ -> skip ; // Define whitespace rule, toss it out