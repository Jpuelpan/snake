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
        self.height = height
        self.width = width

        logging.debug('Canvas dimensions: %s,%s', height, width)

        # Set snake head position to the middle of the screen
        self.y = height // 2
        self.x = width // 2

        self.body = []
        self.rats = []

        self.body.append((self.y, self.x))

        for i in range(1, length):
            self.body.append((self.y + i, self.x))

        self.add_rat()

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
        logging.debug('Snake length: %s, Rats: %s', len(self.body), len(self.rats))

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

    def add_rat(self):
        rat = (
            randint(1, self.height - 1),
            randint(1, self.width - 1)
        )

        if rat in self.rats:
            self.add_rat()
        else:
            self.rats.append(rat)

    def eat(self):
        head = self.body[0]
        last = self.body[-1]

        if head in self.rats:
            logging.debug('Yumy!')
            self.rats.remove(head)

            if self.direction == 'UP':
                self.body.append((last[0] - 1, last[1]))
            if self.direction == 'DOWN':
                self.body.append((last[0] + 1, last[1]))
            if self.direction == 'LEFT':
                self.body.append((last[0], last[1] - 1))
            if self.direction == 'RIGHT':
                self.body.append((last[0], last[1] + 1))

            self.add_rat()

    def get_snake(self):
        return self.body

    def get_rats(self):
        return self.rats


def start_game(screen):
    curses.curs_set(0)
    screen.clear()
    screen.refresh()

    # body = "■"
    body = "X"
    food = "🐀"

    # Start input thread to catch all keypresses
    snake = Snake(screen, length=10)
    snake.daemon = True
    snake.start()

    logging.debug('Snake body: %s', snake.get_snake())

    while True:
        screen.clear()

        for point in snake.get_snake():
            screen.addch(point[0], point[1], body)

        for rat in snake.get_rats():
            screen.addch(rat[0], rat[1], food)


        screen.refresh()
        snake.move()
        snake.eat()

        time.sleep(0.1)

def main():
    curses.wrapper(start_game)

if __name__ == "__main__":
    main()
