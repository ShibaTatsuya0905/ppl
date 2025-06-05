# Generated from ChoiceChat.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ChoiceChatParser import ChoiceChatParser
else:
    from ChoiceChatParser import ChoiceChatParser

# This class defines a complete listener for a parse tree produced by ChoiceChatParser.
class ChoiceChatListener(ParseTreeListener):

    # Enter a parse tree produced by ChoiceChatParser#chatInput.
    def enterChatInput(self, ctx:ChoiceChatParser.ChatInputContext):
        pass

    # Exit a parse tree produced by ChoiceChatParser#chatInput.
    def exitChatInput(self, ctx:ChoiceChatParser.ChatInputContext):
        pass


    # Enter a parse tree produced by ChoiceChatParser#command.
    def enterCommand(self, ctx:ChoiceChatParser.CommandContext):
        pass

    # Exit a parse tree produced by ChoiceChatParser#command.
    def exitCommand(self, ctx:ChoiceChatParser.CommandContext):
        pass


    # Enter a parse tree produced by ChoiceChatParser#selectedChoice.
    def enterSelectedChoice(self, ctx:ChoiceChatParser.SelectedChoiceContext):
        pass

    # Exit a parse tree produced by ChoiceChatParser#selectedChoice.
    def exitSelectedChoice(self, ctx:ChoiceChatParser.SelectedChoiceContext):
        pass


    # Enter a parse tree produced by ChoiceChatParser#trailingGarbage.
    def enterTrailingGarbage(self, ctx:ChoiceChatParser.TrailingGarbageContext):
        pass

    # Exit a parse tree produced by ChoiceChatParser#trailingGarbage.
    def exitTrailingGarbage(self, ctx:ChoiceChatParser.TrailingGarbageContext):
        pass



del ChoiceChatParser