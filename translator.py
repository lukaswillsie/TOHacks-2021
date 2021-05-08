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
        """
        """
        self.text = text
        self.instruction = None

    def translate(self):
        if len(self.text) < 3: # Choose better threshold
            return

        # Extract verb
        verb, nouns = extract_parts(self.text)

        # Extract operation
        if verb in operation.operation_dict:
            operation = operation.operation_dict[verb]

        if operation.standard:
            self.instruction = default_translate(self.text)
        else:
            self.instruction = operation.translate(self.text)


    def extract_parts(text):
        pass


    def default_translate(text):
        # Extract verb
        verb =1

        # Extract operation
        operation =1

        # Extract nouns
        nouns = []

        # Extract arguments
        arguments = []

        # Extract Python instruction
        instruction = "total = " + str(operation.initial_value) + " \n"
        for arg in arguments:
            instruction += "total = total " + str(operation.operation) + " " + str(arg) + " \n"
        instruction += "print(total)" # What should this be?

        return instruction
