from psychopy import core, monitors, visual, data, gui
from psychopy.hardware import keyboard
from psychopy.constants import NOT_STARTED, STARTED, FINISHED
import numpy as np
import os
import datetime

# 刺激作成用クラス
from stim import StimGenerator as stgen
from stim import StimParameters as stprm

# 実験情報の保存
expInfo = {'participant' : ""}

# 被験者の情報入力GUI
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=None)
if dlg.OK == False:                                                             # GUIウインドウがキャンセルされたら実験をしない
    core.quit()

# 色空間の設定
COLOR_SPACE = 'rgb1'
black = [0, 0, 0]
white = [1, 1, 1]
gray = [0.5, 0.5, 0.5]

# モニタの定義
MONITOR_SIZE_PIX = [1440, 900]                                                  # モニタサイズ(x, y) [pixel] (MacOS)
# MONITOR_SIZE_PIX = [1920, 1080]                                                 # モニタサイズ(x, y) [pixel] (Windows)
MONITOR_WIDTH_CM = 53                                                           # モニタの横幅
MONITOR_FRAMERATE = 120                                                         # モニタのフレームレート[Hz]

# ハプロスコープの定義
eye_mirror1_dist = 4                                                            # [cm]
mirror1_mirror2_dist = 8.5                                                      # [cm]
mirror2_display_dist = 36                                                       # [cm]

# 視距離に関する定義
DISTANCE_CM = eye_mirror1_dist+mirror1_mirror2_dist+mirror2_display_dist        # 視距離 [cm]
BOD = 6.3                                                                       # 人間の両眼の間隔 [cm] (BOD : binocular distance)
EYEPOS_IN_MONITOR = BOD/2 + mirror1_mirror2_dist - np.arctan(BOD/2/DISTANCE_CM) # モニタ上での目の位置 [cm]

# モニタの設定
moni = monitors.Monitor("")
moni.newCalib(
    calibName="test",                                                           # キャリブレーションの名前
    width=MONITOR_WIDTH_CM,                                                     # モニタの横幅
    distance=DISTANCE_CM                                                        # 視距離
)
moni.setSizePix(MONITOR_SIZE_PIX)                                               # モニタサイズ[pixel]

# 画面管理クラス
win = visual.Window(
    size = MONITOR_SIZE_PIX,                                                    # モニタサイズ
    colorSpace = COLOR_SPACE,                                                   # 色空間
    color = gray,                                                               # 背景色
    fullscr = True,                                                             # フルスクリーン化
    monitor = moni,                                                             # モニタ情報を設定
    screen = 0,                                                                 # スクリーンを選択 (モニタが複数ある場合に，どのモニタに表示するか)
    allowStencil = True                                                         # Aperture刺激の呈示に用いる (OpenGL)
)

# キーボード入力クラス
keyboard_start = keyboard.Keyboard()                                            # 実験開始用
keyboard_default = keyboard.Keyboard()                                          # 実験中断用
keyboard_resp = keyboard.Keyboard()                                             # 被験者の応答の取得用
clock = core.Clock()                                                            # 時間管理クラス

# 刺激生成クラス
stim_gene = stgen.stim_generator(framerate=MONITOR_FRAMERATE, 
                                    moniSize_pix=MONITOR_SIZE_PIX, 
                                    moniSize_cm=MONITOR_WIDTH_CM, 
                                    eyeOffset_cm=DISTANCE_CM)

centerPos = stim_gene.cm2deg(EYEPOS_IN_MONITOR)                                 # ハプロスコープを使った時、視線がモニタ上のどこに対応するか

# テキスト(教示)を描画するクラス
text_resp_L = visual.TextStim(
    win,
    text = "Press key \n\n <--    ",                                            # 描画する文字
    height = 1,                                                                 # 文字の大きさ
    color = white,                                                              # 文字の色
    units = 'deg',                                                              # 単位
    colorSpace = COLOR_SPACE,                                                   # 色空間
    pos = (-centerPos-2.5, 0)                                                   # 呈示位置
)

