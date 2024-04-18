import curses
import time
import random

from animations import animate_spaceship, blink, fill_orbit_with_garbage
from globals import COROUTINES, TIC_TIMEOUT
from utils import get_random_coord, get_random_symbol


def draw(canvas):
    max_row, max_column = canvas.getmaxyx()
    canvas.nodelay(True)
    canvas.border()
    curses.curs_set(False)
    COROUTINES.append(blink(canvas,
                            row=get_random_coord(max_row),
                            column=get_random_coord(max_column),
                            offset_tics=random.randint(0, 3),
                            symbol=get_random_symbol())
                      for _ in range(100))

    COROUTINES.append(
        animate_spaceship(canvas,
                          max_row / 2,
                          max_column / 2,
                          max_row,
                          max_column)
    )
    COROUTINES.append(
        fill_orbit_with_garbage(canvas, max_column)
    )
    while True:
        for coroutine in COROUTINES.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                COROUTINES.remove(coroutine)
        canvas.refresh()
        if len(COROUTINES) == 0:
            break
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
