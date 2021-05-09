import os

from translator import *

nltk.data.path.append(os.getcwd() + os.sep + "nltk_data")
"""
import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet

from IPython.display import display

from stat_parser import Parser


for ss in wordnet.synsets('sum'):
    print(ss.name(), ss.lemma_names())

parser = Parser()
print(parser.parse("Find the sum from 1 to 100"))
"""


def main(text):
    instruction = Instruction(text)
    instruction.translate()
    if instruction.instruction is not None:
        context = {}
        exec(instruction.instruction, context)
        return context["total"]

    return "Error. These commands could not be parsed."

if __name__ == "__main__":
    print(main("Add the numbers 6 and 7."))
