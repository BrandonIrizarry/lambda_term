import sys, enum, re

IDENT = r"[A-Za-z_][A-Za-z0-9_]*"

class Term(enum.StrEnum):
    NAME = "name"
    ABSTRACTION = "abstraction"
    APPLICATION = "application"

    def __repr__(self):
        return self

def new_name(index):
    """Construct and return a name with the given INDEX."""
    
    return {
        "kind": Term.NAME,
        "index": index,
    }


def new_abstraction(body):
    """Construct and return an abstraction with the given BODY."""
    
    return {
        "kind": Term.ABSTRACTION,
        "body": body,
    }


def new_application(left, right):
    """Construct and return an application with the given LEFT and
    RIGHT terms."""

    return {
        "kind": Term.APPLICATION,
        "left": left,
        "right": right,
    }


def parseApplication(tokens, i, env):
    """Return a parsed application, as well as the index corresponding
    to the start of the next lambda term."""

    print("Parsing application at:", i, tokens[i])

    # Skip the left parenthesis.
    i += 1
    
    left, i = parseTerm(tokens, i, env[:])
    right, i = parseTerm(tokens, i, env[:])

    # Skip the closing parenthesis.
    i += 1
    
    return new_application(left, right), i
    

def parseAbstraction(tokens, i, env):
    print("Parsing abstraction at:", i, tokens[i])
    # Skip the lambda symbol.
    i += 1

    # Record the formal parameter inside env.
    print("Appending to env:", i, tokens[i], env)
    env.append(tokens[i])

    # Move past the dot.
    i += 2

    print("Looking at term:", i, tokens[i])
    
    body, i = parseTerm(tokens, i, env[:])
    
    return new_abstraction(body), i
    
    
def parseName(tokens, i, env):
    print("Parsing name at:", i, tokens[i])
    
    name = new_name(len(env) - env.index(tokens[i]) - 1)
    i += 1

    return name, i
    

def parseTerm(tokens, i, env):
    """Parse TOKENS and return a parse tree (along with the current
    index into TOKENS.)"""
        
    if tokens[i] == "(":
        return parseApplication(tokens, i, env[:])
    elif tokens[i] == "\\":
        return parseAbstraction(tokens, i, env[:])
    elif re.fullmatch(IDENT, tokens[i]):
        return parseName(tokens, i, env[:])
    else:
        print("Wrong", i, tokens[i])
                            
    
# The trick is to parse a string such as:
# ((\x.\y.(y x) \p.\q.p) \i.i)
# and end up with:
#

result = new_application(new_abstraction(new_abstraction(new_application(new_name(0),
                                                                         new_name(1)))),
                         new_abstraction(new_name(0)))


input = "   ((\\input.\\func.(  func input  ) \\first.\\second.first) \\sole.sole)"

def tokenize(s):
    token_pattern = r"[A-Za-z_][A-Za-z0-9_]*|[\\().]"
    return re.findall(token_pattern, s)
    
tokens = tokenize(input)
print(tokens)

import pprint

pp = pprint.PrettyPrinter(depth=10)

pp.pprint(parseTerm(tokens, 0, []))
