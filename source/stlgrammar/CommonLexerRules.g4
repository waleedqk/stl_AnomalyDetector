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
INT :   [0-9]+ ;                // Define token INT as one or more digits
IDENTIFIER : [a-zA-Z_][a-zA-Z_0-9]* ;
REAL : '-'?[0-9]+('.'[0-9]+)?;  // Define token REAL 
// fragment NUM	: ('-'|'+')?((('0'..'9')*'.'('0'..'9')+)|('0'..'9')+);
NL  :   '\r'? '\n' ;            // return newlines to parser (is end-statement signal)
WS  :   [ \t]+ -> skip ;        // Define whitespace rule, toss it out

// https://ivanyu.me/blog/2014/09/13/creating-a-simple-parser-with-antlr/
// https://stackoverflow.com/questions/6487593/what-does-fragment-mean-in-antlr
// NUMBER: DIGITS | OCTAL_DIGITS | HEX_DIGITS;
// fragment DIGITS: '1'..'9' '0'..'9'*;
// fragment OCTAL_DIGITS: '0' '0'..'7'+;
// fragment HEX_DIGITS: '0x' ('0'..'9' | 'a'..'f' | 'A'..'F')+;
// 
// matched "1234", "0xab12", or "0777".