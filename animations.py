import asyncio
import curses
import os
import random
from itertools import cycle

from control_spaceship import read_controls
from curses_tools import draw_frame
from explosion import explode
from get_frame import get_slide
from globals import COROUTINES, OBSTACLES, OBSTACLES_IN_LAST_COLLISIONS
from obstacles import Obstacle, show_obstacles
from physics import update_speed
from sleep import async_sleep
from curses_tools import get_frame_size, get_random_trash


async def animate_spaceship(canvas, row, column, max_row, max_column):
    frame1 = get_slide(os.path.join('frames', 'rocket_frame.txt'))
    frame2 = get_slide(os.path.join('frames', 'rocket_frame_2.txt'))
    row_speed = column_speed = 0

    for frame in cycle([frame1, frame1, frame2, frame2]):
        frame_rows, frame_columns = get_frame_size(frame)
        rows_direction, columns_direction, space_pressed = read_controls(canvas)

        row_speed, column_speed = update_speed(row_speed, column_speed, rows_direction, columns_direction)
        row += row_speed
        column += column_speed

        if row < 0:
            row = 0
        elif row > max_row - frame_rows:
            row = max_row - frame_rows

        if column < 0:
            column = 0
        elif column > max_column - frame_columns:
            column = max_column - frame_columns

        if space_pressed:
            COROUTINES.append(fire(canvas, row - 1, column + 2))

        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)

        draw_frame(canvas, row, column, frame, negative=True)


async def fire(canvas, start_row, start_column, rows_speed=-2, columns_speed=0):
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
        for obstacle in OBSTACLES:
            if obstacle.has_collision(row, column):
                OBSTACLES_IN_LAST_COLLISIONS.append(obstacle)
                return
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
    row_size, columns_size = get_frame_size(garbage_frame)

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    obstacle = Obstacle(row, column, row_size, columns_size)
    OBSTACLES.append(obstacle)
    # COROUTINES.append(show_obstacles(canvas, OBSTACLES))

    try:
        while row < rows_number:
            if obstacle in OBSTACLES_IN_LAST_COLLISIONS:
                OBSTACLES_IN_LAST_COLLISIONS.remove(obstacle)
                await explode(canvas, obstacle.row + row_size // 2, obstacle.column + columns_size // 2)
                return

            obstacle.row = row
            draw_frame(canvas, row, column, garbage_frame)
            await asyncio.sleep(0)
            draw_frame(canvas, row, column, garbage_frame, negative=True)
            row += speed
    finally:
        OBSTACLES.remove(obstacle)


async def fill_orbit_with_garbage(canvas, max_column):
    while True:
        column = random.randint(1, max_column - 1)
        coroutine = fly_garbage(
            canvas,
            column,
            garbage_frame=get_slide(os.path.join('frames', get_random_trash())))
        COROUTINES.append(coroutine)
        await async_sleep(random.randint(15, 20))

