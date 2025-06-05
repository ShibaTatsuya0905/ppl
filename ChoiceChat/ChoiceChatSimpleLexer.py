# Generated from ChoiceChat.g4 by ANTLR 4.13.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,6,64,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,1,
        0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,3,0,24,8,0,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,3,1,35,8,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,44,
        8,2,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,4,4,4,54,8,4,11,4,12,4,55,1,5,
        4,5,59,8,5,11,5,12,5,60,1,5,1,5,0,0,6,1,1,3,2,5,3,7,4,9,5,11,6,1,
        0,2,2,0,48,57,65,90,3,0,9,10,13,13,32,32,68,0,1,1,0,0,0,0,3,1,0,
        0,0,0,5,1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,1,23,1,0,0,
        0,3,34,1,0,0,0,5,43,1,0,0,0,7,45,1,0,0,0,9,53,1,0,0,0,11,58,1,0,
        0,0,13,14,5,99,0,0,14,15,5,104,0,0,15,16,5,111,0,0,16,17,5,111,0,
        0,17,18,5,115,0,0,18,24,5,101,0,0,19,20,5,99,0,0,20,21,5,104,0,0,
        21,22,5,111,0,0,22,24,5,110,0,0,23,13,1,0,0,0,23,19,1,0,0,0,24,2,
        1,0,0,0,25,26,5,115,0,0,26,27,5,101,0,0,27,28,5,108,0,0,28,29,5,
        101,0,0,29,30,5,99,0,0,30,35,5,116,0,0,31,32,5,108,0,0,32,33,5,117,
        0,0,33,35,5,97,0,0,34,25,1,0,0,0,34,31,1,0,0,0,35,4,1,0,0,0,36,37,
        5,112,0,0,37,38,5,105,0,0,38,39,5,99,0,0,39,44,5,107,0,0,40,41,5,
        108,0,0,41,42,5,97,0,0,42,44,5,121,0,0,43,36,1,0,0,0,43,40,1,0,0,
        0,44,6,1,0,0,0,45,46,5,111,0,0,46,47,5,112,0,0,47,48,5,116,0,0,48,
        49,5,105,0,0,49,50,5,111,0,0,50,51,5,110,0,0,51,8,1,0,0,0,52,54,
        7,0,0,0,53,52,1,0,0,0,54,55,1,0,0,0,55,53,1,0,0,0,55,56,1,0,0,0,
        56,10,1,0,0,0,57,59,7,1,0,0,58,57,1,0,0,0,59,60,1,0,0,0,60,58,1,
        0,0,0,60,61,1,0,0,0,61,62,1,0,0,0,62,63,6,5,0,0,63,12,1,0,0,0,6,
        0,23,34,43,55,60,1,6,0,0
    ]

class ChoiceChatSimpleLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    KW_CHOOSE = 1
    KW_SELECT = 2
    KW_PICK = 3
    KW_OPTION = 4
    CHOICE_TOKEN = 5
    WS = 6

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'option'" ]

    symbolicNames = [ "<INVALID>",
            "KW_CHOOSE", "KW_SELECT", "KW_PICK", "KW_OPTION", "CHOICE_TOKEN", 
            "WS" ]

    ruleNames = [ "KW_CHOOSE", "KW_SELECT", "KW_PICK", "KW_OPTION", "CHOICE_TOKEN", 
                  "WS" ]

    grammarFileName = "ChoiceChat.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


