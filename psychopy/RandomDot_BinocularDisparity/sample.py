# PsychoPyライブラリのインポート
from psychopy import core, monitors, visual, data, gui
from psychopy.hardware import keyboard
from psychopy.constants import NOT_STARTED, STARTED, FINISHED
import math
import numpy as np
import os
import datetime


# 実験情報を保存
expInfo = {'participant' : ""}

# 被験者の名前をGUIで入力
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=None)
if dlg.OK == False: # GUIウインドウがキャンセルされたら実験をしない
    core.quit()


# 色空間の設定
COLOR_SPACE = 'rgb1'
red = [1, 0, 0]
black = [0, 0, 0]
white = [1, 1, 1]

# モニタサイズと視距離の定義
MONITOR_SIZE_PIX = [1920, 1080]  # モニターサイズ (x, y)[pixel]
MONITOR_WIDTH_CM = 31.0         # モニターの横幅[cm]
DISTANCE_CM = 57.3              # 視距離[cm]

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
    color = black,              # 背景色
    fullscr = True,             # フルスクリーン化
    monitor = moni,             # モニタ情報を設定 (設定すると、刺激のサイズが正しく描画される)
    screen = 0,                 # スクリーンを選択 (モニタが複数ある場合、刺激呈示する画面を選べる)
    allowStencil = True         # Aperture刺激の呈示に必要 (openGLの使用を許可するらしい)
)

keyboard_default = keyboard.Keyboard()  # 実験中断等に使う
keyboard_resp = keyboard.Keyboard()     # 被験者の応答の取得に使う
clock = core.Clock()                    # 時間管理クラス

# 固視点のパラメータ定義
diam_fp = 0.4   # 固視点の直径[deg]
pos_fp = (0, 0) # 固視点の位置
color_fp = red  # 固視点の色
fixation_point = visual.Circle(
    win,
    units = 'deg',
    radius = diam_fp/2,
    colorSpace = COLOR_SPACE,
    fillColor = red,
    pos = pos_fp,
)

# テキストを描画するクラス
text = visual.TextStim(
    win,
    text = "Press key to respond",     # 描画する文字
    height = 1,                 # 文字の大きさ
    color = white,              # 文字の色
    units = 'deg',
    colorSpace = COLOR_SPACE,
    pos = (0, 0)
)

# ramdom dot motionのパラメータ定義
size_dots = 0.1                         # 1ドットの直径[deg]
color_dots = white                      # ドットの色
pos_field = (0, 0)                      # ドット位置の原点
speed_dots = 3                          # ドットの移動速度[deg/sec]
size_patch = 5                          # ドットが描画される範囲の直径[deg]
density_dots = 10                       # ドットの密度[個/deg^2]
N_dots = (size_patch**2) * density_dots # ドットの個数
time = 2                                # 刺激呈示時間[sec]
frame_rate = 45   # フレームレートを自動取得[frame/sec] 
N_frame = math.ceil(time * frame_rate)  # 呈示に必要なフレーム数(整数にするために小数点以下切り上げ)
dx = speed_dots / frame_rate            # 1フレーム毎のドットの移動量[deg/frame]
xmin, xmax = (-size_patch/2, size_patch/2)
ymin, ymax = (-size_patch/2, size_patch/2)

# ドットを描画するクラス
dot_stim = visual.ElementArrayStim(
    win,
    units = 'deg',              # 単位 (視角) [degree]
    fieldPos = pos_field,       # パッチの位置
    nElements = N_dots,         # ドット数 (ドット数は変更できないので、毎回同じドット数が表示される)
    sizes = size_dots,          # 1ドットのサイズ, 直径 [degree]
    colors = color_dots,        # ドットの色
    colorSpace = COLOR_SPACE,   # カラースペース
    elementTex = None,          # ドットにかけるエフェクト
    elementMask = 'circle',     # ドットの形
)

# 刺激の描画範囲を限定するクラス
aperture = visual.Aperture(
    win,
    size = size_patch,
    pos = pos_field,
    shape = 'circle',
    units = 'deg'
)
aperture.disable()

