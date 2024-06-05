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
mirror1_mirror2_dist = 10                                                      # [cm]
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

fpPos = np.array([stim_gene.cm2deg(EYEPOS_IN_MONITOR),0])                   # ハプロスコープを使った時、視線がモニタ上のどこに対応するか. 固視点の位置．

# テキスト(教示)を描画するクラス
text_resp_L = visual.TextStim(
    win,
    text = "Press key to respond \n\n<--      -->",    # 描画する文字
    height = 1,                         # 文字の大きさ
    color = white,                      # 文字の色
    units = 'deg',                      # 単位
    colorSpace = COLOR_SPACE,           # 色空間
    pos = -fpPos                        # 呈示位置
)

text_resp_R = visual.TextStim(
    win,
    text = "Press key to respond \n\n<--      -->",   # 描画する文字
    height = 1,                         # 文字の大きさ
    color = white,                      # 文字の色
    units = 'deg',                      # 単位
    colorSpace = COLOR_SPACE,           # 色空間
    pos = fpPos                         # 呈示位置
)

text_start_L = visual.TextStim(
    win,
    text = "SPACE START",                    # 描画する文字
    height = 1,                         # 文字の大きさ
    color = white,                      # 文字の色
    units = 'deg',                      # 単位
    colorSpace = COLOR_SPACE,           # 色空間
    pos = -fpPos+(0, 3.5)            # 呈示位置
)

text_start_R = visual.TextStim(
    win,
    text = "SPACE START",                     # 描画する文字
    height = 1,                         # 文字の大きさ
    color = white,                      # 文字の色
    units = 'deg',                      # 単位
    colorSpace = COLOR_SPACE,           # 色空間
    pos = fpPos+(0, 3.5)              # 呈示位置
)

text_continue_L = visual.TextStim(
    win,
    text = " ",                         # 描画する文字
    height = 1,                         # 文字の大きさ
    color = white,                      # 文字の色
    units = 'deg',                      # 単位
    colorSpace = COLOR_SPACE,           # 色空間
    pos = -fpPos+(0,-3.5)            # 呈示位置
)

text_continue_R = visual.TextStim(
    win,
    text = " ",                         # 描画する文字
    height = 1,                         # 文字の大きさ
    color = white,                      # 文字の色
    units = 'deg',                      # 単位
    colorSpace = COLOR_SPACE,           # 色空間
    pos = fpPos+(0,-3.5)              # 呈示位置
)

# 固視点のパラメータ定義
color_fp = white                        # 固視点の色
fp_L = visual.ShapeStim(                # 左目に呈示する固視点の設定
    win,
    units='deg',
    vertices=((-0.3,0.1), (-0.3,0), (-0.1, 0), (-0.1,-0.3), (0,-0.3), (0,0.3), (-0.1,0.3), (-0.1,0.1)),
    colorSpace=COLOR_SPACE,
    lineColor=None,
    fillColor=color_fp,
    pos=-fpPos
)

fp_R = visual.ShapeStim(                # 右目に呈示する固視点の設定
    win,
    units='deg',
    vertices=((0.3,0.1), (0.3,0), (0.1,0), (0.1,-0.3), (0,-0.3), (0,0.3), (0.1,0.3), (0.1,0.1)),
    colorSpace=COLOR_SPACE,
    lineColor=None,
    fillColor=color_fp,
    pos=fpPos
)

print(fpPos)
LeyeDepthCue, ReyeDepthCue = stim_gene.background_depthCue(win, fpPos)
LeyeDepthCue_1, LeyeDepthCue_2, LeyeDepthCue_3, LeyeDepthCue_4, LeyeDepthCue_5 = LeyeDepthCue
ReyeDepthCue_1, ReyeDepthCue_2, ReyeDepthCue_3, ReyeDepthCue_4, ReyeDepthCue_5 = ReyeDepthCue

# =========================================================
# 視覚刺激パラメータ定義
# =========================================================
fieldPos = (0, 0)                                                   # 原点
Disk_radius = stprm.Disk_radius                               # 相関ありパッチの半径 [deg]

disparity_arr = stprm.disparity_arr                                 # 刺激の視差リスト

fp_stim_dist = 5.5                                                  # 固視点と刺激の距離 [deg]
LeyeStim_left_centerPos = -fpPos-np.array([fp_stim_dist, 0])        # 左目の刺激の中心位置
LeyeStim_right_centerPos = -fpPos+np.array([fp_stim_dist, 0])       # 左目の刺激の中心位置
ReyeStim_left_centerPos = fpPos-np.array([fp_stim_dist, 0])         # 右目の刺激の中心位置
ReyeStim_right_centerPos = fpPos+np.array([fp_stim_dist, 0])        # 右目の刺激の中心位置
LorR_arr = ['left', 'right']                                        # 辞書型で管理して実験結果を見やすくする

