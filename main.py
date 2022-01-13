import pyxel
import random
import math

from src.ball import Ball
from src.gen import Gen
from src.pad import Pad


class App:
    def __init__(self):
        pyxel.init(200, 200)
        pyxel.mouse(True)
        self.ball = Ball()
        self.balls = []
        self.gen = Gen()
        self.pad = Pad()
        self.clear = False
        self.gameover = False
        self.fullcombo = True
        self.start_game = False
        self.cnt = 0 
        self.score = 0
        self.miss = 0
        self.button_y = [12.5, 37.5, 62.5, 87.5, 112.5, 137.5]
        
        self.start_music = False
        self.easy = True
        self.rhythm = None
        self.easy_rhythm = [
            106, 170, 182, 207, 230, 279,
            305, 343, 356, 396, 419, 443,
            479, 504, 554, 628, 652, 677,
            727, 754, 768, 802, 828, 865,
            902, 952, 964, 1026, 1051, 1064,
            1100, 1163
        ]
        self.hard_rhythm = [
            106, 130, 155, 170, 182, 207, 230, 254, 279,
            305, 329, 343, 356, 368, 396, 419, 443, 467,
            479, 504, 530, 554, 578, 604, 628, 652, 677,
            702, 727, 741, 754, 768, 802, 828, 852, 865,
            902, 927, 952, 964, 1002, 1026, 1051, 1064,
            1100, 1126, 1151, 1163
        ]
        self.key_list = {
            pyxel.KEY_D: 0,
            pyxel.KEY_F: 1,
            pyxel.KEY_G: 2,
            pyxel.KEY_H: 3,
            pyxel.KEY_J: 4,
            pyxel.KEY_K: 5,
        }
        pyxel.sound(0).set(
            "e2e2c2g1 g1g1c2e2 d2d2d2g2 g2g2rr\
                c2c2a1e1 e1e1a1c2 b1b1b1e2 e2e2rr",
            "s", "6", "vffn fnff vffs vfnn", 25
        )
        pyxel.sound(1).set(
            "r a1b1c2 b1b1c2d2 g2g2g2g2 c2c2d2e2\
                f2f2f2e2 f2e2d2c2 d2d2d2d2 g2g2rr",
            "s", "6", "nnff vfff vvvv vfff svff vfff vvvv svnn", 25
        )
        pyxel.sound(2).set(
            "c1g1c1g1 c1g1c1g1 b0g1b0g1 b0g1b0g1\
                a0e1a0e1 a0e1a0e1 g0d1g0d1 g0d1g0d1",
            "t", "7", "n", 25
        )
        pyxel.sound(3).set(
            "f0c1f0c1 g0d1g0d1 c1g1c1g1 a0e1a0e1\
                f0c1f0c1 f0c1f0c1 g0d1g0d1 g0d1g0d1",
            "t", "7", "n", 25,
        )
        pyxel.sound(4).set(
            "f0ra4r f0ra4r f0ra4r f0f0a4r", "n", "6622 6622 6622 6422", "f", 25
        )
        # self.play_music(True, True, True)
        for i in range(len(self.hard_rhythm)):
            self.hard_rhythm[i] -= 86
        for i in range(len(self.easy_rhythm)):
            self.easy_rhythm[i] -= 86
        pyxel.run(self.update, self.draw)

    def play_music(self, ch0, ch1, ch2):
        if ch0:
            pyxel.play(0, [0, 1], loop=True)
        else:
            pyxel.stop(0)
        if ch1:
            pyxel.play(1, [2, 3], loop=True)
        else:
            pyxel.stop(1)
        if ch2:
            pyxel.play(2, 4, loop=True)
        else:
            pyxel.stop(2)

    def update(self):
        if self.start_game:
            if self.start_music:
                self.play_music(True, True, True)
                self.start_music = False

            if self.miss >= 10:
                self.gameover = True

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                mouse_y = pyxel.mouse_y
                buttonY = -1

                for button_y in self.button_y:
                    if button_y <= mouse_y and mouse_y < button_y + self.pad.w:
                        buttonY = self.button_y.index(button_y)
                for ball in self.balls:
                    if (self.pad.x <= ball.x) \
                            and (ball.x <= self.pad.x + self.pad.w) \
                            and buttonY == ball.idx:
                        ball.x = 200
                        ball.y = random.choice(self.ball.list)
                        self.balls.remove(ball)
                        self.score += 10

                    if ball.x < 0:
                        self.balls.remove(ball)
                        self.miss += 1
                        self.fullcombo = False

            if pyxel.btnp(pyxel.KEY_D):
                self.__input_key(self.button_y[self.key_list[pyxel.KEY_D]])
            elif pyxel.btnp(pyxel.KEY_F):
                self.__input_key(self.button_y[self.key_list[pyxel.KEY_F]])
            elif pyxel.btnp(pyxel.KEY_G):
                self.__input_key(self.button_y[self.key_list[pyxel.KEY_G]])
            elif pyxel.btnp(pyxel.KEY_H):
                self.__input_key(self.button_y[self.key_list[pyxel.KEY_H]])
            elif pyxel.btnp(pyxel.KEY_J):
                self.__input_key(self.button_y[self.key_list[pyxel.KEY_J]])
            elif pyxel.btnp(pyxel.KEY_K):
                self.__input_key(self.button_y[self.key_list[pyxel.KEY_K]])

            for ball in self.balls:
                ball.move()
            if self.cnt in self.rhythm:
                self.balls.append(Ball())
            self.cnt += 1
            if self.cnt == 389 * 3:
                pyxel.stop(0)
                if not self.gameover:
                    self.clear = True
        else:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                mouse_y = pyxel.mouse_y
                if pyxel.height / 2 <= mouse_y and mouse_y < pyxel.height:
                    self.easy = False
                self.start_game = True
                self.start_music = True
                self.rhythm = self.easy_rhythm \
                    if self.easy else self.hard_rhythm

    def draw(self):
        pyxel.cls(7)
        if not self.start_game:
            pyxel.rect(0, 0, pyxel.width, pyxel.height / 2, 14)
            pyxel.rect(0, pyxel.height / 2, pyxel.width, pyxel.height / 2, 1)
            pyxel.text(pyxel.width/2-8, pyxel.height/4, "EASY", 7)
            pyxel.text(pyxel.width/2-8, pyxel.height*3/4, "HARD", 7)
        elif self.fullcombo and self.clear:
            pyxel.text(10, 100, 'Full Combo!', 8)
        elif self.clear:
            pyxel.text(10, 100, 'Game Clear!', 8)

        elif self.gameover:
            pyxel.text(10, 100, 'Game over!', 1)
        else:
            self.pad.show()
            self.gen.show()
            pyxel.text(30, 180, "Score: " + str(self.score), 0)

            for ball in self.balls:
                pyxel.circ(ball.x, ball.y, 8, 6)
                pyxel.rect(ball.x + 8, ball.y - 20, 3, 20, 6)

    def __input_key(self, key_y):
        for button_y in self.button_y:
            if button_y == key_y:
                buttonY = self.button_y.index(button_y)
        for ball in self.balls:
            if (self.pad.x <= ball.x) \
                    and (ball.x <= self.pad.x + self.pad.w) \
                    and buttonY == ball.idx:
                ball.x = 200
                ball.y = random.choice(self.ball.list)
                self.balls.remove(ball)
                self.score += 10

            if ball.x < 0:
                self.balls.remove(ball)
                self.miss += 1
                self.fullcombo = False


App()
