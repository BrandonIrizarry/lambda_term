from wonderwords import RandomWord

import lbd.gamma as g
import lbd.term as term

# Use this to generate ad-hoc local variable names inside 'prettify'.
rword = RandomWord()


def prettify(ast: term.AST, env: list[str] = []) -> str:
    """Create a human-readable lambda expression from AST.

    Since the AST is constructed using DeBruijn indices, the original
    local variable names are discarded, and so synthetic names are used
    for the reconstructed human-readable expression.

    Return the prettified version of AST as a string.

    """

    match ast["kind"]:
        case term.Term.NAME:
            fness = term.freeness(ast)

            if fness < 0:
                # An env_depth of -1 corresponds to TOS, -2 t one underneath, etc.
                # Ex: index = 0 -> -1, index = 1 -> -2, etc.
                idx = ast["index"]
                env_depth = -(idx + 1)

                return env[env_depth]
            else:
                free_sym = g.sym_get(fness)

                if free_sym is None:
                    raise ValueError(f"Fatal: sym_get({fness}) failed")

                return free_sym.label.upper()

        case term.Term.ABSTRACTION:
            # Generate a random word to use as the function parameter.
            param: str = rword.word()
            env.append(param)

            body = prettify(ast["body"], env[:])
            return f"\\{param}.{body}"

        case term.Term.APPLICATION:
            left = prettify(ast["left"], env[:])
            right = prettify(ast["right"], env[:])

            return f"({left} {right})"

        case _:
            raise ValueError("Fatal: wrong AST 'kind' field")