fixation_start = stprm.fixation_start                               # 固視点呈示開始時刻
fixation_end = stprm.fixation_end                                   # 固視点呈示終了時刻
stim_start = stprm.stim_start                                       # 刺激呈示開始時刻
stim_end = stprm.stim_end                                           # 刺激呈示終了時刻
resp_start = stprm.resp_start                                       # 応答開始時刻
# flip_interval = stprm.flip_interval                                 # フリップ間隔

# =========================================================
# 実験条件
# =========================================================
N_repeat = stprm.N_repeat                                           # 各パラメータの繰り返し回数
frame_tolerance = 0.01                                              # sec, フレームの許容誤差
times = {
    'fixation': [fixation_start, np.inf],                           # 固視点の呈示時間
    'stim': [stim_start, stim_end],                                 # 刺激の呈示時間
    'resp': [resp_start, np.inf],                                   # 応答の時間
    'text_start': [fixation_start, fixation_end]                    # テキストの呈示時間
}

# trial毎に変える条件
conditions = data.createFactorialTrialList({
    'disparity_test' : disparity_arr,
    'TestPos_LorR' : LorR_arr
})

stimOder = stprm.stimOder
trials = data.TrialHandler(
    conditions,                                                                                                 # trial毎に変える条件
    nReps = N_repeat,                                                                                           # １条件を何回繰り返すか
    method = stimOder                                                                                           # ランダマイズの方法                                                                                    # ランダマイズの方法
)
trialComponents_start = [text_start_L, text_start_R, text_continue_L, text_continue_R, keyboard_start]          # トライアル開始のコンポーネント
                                                                
Trial_N = len(disparity_arr) * len(LorR_arr) * N_repeat                                                         # 総試行回数
print("トライアル回数 : ", Trial_N, "回")

