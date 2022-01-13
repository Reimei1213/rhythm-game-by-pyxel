import pyxel


class Pad:
    def __init__(self):
        self.x = 15
        self.y = 12.5
        self.w = 30
        self.h = 150

    def show(self):
        pyxel.rect(15, 12.5, self.w, 25, 8)
        pyxel.rect(15, 37.5, self.w, 25, 9)
        pyxel.rect(15, 62.5, self.w, 25, 10)
        pyxel.rect(15, 87.5, self.w, 25, 11)
        pyxel.rect(15, 112.5, self.w, 25, 12)
        pyxel.rect(15, 137.5, self.w, 25, 13)

        pyxel.rectb(15, 12.5, self.w, 150, 0)

        pyxel.text(29, 18, "D", 0)
        pyxel.text(29, 43, "F", 0)
        pyxel.text(29, 68, "G", 0)
        pyxel.text(29, 93, "H", 0)
        pyxel.text(29, 118, "J", 0)
        pyxel.text(29, 143, "K", 0)
