operation_word_map = {"sum": "+",
                      "product": "*",
                      "subtract": "-",
                      "divide": "/",
                      "exponentiate": "**",
                      "modulus": "%",
                      "floor division": "%"}

class Operation:
    """A class where each object stores the relevant information about an
    operation for translation.
    """

    def __init__(self, operation, binary, initial_value = None, standard = True, translate = None):
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

addition = Operation("+", False, initial_value = "0")
subtraction = Operation("-", True)
multiplication = Operation("*", False, initial_value = "1")
division = Operation("/", True)
exponentiation = Operation("**", True)
modulus = Operation("%", True)
floor_division = Operation("//", True)

operation_dict = {
    "add" : addition,
    "sum" : addition,
    "multiply" : multiplication,
    "product" : multiplication,
    "divide" : division,
    "subtract" : subtraction,
    "exponentiate" : exponentiation,
    "mod" : modulus,
    "integer divide" : floor_division
}
