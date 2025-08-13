LAMBDA_SRC = "lambda"


def lambda_filename(filename: str) -> str:
    """Return the true relative filename of FILENAME.

    By convention, all programs in Lambda Term are inside the
    directory contained in the 'LAMBDA_SRC' configuration variable.

    """

    return f"{LAMBDA_SRC}/{filename}"
