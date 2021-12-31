import pyxel
import random
import math


class App:  # [複数個のクラス定義を使用(1 個目)/ゲームの動作]
    # score = 0
    def __init__(self):
        pyxel.init(200, 200, scale=2)  # 200×200 の枠を作成
        pyxel.mouse(True)  # マウスキーを画面に表示
        self.ball = Ball()  # クラス Ball から ball 呼び出し
        self.balls = []  # [リストを使用/ball をさらにリストに入れる]
        self.gen = Gen()  # クラス Gen から呼び出し
        self.pad = Pad()  # クラス Pad から呼び出し
        self.clear = False  # 自作関数
        self.gameover = False  # 自作関数
        self.fullcombo = True  # 自作関数
        self.cnt = 0  # カウントの基本設定
        self.score = 0  # カウントの基本設定
        self.miss = 0  # カウントの基本設定
        self.button_y = [12.5, 37.5, 62.5, 87.5, 112.5, 137.5]  # [リストを使用/
        self.rhythm = [106, 130, 155, 170, 182, 207, 230, 254, 279,
                       305, 329, 343, 356, 368, 396, 419, 443, 467, 479, 504, 530, 554, 578, 604,
                       628, 652, 677, 702, 727, 741, 754, 768, 802, 828, 852, 865, 902, 927, 952,
                       964, 1002, 1026, 1051, 1064, 1100, 1126, 1151,
                       1163]  # [リストを使用/右からボール(音符)が出てくるタイミング:最初のプログラミングで曲のリズムをカウントし、そのタイミングでボールが出てくる。]
        pyxel.sound(0).set(
            "e2e2c2g1 g1g1c2e2 d2d2d2g2 g2g2rr" "c2c2a1e1 e1e1a1c2 b1b1b1e2 e2e2rr", "s", "6", "vffn fnff vffs vfnn",
            25,
        )
        pyxel.sound(1).set(
            "r a1b1c2 b1b1c2d2 g2g2g2g2 c2c2d2e2" "f2f2f2e2 f2e2d2c2 d2d2d2d2 g2g2rr", "s", "6",
            "nnff vfff vvvv vfff svff vfff vvvv svnn", 25,
        )
        pyxel.sound(2).set(
            "c1g1c1g1 c1g1c1g1 b0g1b0g1 b0g1b0g1" "a0e1a0e1 a0e1a0e1 g0d1g0d1 g0d1g0d1", "t", "7", "n", 25,
        )
        pyxel.sound(3).set(
            "f0c1f0c1 g0d1g0d1 c1g1c1g1 a0e1a0e1" "f0c1f0c1 f0c1f0c1 g0d1g0d1 g0d1g0d1", "t", "7", "n", 25,
        )
        pyxel.sound(4).set(
            "f0ra4r f0ra4r f0ra4r f0f0a4r", "n", "6622 6622 6622 6422", "f", 25
        )
        self.play_music(True, True, True)
        # self.play_music(True, False, False)
        for i in range(len(self.rhythm)):
            self.rhythm[i] -= 86
        pyxel.run(self.update, self.draw)

    # 曲のアセット
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
        # init で設定した曲のアセットをチャンネルにいれ、曲を流す

    def update(self):  # プログラミングを更新する
        if self.miss >= 10:
            self.gameover = True  # ミスが 10 回超えたら Game Over となる

        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            mouse_x = pyxel.mouse_x
            mouse_y = pyxel.mouse_y
            buttonY = -1

            # カーソルのマウスが押す場所
            for button_y in self.button_y:
                if button_y < mouse_y and mouse_y < button_y + self.pad.w:
                    buttonY = self.button_y.index(button_y)  # [for 文を使用/Pad の判定を buttonY として定義]
            for ball in self.balls:
                if (self.pad.x <= ball.x) and (ball.x <= self.pad.x + self.pad.w) and buttonY == ball.idx:
                    ball.x = 200
                    ball.y = random.choice(self.ball.l)#[乱数を使用/ランダムに音符が右から出てくるようにする。]
                    self.balls.remove(ball)  # [for 文と if 文を使用/ball が Pad のところにきたときにマウスをタップした場合、ball が消える]
                    self.score += 10  # ボールが消えたら+10 点

                if ball.x < 0:
                    self.balls.remove(ball)
                    self.miss += 1
                    self.fullcombo = False
                # ボールをパッドが受け取られず、通り過ぎ、画面左端までいったら消 える。ミスが増えていく。ミスをすると fullcombo 関数が False になる、

        for ball in self.balls:
            ball.move()
            # [for 文を使用/ボールを無限に発生させる]
        if self.cnt in self.rhythm:
            self.balls.append(Ball())  # ball がでてる間でも ball を出す
        self.cnt += 1
        if self.cnt == 389 * 3:
            pyxel.stop(0)  # 曲がだいたい 3 回しで止まる
            if not self.gameover:
                self.clear = True  # 曲を完走させられたら True となる

    def draw(self):
        pyxel.cls(7)
        # 画面のカラー
        if self.fullcombo and self.clear:
            pyxel.text(10, 100, 'Full Combo!', 8)  # フルコンボでクリアした場合、画面に “Full Combo”と表示
        elif self.clear:
            pyxel.text(10, 100, 'Game Clear!', 8)  # ミスはしたが曲を完走した場合、画面に”Game Clear”と表示

        elif self.gameover:
            pyxel.text(10, 100, 'Game over!', 1)
        else:
            pyxel.rect(15, 12.5, self.pad.w, 25, 8)
            pyxel.rect(15, 37.5, self.pad.w, 25, 9)
            pyxel.rect(15, 62.5, self.pad.w, 25, 10)
            pyxel.rect(15, 87.5, self.pad.w, 25, 11)
            pyxel.rect(15, 112.5, self.pad.w, 25, 12)
            pyxel.rect(15, 137.5, self.pad.w, 25, 13)
            self.gen.show()
            self.pad.show()  # パッドと弦を画面に表示する
            pyxel.text(30, 180, "Score: " + str(self.score), 0)  # 画面左下にスコアを表示

            for ball in self.balls:
                pyxel.circ(ball.x, ball.y, 8, 6)
                pyxel.rect(ball.x + 8, ball.y - 20, 3, 20, 6)
            # [for 文を使用/ボールを次から次へと作成]


