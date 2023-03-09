# PsychoPyライブラリのインポート
from psychopy import core, monitors, visual
from psychopy.hardware import keyboard
from psychopy.constants import NOT_STARTED, STARTED, FINISHED
import numpy as np

# カメラ位置の設定
viewPoint = (0, 0, 0)  # (x, y, z) = (横，縦，奥行き)
plane_dist = 1  # カメラから投射面までの距離

# 色空間の設定
COLOR_SPACE = 'rgb1'
black = [0, 0, 0]
white = [1, 1, 1]
gray = [0.5, 0.5, 0.5]
# red = [0.3, 0.3, 0.3]
# blue = [0.8, 0.8, 0.8]
# green = [0.4, 0.4, 0.4]
red = [1, 0, 0]
green = [0, 1 ,0]
blue = [0, 0, 1]


# モニタサイズと視距離の定義
MONITOR_SIZE_PIX = [1440, 900]  # モニターサイズ (x, y)[pixel]
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
N_dots = 180                            # ドットの個数
size_patch = 30                         # ドットが描画される範囲の直径[deg]
size_dots_max = 2                       # 1ドットの最大直径[deg]
color_dots = [white, black]             # ドットの色
pos_field = (0, 0)                      # ドット位置の原点
pos_noise = 2                           # 設定されたポジションにノイズを足す

# patchの原点も(0, 0)になるように、xとyそれぞれの最大/最小値を定義する。
xmin, xmax = (-size_patch/2, size_patch/2)
ymin, ymax = (-size_patch/2, size_patch/2)

# pos_dots_x = np.random.uniform(xmin, xmax, N_dots)   # ドットの初期位置(x)
# pos_dots_y = np.random.uniform(ymin, ymax, N_dots)   # ドットの初期位置(y)
# pos_dots = np.column_stack((pos_dots_x, pos_dots_y))  # Nx2 arrayの生成

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

pos_adjust_noise = np.random.uniform(-pos_noise,pos_noise, np.shape(pos_dots))         # ドット位置をバラつかせるためのランダム配列を用意
pos_dots += pos_adjust_noise        # ドットの位置をバラつかせる(端にドットが集中してしまうため．)

elemSize = np.zeros(len(pos_dots))                          # ドットサイズ格納用
shdw_pos = np.zeros(np.shape(pos_dots))
pos_dots_z = 60
a=0;b=0;c=0
for ii in range(len(pos_dots)):
    if (pos_dots[ii, 0] > xmin and pos_dots[ii, 0] < xmax) and (pos_dots[ii, 1] > ymin and pos_dots[ii, 1] < ymax):
        pos_dots_z = 40
        shdw_pos[ii] = [0.4, -0.4]
        
    if (pos_dots[ii, 0] > xmin/2 and pos_dots[ii, 0] < xmax/2) and (pos_dots[ii, 1] > ymin/2 and pos_dots[ii, 1] < ymax/2):
        pos_dots_z = 30
        shdw_pos[ii] = [0.3, -0.3]
        
    if (pos_dots[ii, 0] > xmin/4 and pos_dots[ii, 0] < xmax/4) and (pos_dots[ii, 1] > ymin/4 and pos_dots[ii, 1] < ymax/4):
        pos_dots_z = 20
        shdw_pos[ii] = [0.2, -0.2]

    if (pos_dots[ii, 0] > xmin/8 and pos_dots[ii, 0] < xmax/8) and (pos_dots[ii, 1] > ymin/8 and pos_dots[ii, 1] < ymax/8):
        pos_dots_z = 10
        shdw_pos[ii] = [0.1, -0.1]

    elemSize[ii] = pos_dots_z * np.tan(np.radians(size_dots_max))

# # ドットを描画するクラス
# dot_stim_shdw = visual.ElementArrayStim(
#     win,
#     units       = 'deg',            # 単位 (視角) [degree]
#     fieldPos    = pos_field,        # パッチの位置
#     nElements   = len(pos_dots),    # ドット数 (ドット数は変更できないので、毎回同じドット数が表示される)
#     xys         = pos_dots + shdw_pos,         # ドット位置
#     sizes       = elemSize,         # ドットサイズ
#     colors      = black,       # ドットの色
#     colorSpace  = COLOR_SPACE,      # カラースペース
#     elementTex  = None,             # ドットにかけるエフェクト
#     elementMask = 'circle'          # ドットの形
# )
# dot_stim_shdw.draw(win)

# ドットを描画するクラス
dot_stim_obj = visual.ElementArrayStim(
    win,
    units       = 'deg',            # 単位 (視角) [degree]
    fieldPos    = pos_field,        # パッチの位置
    nElements   = len(pos_dots),    # ドット数 (ドット数は変更できないので、毎回同じドット数が表示される)
    xys         = pos_dots,         # ドット位置
    sizes       = elemSize,         # ドットサイズ
    colors      = [red, green, white, blue],       # ドットの色
    colorSpace  = COLOR_SPACE,      # カラースペース
    elementTex  = None,             # ドットにかけるエフェクト
    elementMask = 'circle'          # ドットの形
)
dot_stim_obj.draw(win)

# stimuli1 = visual.Circle(
#     win,
#     units       = 'deg',
#     pos         = (-3, -5),
#     radius      = 1.5,
#     fillColor   = [1.0, 0, 0]
# )
# stimuli1.draw(win)

# stimuli2 = visual.Circle(
#     win,
#     units       = 'deg',
#     pos         = (-0.7, -1),
#     radius      = 0.7,
#     fillColor   = [1.0, 0, 0]
# )
# stimuli2.draw(win)

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
