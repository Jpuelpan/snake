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

class Snake(Thread):
    def __init__(self, screen, length=10):
        self.screen = screen
        self.direction = 'UP'

        # Get screen dimensions
        height, width = screen.getmaxyx()
        logging.debug('Canvas dimensions: %s,%s', height, width)

        # Set snake head position to the middle of the screen
        self.y = height // 2
        self.x = width // 2

        self.body = []
        self.body.append((self.y, self.x))

        for i in range(1, length):
            self.body.append((self.y + i, self.x))

        logging.debug('Initial Position: %s', self.body[0])

        Thread.__init__(self)

    def run(self):
        self.key = None

        while True:
            self.key = self.screen.getch()

            if self.key == curses.KEY_UP:
                self.direction = 'UP'
            elif self.key == curses.KEY_LEFT:
                self.direction = 'LEFT'
            elif self.key == curses.KEY_DOWN:
                self.direction = 'DOWN'
            elif self.key == curses.KEY_RIGHT:
                self.direction = 'RIGHT'

            logging.debug('Direction changed to: %s', self.direction)

    def move(self):
        head, *tail = self.body
        previous = head

        if self.direction == 'UP':
            head = (head[0] - 1, head[1])
        elif self.direction == 'LEFT':
            head = (head[0], head[1] - 1)
        elif self.direction == 'RIGHT':
            head = (head[0], head[1] + 1)
        elif self.direction == 'DOWN':
            head = (head[0] + 1, head[1])

        self.body = [head]

        for point in tail:
            self.body.append(previous)
            previous = point

        logging.debug('Snake: %s', self.body)

    def get_snake(self):
        return self.body


def start_game(screen):
    curses.curs_set(0)
    screen.clear()
    screen.refresh()

    # body = "■"
    body = "X"
    food = "◆"

    # Start input thread to catch all keypresses
    controls = Snake(screen, length=10)
    controls.daemon = True
    controls.start()

    logging.debug('Snake body: %s', controls.get_snake())

    while True:
        screen.clear()

        snake = controls.get_snake()

        for point in snake:
            screen.addch(point[0], point[1], body)

        screen.refresh()
        controls.move()

        time.sleep(0.1)

def main():
    curses.wrapper(start_game)

if __name__ == "__main__":
    main()
