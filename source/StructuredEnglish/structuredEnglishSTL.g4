/** Grammars always start with a grammar header. This grammar is called
 */
grammar structuredEnglishSTL;
import CommonLexerRules; // includes all rules from CommonLexerRules.g4

// parser rules start with lowercase letters, lexer rules with uppercase


prog: (stlFormula EOF) ; // + // (temporalLogic NL)+ ;

//stlFormula:
//        'If (' stlFormula ') occur it implies (' stlFormula ')'                   # stlFormulaImplies
//        | 'Both (' stlFormula andorOp stlFormula  ')'             # stlConjDisjFormula
//        | stlFormula 'U' timeSlice stlFormula           # stlUntilFormula
//        | NOT '(' stlFormula ')'                        # stlNotFormula
//        | 'Always that' timeSlice? '(' stlFormula ')'             # stlGlobalFormula
//        | 'Eventually that' timeSlice? '(' stlFormula ')'             # stlEventualFormula
//        | signalComp                                    # stlSignalComp
//        | signal                                        # stlSignal
//        | Bool                                          # stlProp
//        | '(' stlFormula ')'                            # stlParens
//      ;


stlFormula:
    scope ', ' speciflcation '.'
    ;

scope:
    'Globally' | 'Before ' signalComp | 'After ' signalComp | 'Between ' signalComp ' and ' signalComp | 'After ' signalComp ' until ' signalComp
    ;

speciflcation:
    qualitativeType | realtimeType
    ;

qualitativeType:
    occurrenceCategory | orderCategory
    ;

occurrenceCategory:
    absencePattern | universalityPattern | existencePattern | boundedExistencePattern
    ;

absencePattern:
    'it is never the case that ' signalComp ' holds'
    ;

universalityPattern:
    'it is always the case that ' signalComp ' holds'
    ;

existencePattern:
    signalComp ' eventually holds'
    ;

boundedExistencePattern:
    'transitions to states in which ' signalComp ' holds occur at most twice'
    ;

orderCategory:
    'it is always the case that if ' signalComp ' holds' (precedencePattern | precedenceChainPattern1_2 | precedenceChainPattern2_1 | responsePattern | responseChainPattern1_2 | responseChainPattern2_1 | constrainedChainPattern1_2)
    ;


precedencePattern:
    ', then ' signalComp ' previously held'
    ;

precedenceChainPattern1_2:
    ' and is succeeded by ' signalComp ', then ' signalComp ' previously held'
    ;

precedenceChainPattern2_1:
    ', then ' signalComp ' previously held and was preceded by ' signalComp
    ;

responsePattern:
    ', then ' signalComp ' eventually holds'
    ;

responseChainPattern1_2:
    ', then ' signalComp ' eventually holds and is succeeded by ' signalComp
    ;

responseChainPattern2_1:
    ' and is succeeded by ' signalComp ', then ' signalComp ' eventually holds after ' signalComp
    ;

constrainedChainPattern1_2:
    ', then ' signalComp ' eventually holds and is succeeded by ' signalComp ', where ' signalComp ' does not hold between ' signalComp ' and ' signalComp
    ;

realtimeType:
    'it is always the case that ' (durationCategory | periodicCategory | realtimeOrderCategory)
    ;


durationCategory:
    'once ' signalComp ' becomes satisfled, it holds for ' (minDurationPattern | maxDurationPattern)
    ;

minDurationPattern:
    'at least ' INT ' time unit(s)'
    ;

maxDurationPattern:
    'less than ' INT ' time unit(s)'
    ;

 periodicCategory:
    signalComp ' holds ' boundedRecurrencePattern
    ;

boundedRecurrencePattern:
    'at least every ' INT ' time unit(s)'
    ;

realtimeOrderCategory:
    'if ' signalComp 'holds, then ' signalComp ' holds ' (boundedResponsePattern | boundedInvariancePattern)
    ;

boundedResponsePattern:
    'after at most ' INT ' time unit(s)'
    ;

boundedInvariancePattern:
    'for at least ' INT ' time unit(s)'
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