text_resp_R = visual.TextStim(
    win,
    text = "to respond \n\n    --> ",                                           # 描画する文字
    height = 1,                                                                 # 文字の大きさ
    color = white,                                                              # 文字の色
    units = 'deg',                                                              # 単位
    colorSpace = COLOR_SPACE,                                                   # 色空間
    pos = (centerPos+2.5, 0)                                                    # 呈示位置
)

text_start_L = visual.TextStim(
    win,
    text = "SPACE ",                                                            # 描画する文字
    height = 1,                                                                 # 文字の大きさ
    color = white,                                                              # 文字の色
    units = 'deg',                                                              # 単位
    colorSpace = COLOR_SPACE,                                                   # 色空間
    pos = (-centerPos-2.5, 3.5)                                                 # 呈示位置
)

text_start_R = visual.TextStim(
    win,
    text = "START",                                                             # 描画する文字
    height = 1,                                                                 # 文字の大きさ
    color = white,                                                              # 文字の色
    units = 'deg',                                                              # 単位
    colorSpace = COLOR_SPACE,                                                   # 色空間
    pos = (centerPos+2.5, 3.5)                                                  # 呈示位置
)

text_continue_L = visual.TextStim(
    win,
    text = " ",                                                                 # 描画する文字
    height = 1,                                                                 # 文字の大きさ
    color = white,                                                              # 文字の色
    units = 'deg',                                                              # 単位
    colorSpace = COLOR_SPACE,                                                   # 色空間
    pos = (-centerPos-2.5,-3.5)                                                 # 呈示位置
)

text_continue_R = visual.TextStim(
    win,
    text = " ",                                                                 # 描画する文字
    height = 1,                                                                 # 文字の大きさ
    color = white,                                                              # 文字の色
    units = 'deg',                                                              # 単位
    colorSpace = COLOR_SPACE,                                                   # 色空間
    pos = (centerPos+2.5,-3.5)                                                  # 呈示位置
)

# 固視点のパラメータ定義
color_fp = white                                                                # 固視点の色
pos_fp = (-centerPos, 0)                                                        # 左目に呈示する固視点の場所
fp_L = visual.ShapeStim(                                                        # 左目に呈示する固視点の設定
    win,
    units='deg',
    vertices=((-0.3,0.1), (-0.3,0), (-0.1, 0), (-0.1,-0.3), (0,-0.3), (0,0.3), (-0.1,0.3), (-0.1,0.1)),
    colorSpace=COLOR_SPACE,
    lineColor=None,
    fillColor=color_fp,
    pos=pos_fp
)
pos_fp = (centerPos, 0)                                                         # 右目に呈示する固視点の場所
fp_R = visual.ShapeStim(                                                        # 右目に呈示する固視点の設定
    win,
    units='deg',
    vertices=((0.3,0.1), (0.3,0), (0.1,0), (0.1,-0.3), (0,-0.3), (0,0.3), (0.1,0.3), (0.1,0.1)),
    colorSpace=COLOR_SPACE,
    lineColor=None,
    fillColor=color_fp,
    pos=pos_fp
)

# =========================================================
# 視覚刺激パラメータ定義
# =========================================================
fieldPos = (0, 0)                                                                                               # 原点
elemColor = [black, white]                                                                                      # ドットの色
elemSize = stprm.elemSize                                                                                       # ドットサイズ [deg]
dotsDensity = stprm.dotsDensity                                                                                 # ドット密度[%]
surrPatch_range = stprm.surrPatch_range                                                                         # 無相関パッチの描画範囲 [deg]
RefDisk_radius = stprm.RefDisk_radius                                                                           # 相関ありパッチの半径 [deg]

disparity_arr = stprm.disparity_arr                                                                             # 刺激の視差リスト
TestDisk_radius_arr = stprm.TestDisk_radius_arr                                                                 # test刺激の半径

