SOURCE_CODE = """
    let pi = 314;
    fun area(ratio) {
        pi * ratio * ratio + 0;
    }

    13 / 3 > 16;

    if(10 - 8 < 16) {
        return true;
    } else {
        return false;
    }

    10 == 10;
    10 != 9;
"""

DELIMETERS = "(){},;"

ILLEGAL = "~`^"

OPERATORS = "+=-!*/<>"

TWO_CHARACTER_SYMBOLS = "! == != ="

IDENTIFIERS = "someone in the crowd"

NUMBERS = "314 217 161"

KEYWORDS = "let fun true false if else return"
