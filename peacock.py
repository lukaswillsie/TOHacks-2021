from translator import *
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
        exec(instruction.instruction)
        return

    print("Error. These commands could not be parsed.")

if __name__ == "__main__":
    main("Translate to French I love food.")
