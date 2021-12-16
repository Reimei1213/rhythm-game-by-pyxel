import pyxel


class App:

    NOTES = [106, 130, 155, 170, 182, 207, 230, 254, 279,
              305, 329, 343, 356, 368, 396, 419, 443, 467, 479, 504, 530, 554, 578, 604,
              628, 652, 677, 702, 727, 741, 754, 768, 802, 828, 852, 865, 902, 927, 952,
              964, 1002, 1026, 1051, 1064, 1100, 1126, 1151,
              1163]

    def __init__(self):
        pyxel.init(200, 150, caption="RHYTHM RPG")
        self.timing = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(7)
        pyxel.rect(0, 110,200, 20, 2)
        pyxel.circ(30, 120, 15, 3)

App()
