
def count_bool(
    a1: bool,
    a2: bool,
    a3: bool,
    a4: bool,
    a5: bool,
    a6: bool,
    a7: bool,
    a8: bool,
    a9: bool,
    a10: bool,
    a11: bool,
    a12: bool,
    a13: bool,
    a14: bool,
    a15: bool,
    a16: bool,
    a17: bool,
    a18: bool,
    a19: bool,
    a20: bool,
    a21: bool,
    a22: bool,
    a23: bool,
    a24: bool,
    a25: bool,
    a26: bool,
    a27: bool,
    a28: bool,
    a29: bool,
    a30: bool,
    a31: bool,
    a32: bool,
    a33: bool,
    a34: bool,
    a35: bool,
    a36: bool,
    a37: bool,
    a38: bool,
    a39: bool,
    a40: bool,
    a41: bool,
    a42: bool,
    a43: bool,
    a44: bool,
    a45: bool,
    a46: bool,
    a47: bool,
    a48: bool,
    a49: bool,
    a50: bool
) -> int:
    count = 0

    if a1:
        count += 1
    else:
        return count

    if a2:
        count += 1
    else:
        return count

    if a3:
        count += 1
    else:
        return count

    if a4:
        count += 1
    else:
        return count

    if a5:
        count += 1
    else:
        return count

    if a6:
        count += 1
    else:
        return count

    if a7:
        count += 1
    else:
        return count

    if a8:
        count += 1
    else:
        return count

    if a9:
        count += 1
    else:
        return count

    if a10:
        count += 1
    else:
        return count

    if a11:
        count += 1
    else:
        return count

    if a12:
        count += 1
    else:
        return count

    if a13:
        count += 1
    else:
        return count

    if a14:
        count += 1
    else:
        return count

    if a15:
        count += 1
    else:
        return count

    if a16:
        count += 1
    else:
        return count

    if a17:
        count += 1
    else:
        return count

    if a18:
        count += 1
    else:
        return count

    if a19:
        count += 1
    else:
        return count

    if a20:
        count += 1
    else:
        return count

    if a21:
        count += 1
    else:
        return count

    if a22:
        count += 1
    else:
        return count

    if a23:
        count += 1
    else:
        return count

    if a24:
        count += 1
    else:
        return count

    if a25:
        count += 1
    else:
        return count

    if a26:
        count += 1
    else:
        return count

    if a27:
        count += 1
    else:
        return count

    if a28:
        count += 1
    else:
        return count

    if a29:
        count += 1
    else:
        return count

    if a30:
        count += 1
    else:
        return count

    if a31:
        count += 1
    else:
        return count

    if a32:
        count += 1
    else:
        return count

    if a33:
        count += 1
    else:
        return count

    if a34:
        count += 1
    else:
        return count

    if a35:
        count += 1
    else:
        return count

    if a36:
        count += 1
    else:
        return count

    if a37:
        count += 1
    else:
        return count

    if a38:
        count += 1
    else:
        return count

    if a39:
        count += 1
    else:
        return count

    if a40:
        count += 1
    else:
        return count

    if a41:
        count += 1
    else:
        return count

    if a42:
        count += 1
    else:
        return count

    if a43:
        count += 1
    else:
        return count

    if a44:
        count += 1
    else:
        return count

    if a45:
        count += 1
    else:
        return count

    if a46:
        count += 1
    else:
        return count

    if a47:
        count += 1
    else:
        return count

    if a48:
        count += 1
    else:
        return count

    if a49:
        count += 1
    else:
        return count

    if a50:
        count += 1
    else:
        return count

    return count

EXPORT_FUNCTION = count_bool
import afl
import sys
afl.init()
try:
    s=sys.stdin.read()
    bool_list = [word.lower() == "true" for word in s.split()]
    EXPORT_FUNCTION(*bool_list)
except ValueError:
    pass