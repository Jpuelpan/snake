import curses
import time
import logging

from threading import Thread
from random import randint

logging.basicConfig(
    level=logging.DEBUG,
    filename="debug.log",
    filemode='a',
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S'
)

class SnakeControls(Thread):
    def __init__(self, screen, position):
        self.screen = screen
        self.position = position
        self.y = position[0]
        self.x = position[1]

        Thread.__init__(self)

    def run(self):
        self.key = None

        while True:
            self.key = self.screen.getch()
            logging.debug('Pressed key: %s', self.key)

            if self.key == curses.KEY_UP:
                self.y = self.y - 1
            elif self.key == curses.KEY_LEFT:
                self.x = self.x - 1
            elif self.key == curses.KEY_DOWN:
                self.y = self.y + 1
            elif self.key == curses.KEY_RIGHT:
                self.x = self.x + 1

    def get_position(self):
        return (self.y, self.x)

def start_game(screen):
    curses.curs_set(0)
    screen.clear()
    screen.refresh()

    # Body
    body = "■"
    food = "◆"

    height, width = screen.getmaxyx()
    logging.debug('Canvas dimensions: %s,%s', height, width)

    # Set random initial position (y, x)
    position = (randint(1, height - 1), randint(1, width - 1))

    logging.debug('Initial Position: %s', position)

    # Start input thread to catch all keypresses
    controls = SnakeControls(screen, position)
    controls.daemon = True
    controls.start()

    while True:
        screen.clear()

        y, x = controls.get_position()
        screen.addch(y, x, body)

        screen.refresh()
        time.sleep(0.1)

def main():
    curses.wrapper(start_game)

if __name__ == "__main__":
    main()
