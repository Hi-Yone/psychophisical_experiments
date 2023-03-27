from psychopy import core, monitors, visual
from psychopy.hardware import keyboard
from psychopy.constants import NOT_STARTED, STARTED, FINISHED
import numpy as np

# 色空間の設定
COLOR_SPACE = 'rgb1'
black = [0, 0, 0]
white = [1, 1, 1]
gray = [0.5, 0.5, 0.5]
red = [1, 0, 0]
blue = [0, 0, 1]
green = [0, 1, 0]

# モニタサイズと視距離の定義
# MONITOR_SIZE_PIX = [1440, 900]  # モニタサイズ(x, y) [pixel] (Mac)
MONITOR_SIZE_PIX = [1920, 1080] # モニタサイズ(x, y) [pixel] (Windows)
MONITOR_WIDTH_CM  = 31.0        # モニタの横幅
DISTANCE_CM = 57.3              # 視距離 : 目 -> 鏡，鏡 -> モニタまでの合計距離

# モニタの設定
moni = monitors.Monitor("")
moni.newCalib(
    calibName="test",               # キャリブレーションの名前
    width=MONITOR_WIDTH_CM,         # モニタの横幅
    distance=DISTANCE_CM            # 視距離
)
moni.setSizePix(MONITOR_SIZE_PIX)   #モニタサイズ[pixel]

# 画面管理クラス
win = visual.Window(
    size = MONITOR_SIZE_PIX,          # モニタサイズ
    colorSpace = COLOR_SPACE,         # 色空間
    color = gray,                     # 背景色
    fullscr = True,                   # フルスクリーン化
    monitor = moni,                   # モニタ情報を設定
    screen = 0,                       # スクリーンを選択 (モニタが複数ある場合に，どのモニタに表示するか)
    allowStencil = True               # Aperture刺激の呈示に用いる (OpenGL)
)

# キーボード入力クラス
keyboard = keyboard.Keyboard()

# 固視点のパラメータ定義
pos_fp = (0, 0)
color_fp = black
fixation_point = visual.Circle(
    win,
    units = 'deg',
    radius = 0.1,
    colorSpace = COLOR_SPACE,
    fillColor = white,
    pos = pos_fp
)
fixation_point.draw(win)


# ========================================================================
# 刺激のドット配列を定義
# ========================================================================
"""
そもそも両眼視差とは : 左右の目の位相差 -> 位相差を強くしたり弱くすることで奥行きを調整
とりあえcyclopean diskを真ん中だけ生成
中心が相関ありドット : correlated_dots_L, correlated_dots_R = np.random.uniform(-0.7, 0.7, (2, Ndots))
周辺が相関なしドット

"""

corrDots_r = 6        # 相関ありドットの描画半径 [deg]
patchPos = 0            # 相関ありドットパッチの中心位置
Ndots = 4000            # ドットの生成数
patch_centerPos = 7     # パッチの位置 [deg]
disparity = -0.15           # 視差の大きさ [deg]
# disparity = 0.3           # 視差の大きさ [deg]
elemSize = 0.14         # ドットサイズ [deg]

pos_dots_x = np.random.uniform(-corrDots_r, corrDots_r, Ndots)      # ドット生成
pos_dots_y = np.random.uniform(-corrDots_r, corrDots_r, Ndots)      # ドット生成
pos_dots = np.column_stack((pos_dots_x, pos_dots_y))                # Nx2 arrayの生成

select_range = (np.sqrt(np.sum(pos_dots**2, axis=1)) < 3)

corr_dots_Leye = pos_dots[select_range]
corr_dots_Leye[:, 0] -= patch_centerPos - disparity
corr_dots_Reye = pos_dots[select_range]
corr_dots_Reye[:, 0] += patch_centerPos

corrStim_Leye = visual.ElementArrayStim(
    win,
    units       = 'deg',                            # 単位 (視角) [degree]
    fieldPos    = (0, 0),                           # パッチの位置
    nElements   = len(pos_dots[select_range]),      # ドット数 (ドット数は変更できないので、毎回同じドット数が表示される)
    xys         = corr_dots_Leye,                   # ドット位置
    sizes       = elemSize,                         # ドットサイズ
    colors      = [black, white],                   # ドットの色
    colorSpace  = COLOR_SPACE,                      # カラースペース
    elementTex  = None,                             # ドットにかけるエフェクト
    elementMask = 'circle'                          # ドットの形
)
corrStim_Leye.draw(win)

corrStim_Reye = visual.ElementArrayStim(
    win,
    units       = 'deg',                        # 単位 (視角) [degree]
    fieldPos    = (0, 0),                       # パッチの位置
    nElements   = len(pos_dots[select_range]),  # ドット数 (ドット数は変更できないので、毎回同じドット数が表示される)
    xys         = corr_dots_Reye,               # ドット位置
    sizes       = elemSize,                     # ドットサイズ
    colors      = [black, white],               # ドットの色
    colorSpace  = COLOR_SPACE,                  # カラースペース
    elementTex  = None,                         # ドットにかけるエフェクト
    elementMask = 'circle'                      # ドットの形
)
corrStim_Reye.draw(win)


uncorr_dots_Leye = pos_dots[~select_range]
uncorr_dots_Leye[:, 0] -= patch_centerPos
# uncorr_dots_Leye -= np.random.uniform(-0.15, 0.15, (len(uncorr_dots_Leye), 2))
uncorr_dots_Reye = pos_dots[~select_range]
uncorr_dots_Reye[:, 0] += patch_centerPos
# uncorr_dots_Reye += np.random.uniform(-0.15, 0.15, (len(uncorr_dots_Reye), 2))

uncorrStim_Leye = visual.ElementArrayStim(
    win,
    units       = 'deg',                        # 単位 (視角) [degree]
    fieldPos    = (0, 0),                       # パッチの位置
    nElements   = len(pos_dots[~select_range]), # ドット数 (ドット数は変更できないので、毎回同じドット数が表示される)
    xys         = uncorr_dots_Leye,             # ドット位置
    sizes       = elemSize,                     # ドットサイズ
    colors      = [black, white],               # ドットの色
    colorSpace  = COLOR_SPACE,                  # カラースペース
    elementTex  = None,                         # ドットにかけるエフェクト
    elementMask = 'circle'                      # ドットの形
)
uncorrStim_Leye.draw(win)

uncorrStim_Reye = visual.ElementArrayStim(
    win,
    units       = 'deg',                        # 単位 (視角) [degree]
    fieldPos    = (0, 0),                       # パッチの位置
    nElements   = len(pos_dots[~select_range]), # ドット数 (ドット数は変更できないので、毎回同じドット数が表示される)
    xys         = uncorr_dots_Reye,             # ドット位置
    sizes       = elemSize,                     # ドットサイズ
    colors      = [black, white],               # ドットの色
    colorSpace  = COLOR_SPACE,                  # カラースペース
    elementTex  = None,                         # ドットにかけるエフェクト
    elementMask = 'circle'                      # ドットの形
)
uncorrStim_Reye.draw(win)

win.flip()  # 画面書き換え

keyboard.waitKeys(keyList=["space", "escape"])  # キー入力を受け付ける
core.quit() # 実験終了