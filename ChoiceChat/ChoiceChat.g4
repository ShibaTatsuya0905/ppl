grammar ChoiceChat;

chatInput
    : (command WS?)? selectedChoice (WS? trailingGarbage)? EOF
    ;

command
    : (KW_CHOOSE | KW_SELECT | KW_PICK | KW_OPTION)
    ;

selectedChoice
    : CHOICE_TOKEN 
    ;

// To consume any extra text after the choice that we don't care about
trailingGarbage
    : .*? 
    ;

KW_CHOOSE   : C H O O S E | C H O N ; 
KW_SELECT   : S E L E C T | L U A ;  
KW_PICK     : P I C K | L A Y ;       
KW_OPTION   : O P T I O N ;        

CHOICE_TOKEN : [A-Z] | [0-9]+ ;

WS          : [ \t\r\n]+ -> skip ;

fragment A:('a'|'A'); fragment B:('b'|'B'); fragment C:('c'|'C');
fragment D:('d'|'D'); fragment E:('e'|'E'); fragment F:('f'|'F');
fragment G:('g'|'G'); fragment H:('h'|'H'); fragment I:('i'|'I');
fragment J:('j'|'J'); fragment K:('k'|'K'); fragment L:('l'|'L');
fragment M:('m'|'M'); fragment N:('n'|'N'); fragment O:('o'|'O');
fragment P:('p'|'P'); fragment Q:('q'|'Q'); fragment R:('r'|'R');
fragment S:('s'|'S'); fragment T:('t'|'T'); fragment U:('u'|'U');
fragment V:('v'|'V'); fragment W:('w'|'W'); fragment X:('x'|'X');
fragment Y:('y'|'Y'); fragment Z:('z'|'Z');
fragment C_acute:('á'|'Á'); fragment H_h:('h'|'H'); fragment O_o:('ọ'|'Ọ');
fragment N_n:('n'|'N');