# =========================================================
# 実験開始
# =========================================================
trial_cnt = 1
for trial in trials:
    disparity_test = trial['disparity_test']
    TestPos_LorR = trial['TestPos_LorR']

    # test刺激が固視点の左に呈示される条件
    if TestPos_LorR == 'left':
        # 円形のパッチ刺激
        LeyeStim_left = visual.Circle(win, units='deg', radius=Disk_radius, fillColor='white', pos=LeyeStim_left_centerPos+(disparity_test, 0))
        LeyeStim_right = visual.Circle(win, units='deg', radius=Disk_radius, fillColor='white', pos=LeyeStim_right_centerPos)
    
        ReyeStim_left = visual.Circle(win, units='deg', radius=Disk_radius, fillColor='white', pos=ReyeStim_left_centerPos-(disparity_test, 0))
        ReyeStim_right = visual.Circle(win, units='deg', radius=Disk_radius, fillColor='white', pos=ReyeStim_right_centerPos)

    # test刺激が固視点の右に呈示される条件
    else:
        # 円形のパッチ刺激
        LeyeStim_left = visual.Circle(win, units='deg', radius=Disk_radius, fillColor='white', pos=LeyeStim_left_centerPos)
        LeyeStim_right = visual.Circle(win, units='deg', radius=Disk_radius, fillColor='white', pos=LeyeStim_right_centerPos-(disparity_test, 0))
    
        ReyeStim_left = visual.Circle(win, units='deg', radius=Disk_radius, fillColor='white', pos=ReyeStim_left_centerPos)
        ReyeStim_right = visual.Circle(win, units='deg', radius=Disk_radius, fillColor='white', pos=ReyeStim_right_centerPos+(disparity_test, 0))

    # trialに使うコンポーネント
    trialComponents_present = [fp_L, fp_R, 
                               LeyeStim_left, LeyeStim_right, ReyeStim_left, ReyeStim_right, 
                               LeyeDepthCue_1, LeyeDepthCue_2, LeyeDepthCue_3, LeyeDepthCue_4, LeyeDepthCue_5,
                               ReyeDepthCue_1, ReyeDepthCue_2, ReyeDepthCue_3, ReyeDepthCue_4, ReyeDepthCue_5,
                               text_resp_L, text_resp_R, keyboard_resp]


    ########################################### スタート画面 ############################################
    # コンポーネントの状態を初期化
    continueRoutine = True                                                                                      # trial中はTrue
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
            text_continue_L.text = "current number of trials : {trial} \n {left} trials left".format(left=Trial_N-trial_cnt+1, trial=trial_cnt)            # 描画する文字を設定
            text_continue_R.text = "current number of trials : {trial} \n {left} trials left".format(left=Trial_N-trial_cnt+1, trial=trial_cnt)            # 描画する文字を設定
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
    keyboard_resp.keys = None                                                                           # キーボード応答を初期化

    # 各コンポーネントのステータスをリセット
    for thisComponent_present in trialComponents_present:
        if hasattr(thisComponent_present, 'status'):
            thisComponent_present.status = NOT_STARTED
    
    # タイマーリセット
    time_first_frame = win.getFutureFlipTime(clock="now")                                               # 次の画面フリップまでにかかる時間
    clock.reset(-time_first_frame)                                                                      # 次に画面フリップしたときに時間が0になるように設定
    i_frame = -1                                                                                        # 刺激呈示中のフレーム番号

    stim_opacity = 1                                                                            # 刺激の透明度の初期化
    ### トライアル開始 ###
    while routine:
        i_frame += 1
        t_flip = win.getFutureFlipTime(clock=clock)                                                     # 次にflipが行われる時刻(trial内)
        t_flip_global = win.getFutureFlipTime(clock=None)                                               # 次にflipが行われる時刻(実験全体)

        # dynamic random dotの呈示
        if (LeyeStim_left.status==NOT_STARTED) and (t_flip >= times['stim'][0]-frame_tolerance):
            print('========呈示開始=======')
            LeyeStim_left.status = STARTED                                                              # 呈示開始
            LeyeStim_right.status = STARTED                                                             # 呈示開始
            ReyeStim_left.status = STARTED                                                              # 呈示開始
            ReyeStim_right.status = STARTED                                                             # 呈示開始
            
            LeyeDepthCue_1.status = STARTED                                                               # 呈示開始
            LeyeDepthCue_2.status = STARTED                                                               # 呈示開始
            LeyeDepthCue_3.status = STARTED                                                               # 呈示開始
            LeyeDepthCue_4.status = STARTED                                                               # 呈示開始
            LeyeDepthCue_5.status = STARTED                                                               # 呈示開始
            
            ReyeDepthCue_1.status = STARTED                                                               # 呈示開始
            ReyeDepthCue_2.status = STARTED                                                               # 呈示開始
            ReyeDepthCue_3.status = STARTED                                                               # 呈示開始
            ReyeDepthCue_4.status = STARTED                                                               # 呈示開始
            ReyeDepthCue_5.status = STARTED                                                               # 呈示開始
        
            LeyeStim_left.frameNStart = i_frame                                                         # 呈示開始時のフレームを保存

            LeyeDepthCue_1.draw(win)                                                                    # 刺激を描画
            LeyeDepthCue_2.draw(win)                                                                    # 刺激を描画
            LeyeDepthCue_3.draw(win)                                                                    # 刺激を描画
            LeyeDepthCue_4.draw(win)                                                                    # 刺激を描画
            LeyeDepthCue_5.draw(win)                                                                    # 刺激を描画
            
            ReyeDepthCue_1.draw(win)                                                                    # 刺激を描画
            ReyeDepthCue_2.draw(win)                                                                    # 刺激を描画
            ReyeDepthCue_3.draw(win)                                                                    # 刺激を描画
            ReyeDepthCue_4.draw(win)                                                                    # 刺激を描画
            ReyeDepthCue_5.draw(win)                                                                    # 刺激を描画

            LeyeStim_left.draw(win)                                                                     # 刺激を描画
            LeyeStim_right.draw(win)                                                                    # 刺激を描画
            ReyeStim_left.draw(win)                                                                     # 刺激を描画
            ReyeStim_right.draw(win)                                                                    # 刺激を描画
        
        # 刺激が呈示されているとき
        if LeyeStim_left.status == STARTED:
    
            LeyeDepthCue_1.draw(win)                                                                    # 刺激を描画
            LeyeDepthCue_2.draw(win)                                                                    # 刺激を描画
            LeyeDepthCue_3.draw(win)                                                                    # 刺激を描画
            LeyeDepthCue_4.draw(win)                                                                    # 刺激を描画
            LeyeDepthCue_5.draw(win)                                                                    # 刺激を描画
            
            ReyeDepthCue_1.draw(win)                                                                    # 刺激を描画
            ReyeDepthCue_2.draw(win)                                                                    # 刺激を描画
            ReyeDepthCue_3.draw(win)                                                                    # 刺激を描画
            ReyeDepthCue_4.draw(win)                                                                    # 刺激を描画
            ReyeDepthCue_5.draw(win)                                                                    # 刺激を描画

            LeyeStim_left.draw(win)                                                                     # 刺激を描画
            LeyeStim_right.draw(win)                                                                    # 刺激を描画
            ReyeStim_left.draw(win)                                                                     # 刺激を描画
            ReyeStim_right.draw(win)                                                                    # 刺激を描画
            
            # 次のフリップで呈示終了時刻を過ぎるとき
            if t_flip >= times['stim'][1] - frame_tolerance:
                print('========呈示終了=======')
                LeyeStim_left.status = FINISHED                                                         # 呈示終了
                LeyeStim_right.status = FINISHED                                                        # 呈示終了
                ReyeStim_left.status = FINISHED                                                         # 呈示終了
                ReyeStim_right.status = FINISHED                                                        # 呈示終了

                LeyeDepthCue_1.status = FINISHED                                                        # 呈示終了
                LeyeDepthCue_2.status = FINISHED                                                        # 呈示終了
                LeyeDepthCue_3.status = FINISHED                                                        # 呈示終了
                LeyeDepthCue_4.status = FINISHED                                                        # 呈示終了
                LeyeDepthCue_5.status = FINISHED                                                        # 呈示終了

                ReyeDepthCue_1.status = FINISHED                                                        # 呈示終了
                ReyeDepthCue_2.status = FINISHED                                                        # 呈示終了
                ReyeDepthCue_3.status = FINISHED                                                        # 呈示終了
                ReyeDepthCue_4.status = FINISHED                                                        # 呈示終了
                ReyeDepthCue_5.status = FINISHED                                                        # 呈示終了

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
                
        
        ############################################ 応答画面 #############################################
        # 入力開始していない かつ 次のフリップで開始時刻を過ぎるとき
        if (keyboard_resp.status==NOT_STARTED) and (t_flip >= times['resp'][0]-frame_tolerance):
            print('========応答開始=======')
            keyboard_resp.status = STARTED                                                              # キーボードの状態を開始にする
            waitOnFlip = True

            win.callOnFlip(keyboard_resp.clearEvents, eventType='keyboard')                             # 次のフリップでキーボードのイベントをリセット
            print('response : ', keyboard_resp.keys)
            print('t_flip : ', t_flip, 'time : ', times['resp'][0])
          
        # キーボード入力が既に始まった かつ フリップを待った後
        # if (keyboard_resp.status==STARTED) and (t_flip >= times['resp'][0]-frame_tolerance):
        if (keyboard_resp.status==STARTED) and not waitOnFlip:
            # 何も入力されていないときは空のリストが返る
            all_key_resp = keyboard_resp.getKeys(keyList=['left', 'right'], waitRelease=False)             # キーボード入力を取得 (keyList中のキーのみ取得)
            text_resp_L.setAutoDraw(True)                                                               # text_resp_Lの描画
            text_resp_R.setAutoDraw(True)                                                               # text_resp_Rの描画

            # もし何かしら入力されたら
            if all_key_resp:
                keyboard_resp.keys = all_key_resp[-1].name                                              # 押されたキーの名前を取得
                print('response : ', keyboard_resp.keys)
                print('========応答終了=======###')
                text_resp_L.setAutoDraw(False)                                                          # テキストの描画を辞める
                text_resp_R.setAutoDraw(False)                                                          # テキストの描画を辞める
                routine = False
                win.flip(clearBuffer=True)  # ウィンドウを手動で更新して即座に次のトライアルに移る
        
        waitOnFlip = False
        
        # キー入力が何もなかったら、Noneにする
        if keyboard_resp.keys in ['', [], None]:
            keyboard_resp.keys = None
        
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
    
    # 入力されたキーをデータに追加
    trials.addData('key', keyboard_resp.keys)
    print("TestPos:", TestPos_LorR, ", resp:", keyboard_resp.keys, "Disparity:", disparity_test)


# 実験条件とレスポンスのデータを保存
# ファイル名は -> data/被験者名_実験をした時間.csv  とする
if not os.path.isdir('data/'):
    os.mkdir('data/')
now = datetime.datetime.now()                                                                           # 現在の時間を取得
now_str = now.strftime('%Y%m%d%H%M')                                                                    # 時間をYYYYmmddHHMMに変換
filename = "data/{}_{}.csv".format(now_str, expInfo['participant'])
trials.saveAsWideText(fileName=filename)                                                                # CSVファイルとして保存

core.quit()                                                                                             # 実験終了