import re
from typing import Optional

from pyModeS import common

CHAR_LOOKUP = "#ABCDEFGHIJKLMNOPQRSTUVWXYZ##### ###############0123456789######"

def is21(msg: str) -> bool:
    """Check if a message is likely to be BDS code 2,1

    Args:
        msg (str): 28 hexdigits string

    Returns:
        bool: True or False
    """
    if common.allzeros(msg):
        return False

    d = common.hex2bin(common.data(msg))

    # Last 13 bits should be zero (airline registration is rarely filled)
    if d[43:56] != "0000000000000":
        return False

    return ar21(msg) is not None


def ar21(msg: str) -> Optional[str]:
    """
    Args:
       msg (str): 28 hexdigits string

    Returns:
      tuple[bool, Optional[str]]: A tuple containing the status and the aircraft registration (if valid found)

    Note: implementation ported from https://github.com/xoolive/rs1090/blob/master/crates/rs1090/src/decode/bds/bds21.rs
    """
    d = common.hex2bin(common.data(msg))

    status = bool(d[0])
    if not status:
        return None

    chars: list[int] = []
    for i in range(1, 42, 6):
        c = common.bin2int(d[i:i+6])
        if c != 32:
            chars.append(c)

    encoded = ''.join(CHAR_LOOKUP[b] for b in chars)

    if re.match(r'^[A-Z0-9]+[\s#]?[A-Z0-9]+$', encoded):
        return encoded

    return None