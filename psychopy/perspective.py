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


# カメラ位置の設定
viewPoint = (0, 0, 0)  # (x, y, z) = (横，縦，奥行き)
plane_dist = 1  # カメラから投射面までの距離


# 色空間の設定
COLOR_SPACE = 'rgb1'
black = [0, 0, 0]
white = [1, 1, 1]
gray = [0.5, 0.5, 0.5]

# モニタサイズと視距離の定義
MONITOR_SIZE_PIX = [1280, 720]  # モニターサイズ (x, y)[pixel]
MONITOR_WIDTH_CM = 31         # モニターの横幅[cm]
DISTANCE_CM = 57.29             # モニタまでの視距離[cm]
DIVISION_NUM = 3                # 視距離の分割数

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
diam_fp = 0.4       # 固視点の直径[deg]
pos_fp = (0, 0)     # 固視点の位置
color_fp = black    # 固視点の色
fixation_point = visual.Circle(
    win,
    units = 'deg',
    radius = diam_fp/2,
    colorSpace = COLOR_SPACE,
    fillColor = black,
    pos = pos_fp,
)

# ==============================================================
# 奥行きにに応じたドットの生成
# ==============================================================
# ramdom dotのパラメータ定義
N_dots = 150                            # ドットの個数
size_patch = 20                         # ドットが描画される範囲の直径[deg]
size_dots_max = 2                       # 1ドットの最大直径[deg]
color_dots = [white, black]             # ドットの色
pos_field = (0, 0)                      # ドット位置の原点
pos_noise = 2                           # 設定されたポジションにノイズを足す

# patchの原点も(0, 0)になるように、xとyそれぞれの最大/最小値を定義する。
xmin, xmax = (-size_patch/2, size_patch/2)
ymin, ymax = (-size_patch/2, size_patch/2)

pos_dots_x = np.random.uniform(xmin, xmax, N_dots)   # ドットの初期位置(x)
pos_dots_y = np.random.uniform(ymin, ymax, N_dots)   # ドットの初期位置(y)

pos_dots = np.column_stack((pos_dots_x, pos_dots_y))  # Nx2 arrayの生成

pos_adjust_noise = np.random.uniform(-pos_noise,pos_noise, np.shape(pos_dots))         # ドット位置をバラつかせるためのランダム配列を用意
pos_dots += pos_adjust_noise        # ドットの位置をバラつかせる(端にドットが集中してしまうため．)
# pos_dots = pos_dots[np.where( (np.abs(pos_dots[:, 0]) > pos_noise) | (np.abs(pos_dots[:, 1]) > pos_noise) )]    # (x, y) < |pos_noise|のドットを削除

elemSize = np.zeros(len(pos_dots))                          # ドットサイズ格納用
pos_dots_z = 60
a=0;b=0;c=0
for ii in range(len(pos_dots)):
    if (pos_dots[ii, 0] > xmin and pos_dots[ii, 0] < xmax) and (pos_dots[ii, 1] > ymin and pos_dots[ii, 1] < ymax):
        pos_dots_z = 60
        a+=1
    if (pos_dots[ii, 0] > xmin/2 and pos_dots[ii, 0] < xmax/2) and (pos_dots[ii, 1] > ymin/2 and pos_dots[ii, 1] < ymax/2):
        pos_dots_z = 40
        b+=1
    if (pos_dots[ii, 0] > xmin/4 and pos_dots[ii, 0] < xmax/4) and (pos_dots[ii, 1] > ymin/4 and pos_dots[ii, 1] < ymax/4):
        pos_dots_z = 20
        c+=1

    # elemSize[ii] = np.array([pos_dots[ii, 0], pos_dots[ii, 1], pos_dots_z, 1])*np.tan(np.radians(size_dots_max))   # 1ドットのサイズを視距離から計算, 直径 [degree]
    elemSize[ii] = pos_dots_z * np.tan(np.radians(size_dots_max))

print(pos_dots)
print(np.min(np.abs(pos_dots)), np.max(np.abs(pos_dots)))
print(a, b, c)
print(xmax, ymax)

# ドットを描画するクラス
dot_stim = visual.ElementArrayStim(
    win,
    units       = 'deg',            # 単位 (視角) [degree]
    fieldPos    = pos_field,        # パッチの位置
    nElements   = len(pos_dots),    # ドット数 (ドット数は変更できないので、毎回同じドット数が表示される)
    xys         = pos_dots,         # ドット位置
    sizes       = elemSize,         # ドットサイズ
    colors      = color_dots,       # ドットの色
    colorSpace  = COLOR_SPACE,      # カラースペース
    elementTex  = None,             # ドットにかけるエフェクト
    elementMask = 'circle'          # ドットの形
)
dot_stim.draw(win)


# # ==============================================================
# # 一番奥のドットを生成（壁）
# # ==============================================================
# # ramdom dotのパラメータ定義
# density_dots_backWall = 30                       # ドットの密度[個/deg^2]
# N_dots_backWall = 5 * density_dots              # ドットの個数
# size_patch_backWall = depth_max*2                         # ドットが描画される範囲の直径[deg]
# size_dots_max_backWall = 10                      # 1ドットの最大直径[deg]
# color_dots_backWall = [white, black]             # ドットの色
# pos_field_backWall = (0, 0)                      # ドット位置の原点

# # patchの原点も(0, 0)になるように、xとyそれぞれの最大/最小値を定義する。
# xmin, xmax = (-size_patch_backWall/2, size_patch_backWall/2)
# ymin, ymax = (-size_patch_backWall/2, size_patch_backWall/2)

# pos_dots_x_backWall = np.random.uniform(xmin, xmax, N_dots_backWall)   # ドットの初期位置(x)
# pos_dots_y_backWall = np.random.uniform(ymin, ymax, N_dots_backWall)   # ドットの初期位置(y)
# pos_dots_backWall = np.column_stack((pos_dots_x_backWall, pos_dots_y_backWall))  # Nx2 arrayの生成

# elemSize_backWall = depth_max*np.tan(np.radians(size_dots_max))

# # ドットを描画するクラス
# dot_stim_backWall = visual.ElementArrayStim(
#     win,
#     units       = 'deg',            # 単位 (視角) [degree]
#     fieldPos    = pos_field_backWall,        # パッチの位置
#     nElements   = len(pos_dots_backWall),    # ドット数 (ドット数は変更できないので、毎回同じドット数が表示される)
#     xys         = pos_dots_backWall,         # ドット位置
#     sizes       = elemSize_backWall,         # ドットサイズ
#     colors      = color_dots_backWall,       # ドットの色
#     colorSpace  = COLOR_SPACE,      # カラースペース
#     elementTex  = None,             # ドットにかけるエフェクト
#     elementMask = 'circle'          # ドットの形
# )
# dot_stim_backWall.draw(win)

win.flip()  # 画面書き換え

keyboard.waitKeys(keyList=["space", "escape"])    # キー入力を受け付ける
core.quit() # 実験終了
