import operation
from parser import *
from collections.abc import Iterable
"""
import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from IPython.display import display
from stat_parser import Parser



for ss in wordnet.synsets('sum'):
    print(ss.name(), ss.lemma_names())
"""

class Instruction:
    """A class that represents an instruction. Each object contains the
    original English instruction and then processes it into a Python command.
    """

    def clean_word(word): #TODO
        """Apply all needed preprocessing to <word> and return the result."""
        return word.lower().strip()

    def __init__(self, text):
        self.text = Instruction.clean_word(text) # Raw text
        self.instruction = None # Python code

    def extract_verb(text): #TODO
        """Extract the verb or main action word from <text> and return it."""
        return "sum"

    def extract_operation(verb): #TODO
        """Extract the operation from <verb>."""
        verb = Instruction.clean_word(verb)
        if verb in operation.operation_dict:
            return operation.operation_dict[verb]

        return None

    def binary_translate(operation, arguments):
        if len(arguments) != 2:
            return None
        return "print(" + str(arguments[0]) + " " + str(operation.operation) + " " + str(arguments[1]) + ") \n"

    def default_translate(text):
        """Returns the Python code for <text> provided that the verb refers to a
        standard operation."""

        # Extract operation and arguments
        parser = TextParser(text)
        parser.extract_verb_math()
        verb = parser.verb
        operation = Instruction.extract_operation(verb)
        arguments = parser.collect_args_math()

        if operation.binary:
            return Instruction.binary_translate(operation, arguments)


        # Extract Python instruction
        instruction = "total = " + str(operation.initial_value) + " \n"
        for arg in arguments:
            if not isinstance(arg, Iterable):
                instruction += "total = total " + str(operation.operation) + " " + str(arg) + " \n"
            else:
                for a in arg:
                    instruction += "total = total " + str(operation.operation) + " " + str(a) + " \n"
        instruction += "print(total) \n" # What should this be?

        return instruction

    def translate(self):
        """Sets self.instruction to the Python code for self.text."""
        if len(self.text) < 5:
            self.instruction = None
            return

        # Extract verbparser = Parser()
        parser = TextParser(self.text)
        parser.extract_verb_math()
        verb = parser.verb

        # Extract operation
        operation = Instruction.extract_operation(verb)

        if operation.standard:
            self.instruction = Instruction.default_translate(self.text)
        else:
            self.instruction = operation.translate(self.text)
