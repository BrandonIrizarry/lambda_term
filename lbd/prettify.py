from wonderwords import RandomWord

import lbd.gamma as g
import lbd.term as term

# Use this to generate ad-hoc local variable names inside 'prettify'.
rword = RandomWord()


def prettify(ast: term.AST, env: list[str] = [], level=0, omit_parens=False) -> str:
    """Create a human-readable lambda expression from AST.

    Since the AST is constructed using DeBruijn indices, the original
    local variable names are discarded, and so synthetic names are used
    for the reconstructed human-readable expression.

    Return the prettified version of AST as a string.

    """

    match ast:
        case term.Name():
            fness = ast.freeness

            if fness < 0:
                # An env_depth of -1 corresponds to TOS, -2 t one underneath, etc.
                # Ex: index = 0 -> -1, index = 1 -> -2, etc.
                idx = ast.index
                env_depth = -(idx + 1)

                return env[env_depth]
            else:
                free_sym = g.sym_get(fness)

                if free_sym is None:
                    raise ValueError(f"Fatal: sym_get({fness}) failed")

                return free_sym.label.upper()

        case term.Abstraction():
            # Generate a random word to use as the function parameter.
            param: str = rword.word(regex=r"[a-z]+")

            # Make sure that binders are unique as we move down the
            # scope.
            while param in env:
                param = rword.word(regex=r"[a-z]+")

            # + 2 for \ and .
            level += len(param) + 2

            body = prettify(ast.body, [*env, param], level)
            return f"\\{param}.{body}"

        case term.Application():
            # ( adds a space of indentation
            level += 1

            left = prettify(ast.left, env, level=level, omit_parens=True)
            right = prettify(ast.right, env, level=level)

            indent = " " * level

            if omit_parens:
                return f"{left}\n{indent}{right}"

            return f"({left}\n{indent}{right})"

        case term.Assignment():
            name = prettify(ast.name, env)
            value = prettify(ast.value, env)

            return f"<{name}, {value}>"

        case term.Empty():
            return f"{ast}"

        case _:
            raise ValueError("Fatal: wrong AST 'kind' field")
