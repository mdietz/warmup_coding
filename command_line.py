import sys
import re

class Parser:

    # required and optional flags represented as dictionaries with key=flag name
    # and value=validation function
    def __init__(self, required_flags, optional_flags={}, usage_msg=''):
        self.required = required_flags
        self.optional = optional_flags
        self.usage = usage_msg

    # Extract flags from an argument string that has already been tokenized
    # Throws an exception on malformed argument or missing required flag
    #
    # Returns a dictionary of flagnames to values
    #
    # argv[0] should be the first flag element rather than the program name
    def parse_args(self, argv):
        res = {}

        i = 0
        while i < len(argv):
            arg = argv[i]

            # Set next to be the possible value of the current flag or None if the next token
            # is a flag
            next = None
            if not i+1 >= len(argv) and not (argv[i+1][0:1] == '-' or argv[i+1][0:2] == "--"):
                next = argv[i+1]

            # Strip leading - or -- from flagname
            if arg[0:2] == '--':
                flag_name = arg[2:len(arg)]
            elif arg[0:1] == '-':
                flag_name = arg[1:len(arg)]

            if flag_name in self.required: #or flag_name in self.optional:
                flag_val = self.required[flag_name](flag_name, val=next)
                res[flag_name] = flag_val
            else:
                raise Exception("Undefined flag")

            # Skip to next flag if no value for this flag, otherwise skip forward twice
            if next is None:
                i = i + 1
            else:
                i = i + 2

        # Check for missing required flags        
        for req_flag in self.required:
            if not req_flag in res:
                raise Exception("Missing required flag")

        return res


    # Tokenize a string of arguments to approximate sys.argv support for
    # systems that lack it
    #
    # The passed string should have the program name removed if the underlying
    # command line arguments would include it as argv[0]
    def parse_string(self, s):
        tokens = []

        literal_start = False
        # Tokenize on literal string tokens, assume literals are between a pair of ' or "
        # characters with any ' or " in the literal escaped with a \\
        for elem in re.split('(?<!\\\)\'|"', s):
            if not literal_start:
                tokens.append((elem, False))
                literal_start = True
            else:
                tokens.append((elem, True))
                literal_start = False

        # Trim empty and whitespace elements (that are not literals) from token list
        for elem in tokens:
            if elem[1] == False and (len(elem[0]) == 0 or re.match('^\s*$', elem[0]) != None):
                tokens.remove(elem)

        # Split non literal tokens on whitespace keeping token order intact
        split_tokens = []
        for elem in tokens:
            if elem[1] == False:
                for part in re.split('\s+', elem[0]):
                    # Strip empty elements from the split result
                    if not len(part) == 0 and not re.match('^\s*$', part) != None:
                        split_tokens.append(part)
            else:
                split_tokens.append(elem[0])

        return split_tokens

# Verifier function, allows developer to translate a flag value into a different value set to the
# flag in the result dictionary returned by the parse_args function
def check_foo(flag_name, val=None):
    if val is None:
        raise Exception("Value required for flag %s" % flag_name)
    else:
        # Translate string to int in eventual flagname to value mapping returned by parse_args
        if val == "bar":
            return 1
        else:
            raise Exception("Foo flag must be one of [bar]")

def check_baz(flag_name, val=None):
    # Translate string -baz flag to baz=True mapping in result dictionary returned by parse_args
    return True

def check_literal(flag_name, val=None):
    if val is None:
        raise Exception("Value required for flag %s" % flag_name)
    return val

# A bit of testing
p = Parser({"foo":check_foo, "baz":check_baz, "literal1":check_literal, "literal2":check_literal}, None, None)

res = p.parse_args(p.parse_string("--foo bar -baz -literal1 \"This is\" --literal2 \"A Test\""))
print res