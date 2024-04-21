import curses
import time
import random

from animations import animate_spaceship, blink, fill_orbit_with_garbage
from game_scenario import increase_in_time, show_year
from globals import constants
from curses_tools import get_random_coord, get_random_symbol


def draw(canvas):
    max_row, max_column = canvas.getmaxyx()
    canvas.nodelay(True)
    canvas.border()
    curses.curs_set(False)
    constants.coroutines.append(blink(canvas,
                                    row=get_random_coord(max_row),
                                    column=get_random_coord(max_column),
                                    offset_tics=random.randint(0, 3),
                                    symbol=get_random_symbol())
                              for _ in range(100))

    constants.coroutines.append(
        animate_spaceship(canvas,
                          max_row / 2,
                          max_column / 2,
                          max_row,
                          max_column)
    )
    constants.coroutines.append(
        fill_orbit_with_garbage(canvas, max_column)
    )
    constants.coroutines.append(show_year(canvas))
    constants.coroutines.append(increase_in_time())
    while True:
        for coroutine in constants.coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                constants.coroutines.remove(coroutine)
        canvas.refresh()
        if len(constants.coroutines) == 0:
            break
        time.sleep(constants.tic_timeout)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
