# パラメータ設定用プログラム

import numpy as np
# =========================================================
# 視覚刺激パラメータ定義
# =========================================================
elemSize = 0.07                                                                                                 # ドットサイズ [deg]
dotsDensity = 15                                                                                                # ドット密度[%]
surrPatch_range = 11                                                                                            # 無相関パッチの描画範囲 [deg]
RefDisk_radius = 3                                                                                              # 相関ありパッチの半径 [deg]

disparity_arr = [-0.3, 0, 0.3]                                                                                  # 刺激の視差リスト

# TestDiskPos_LorR_dict = {'left':np.array([1, -1]), 'right':np.array([-1, 1])}                                   # reference刺激とtest刺激が左右どちらに出るか[ref, test]

TestDisk_radius_arr = np.array([0.569, 0.727, 0.825, 1, 1.169, 1.340, 1.530]) * RefDisk_radius                  # test刺激の半径

# =========================================================
# 呈示パラメータ定義
# =========================================================
fixation_start = 0.5                                                                                            # 固視点呈示開始時刻
fixation_end = 1.5                                                                                              # 固視点呈示終了時刻

stim_start = fixation_end                                                                                       # 刺激呈示開始時刻
present_time = 3.01                                                                                             # 刺激呈示時間
stim_end = stim_start + present_time                                                                            # 刺激呈示終了時刻

resp_start = stim_end+0.3                                                                                       # 応答開始時間

# flip_interval = 5                                                                                               # フリップ間隔

# =========================================================
# 実験パラメータ定義
# =========================================================
N_repeat = 5
stimOder = 'random'
