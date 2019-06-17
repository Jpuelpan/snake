import curses
import time
import logging

from threading import Thread

logging.basicConfig(
    level=logging.DEBUG,
    filename="debug.log",
    filemode='a',
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S'
)

class SnakeControls(Thread):
    def __init__(self, screen):
        self.screen = screen
        Thread.__init__(self)

    def run(self):
        self.key = None

        while True:
            self.key = self.screen.getch()
            logging.debug('Pressed key: %s', self.key)

def start_game(screen):
    curses.curs_set(0)
    screen.clear()
    screen.refresh()

    # Start input thread to catch all keypresses
    controls = SnakeControls(screen)
    controls.daemon = True
    controls.start()
    # height, width = screen.getmaxyx()

    while True:
        screen.clear()
        screen.addstr('Snake')
        screen.refresh()

        logging.debug('Loop!')

        time.sleep(1)

def main():
    curses.wrapper(start_game)

if __name__ == "__main__":
    main()