patch_centerPos = np.array([centerPos , 0])                                                                     # パッチの位置 [deg]
RefTest_dist = np.array([11 , 0])                                                                               # reference刺激とtest刺激の間の距離[deg]
LorR_arr = ['left', 'right']                                                                                    # 辞書型で管理して実験結果を見やすくする
TestDiskPos_LorR_dict = {'left':np.array([1, -1]), 'right':np.array([-1, 1])}                                   # reference刺激とtest刺激が左右どちらに出るか[ref, test]

RefDisk_Ndots_arr, TestDisk_Ndots_arr, uncorrPatch_Ndots_arr = stim_gene.calc_Ndots(RefDisk_radius,             # ドット数の計算
                                                                        TestDisk_radius_arr, 
                                                                        surrPatch_range, 
                                                                        elemSize, 
                                                                        dotsDensity)
RefDisk_Ndots = RefDisk_Ndots_arr[0]                                                                            # reference diskのドット数
TestDisk_Ndots_dict = dict(zip(TestDisk_radius_arr, TestDisk_Ndots_arr))                                        # test diskのドット数
uncorrPatch_Ndots_dict = dict(zip(TestDisk_radius_arr, uncorrPatch_Ndots_arr))                                  # 無相関領域のドット数

fixation_start = stprm.fixation_start                                                                           # 固視点呈示開始時刻
stim_start = stprm.stim_start                                                                                   # 刺激開始時刻
present_time = stprm.present_time                                                                               # 刺激呈示時間
resp_start = stprm.resp_start                                                                                   # 応答開始時間
flip_interval = stprm.flip_interval                                                                             # フリップ間隔

# =========================================================
# 実験条件
# =========================================================
N_repeat = stprm.N_repeat                                                                                       # 各パラメータの繰り返し回数
frame_tolerance = 0.01                                                                                          # sec, フレームの許容誤差
times = {                                                                                                       # 刺激呈示時間 (開始時間, 終了時間) [sec]
    'fixation': [fixation_start, np.inf],
    'stim': [stim_start, resp_start],
    'resp': [resp_start, np.inf],
    'text_start': [fixation_start, stim_start] 
}

# trial毎に変える条件
conditions = data.createFactorialTrialList({
    'disparity_test' : disparity_arr,
    'TestDisk_radius': TestDisk_radius_arr,
    'TestPos_LorR' : LorR_arr
})

stimOder = stprm.stimOder
trials = data.TrialHandler(
    conditions,                                                                                                 # trial毎に変える条件
    nReps = N_repeat,                                                                                           # １条件を何回繰り返すか
    method = stimOder                                                                                           # ランダマイズの方法                                                                                    # ランダマイズの方法
)
trialComponents_start = [text_start_L, text_start_R, text_continue_L, text_continue_R, keyboard_start]          # トライアル開始のコンポーネント
trialComponents_resp = [text_resp_L, text_resp_R]                                                               # 応答時のコンポーネント
                                                                
Trial_N = len(TestDisk_radius_arr) * len(disparity_arr) * len(LorR_arr) * N_repeat                              # 総試行回数
print("トライアル回数 : ", Trial_N, "回")

