/** Grammars always start with a grammar header. This grammar is called
 */
grammar stlgrammar;
import CommonLexerRules; // includes all rules from CommonLexerRules.g4

// parser rules start with lowercase letters, lexer rules with uppercase


prog: (stl NL) ; // + // (temporalLogic NL)+ ;

stl:
        globallyeventuallyCall                  # GLOBALLYEVENTUALLY
      | eventuallygloballyCall                  # EVENTUALLYGLOBALLY
      | globallyCall                            # GLOBALLY
      | eventuallyCall                          # EVENTUALLY
      | formula                                 # STLFORMULA
//       |   NL       # blank
      ;


globallyeventuallyCall:
      ALWAYS timeslice? EVENTUALLY timeslice? '(' stl (implies stl)? ')'            # GFcall
      ;

eventuallygloballyCall:
      EVENTUALLY timeslice? ALWAYS timeslice? '(' stl (implies stl)? ')'            # FGcall
      ;


globallyCall:
      ALWAYS timeslice? '(' stl (implies stl)? ')'                                  # Gcall
      ;

eventuallyCall:
      EVENTUALLY timeslice? '(' stl (implies stl)? ')'                              # Fcall
      ;


formula :

        formula 'U' timeslice formula                   # untilFormula
        | formula andorOp formula                       # conjdisjFormula
        | '(' formula andorOp formula ')'               # conjdisjFormula
        | signalComp                                    # signalFormula
        | '(' signalComp ')'                            # parensSignalFormula
        | Bool                                          # propFormula
    ;

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

implies:
        '->'
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
