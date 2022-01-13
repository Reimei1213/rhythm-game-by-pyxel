import pyxel
import random


class Ball:
    def __init__(self):
        self.speed = 2
        self.list = [25, 50, 75, 100, 125, 150]
        self.x = 200
        self.num = random.choice(self.list)
        self.idx = self.list.index(self.num)
        self.y = self.num

    def move(self):
        self.x -= self.speed

    def show(self):
        pyxel.circ(self.ball.x, self.ball.y, 10, 6)
