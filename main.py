import curses
import time
import random

from animations import animate_spaceship, blink, fire, fill_orbit_with_garbage
from text_utils import get_random_coord, get_random_symbol

TIC_TIMEOUT = 0.1


def draw(canvas):
    max_row, max_column = canvas.getmaxyx()
    canvas.nodelay(True)
    canvas.border()
    curses.curs_set(False)
    coroutines = [
        blink(canvas,
              row=get_random_coord(max_row),
              column=get_random_coord(max_column),
              offset_tics=random.randint(0, 3),
              symbol=get_random_symbol())
        for _ in range(100)]
    # coroutines.append(
    #     fire(canvas,
    #          start_row=max_row - 2,
    #          start_column=max_column / 2 + 2)
    # )
    coroutines.append(
        animate_spaceship(canvas,
                          max_row / 2,
                          max_column / 2,
                          max_row,
                          max_column,
                          coroutines))
    coroutines.append(
        fill_orbit_with_garbage(canvas, max_column, coroutines)
    )
    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        if len(coroutines) == 0:
            break
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
