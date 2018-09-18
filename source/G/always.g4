/** Grammars always start with a grammar header. This grammar is called */
grammar always;

// parser rules start with lowercase letters, lexer rules with uppercase

prog: stlrule+ ;

stlrule: 
      globallyCall        # GLOBALLY
      |   NEWLINE       # blank
      ;

globallyCall:
      GLOBALLY '[' INT ',' INT ']' expr NEWLINE
      ;


expr : 
      '-' expr                 # unaryNegExpr
      | '!' expr               # notExpr
      | INT                    # int
      | ID                     # id
      | '(' expr ')'           # parensExpr
      ;

/*STL KEYWORDS*/
 GLOBALLY : 'G';


operator:
      '==' | '!=' | '<' | '<=' | '>' | '>='
;

Bool:
      'true' 
      | 'false'
 ;


ID  :   [a-zA-Z]+ ;      // match identifiers
INT :   [0-9]+ ;         // Define token INT as one or more digits
DOUBLE :   [0-9]+ ('.' [0-9]+)? ;


NEWLINE:'\r'? '\n' ;     // return newlines to parser (is end-statement signal)
WS  :   [ \t\r]+ -> skip ; // Define whitespace rule, toss it out