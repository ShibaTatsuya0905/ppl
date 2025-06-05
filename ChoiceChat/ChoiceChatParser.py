# Generated from ChoiceChat.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,6,34,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,1,0,1,0,3,0,11,8,0,3,0,
        13,8,0,1,0,1,0,3,0,17,8,0,1,0,3,0,20,8,0,1,0,1,0,1,1,1,1,1,2,1,2,
        1,3,5,3,29,8,3,10,3,12,3,32,9,3,1,3,1,30,0,4,0,2,4,6,0,1,1,0,1,4,
        34,0,12,1,0,0,0,2,23,1,0,0,0,4,25,1,0,0,0,6,30,1,0,0,0,8,10,3,2,
        1,0,9,11,5,6,0,0,10,9,1,0,0,0,10,11,1,0,0,0,11,13,1,0,0,0,12,8,1,
        0,0,0,12,13,1,0,0,0,13,14,1,0,0,0,14,19,3,4,2,0,15,17,5,6,0,0,16,
        15,1,0,0,0,16,17,1,0,0,0,17,18,1,0,0,0,18,20,3,6,3,0,19,16,1,0,0,
        0,19,20,1,0,0,0,20,21,1,0,0,0,21,22,5,0,0,1,22,1,1,0,0,0,23,24,7,
        0,0,0,24,3,1,0,0,0,25,26,5,5,0,0,26,5,1,0,0,0,27,29,9,0,0,0,28,27,
        1,0,0,0,29,32,1,0,0,0,30,31,1,0,0,0,30,28,1,0,0,0,31,7,1,0,0,0,32,
        30,1,0,0,0,5,10,12,16,19,30
    ]

class ChoiceChatParser ( Parser ):

    grammarFileName = "ChoiceChat.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [  ]

    symbolicNames = [ "<INVALID>", "KW_CHOOSE", "KW_SELECT", "KW_PICK", 
                      "KW_OPTION", "CHOICE_TOKEN", "WS" ]

    RULE_chatInput = 0
    RULE_command = 1
    RULE_selectedChoice = 2
    RULE_trailingGarbage = 3

    ruleNames =  [ "chatInput", "command", "selectedChoice", "trailingGarbage" ]

    EOF = Token.EOF
    KW_CHOOSE=1
    KW_SELECT=2
    KW_PICK=3
    KW_OPTION=4
    CHOICE_TOKEN=5
    WS=6

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ChatInputContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def selectedChoice(self):
            return self.getTypedRuleContext(ChoiceChatParser.SelectedChoiceContext,0)


        def EOF(self):
            return self.getToken(ChoiceChatParser.EOF, 0)

        def command(self):
            return self.getTypedRuleContext(ChoiceChatParser.CommandContext,0)


        def trailingGarbage(self):
            return self.getTypedRuleContext(ChoiceChatParser.TrailingGarbageContext,0)


        def WS(self, i:int=None):
            if i is None:
                return self.getTokens(ChoiceChatParser.WS)
            else:
                return self.getToken(ChoiceChatParser.WS, i)

        def getRuleIndex(self):
            return ChoiceChatParser.RULE_chatInput

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterChatInput" ):
                listener.enterChatInput(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitChatInput" ):
                listener.exitChatInput(self)




    def chatInput(self):

        localctx = ChoiceChatParser.ChatInputContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_chatInput)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 12
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 30) != 0):
                self.state = 8
                self.command()
                self.state = 10
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==6:
                    self.state = 9
                    self.match(ChoiceChatParser.WS)




            self.state = 14
            self.selectedChoice()
            self.state = 19
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.state = 16
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
                if la_ == 1:
                    self.state = 15
                    self.match(ChoiceChatParser.WS)


                self.state = 18
                self.trailingGarbage()


            self.state = 21
            self.match(ChoiceChatParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CommandContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_CHOOSE(self):
            return self.getToken(ChoiceChatParser.KW_CHOOSE, 0)

        def KW_SELECT(self):
            return self.getToken(ChoiceChatParser.KW_SELECT, 0)

        def KW_PICK(self):
            return self.getToken(ChoiceChatParser.KW_PICK, 0)

        def KW_OPTION(self):
            return self.getToken(ChoiceChatParser.KW_OPTION, 0)

        def getRuleIndex(self):
            return ChoiceChatParser.RULE_command

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCommand" ):
                listener.enterCommand(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCommand" ):
                listener.exitCommand(self)




    def command(self):

        localctx = ChoiceChatParser.CommandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_command)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 23
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 30) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SelectedChoiceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CHOICE_TOKEN(self):
            return self.getToken(ChoiceChatParser.CHOICE_TOKEN, 0)

        def getRuleIndex(self):
            return ChoiceChatParser.RULE_selectedChoice

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelectedChoice" ):
                listener.enterSelectedChoice(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelectedChoice" ):
                listener.exitSelectedChoice(self)




    def selectedChoice(self):

        localctx = ChoiceChatParser.SelectedChoiceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_selectedChoice)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 25
            self.match(ChoiceChatParser.CHOICE_TOKEN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TrailingGarbageContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ChoiceChatParser.RULE_trailingGarbage

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTrailingGarbage" ):
                listener.enterTrailingGarbage(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTrailingGarbage" ):
                listener.exitTrailingGarbage(self)




    def trailingGarbage(self):

        localctx = ChoiceChatParser.TrailingGarbageContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_trailingGarbage)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 30
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=1 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1+1:
                    self.state = 27
                    self.matchWildcard() 
                self.state = 32
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





