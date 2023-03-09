# PsychoPyライブラリのインポート
from psychopy import core, monitors, visual
from psychopy.hardware import keyboard
from psychopy.constants import NOT_STARTED, STARTED, FINISHED
import numpy as np

'''
[透視投影変換]

視錐台について
    > 視錐台 : カメラに映る範囲 (x, y, z)
        -1 <= x <= 1 
        -1 <= y <= 1 
        -1 <= z <= 1

    > fov(field of view)の水平角度 fovx
    > fovy fovxとの垂直角度
    > near カメラから最前面までの距離
    > far 画面の縦横比であるアスペクト比(縦を1)
        0 <= fovx <= pi
        0 <= fovy <= pi

x座標変換
theta = 水平視野角の半分 = fovx/2 と定めると，
zにおけるxの最大値xmaxは
    tan(theta) = |xmax|/|z|
    xの範囲は-1 < x <= 1なので
    -1 <= x / (|z|tan(theta)) <= 1
各xに1/|z|tan(theta)をかける


y座標変換
垂直視野角fovyとアスペクト比は
phi = fovy/2
zにおけるyの最大値ymaxは
    |z|tan(phi) = |z|tan(theta) / aspect
各yに1/|z|tan(phi) = aspect/|z|tan(theta)をかける

透視投影変換行列
[[1/tan(theta)          0.0,                    0.0,                0.0]
 [  0.0         1/tan(theta) * aspect,          0.0,                0.0]
 [  0.0,                0.0,            (far+near)/(far-near),      -1.0]
 [  0.0,                0.0,            2*far*near/(far-near),      0.0]]
'''

# 色空間の設定
COLOR_SPACE = 'rgb1'
black = [0, 0, 0]
white = [1, 1, 1]
gray = [0.5, 0.5, 0.5]

# モニタサイズと視距離の定義
MONITOR_SIZE_PIX = [1280, 720]  # モニターサイズ (x, y)[pixel]
MONITOR_WIDTH_CM = 31.0         # モニターの横幅[cm]
DISTANCE_CM = 57.3              # 視距離[cm]]
depth_max = 2

# モニタの設定
moni = monitors.Monitor("")
moni.newCalib(                      # モニタの設定を新規作成
    calibName = "test",             # キャリブレーションの名前
    width = MONITOR_WIDTH_CM,       # モニターの横幅[cm]
    distance = DISTANCE_CM          # 視距離[cm]
)
moni.setSizePix(MONITOR_SIZE_PIX)   # モニターサイズ[pixel]

# 画面管理クラス
win = visual.Window(
    size = MONITOR_SIZE_PIX,    # モニターサイズ (x, y)[pixel]
    colorSpace = COLOR_SPACE,   # カラースペース
    color = gray,               # 背景色
    fullscr = True,             # フルスクリーン化
    monitor = moni,             # モニタ情報を設定 (設定すると、刺激のサイズが正しく描画される)
    screen = 0,                 # スクリーンを選択 (モニタが複数ある場合、刺激呈示する画面を選べる)
    allowStencil = True         # Aperture刺激の呈示に必要 (openGLの使用を許可するらしい)
)

# キーボード入力クラス
keyboard = keyboard.Keyboard()

# 固視点のパラメータ定義
pos_fp = (0, 0)     # 固視点の位置
color_fp = black    # 固視点の色
fixation_point = visual.Circle(
    win,
    units = 'deg',
    radius = 0.1,
    colorSpace = COLOR_SPACE,
    fillColor = white,
    pos = pos_fp,
)
fixation_point.draw(win)

line = visual.Line(
    win,
    lineColor   = white,
    lineWidth   = 8,
)

startPos = np.array(
    [[0.1, 0.3],
     [0.1, -0.3],
     [-0.1, 0.3],
     [-0.1, -0.3],
     [0.1, 0.3],
     [0.1, 0.3],
     [-0.1, -0.3],
     [-0.1, -0.3]]
)

endPos = np.array(
    [[0.8, 1],
     [0.8, -1],
     [-0.8, 1],
     [-0.8, -1],
     [-0.1, 0.3],
     [0.1, -0.3],
     [-0.1, 0.3],
     [0.1, -0.3]]
)
for ii in range(len(startPos)):
    line.setStart(startPos[ii])
    line.setEnd(endPos[ii])

    line.draw(win)

stimuli1 = visual.GratingStim(
    win,
    units       = 'deg',
    tex         = 'sin',
    sf          = 2,
    ori         = 0,
    phase       = 0,
    pos         = (-3, -4),
    size        = 3,
    mask        = 'circle'
)
stimuli1.draw(win)

stimuli2 = visual.GratingStim(
    win,
    units       = 'deg',
    tex         = 'sin',
    sf          = 4,
    ori         = 0,
    phase       = 0,
    pos         = (-0.7, -1.5),
    size        = 1.5,
    mask        = 'circle'
)
stimuli2.draw(win)

win.flip()  # 画面書き換え

keyboard.waitKeys(keyList=["space", "escape"])    # キー入力を受け付ける
core.quit() # 実験終了
