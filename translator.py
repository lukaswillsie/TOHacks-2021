import operation

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

    def __init__(self, text):
        self.text = text # Raw text
        self.instruction = None # Python code

    def clean_word(word): #TODO
        """Apply all needed preprocessing to <word> and return the result."""
        return word.lower().strip()

    def extract_verb(text): #TODO
        """Extract the verb or main action word from <text> and return it."""
        return "sum"

    def extract_operation(verb): #TODO
        """Extract the operation from <verb>."""
        verb = Instruction.clean_word(verb)
        if verb in operation.operation_dict:
            return operation.operation_dict[verb]

        return None

    def extract_all(text): #TODO
        return operation.operation_dict["sum"], range(1,11)

    def default_translate(text):
        """Returns the Python code for <text> provided that the verb refers to a
        standard operation."""

        # Extract all
        operation, arguments = Instruction.extract_all(text)

        if operation.binary:
            if len(arguments) != 2:
                return None

        # Extract Python instruction
        instruction = "total = " + str(operation.initial_value) + " \n"
        for arg in arguments:
            instruction += "total = total " + str(operation.operation) + " " + str(arg) + " \n"
        instruction += "total \n" # What should this be?

        return instruction

    def translate(self):
        """Sets self.instruction to the Python code for self.text."""
        if len(self.text) < 5:
            self.instruction = None
            return

        # Extract verb
        verb = Instruction.extract_verb(self.text)

        # Extract operation
        operation = Instruction.extract_operation(verb)

        if operation.standard:
            self.instruction = Instruction.default_translate(self.text)
        else:
            self.instruction = operation.translate(self.text)
