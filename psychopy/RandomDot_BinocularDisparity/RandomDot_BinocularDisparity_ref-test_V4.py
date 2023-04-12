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
    screen = 1,                       # スクリーンを選択 (モニタが複数ある場合に，どのモニタに表示するか)
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

Ndots = 4000            # ドットの生成数
# 刺激描画クラス
elemSize = 0.14         # ドットサイズ [deg]
Stim_Leye = visual.ElementArrayStim(
    win,
    nElements = Ndots,
    units       = 'deg',                            # 単位 (視角) [degree]
    fieldPos    = (0, 0),                           # パッチの位置
    sizes       = elemSize,                         # ドットサイズ
    colors      = [black, white],                   # ドットの色
    colorSpace  = COLOR_SPACE,                      # カラースペース
    elementTex  = None,                             # ドットにかけるエフェクト
    elementMask = 'circle'                          # ドットの形
)

Stim_Reye = visual.ElementArrayStim(
    win,
    nElements = Ndots,
    units       = 'deg',                        # 単位 (視角) [degree]
    fieldPos    = (0, 0),                       # パッチの位置
    sizes       = elemSize,                     # ドットサイズ
    colors      = [black, white],               # ドットの色
    colorSpace  = COLOR_SPACE,                  # カラースペース
    elementTex  = None,                         # ドットにかけるエフェクト
    elementMask = 'circle'                      # ドットの形
)

# ========================================================================
# 実験条件
# ========================================================================
N_repeat = 5    # 刺激1条件あたりの呈示回数

# ========================================================================
# 刺激のドット配列を定義
# ========================================================================
patch_range = 6         # パッチの描画範囲 [deg]
corr_dots_radius = 1    # 相関ありドットパッチの半径
Ndots = 4000            # ドットの生成数
patch_centerPos = 7     # パッチの位置 [deg]

disparity_ref = 0       # 視差の大きさ [deg]
disparity_test = 0.3    # 視差の大きさ [deg]
disparity_arr = np.linspace(-0.3, 0.3, 13)  # 刺激の視差リスト
RefTest_adjPosArr = [np.array([-1, 1]), np.array([1, -1])]  # 参照刺激とtest刺激が左右のどちらに出るかのリスト

pos_dots_x = np.random.uniform(-patch_range, patch_range, Ndots)      # ドット生成
pos_dots_y = np.random.uniform(-patch_range, patch_range, Ndots)      # ドット生成
pos_dots = np.column_stack((pos_dots_x, pos_dots_y))                # Nx2 arrayの生成

# ===============================================================================================
# ドット生成
# ===============================================================================================
RefTest_adjPos = np.array([2, 0])   # 参照刺激とテスト刺激の位置調整用
select_range_Ref = np.sqrt(np.sum((pos_dots + RefTest_adjPos)**2, axis=1)) < corr_dots_radius
select_range_Test = np.sqrt(np.sum((pos_dots - RefTest_adjPos)**2, axis=1)) < corr_dots_radius

# ===============================================================================================
# 参照刺激
# ===============================================================================================
dots_Leye = np.copy(pos_dots)
dots_Leye[select_range_Ref, 0] -= patch_centerPos - disparity_ref       # correlated dots
dots_Leye[select_range_Test, 0] -= patch_centerPos - disparity_test     # correlated dots
jitter_pos = np.random.uniform(-0.3, 0.3, (len(dots_Leye[~(select_range_Ref | select_range_Test)])))
dots_Leye[~(select_range_Ref | select_range_Test), 0] -= patch_centerPos + jitter_pos       # uncorrelated dots

dots_Reye = np.copy(pos_dots)
dots_Reye[select_range_Ref, 0] += patch_centerPos + disparity_ref     # correlated dots
dots_Reye[select_range_Test, 0] += patch_centerPos + disparity_test     # correlated dots
jitter_pos = np.random.uniform(-0.3, 0.3, (len(dots_Reye[~(select_range_Ref | select_range_Test)])))
dots_Reye[~(select_range_Ref | select_range_Test), 0] += patch_centerPos                    # uncorrelated dots 

Stim_Leye.setXYs(dots_Leye)               # ドット位置
Stim_Reye.setXYs(dots_Reye)               # ドット位置

# ===============================================================================================
# 刺激描画
# ===============================================================================================
Stim_Leye.draw(win)
Stim_Reye.draw(win)

win.flip()  # 画面書き換え

keyboard.waitKeys(keyList=["space", "escape"])  # キー入力を受け付ける
core.quit() # 実験終了