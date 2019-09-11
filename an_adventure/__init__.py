import curses
# https://docs.python.org/3/howto/curses.html

import time

def main(stdscr):
    curses.start_color()
    stdscr.clear()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_RED)
    for i in reversed(range(1, 11)):
        stdscr.addstr(10-i, 0, '10 divided by {} is {}'.format(i, 10/i), curses.color_pair(1))
        stdscr.refresh()
        time.sleep(1)
    for lives in reversed(range(1,11)):
        stdscr.addstr(10-lives, 25, 'Fuck You in {}'.format(lives), curses.color_pair(2))
        stdscr.refresh()
        time.sleep(.001)
    time.sleep(10)


def start():
    curses.wrapper(main)
