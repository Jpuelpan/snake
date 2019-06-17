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
        self.direction = 'UP'

        self.y = position[0]
        self.x = position[1]

        self.body = [self.position]

        self.body.append((self.y + 1, self.x))
        self.body.append((self.y + 2, self.x))
        self.body.append((self.y + 3, self.x))

        Thread.__init__(self)

    def run(self):
        self.key = None

        while True:
            self.key = self.screen.getch()
            # logging.debug('Pressed key: %s', self.key)

            if self.key == curses.KEY_UP:
                self.direction = 'UP'
            elif self.key == curses.KEY_LEFT:
                self.direction = 'LEFT'
            elif self.key == curses.KEY_DOWN:
                self.direction = 'DOWN'
            elif self.key == curses.KEY_RIGHT:
                self.direction = 'RIGHT'

            logging.debug('Direction changed to: %s', self.direction)

    def get_position(self):
        return (self.y, self.x)

    def get_snake(self):
        return self.body

    def move(self):
        if self.direction == 'UP':
            self.body = list(map(lambda x: (x[0] - 1, x[1]), self.body))
        elif self.direction == 'LEFT':
            self.body = list(map(lambda x: (x[0], x[1] - 1), self.body))

def start_game(screen):
    curses.curs_set(0)
    screen.clear()
    screen.refresh()

    # Body
    # body = "■"
    body = "X"
    food = "◆"

    height, width = screen.getmaxyx()
    logging.debug('Canvas dimensions: %s,%s', height, width)

    # Set random initial position (y, x)
    # position = (randint(1, height - 1), randint(1, width - 1))
    position = (height // 2, width // 2)

    logging.debug('Initial Position: %s', position)

    # Start input thread to catch all keypresses
    controls = SnakeControls(screen, position)
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

        time.sleep(0.6)

def main():
    curses.wrapper(start_game)

if __name__ == "__main__":
    main()