# 実験パラメータ
frame_tolerance = 0.01  #sec, フレームの許容誤差
times = {   # 刺激呈示時間 (開始時間, 終了時間) [sec]
    'fixation': [0.3, 0.9],
    'stim': [0.6, 0.9],
    'resp': [1.0, np.inf],
    'text': [1.0, np.inf]
}
N_repeat = 20   # 各パラメータを何回繰り返すか

# coherence, 試行毎に可変なパラメータ
# 負の値: ドットは右➔左に動く,  正の値: ドットは左➔右に動く
coherence_arr = [-1, -0.64, -0.32, -0.16, -0.08, 0, 0.08, 0.16, 0.32, 0.64, 1]

# 実験に使う全てのコンポーネント
trialComponents = [fixation_point, dot_stim, text, keyboard_resp]

# trial毎に変える条件を指定 (複数指定も可能)
# trial毎にリストの中の値の組み合わせがランダムに1つ選ばれる
conditions = data.createFactorialTrialList({
    'coherence': coherence_arr
})

# コヒーレンスがn種類, N_repeatがm回のとき -> trialの総数はn×m回になる
# method='random' -> コヒーレンスがランダムに選ばれるが、全コヒーレンスがn回選ばれたあと、n+1回目が選ばれる (同じコヒーレンスが連続で選ばれたりはしない)
# method='fullRandom' -> コヒーレンスが完全にランダムに選ばれる(同じコヒーレンスが連続で選ばれることがある)
# method='sequential' -> コヒーレンスがリストの順番通りに選ばれる
trials = data.TrialHandler(
    conditions,           # trial毎に変える条件
    nReps = N_repeat,     # １条件を何回繰り返すか
    method = 'random'     # ランダマイズの方法
)

