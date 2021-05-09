import operation
from parser import *
from collections.abc import Iterable

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

    def extract_operation(verb): #TODO
        """Extract the operation from <verb>."""
        verb = Instruction.clean_word(verb)
        if verb in operation.operation_dict:
            return operation.operation_dict[verb]

        return None

    def binary_translate(operation, arguments):

        if len(arguments) not in [1,2]:
            return None

        if len(arguments) == 1:
            return "total = total " + str(operation.operation) + " " + str(arguments[0]) + "\n"
        return "total = " + str(arguments[0]) + " " + str(operation.operation) + " " + str(arguments[1]) + "\n"

    def default_translate(text):
        """Returns the Python code for <text> provided that the verb refers to a
        standard operation."""

        # Extract operation and arguments
        parser = TextParser(text)
        parser.extract_verb()
        verbs = parser.verb
        operations = [Instruction.extract_operation(verb) for verb in verbs]
        arguments = parser.collect_args()
        #print(verbs, operations, arguments)
        instruction = ""
        for i in range(len(operations)):
            operation = operations[i]
            if operation.binary:
                instruction += Instruction.binary_translate(operation, arguments[i])
                continue

            # Extract Python instruction
            if i == 0:
                instruction = "total = " + str(operation.initial_value) + " \n"
            for arg in arguments[i]:
                if not isinstance(arg, Iterable):
                    instruction += "total = total " + str(operation.operation) + " " + str(arg) + " \n"
                else:
                    for a in arg:
                        instruction += "total = total " + str(operation.operation) + " " + str(a) + " \n"

        instruction += "print(total) \n" # What should this be?
        #print("i", instruction)
        return instruction

    def translate(self):
        """Sets self.instruction to the Python code for self.text."""
        if len(self.text) < 5:
            self.instruction = None
            return

        # Extract verbparser = Parser()
        parser = TextParser(self.text)
        parser.extract_verb()
        verbs = parser.verb
        print("v", verbs)
        # Extract operation
        operations = [Instruction.extract_operation(verb) for verb in verbs]
        if operations[0].standard:
            self.instruction = Instruction.default_translate(self.text)
        else:
            self.instruction = operations[0].translate(self.text)
