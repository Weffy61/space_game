import asyncio
import curses
import os
import random
from itertools import cycle

from control_spaceship import read_controls
from get_frame import get_slide
from sleep import async_sleep
from text_utils import get_frame_size, get_random_trash


def draw_frame(canvas, start_row, start_column, text, negative=False):
    """Draw multiline text fragment on canvas, erase text instead of drawing if negative=True is specified."""
    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue

        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue

            if column >= columns_number:
                break

            if symbol == ' ':
                continue

            # Check that current position it is not in a lower right corner of the window
            # Curses will raise exception in that case. Don`t ask why…
            # https://docs.python.org/3/library/curses.html#curses.window.addch
            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)


async def animate_spaceship(canvas, row, column, max_row, max_column):
    frame1 = get_slide(os.path.join('frames', 'rocket_frame.txt'))
    frame2 = get_slide(os.path.join('frames', 'rocket_frame_2.txt'))

    for frame in cycle([frame1, frame1, frame2, frame2]):
        frame_rows, frame_columns = get_frame_size(frame)
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        position_row = rows_direction + row
        position_column = columns_direction + column

        if 0 < position_row < max_row - frame_rows:
            row = position_row

        if 0 < position_column < max_column - frame_columns:
            column = position_column

        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)

        draw_frame(canvas, row, column, frame, negative=True)


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def blink(canvas, row, column, offset_tics, symbol='*'):
    while True:
        await async_sleep(offset_tics)

        canvas.addstr(row, column, symbol, curses.A_DIM)
        await async_sleep(20)

        canvas.addstr(row, column, symbol)
        await async_sleep(3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await async_sleep(5)

        canvas.addstr(row, column, symbol)
        await async_sleep(3)


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed


async def fill_orbit_with_garbage(canvas, max_column, coroutines):
    while True:
        column = random.randint(1, max_column - 1)
        coroutine = fly_garbage(
            canvas,
            column,
            garbage_frame=get_slide(os.path.join('frames', get_random_trash())))
        coroutines.append(coroutine)
        await async_sleep(random.randint(5, 10))
        # for _ in range(random.randint(5, 10)):
        #     await asyncio.sleep(0)
        #     await asyncio.sleep(0)