# ここから実験
for trial in trials:
    # trial毎に選ばれた条件(conditions)はtrial['条件の名前']で取り出せる
    coherence = trial['coherence']
    sign = 1 if coherence > 0 else -1               # 刺激の運動方向
    N_dots_noise = round(N_dots * (1 - np.abs(coherence)))  # noise dotの数

    pos_list = []                                       # フレーム毎のドット位置を格納
    pos_dots_x = np.random.uniform(xmin, xmax, N_dots)  # ドットの初期位置(x)
    pos_dots_y = np.random.uniform(ymin, ymax, N_dots)  # ドットの初期位置(y)
    index_dots = np.arange(N_dots)                      # ドットのindex

    # 10フレーム分余分に作成
    for _ in range(N_frame+10):
        pos_dots = np.column_stack((pos_dots_x, pos_dots_y))    # Nx2 arrayの生成
        pos_list.append(pos_dots)                               # ドット位置を格納
        
        pos_dots_x += sign * dx                                 # ドットを右方向に移動
        pos_dots_x[pos_dots_x > xmax] = xmin                    # 描画範囲を超えたドットは左端に戻す

        # noise dotを選択する
        index_dots_noise = np.random.choice(index_dots, size=N_dots_noise, replace=False)

        # noise dotのxy位置を生成してセット
        pos_dots_x_noise = np.random.uniform(xmin, xmax, N_dots_noise)
        pos_dots_y_noise = np.random.uniform(ymin, ymax, N_dots_noise)
        pos_dots_x[index_dots_noise] = pos_dots_x_noise
        pos_dots_y[index_dots_noise] = pos_dots_y_noise

    routine = True                                          # trial中はTrue
    all_key_resp = None                                     # キーボード応答を初期化
    keyboard_default.keys = None                            # キーボード応答を初期化
    keyboard_resp.keys = None                               # キーボード応答を初期化
    time_first_frame = win.getFutureFlipTime(clock="now")   # 次の画面フリップまでにかかる時間
    clock.reset(-time_first_frame)                          # 次に画面フリップしたときに時間が0になるように設定
    i_frame = -1                                            # 刺激呈示中のフレーム番号

    # 各コンポーネントのステータスをリセット
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # 現在の実験条件をcmdに表示
    print("N_trial: {},  N_rep: {}, coh: {}\n".format(trials.thisN+1, trials.thisRepN+1, coherence))

    # ここからtrialがスタート
    while routine:
        i_frame += 1
        t_flip = win.getFutureFlipTime(clock=clock)         # 次にflipが行われる時刻(trial内)
        t_flip_global = win.getFutureFlipTime(clock=None)   # 次にflipが行われる時刻(実験全体)


        # ランダムドットモーションの呈示 ==========
        # 刺激がまだ呈示されていない かつ 次のフリップで呈示開始時刻を過ぎるとき
        if (dot_stim.status==NOT_STARTED) and (t_flip >= times['stim'][0]-frame_tolerance):
            dot_stim.status = STARTED       # 呈示開始
            dot_stim.frameNStart = i_frame  # 呈示開始時のフレームを保存
            dot_stim.draw(win)              # setAutoDrawがないので、毎回drawする
            aperture.enable()               # Apertureをon
            
        # 刺激が呈示されているとき
        if dot_stim.status == STARTED:
            i_pos = i_frame - dot_stim.frameNStart  # pos_listのインデックス
            dot_stim.setXYs(pos_list[i_pos])        # ドット位置のセット
            dot_stim.draw(win)                      # 刺激を描画

            # 次のフリップで呈示終了時刻を過ぎるとき
            if t_flip >= times['stim'][1] - frame_tolerance:
                dot_stim.status = FINISHED  # 呈示終了
                aperture.disable()          # Apertureをoff


        # 固視点の呈示 ==========
        if (fixation_point.status==NOT_STARTED) and (t_flip >= times['fixation'][0]-frame_tolerance):
            fixation_point.status = STARTED
            fixation_point.setAutoDraw(True)    # flip毎に自動で描画する

        if fixation_point.status == STARTED:
            if t_flip >= times['fixation'][1] - frame_tolerance:
                fixation_point.status = FINISHED
                fixation_point.setAutoDraw(False)
        

        # テキストの呈示 ==========
        if (text.status==NOT_STARTED) and (t_flip >= times['text'][0]-frame_tolerance):
            text.status = STARTED
            text.setAutoDraw(True)    # flip毎に自動で描画する


        # キーボード入力の受付開始 ==========
        waitOnFlip = False  # 次のフリップを待つ

        # 入力開始していにない かつ 次のフリップで開始時刻を過ぎるとき
        if (keyboard_resp.status==NOT_STARTED) and (t_flip >= times['resp'][0]-frame_tolerance):
            keyboard_resp.status = STARTED
            waitOnFlip = True

            # 次のフリップでキーボードのイベントをリセット
            win.callOnFlip(keyboard_resp.clearEvents, eventType='keyboard')
            
        # キーボード入力が既に始まった かつ フリップを待った後
        if (keyboard_resp.status==STARTED) and (not waitOnFlip):
            # キーボード入力を取得 (keyList中のキーしか取得できない)
            # 何も入力されていないときは空のリストが返る
            all_key_resp = keyboard_resp.getKeys(keyList=['right', 'left'], waitRelease=False)

            # もし何かしら入力されたら
            if all_key_resp:
                keyboard_resp.keys = all_key_resp[-1].name  # 押されたキーの名前を取得
                routine = False                     # trialの継続をFalseにする
            
        # エスケープが押されたら実験終了
        if keyboard_default.getKeys(keyList=["escape"]):
            core.quit()
                
        if not routine:
            break       # trial終了
        else:
            win.flip()  # trial継続


    # trialを抜けた後の処理 ==========
    text.setAutoDraw(False) # テキストの描画を辞める
   
    # 入力されたキーをデータに追加
    # thisTrial['条件の名前']で取得できる実験条件は、自動的にデータに追加される
    trials.addData('key', keyboard_resp.keys)


win.flip()

# 実験条件(コヒーレンスなど)とレスポンスのデータを保存
# ファイル名は -> data/被験者名_実験をした時間.csv  とする
if not os.path.isdir('data/'):
    os.mkdir('data/')
now = datetime.datetime.now()                           # 現在の時間を取得
now_str = now.strftime('%Y%m%d%H%M')                    # 時間をYYYYmmddHHMMに変換
filename = "data/{}_{}.csv".format(now_str, expInfo['participant'])
trials.saveAsWideText(fileName=filename)              # CSVファイルとして保存

core.quit() # 実験終了