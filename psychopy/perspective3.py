# PsychoPyライブラリのインポート
from psychopy import core, monitors, visual
from psychopy.hardware import keyboard
from psychopy.constants import NOT_STARTED, STARTED, FINISHED
import numpy as np

# 色空間の設定
COLOR_SPACE = 'rgb1'
black = [0, 0, 0]
white = [1, 1, 1]
gray = [0.5, 0.5, 0.5]

# モニタサイズと視距離の定義
MONITOR_SIZE_PIX = [1280, 720]  # モニターサイズ (x, y)[pixel]
MONITOR_WIDTH_CM = 31.0         # モニターの横幅[cm]
DISTANCE_CM = 57.3              # 視距離[cm]]
DIVISION_NUM = 3                # 視距離の分割数
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
density_dots = 30                       # ドットの密度[個/deg^2]
N_dots = 15 * density_dots              # ドットの個数
size_patch = 31                         # ドットが描画される範囲の直径[deg]
size_dots_max = 10                      # 1ドットの最大直径[deg]
color_dots = [white, black]             # ドットの色
pos_field = (0, 0)                      # ドット位置の原点

# patchの原点も(0, 0)になるように、xとyそれぞれの最大/最小値を定義する。
xmin, xmax = (-size_patch/2, size_patch/2)
ymin, ymax = (-size_patch/2, size_patch/2)

pos_dots_xList = []
pos_dots_yList = []
NdotInterval = 0
for ii in range(DIVISION_NUM-1, -1, -1):
    # 遠い時幅は1/2^DIVISION_NUM-1, ドット数は1倍
    divInterval = ii
    NdotInterval += 0.5
    pos_dots_x = np.random.uniform(xmin*1/2**divInterval, xmax*1/2**divInterval, int(N_dots*1/2**NdotInterval))   # ドットの初期位置(x)
    pos_dots_y = np.random.uniform(ymin*1/2**divInterval, ymax*1/2**divInterval, int(N_dots*1/2**NdotInterval))   # ドットの初期位置(y)
    pos_dots_xList.append(pos_dots_x)
    pos_dots_yList.append(pos_dots_y)

pos_dots_xList_flat = [x for row in pos_dots_xList for x in row]        # リストを1次元に変換
pos_dots_yList_flat = [y for row in pos_dots_yList for y in row]        # リストを1次元に変換

pos_dots = np.column_stack((pos_dots_xList_flat, pos_dots_yList_flat))  # Nx2 arrayの生成

pos_adjust_noise = np.random.uniform(-depth_max, depth_max, np.shape(pos_dots))         # ドット位置をバラつかせるためのランダム配列を用意
pos_dots += pos_adjust_noise                                            # ドットの位置をバラつかせる(端にドットが集中してしまうため．)
pos_dots = pos_dots[np.where( (np.abs(pos_dots[:, 0]) > depth_max) | (np.abs(pos_dots[:, 1]) > depth_max) )]    # (x, y) < |2|のドットを削除

print(len(pos_dots))

elemSize = np.zeros(len(pos_dots))                          # ドットサイズ格納用
for ii in range(len(pos_dots)):
    dist = np.sqrt(np.sum(pos_dots[ii]**2))                 # 消失点からのユークリッド距離
    elemSize[ii] = dist*np.tan(np.radians(size_dots_max))   # 1ドットのサイズを視距離から計算, 直径 [degree]
    # print(dist)

# ドットを描画するクラス
dot_stim = visual.ElementArrayStim(
    win,
    units       = 'deg',            # 単位 (視角) [degree]
    fieldPos    = pos_field,        # パッチの位置
    nElements   = len(pos_dots),           # ドット数 (ドット数は変更できないので、毎回同じドット数が表示される)
    xys         = pos_dots,         # ドット位置
    sizes       = elemSize,         # ドットサイズ
    colors      = color_dots,       # ドットの色
    colorSpace  = COLOR_SPACE,      # カラースペース
    elementTex  = None,             # ドットにかけるエフェクト
    elementMask = 'circle'          # ドットの形
)
dot_stim.draw(win)


# ==============================================================
# 一番奥のドットを生成（壁）
# ==============================================================
# ramdom dotのパラメータ定義
density_dots_backWall = 30                       # ドットの密度[個/deg^2]
N_dots_backWall = 5 * density_dots              # ドットの個数
size_patch_backWall = depth_max*2                         # ドットが描画される範囲の直径[deg]
size_dots_max_backWall = 10                      # 1ドットの最大直径[deg]
color_dots_backWall = [white, black]             # ドットの色
pos_field_backWall = (0, 0)                      # ドット位置の原点

# patchの原点も(0, 0)になるように、xとyそれぞれの最大/最小値を定義する。
xmin, xmax = (-size_patch_backWall/2, size_patch_backWall/2)
ymin, ymax = (-size_patch_backWall/2, size_patch_backWall/2)

pos_dots_x_backWall = np.random.uniform(xmin, xmax, N_dots_backWall)   # ドットの初期位置(x)
pos_dots_y_backWall = np.random.uniform(ymin, ymax, N_dots_backWall)   # ドットの初期位置(y)
pos_dots_backWall = np.column_stack((pos_dots_x_backWall, pos_dots_y_backWall))  # Nx2 arrayの生成

elemSize_backWall = depth_max*np.tan(np.radians(size_dots_max))

# ドットを描画するクラス
dot_stim_backWall = visual.ElementArrayStim(
    win,
    units       = 'deg',            # 単位 (視角) [degree]
    fieldPos    = pos_field_backWall,        # パッチの位置
    nElements   = len(pos_dots_backWall),    # ドット数 (ドット数は変更できないので、毎回同じドット数が表示される)
    xys         = pos_dots_backWall,         # ドット位置
    sizes       = elemSize_backWall,         # ドットサイズ
    colors      = color_dots_backWall,       # ドットの色
    colorSpace  = COLOR_SPACE,      # カラースペース
    elementTex  = None,             # ドットにかけるエフェクト
    elementMask = 'circle'          # ドットの形
)
dot_stim_backWall.draw(win)

stimuli1 = visual.GratingStim(
    win,
    units       = 'deg',
    tex         = 'sin',
    sf          = 2,
    ori         = 0,
    phase       = 0,
    pos         = (-3, -5),
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
    pos         = (-0.7, -1),
    size        = 1.5,
    mask        = 'circle'
)
stimuli2.draw(win)

win.flip()  # 画面書き換え

keyboard.waitKeys(keyList=["space", "escape"])    # キー入力を受け付ける
core.quit() # 実験終了
