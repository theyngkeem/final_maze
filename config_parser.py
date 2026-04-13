from typing import Callable
import sys


KEYS: dict[str, Callable[[str], object]] = {
    "WIDTH": lambda v: int(v),
    "HEIGHT": lambda v: int(v),
    "ENTRY": lambda v: parse_coord(v),
    "EXIT": lambda v: parse_coord(v),
    "OUTPUT_FILE": lambda v: v,
    "PERFECT": lambda v: v.lower() in
    ("true", "false") and v.lower() == "true",
}

OP_KEYS: dict[str, Callable[[str], object]] = {
    "SEED": lambda v: int(v),
}


def parser(file: str) -> dict[str, str]:
    """ parse the config file and return dict of params"""
    res = {}
    with open(file, "r") as f:
        text = f.read()
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ValueError("invalide format")
            key, value = line.split('=', 1)
            res[key.upper()] = value
        return res


def parse_coord(point: str) -> tuple[int, int]:
    """parse width or height return them as tuple"""
    if not point or ',' not in point:
        raise ValueError("the coords are wrong we expect [x,y]")
    cord = point.split(',', 1)
    if len(cord) != 2:
        raise ValueError("the coords are wrong we expect [x,y]")
    try:
        x, y = int(cord[0]), int(cord[1])
    except ValueError:
        raise ValueError("coords must be integers")
    return (x, y)


def exec_converter(inp: dict[str, str]) -> dict:
    """use the key dict to convert every value"""
    res = {}
    for key, conv in KEYS.items():
        if key not in inp:
            raise ValueError("the key isnt valid")
        try:
            res[key] = conv(inp[key])
        except Exception:
            raise ValueError(f"invalid value for {key}: {inp[key]}")

    for key, conv in OP_KEYS.items():
        if key not in inp:
            res[key] = None
        else:
            try:
                res[key] = conv(inp[key])
            except Exception:
                res[key] = None
    return res


def check_validition(keys: dict) -> None:
    """check if the input valid"""
    width = keys["WIDTH"]
    height = keys["HEIGHT"]
    entry = keys["ENTRY"]
    exit_ = keys["EXIT"]
    if width <= 0 or height <= 0:
        raise ValueError("WIDTH and HEIGHT must be positive integers")
    if entry == exit_:
        raise ValueError("ENTRY and EXIT must be different positions")

    entry_x, entry_y = entry
    exit_x, exit_y = exit_
    if not (0 <= entry_x < width and 0 <= entry_y < height):
        raise ValueError("the entry point aint in maze bounds")
    if not (0 <= exit_x < width and 0 <= exit_y < height):
        raise ValueError("the exit point aint in maze bounds")


def iniesta_parser(path: str) -> dict:
    """the engine of parsing callin every func separetly for easy management"""
    try:
        inp = parser(path)
        res = exec_converter(inp)
        check_validition(res)
        return res
    except Exception as error:
        print(f"ERROOOOOOOR: {error}")
        sys.exit(1)
