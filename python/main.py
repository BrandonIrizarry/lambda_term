import atexit
import os
import re
import readline

from wonderwords import RandomWord

import directive as dtv
import error as err
import program_env
import term

histfile = os.path.join(os.getcwd(), ".repl_history")

try:
    readline.read_history_file(histfile)
    readline.set_history_length(1000)
except FileNotFoundError:
    pass

atexit.register(readline.write_history_file, histfile)


print("""
Welcome to the lambda REPL.

You can enter an lambda term at the prompt to see its result under
normal order beta reduction.

See the TUTORIAL file accompanying this project for details.

""")

# Use this to generate ad-hoc local variable names (see docstring of
# 'pretty_print_term_ast'.)
rword = RandomWord()


def pretty_print_term_ast(ast, env):
    """Pretty print AST as a human-readable lambda expression.

    Since the AST is constructed using DeBruijn indices, the original
    local variable names are discarded, and so original names are used
    for the reconstructed human-readable expression.

    """

    if ast["kind"] == term.Term.NAME:
        # A depth of -1 corresponds to TOS, -2 t one underneath, etc.
        # Ex: index = 0 -> -1, index = 1 -> -2, etc.
        depth = -(ast["index"] + 1)

        print(env[depth], end="")
    elif ast["kind"] == term.Term.ABSTRACTION:
        # Generate a random word to use as the function parameter.
        param = rword.word()
        env.append(param)

        print("\\{}.".format(param), end="")
        pretty_print_term_ast(ast["body"], env[:])
    elif ast["kind"] == term.Term.APPLICATION:
        print("(", end="")
        pretty_print_term_ast(ast["left"], env[:])
        print(" ", end="")
        pretty_print_term_ast(ast["right"], env[:])
        print(")")


def eval_as_lambda(raw_term, penv):
    try:
        value = penv.evaluate(raw_term)
    except (err.IllegalTokenError, err.ParseError) as e:
        print(e)
        return

    # I suspect we don't need this, but we'll see.
    penv.append_line(raw_term)

    print()
    pretty_print_term_ast(value, [])
    print()


def eval_as_directive(directive: re.Match[str], penv):
    cmd = directive.group("cmd")
    params = directive.group("params").strip().split(" ")

    match cmd:
        case "load":
            filename = params[0]
            status = dtv.load_d(filename)

            if status["error"] is not None:
                print(status["error"])
            else:
                program = status["user_data"]
                penv.load_program(program)
                penv.run()
        case _:
            print(f"Invalid directive: '.{cmd}'")


def repl():
    penv = program_env.ProgramEnv()

    while True:
        try:
            repl_input = input("> ")
        except EOFError:
            break

        if repl_input == "":
            continue

        readline.add_history(repl_input)

        directive = re.match(
            r"(\.)(?P<cmd>.+?\b)(?P<params>.*)", repl_input)

        if directive is None:
            eval_as_lambda(repl_input, penv)
        else:
            eval_as_directive(directive, penv)


repl()
