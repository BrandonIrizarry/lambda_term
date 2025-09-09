from wonderwords import RandomWord

import lbd.gamma as g
import lbd.term as term

# Use this to generate ad-hoc local variable names inside 'prettify'.
rword = RandomWord()


def prettify_rec(ast: term.AST,
                 env: list[str],
                 indent: int,
                 omit_parens: bool,
                 used_names: set[str]) -> tuple[str, set[str]]:
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
                return name, {*used_names, name}

            free_idx = idx - len(env)
            free_sym = g.sym_get(free_idx)

            if free_sym is None:
                raise ValueError(f"Fatal: sym_get({free_idx}) failed")

            return free_sym.label.upper(), used_names

        case term.Abstraction():
            # Generate a random word to use as the function parameter.
            param: str = rword.word(regex=r"[a-z]+")

            # Make sure that binders are unique as we move down the
            # scope.
            while param in env:
                param = rword.word(regex=r"[a-z]+")

            body, used = prettify_rec(ast.body,
                                      [*env, param],
                                      indent,
                                      False,
                                      used_names)

            if param in used:
                return f"\\{param}.{body}", {*used_names, *used}

            return f"\\_.{body}", {*used_names, *used}

        case term.Application():
            # ( adds a space of indentation
            indent += 1

            left, used_left = prettify_rec(ast.left,
                                           env,
                                           indent,
                                           True,
                                           used_names)

            right, used_right = prettify_rec(ast.right,
                                             env,
                                             indent,
                                             False,
                                             used_names)

            used_app = {*used_left, *used_right}

            # + 2 for \ and . If param is unused in 'union', then
            # param will be set as '_', giving a total of 3 in that
            # case.
            for param in env:
                if param in used_app:
                    indent += len(param) + 2
                else:
                    indent += 3

            padding = " " * indent

            if omit_parens:
                return f"{left}\n{padding}{right}", used_app

            return f"({left}\n{padding}{right})", used_app

        case term.Assignment():
            # I know prettifying a name won't add a used name, but
            # let's leave it this way for completion.
            name, used_in_name = prettify_rec(ast.name,
                                              env,
                                              indent,
                                              False,
                                              used_names)

            value, used_in_value = prettify_rec(ast.value,
                                                env,
                                                indent,
                                                False,
                                                used_names)

            return f"<{name}, {value}>", {*used_in_name, *used_in_value}

        case term.Empty():
            return f"{ast}", used_names

        case _:
            raise ValueError("Fatal: wrong AST 'kind' field")


def prettify(ast: term.AST) -> str:
    """Create a human-readable lambda expression from AST.

   Since the AST is constructed using DeBruijn indices, the original
   local variable names are discarded, and so synthetic names are used
   for the reconstructed human-readable expression.

   Return the prettified version of AST as a string.

   """

    # The set of used binders isn't used at this top-level invocation.
    pretty, _ = prettify_rec(ast, [], 0, False, set())

    return pretty
