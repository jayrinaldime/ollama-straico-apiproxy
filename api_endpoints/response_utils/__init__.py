import codecs
from os import environ

__FIX_ESCAPE_TYPOS = environ.get("FIX_ESCAPE_TYPOS", "true").strip() == "true"


def fix_escaped_characters(text_with_errors: str) -> str:
    """
    Corrects "double-escaped" character sequences in a string.

    For example, '\\n' becomes '\n'. It uses codecs.decode('unicode_escape')
    to handle a wide range of standard Python escape sequences.

    Args:
        text_with_errors: The input string with potential double-escaped sequences.

    Returns:
        A string with escape sequences corrected.
    """

    if not __FIX_ESCAPE_TYPOS:
        return text_with_errors
    try:
        return codecs.decode(text_with_errors, "unicode_escape")
    except:
        return text_with_errors


if __name__ == "__main__":
    print(fix_escaped_characters("This should be a newline |\n|"))
    print(fix_escaped_characters("This should be a newline |\\n|"))
    print(fix_escaped_characters("This should be a tab |\t|"))
    print(fix_escaped_characters("This should be a tab |\\t|"))
    print(fix_escaped_characters("This should be a newline |\\n\\n|"))
    print(fix_escaped_characters("This should be a newline |\n\n|"))
