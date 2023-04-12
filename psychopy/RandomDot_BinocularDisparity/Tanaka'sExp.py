# ===================================================
# library import
# ===================================================
from psychopy import core, monitors, visual, data, gui, logging
from psychopy.hardware import keyboard
from psychopy.constants import NOT_STARTED, STARTED, FINISHED
import math
import numpy as np
import os

from stim import Tanaka_stim as stm

# ===================================================
# properties
# ===================================================
# ========== monitor ==========
SCREEN_NUM = 1
MONITOR_SIZE_PIX = [1920, 1080] # monitor size
MONITOR_WIDTH_CM  = 31.0        # モニタの横幅 (cm)
DISTANCE_CM = 57.3              # 視距離 : 目 -> 鏡，鏡 -> モニタまでの合計距離

# ========== color  ==========
COLOR_SPACE = 'rgb1'
black=[0, 0, 0]
white=[1, 1, 1]
gray=[0.5, 0.5, 0.5]

white_lum = 1.90    # luminance (cd/m^2)
black_lum = 0.01    # luminance (cd/m^2)
gray_lum = 0.95     # luminance (cd/m^2)

# ========== frame rate ==========
framerate = 4

# ========== time ==========
stimTime = 141  #ms

# ========== fixation point ==========
fp_deg = 0.2

# ========== stimulus ==========
Ndots = 4000
dotDensity = 0.15

dotSize_deg = 0.14
disparities_deg = np.array([-0.3, -0.15, 0, 0.15, 0.3])
jitter_deg = 0.2

patchDist_deg = 5
patchDiam_deg = 6

patchLRpos_deg = 7
RefTestPos_deg = np.array([2, 0])
RefTestPos_lr = [np.array([-1, 1]), np.array([1, -1])]  # RefTestPos_degと掛けてreferenceが左右どちらにあるかを決める

# ========== experiment ==========
Nrepeat = 30    # number of repetitions of stimulus conditions


# ===================================================
# experiment information
# ===================================================
thisDir = os.path.dirname(os.path.abspath(__file__)); os.chdir(thisDir)

psychopyVersion = '2022.1.4'
expName = 'pra'
expInfo = {'participant' : '', 'session' : '001'}
dlg = gui.DlgFromDict(
    dictionary=expInfo, 
    sortKeys=False, 
    title=expName
    )

if dlg.OK == False:
    core.quit()

expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

fileName = thisDir + os.sep + "data/demo"

thisExp = data.ExperimentHandler(
    name = expName,
    version='',
    extraInfo=expInfo,
)