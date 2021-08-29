SOURCE_CODE = """
    && ||
    # comment
    let pi = 314;
    fun area(ratio) { # comment
        pi * ratio * ratio + 0;
    }

    13 / 3 > 16;
    # comment
    if(10 - 8 < 16) {
        return true;
        # comment
    } else {
        return false;
    }

    # comment
    10 == 10;
    10 != 9;
"""

DELIMETERS = "(){},;"

ILLEGAL = "~`^"

OPERATORS = "+=-!*/<>%"

TWO_CHARACTER_SYMBOLS = "&& || ! == != ="

IDENTIFIERS = "someone in the crowd"

NUMBERS = "314 217 161"

KEYWORDS = "let fun true false null if else return"

STRINGS = '"hello world" "good morning" "happy jueves"'
