lexer grammar CommonLexerRules; // note "lexer grammar"


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

ID  :   [a-zA-Z]+ ;             // match identifiers
REAL : '-'?[0-9]+('.'[0-9]+)?;  // Define token REAL 
INT :   [0-9]+ ;                // Define token INT as one or more digits
NL  :   '\r'? '\n' ;            // return newlines to parser (is end-statement signal)
WS  :   [ \t]+ -> skip ;        // Define whitespace rule, toss it out