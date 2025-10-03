from wonderwords import RandomWord

import lbd.gamma as g
import lbd.term as term

# Use this to generate ad-hoc local variable names inside 'prettify'.
rword = RandomWord()


def prettify_free_symbol(name: term.Name, depth: int) -> str:
    free_idx = name.index - depth
    free_sym = g.sym_get(free_idx)

    if free_sym is None:
        raise ValueError(f"Fatal: sym_get({free_idx}) failed")

    return free_sym.label.upper()


def prettify_rec(ast: term.AST,
                 env: list[str],
                 indent: int) -> str:
    """Recursive helper for 'prettify'.

    The actual prettification logic lives here.

    """

    match ast:
        case term.Name():
            # An env_depth of -1 corresponds to TOS, -2 t one underneath, etc.
            # Ex: index = 0 -> -1, index = 1 -> -2, etc.
            idx = ast.index
            env_depth = -(idx + 1)

            if abs(env_depth) <= len(env):
                name = env[env_depth]
                return name

            return prettify_free_symbol(ast, len(env))

        case term.Abstraction():
            # Generate a random word to use as the function parameter.
            param: str = rword.word(regex=r"[a-z]+")

            # Make sure that binders are unique as we move down the
            # scope.
            while param in env:
                param = rword.word(regex=r"[a-z]+")

            indent += len(param) + 2

            body = prettify_rec(ast.body,
                                [*env, param],
                                indent)

            return f"\\{param}.{body}"

        case term.Application():
            # ( adds a space of indentation
            indent += 1

            left = prettify_rec(ast.left,
                                env,
                                indent)

            right = prettify_rec(ast.right,
                                 env,
                                 indent)

            padding = " " * indent

            return f"({left}\n{padding}{right})"

        case term.Assignment():
            name = prettify_rec(ast.name,
                                env,
                                indent)

            indent += len(f"def {name}:=")

            value = prettify_rec(ast.value,
                                 env,
                                 indent)

            return f"def {name}:={value}"

        case term.Empty():
            return f"{ast}"

        case _:
            raise ValueError("Fatal: wrong AST 'kind' field")


def prettify(ast: term.AST) -> str:
    """Create a human-readable lambda expression from AST.

    Since the AST is constructed using DeBruijn indices, the original
    local variable names are discarded, and so synthetic names are used
    for the reconstructed human-readable expression.

    Return the prettified version of AST as a string.

    """

    pretty = prettify_rec(ast, [], 0)

    return pretty
