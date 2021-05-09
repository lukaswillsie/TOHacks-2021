from local_parser import *
from google.cloud import translate_v2
import six

operation_word_map = {"sum": "+",
                      "product": "*",
                      "subtract": "-",
                      "divide": "/",
                      "exponentiate": "**",
                      "modulus": "%",
                      "floor division": "%"}


def news_translate(text):
    parser = TextParser(text)
    parser.extract_verb()
    arguments = parser.collect_args()
    instruction = "from news_content_extraction_by_keyword import *\ntotal = summarize_article_search(\"" + " ".join(arguments)+ "\")\n"
    return instruction

def language_translate(text):
    parser = TextParser(text)
    parser.extract_verb()
    arguments = parser.collect_args()
    language = parser.language
    translate_client = translate_v2.Client()
    language_lst = translate_client.get_languages()
    language_code = "fr" # Default
    for d in language_lst:
        if language == d['name'].lower().strip():
            language_code = d['language']
            break

    language_code
    instruction = "from language_translate import *\ntotal =translate_text(\"" + str(language_code) + "\", \"" + arguments + "\")\n"
    return instruction


class Operation:
    """A class where each object stores the relevant information about an
    operation for translation.
    """

    def __init__(self, operation = None, binary = False, initial_value = None, standard = True, translate = None):
        """Initialize an object associated with the operation string <operation>.
        <binary> is a boolean indicating if the oepration only works with two operands
        <initial_value> is the value that total starts off at when evaluating
        <standard> is a boolean of whether this is a default operation
        If false, the default translation will not work and a new function
        <translate> should be provided
        If true and <binary> is false then
        <initial_value> is the value that total starts off at when evaluating
        """
        self.operation = operation
        self.binary = binary
        self.initial_value = initial_value
        self.standard = standard
        self.translate = translate

addition = Operation(operation = "+", binary = False, initial_value = "0")
subtraction = Operation(operation = "-", binary = True)
multiplication = Operation(operation = "*", binary = False, initial_value = "1")
division = Operation(operation = "/", binary = True)
exponentiation = Operation(operation = "**", binary = True)
news_extract = Operation(standard = False, translate = news_translate)
translate = Operation(standard = False, translate = language_translate)

operation_dict = {
    "add" : addition,
    "sum" : addition,
    "multiply" : multiplication,
    "product" : multiplication,
    "divide" : division,
    "subtract" : subtraction,
    "exponentiate" : exponentiation,
    "power" : exponentiation,
    "summarize" : news_extract,
    "translate" : translate
    }
