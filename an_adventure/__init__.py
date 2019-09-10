import curses
# https://docs.python.org/3/howto/curses.html

import time

def main(stdscr):
    curses.start_color()
    stdscr.clear()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLUE)
    for i in reversed(range(1, 11)):
        stdscr.addstr(10-i, 0, '10 divided by {} is {}'.format(i, 10/i), curses.color_pair(1))
        stdscr.refresh()
        time.sleep(1)


def start():
    curses.wrapper(main)