class Gen:  # [複数個のクラス定義を使用(2 個目)/音符が流れてくる 6 本の線]
    def __init__(self):
        self.show()

    def show(self):
        pyxel.line(0, 25, 200, 25, 0)
        pyxel.line(0, 50, 200, 50, 0)
        pyxel.line(0, 75, 200, 75, 0)
        pyxel.line(0, 100, 200, 100, 0)
        pyxel.line(0, 125, 200, 125, 0)
        pyxel.line(0, 150, 200, 150, 0)
        # 線6本を表示


class Ball:  # [複数個のクラス定義を使用(3個目)/音符の動き]
    def __init__(self):
        self.speed = 2
        self.l = [25, 50, 75, 100, 125, 150]  # [リストを使用/ランダムで呼び出す]
        self.x = 200  # 右端からボールを出す
        self.num = random.choice(self.l)  # [乱数を使用/ 6つの線(弦)の位置から出る場所をランダムにする]
        self.idx = self.l.index(self.num)
        self.y = self.num

    def move(self):
        self.x -= self.speed

    def show(self):
        pyxel.circ(self.ball.x, self.ball.y, 10, 6)


class Pad:  # [複数個のクラス定義を使用(4個目)/音符の受け取る部分]
    def __init__(self):
        self.x = 15
        self.y = 12.5
        self.w = 30
        self.h = 150

    def show(self):
        pyxel.rectb(15, 12.5, self.w, 150, 0)
    # パッドを描く


App()  # 実行
