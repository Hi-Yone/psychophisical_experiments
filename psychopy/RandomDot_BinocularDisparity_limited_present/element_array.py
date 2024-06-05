from psychopy import core, monitors, visual, data, gui
from psychopy.hardware import keyboard
from psychopy.constants import NOT_STARTED, STARTED, FINISHED
import numpy as np

# 色空間の設定
COLOR_SPACE = 'rgb1'
black = [0, 0, 0]
white = [1, 1, 1]
gray = [0.5, 0.5, 0.5]
red = [1.0, 0, 0]

### Monitor definitions
MONITOR_SIZE_PIX = [1440, 900]  # モニタサイズ(x, y) [pixel] (Mac)
# MONITOR_SIZE_PIX = [1920, 1080] # モニタサイズ(x, y) [pixel] (Windows)
# MONITOR_WIDTH_CM  = 47.5        # モニタの横幅
MONITOR_WIDTH_CM = 53
MONITOR_FRAMERATE = 120         # モニタのフレームレート[Hz]

### Haplo scope definitions
eye_mirror1_dist = 4             # [cm]
mirror1_mirror2_dist = 8.5
mirror2_display_dist = 36

### Visual definitions
DISTANCE_CM = eye_mirror1_dist+mirror1_mirror2_dist+mirror2_display_dist     # 視距離 [cm]
BOD = 6.3                       # 人間の両眼の間隔 [cm] (BOD : binocular distance)
EYEPOS_IN_MONITOR = BOD/2 + mirror1_mirror2_dist - np.arctan(BOD/2/DISTANCE_CM)        # モニタ上での目の位置 [cm]

# モニタの設定
# モニタの設定
moni = monitors.Monitor("")
moni.newCalib(
    calibName="test",               # キャリブレーションの名前
    width=MONITOR_WIDTH_CM,         # モニタの横幅
    distance=DISTANCE_CM            # 視距離
)
moni.setSizePix(MONITOR_SIZE_PIX)       #モニタサイズ[pixel]

# 画面管理クラス
win = visual.Window(
    size = MONITOR_SIZE_PIX,          # モニタサイズ
    colorSpace = COLOR_SPACE,         # 色空間
    color = gray,                     # 背景色
    fullscr = True,                   # フルスクリーン化
    monitor = moni,                   # モニタ情報を設定
    screen = 1,                       # スクリーンを選択 (モニタが複数ある場合に，どのモニタに表示するか)
    allowStencil = True               # Aperture刺激の呈示に用いる (OpenGL)
)

keyboard = keyboard.Keyboard()  # 実験中断用

# 刺激描画クラスはここで定義(NdotsがTestDiskの大きさによって変化するため．)
Stim_corr = visual.ElementArrayStim(
    win,
    nElements = 100,
    units       = 'deg',                            # 単位 (視角) [degree]
    fieldPos    = (0, 0),                         # パッチの位置
    sizes       = 0.1,                         # ドットサイズ
    colors      = [black, white, white, black],                        # ドットの色
    colorSpace  = COLOR_SPACE,                      # カラースペース
    elementTex  = None,                             # ドットにかけるエフェクト
    elementMask = 'circle'                          # ドットの形
)

xys = [np.array([ii, jj]) for ii in range(-5, 5) for jj in range(-5, 5)]

print(np.size(xys), np.shape(xys))
print(xys)

Stim_corr.setXYs(xys)

Stim_corr.draw(win)
win.flip()  # 画面書き換え
keyboard.waitKeys(keyList=["escape"])   # Escキーが押されるまで待機
core.quit() # 実験終了