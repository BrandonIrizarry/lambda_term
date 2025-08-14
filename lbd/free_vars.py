import lbd.evaluate as evl
import lbd.term as term

# FIXME: we need to ensure that this never clashes with the local-var
# indices assigned by 'parse_name'. Perhaps define a globals.py
# constant that sets this limit (right now hardcoded with some very
# large value.)
fvar_idx = 100000000


def new_free_var(symbol_name: str):
    global fvar_idx

    name = term.new_name(fvar_idx)
    name["symbol_name"] = symbol_name

    fvar_idx += 1

    return name


def lookup_free_var(genv: "evl.Genv", symbol_name: str):
    for gdef in reversed(genv):
        if gdef["label"] == symbol_name:
            return gdef["ast"]

    return None
