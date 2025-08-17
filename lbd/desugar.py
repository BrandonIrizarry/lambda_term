import lbd.error as err
import lbd.tokenize_lambda as tkz


def desugar_def(tokens: list[tkz.Token]) -> tuple[list[tkz.Token], str | None] | Exception:
    if not tkz.is_def_t(tokens[0]):
        return tokens, None

    second_token = tokens[1]

    if not tkz.is_name_t(second_token):
        return err.error(tokens, 1, err.Err.MALFORMED_DEF)

    label = second_token["value"]

    # Move the left-side params to the right side as lambda
    # binders.
    mid = tkz.find(tokens, tkz.assign_t())

    if mid == -1:
        return err.error(tokens, len(tokens), err.Err.MISSING_ASSIGN_OP)

    params = tokens[2:mid]
    body = tokens[mid+1:]

    fn_prefix = []

    for p in params:
        for t in [tkz.lambda_t(), p, tkz.dot_t()]:
            fn_prefix.append(t)

    tokens = fn_prefix + body

    return tokens, label
