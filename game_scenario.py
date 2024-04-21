import asyncio

from globals import Globals
from sleep import async_sleep

PHRASES = {
    1957: "First Sputnik",
    1961: "Gagarin flew!",
    1969: "Armstrong got on the moon!",
    1971: "First orbital space station Salute-1",
    1981: "Flight of the Shuttle Columbia",
    1998: 'ISS start building',
    2011: 'Messenger launch to Mercury',
    2020: "Take the plasma gun! Shoot the garbage!",
}


def get_garbage_delay_tics(year):
    if year < 1961:
        return None
    elif year < 1969:
        return 20
    elif year < 1981:
        return 14
    elif year < 1995:
        return 10
    elif year < 2010:
        return 8
    elif year < 2020:
        return 6
    else:
        return 2


async def show_year(canvas):
    max_row, max_column = canvas.getmaxyx()
    inscription = canvas.derwin(4, max_column, max_row - 4, 0)
    while True:
        if Globals.year in PHRASES.keys():
            phrase = PHRASES.get(Globals.year)
            inscription.addstr(2, 2, phrase)
        else:
            inscription.addstr(2, 2, ' ' * max_column)
        inscription.addstr(1, 1, f'YEAR: {Globals.year}')
        inscription.refresh()
        await asyncio.sleep(0)


async def increase_in_time():
    while True:
        await async_sleep(15)
        Globals.year += 1



