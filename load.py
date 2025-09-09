import re

from lbd.error import LambdaError
from lbd.evaluate import eval_raw_term


def chunks(filename: str) -> list[str]:
    """Isolate individual expressions.

    Return a list of the expressions in FILENAME, with comments first
    stripped away.

    """

    with open(filename, "r") as f:
        contents = f.read().strip()
        contents = re.sub(r"\#.+?\#", "", contents, flags=re.DOTALL)

        chunks = [chunk.strip() for chunk in contents.split(";")]

        # If a stray empty string makes it in at the end, remove it.
        if chunks[-1] == "":
            chunks.pop()

        return chunks


def load(filenames: list[str]) -> LambdaError | None:
    for filename in filenames:
        cks = chunks(filename)

        # For now, terms are only evaluated for their side-effects;
        # hence, the result of 'eval_raw_term' isn't stored anywhere.
        for c in cks:
            err = eval_raw_term(c)

            if isinstance(err, LambdaError):
                return err

        return None