# =========================================================
# 実験開始
# =========================================================
trial_cnt = 1
for trial in trials:
    disparity_test = trial['disparity_test']
    TestDisk_radius = trial['TestDisk_radius']
    TestPos_LorR = trial['TestPos_LorR']

    # ドット位置のリストをあらかじめ何パターンか作っておく
    corrDots_arr_left=[]; corrDots_arr_right=[]; uncorrDots_arr=[]
    for __ in range(int(MONITOR_FRAMERATE/present_time/flip_interval)+3):
        # =========================================================
        # 実験刺激の生成
        # =========================================================
        TestDisk_Ndots = TestDisk_Ndots_dict[TestDisk_radius]
        uncorrPatch_Ndots = uncorrPatch_Ndots_dict[TestDisk_radius]

        # 刺激描画クラスはここで定義(NdotsがTestDiskの大きさによって変化するため．)
        Stim_corr_left = visual.ElementArrayStim(
            win,
            nElements = RefDisk_Ndots + TestDisk_Ndots,
            units       = 'deg',                                                                                # 単位 (視角) [degree]
            fieldPos    = fieldPos,                                                                             # パッチの位置
            sizes       = elemSize,                                                                             # ドットサイズ
            colors      = elemColor,                                                                            # ドットの色
            colorSpace  = COLOR_SPACE,                                                                          # カラースペース
            elementTex  = None,                                                                                 # ドットにかけるエフェクト
            elementMask = 'circle'                                                                              # ドットの形
        )
        Stim_corr_right = visual.ElementArrayStim(
            win,
            nElements = RefDisk_Ndots + TestDisk_Ndots,
            units       = 'deg',                                                                                # 単位 (視角) [degree]
            fieldPos    = fieldPos,                                                                             # パッチの位置
            sizes       = elemSize,                                                                             # ドットサイズ
            colors      = elemColor,                                                                            # ドットの色
            colorSpace  = COLOR_SPACE,                                                                          # カラースペース
            elementTex  = None,                                                                                 # ドットにかけるエフェクト
            elementMask = 'circle'                                                                              # ドットの形
        )
        Stim_uncorr = visual.ElementArrayStim(
            win,
            nElements = uncorrPatch_Ndots*2,
            units       = 'deg',                                                                                # 単位 (視角) [degree]
            fieldPos    = fieldPos,                                                                             # パッチの位置
            sizes       = elemSize,                                                                             # ドットサイズ
            colors      = elemColor,                                                                            # ドットの色
            colorSpace  = COLOR_SPACE,                                                                          # カラースペース
            elementTex  = None,                                                                                 # ドットにかけるエフェクト
            elementMask = 'circle'                                                                              # ドットの形
        )

        # trialに使うコンポーネント
        trialComponents_present = [fp_L, fp_R, Stim_corr_left, Stim_corr_right, Stim_uncorr]

        # 相関ありのドット刺激を生成
        corrDots_left, corrDots_right = stim_gene.RefTestDisk(RefDisk_Ndots, TestDisk_Ndots,
                                        RefDisk_radius, TestDisk_radius, 
                                        patch_centerPos, disparity_test, 
                                        RefTest_dist, TestDiskPos_LorR_dict[TestPos_LorR])
        # 無相関のランダムノイズを生成
        uncorrDots = stim_gene.surroundPatch(uncorrPatch_Ndots, surrPatch_range,
                                        RefDisk_radius, TestDisk_radius, 
                                        patch_centerPos, RefTest_dist, TestDiskPos_LorR_dict[TestPos_LorR], disparity_test)
        corrDots_arr_left.append(corrDots_left)
        corrDots_arr_right.append(corrDots_right)
        uncorrDots_arr.append(uncorrDots)   

    print('corrドット数 : ', Stim_corr_left.nElements, 'uncorrドット数 : ',Stim_uncorr.nElements)


    ########################################### スタート画面 ############################################
    # コンポーネントの状態を初期化
    continueRoutine = True                                                                                      # trial中はTrue
    all_key_resp = None                                                                                         # キーボード応答を初期化
    keyboard_default.keys = None                                                                                # キーボード応答を初期化
    keyboard_start.keys = None                                                                                  # キーボード応答を初期化

    # 固視点は常に表示する
    fp_L.draw(win)
    fp_R.draw(win)

    # 各コンポーネントのステータスをリセット
    for thisComponent_start in trialComponents_start:
        if hasattr(thisComponent_start, 'status'):
            thisComponent_start.status = NOT_STARTED                                                            # ステータスのリセット
    
    # タイマーリセット
    time_first_frame = win.getFutureFlipTime(clock="now")                                                       # 次の画面フリップまでにかかる時間
    clock.reset(-time_first_frame)                                                                              # 次に画面フリップしたときに時間が0になるように設定
    i_frame = -1                                                                                                # 刺激呈示中のフレーム番号

    ### トライアル開始 ###
    while continueRoutine:
        i_frame += 1
        t_flip = win.getFutureFlipTime(clock=clock)                                                             # 次にflipが行われる時刻(trial内)
        t_flip_global = win.getFutureFlipTime(clock=None)                                                       # 次にflipが行われる時刻(実験全体)

        # テキストの開始時間を過ぎるとき
        if text_start_L.status == NOT_STARTED and t_flip >= times['text_start'][0] - frame_tolerance:
            text_start_L.setAutoDraw(True)                                                                      # text_start_Lの描画開始
            text_start_R.setAutoDraw(True)                                                                      # text_start_Rの描画開始
    
        if text_continue_L.status == NOT_STARTED and t_flip >= times['text_start'][0] - frame_tolerance:
            text_continue_L.text = "current number\n {left} ".format(left = Trial_N - trial_cnt + 1)            # 描画する文字を設定
            text_continue_R.text = " of trials : {trial} \n trials left".format(trial=trial_cnt)                # 描画する文字を設定
            text_continue_L.setAutoDraw(True)                                                                   # text_continue_Lの描画
            text_continue_R.setAutoDraw(True)                                                                   # text_continue_Rの描画
            fp_L.setAutoDraw(True)                                                                              # fp_Lの描画
            fp_R.setAutoDraw(True)                                                                              # fp_Rの描画

        waitOnFlip = False

        # キーボード入力の開始時間を過ぎるとき
        if keyboard_start.status == NOT_STARTED and t_flip >= times['text_start'][0] - frame_tolerance:
            keyboard_start.status = STARTED                                                                     # keyboard_startのキーを受け付けるようにする
            waitOnFlip = True

            win.callOnFlip(keyboard_start.clock.reset)                                                          # 次のフリップで時間をリセット
            win.callOnFlip(keyboard_start.clearEvents, eventType='keyboard')                                    # 次のフリップでキーボードのイベントをリセット
            
        # キーボード入力が既に始まった
        if keyboard_start.status == STARTED and not waitOnFlip:
            # キーボード入力を取得 (keyList中のキーしか取得できない)
            all_key_resp_start = keyboard_start.getKeys(keyList=['space'], waitRelease=False)

            # もし何かしら入力されたら
            if len(all_key_resp_start):
                keyboard_start.keys = all_key_resp_start[-1].name                                               # 押されたキーの名前を取得
                continueRoutine = False                                                                         # trialの継続をFalseにする
            
        # エスケープが押されたら実験終了
        if keyboard_default.getKeys(keyList=["escape"]):
            core.quit()
                
        if not continueRoutine:
            # 今のtrialを終了
            # whileループを抜ける
            break
        else:
            # trialを継続
            # 画面をフリップさせて次フレームへ
            win.flip()

    # テキストの描画を辞める        
    text_start_L.setAutoDraw(False)
    text_start_R.setAutoDraw(False)
    text_continue_L.setAutoDraw(False)
    text_continue_R.setAutoDraw(False)

    ########################################### 刺激呈示画面 ############################################
    # コンポーネントの状態を初期化
    routine = True                                                                                      # trial中はTrue
    all_key_resp = None                                                                                 # キーボード応答を初期化
    keyboard_default.keys = None                                                                        # キーボード応答を初期化

    # 各コンポーネントのステータスをリセット
    for thisComponent_present in trialComponents_present:
        if hasattr(thisComponent_present, 'status'):
            thisComponent_present.status = NOT_STARTED
    
    # タイマーリセット
    time_first_frame = win.getFutureFlipTime(clock="now")                                               # 次の画面フリップまでにかかる時間
    clock.reset(-time_first_frame)                                                                      # 次に画面フリップしたときに時間が0になるように設定
    i_frame = -1                                                                                        # 刺激呈示中のフレーム番号

    i_pos = 0
    ### トライアル開始 ###
    while routine:
        i_frame += 1
        t_flip = win.getFutureFlipTime(clock=clock)                                                     # 次にflipが行われる時刻(trial内)
        t_flip_global = win.getFutureFlipTime(clock=None)                                               # 次にflipが行われる時刻(実験全体)

        # dynamic random dotの呈示
        if (Stim_corr_left.status==NOT_STARTED) and (t_flip >= times['stim'][0]-frame_tolerance):
            print('========呈示開始=======')
            Stim_corr_left.status = STARTED                                                             # 呈示開始
            Stim_corr_right.status = STARTED                                                            # 呈示開始
            Stim_uncorr.status = STARTED                                                                # 呈示開始 
            Stim_corr_left.frameNStart = i_frame                                                        # 呈示開始時のフレームを保存

            Stim_corr_left.setXYs(corrDots_arr_left[1])                                                 # ドット位置のセット
            Stim_corr_right.setXYs(corrDots_arr_right[1])                                               # ドット位置のセット
            Stim_uncorr.setXYs(uncorrDots_arr[1])                                                       # ドット位置のセット
            Stim_corr_left.draw(win)                                                                    # setAutoDrawがないので、毎回drawする
            Stim_corr_right.draw(win)                                                                   # setAutoDrawがないので、毎回drawする
            Stim_uncorr.draw(win) 

        # リフレッシュする刺激が一周したとき
        if i_pos > len(corrDots_arr_left)-2:
            i_pos = 0                                                                                   # 刺激のインデックスをリセット
        
        # 刺激が呈示されているとき
        if Stim_corr_left.status == STARTED:
            if i_frame%flip_interval==0:                                                                # 4フレームごとに刺激をリフレッシュ
                i_pos += 1                                                                              # 刺激のインデックスをインクリメント
            Stim_corr_left.setXYs(corrDots_arr_left[i_pos])                                             # ドット位置のセット
            Stim_corr_right.setXYs(corrDots_arr_right[i_pos])                                           # ドット位置のセット
            Stim_uncorr.setXYs(uncorrDots_arr[i_pos])                                                   # ドット位置のセット
            Stim_corr_left.draw(win)                                                                    # 刺激を描画
            Stim_corr_right.draw(win)                                                                   # 刺激を描画
            Stim_uncorr.draw(win)                                                                       # 刺激を描画

            # 次のフリップで呈示終了時刻を過ぎるとき
            if t_flip >= times['stim'][1] - frame_tolerance:
                print('========呈示終了=======')
                Stim_corr_left.status = FINISHED                                                        # 呈示終了
                Stim_corr_right.status = FINISHED                                                       # 呈示終了
                Stim_uncorr.status = FINISHED                                                           # 呈示終了
                routine = False
                win.flip()

        # fixation pointの呈示
        if (fp_L.status==NOT_STARTED) and (t_flip >= times['fixation'][0]-frame_tolerance):
            print('========fixation開始=======')
            fp_L.status = STARTED                                                                       # 呈示開始
            fp_R.status = STARTED                                                                       # 呈示開始 
            fp_L.frameNStart = i_frame                                                                  # 呈示開始時のフレームを保存

            fp_L.draw(win)                                                                              # setAutoDrawがないので、毎回drawする
            fp_R.draw(win)                                                                              # setAutoDrawがないので、毎回drawする

        # 刺激が呈示されているとき
        if fp_L.status == STARTED:
            fp_L.draw(win)                                                                              # 固視点を描画
            fp_R.draw(win)                                                                              # 固視点を描画
                
        # エスケープが押されたら実験終了
        if keyboard_default.getKeys(keyList=["escape"]):
            core.quit()
                
        if not routine:
            # trial終了
            break
        else:
            # trial継続
            win.flip()

    trial_cnt+=1

    ############################################ 応答画面 #############################################
    # コンポーネントの状態を初期化
    respRoutine = True                                                                                  # trial中はTrue
    all_key_resp = None                                                                                 # キーボード応答を初期化
    keyboard_default.keys = None                                                                        # キーボード応答を初期化
    keyboard_resp.keys = None                                                                           # キーボード応答を初期化

    # 各コンポーネントのステータスをリセット
    for thisComponent_resp in trialComponents_resp:
        if hasattr(thisComponent_resp, 'status'):
            thisComponent_resp.status = NOT_STARTED                                                     # コンポーネントの状態をリセット
    
    ### トライアル開始 ###
    while respRoutine:
        i_frame += 1
        t_flip = win.getFutureFlipTime(clock=clock)                                                     # 次にflipが行われる時刻(trial内)
        t_flip_global = win.getFutureFlipTime(clock=None)                                               # 次にflipが行われる時刻(実験全体)

        # キーボード入力の受付開始
        waitOnFlip = False                                                                              # 次のフリップを待つ

        # 入力開始していない かつ 次のフリップで開始時刻を過ぎるとき
        if (keyboard_resp.status==NOT_STARTED) and (t_flip >= times['resp'][0]-frame_tolerance):
            print('========応答開始=======')
            keyboard_resp.status = STARTED                                                              # キーボードの状態を開始にする
            waitOnFlip = True

            win.callOnFlip(keyboard_resp.clearEvents, eventType='keyboard')                             # 次のフリップでキーボードのイベントをリセット
            
        # キーボード入力が既に始まった かつ フリップを待った後
        waitOnFlip = False  # 次のフリップを待つ
        if (keyboard_resp.status==STARTED) and (not waitOnFlip):
            # 何も入力されていないときは空のリストが返る
            all_key_resp = keyboard_resp.getKeys(keyList=['right', 'left'], waitRelease=False)          # キーボード入力を取得 (keyList中のキーのみ取得)
            text_resp_L.setAutoDraw(True)                                                               # text_resp_Lの描画
            text_resp_R.setAutoDraw(True)                                                               # text_resp_Rの描画
            
            # もし何かしら入力されたら
            if all_key_resp:
                keyboard_resp.keys = all_key_resp[-1].name                                              # 押されたキーの名前を取得
                print('========応答終了=======###')
                text_resp_L.setAutoDraw(False)                                                          # テキストの描画を辞める
                text_resp_R.setAutoDraw(False)                                                          # テキストの描画を辞める
                keyboard_resp.status = NOT_STARTED                                                      # キーボードの状態をリセットする
                respRoutine = False                                                                     # trialの継続をFalseにする
                win.flip(clearBuffer=True)  # ウィンドウを手動で更新して即座に次のトライアルに移る
            
        # エスケープが押されたら実験終了
        if keyboard_default.getKeys(keyList=["escape"]):
            # win.saveFrameIntervals(fileName="RandomDot_BinocularDisparity_ref-test.log", clear=True)
            core.quit()
                
        if not respRoutine:
            # 今のtrialを終了
            # whileループを抜ける
            break
        else:
            # trialを継続
            # 画面をフリップさせて次フレームへ
            win.flip()

        # キー入力が何もなかったら、Noneにする
        if keyboard_resp.keys in ['', [], None]:
            keyboard_resp.keys = None


    # 入力されたキーをデータに追加
    trials.addData('key', keyboard_resp.keys)
    print("TestPos:", TestPos_LorR, ", resp:", keyboard_resp.keys, ", TestDisk_radius:", TestDisk_radius, ", Disparity:", disparity_test)

# 実験条件とレスポンスのデータを保存
# ファイル名は -> data/被験者名_実験をした時間.csv  とする
if not os.path.isdir('data/'):
    os.mkdir('data/')
now = datetime.datetime.now()                                                                           # 現在の時間を取得
now_str = now.strftime('%Y%m%d%H%M')                                                                    # 時間をYYYYmmddHHMMに変換
filename = "data/{}_{}.csv".format(now_str, expInfo['participant'])
trials.saveAsWideText(fileName=filename)                                                                # CSVファイルとして保存

core.quit()                                                                                             # 実験終了