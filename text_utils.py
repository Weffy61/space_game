import random


def get_frame_size(text):
    """Calculate size of multiline text fragment, return pair — number of rows and colums."""

    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])
    return rows, columns


def get_random_coord(max_coord):
    return random.randint(1, max_coord - 2)


def get_random_symbol():
    symbols = '+*.:'
    return random.choice(symbols)

