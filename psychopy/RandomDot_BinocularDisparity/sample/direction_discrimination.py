from __future__ import absolute_import, division

from psychopy import locale_setup
from psychopy import prefs
from psychopy import gui, visual, core, data, event, logging, clock, colors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
from psychopy.hardware import keyboard

import numpy as np
import os
import sys

from stim import Stimulator

SCREEN_NUM = 1
SIZE_PIX = [1920, 1080]
SIZE_CM = [53.3, 29.9] #cm
EYE_OFFSET = 57
VMIN = 0
VMAX = 1
VMEAN = (VMAX + VMIN) / 2
COLOR_SPACE = 'rgb1'

BLACK = [VMIN, VMIN, VMIN]
GRAY = [VMEAN, VMEAN, VMEAN]
WHITE = [VMAX, VMAX, VMAX]
RED = [VMAX, VMIN, VMIN]

# time property
# [ start-time[s], duaring[s] ]
fixation_time_prpty = [0, 0.5]
stim_time_prpty = [0.5, 0.5]
resp_time_prpty = [1.1, None]

# fixation point
fp_deg = 0.4

# stim property
speeds = [3] # deg/sec
cohs = [0.06, 0.12, 0.24, 0.48]
cohs = np.array(cohs)
cohs = np.append(cohs, -cohs)

noise_contrast = 0.1
contStim_contrast = 1.0

n_repeat = 30
n_stim = len(cohs) * len(speeds) * n_repeat

stim_patch_deg = 5
dot_size_deg = 0.1
n_dot = 200
lifetime_frame = 4

# ---------------------------------------------------------------------------
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

psychopyVersion = '2021.2.3'
expName = 'test'
expInfo = {'participant': '', 'session': '001'}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)

if dlg.OK == False:
    core.quit()
    
expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

filename = _thisDir + os.sep + "data/demo"

thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\ReiTakahashi\\psycho_exprm\\1\\prac2.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
    
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)

endExpNow = False
frameTolerance = 0.001

# ---------------------------------------------------------------------------

# Setup the Window
win = visual.Window(
    size = SIZE_PIX, fullscr = True, winType = 'pyglet', allowGUI = False,
    allowStencil = False, monitor = 'testMonitor', color = 'gray',
    colorSpace = COLOR_SPACE, blendMode = 'avg', useFBO = True, units = 'pix',
    screen = SCREEN_NUM)

# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "trial1"
trialClock = core.Clock()


# experimental property-----------------------------------------------------

stimulator = Stimulator(
    moni_size_pix = SIZE_PIX,
    moni_size_cm = SIZE_CM,
    frame_rate = round(expInfo['frameRate']),
    eye_ofst_cm = 57,
    vmin = VMIN, vmax = VMAX);

stimulator.set_stim_prpty(
        patch_size_deg = stim_patch_deg,
        dot_size_deg = dot_size_deg,
        n_repeat = n_repeat,
        stim_time_sec = stim_time_prpty[1],
        speeds = speeds,
        cohs = cohs,
        n_dot = n_dot,
        lifetime_frame = lifetime_frame,
        noise_cont = noise_contrast,
        stim_cont = contStim_contrast)

index_lum = stimulator.generate_stim_seq()

fp_size_pix = stimulator.deg2pix(fp_deg)
fp = stimulator.patch_mono(RED, size_deg = fp_deg)
fixation_point = visual.ImageStim(
    win = win,
    name = 'fixation_point',
    size = fp_size_pix,
    units = 'pix',
    image = fp,
    colorSpace = COLOR_SPACE);

stim_patch_pix = stimulator.deg2pix(stim_patch_deg)
stim = visual.ImageStim(
    win = win,
    name = 'stim',
    size = stim_patch_pix,
    pos = [0, 0],
    flipVert = True,
    units = 'pix',
    colorSpace = COLOR_SPACE)

resp_text = visual.TextStim(
    win = win,
    name = 'resp_text',
    text = 'respond',
    height = 100,
    color = [1, 1, 1],
    units = 'pix',
    colorSpace = COLOR_SPACE)
    
key_resp = keyboard.Keyboard()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# set up handler to look after randomisation of conditions etc
trials1 = data.TrialHandler(
    nReps = n_stim, 
    method = 'random', 
    extraInfo = expInfo,
    originPath = -1,
    trialList = [None],
    seed = None,
    name = 'trials1')
thisExp.addLoop(trials1)  # add the loop to the experiment
thisTrials1 = trials1.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrials1.rgb)

if thisTrials1 != None:
    for paramName in thisTrials1:
        exec('{} = thisTrials1[paramName]'.format(paramName))

i_repeat = -1

for thisTrials1 in trials1:
    currentLoop = trials1
    i_repeat += 1
    
    # abbreviate parameter names if possible (e.g. rgb = thisTrials1.rgb)
    if thisTrials1 != None:
        for paramName in thisTrials1:
            exec('{} = thisTrials1[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "trial"-------
    continueRoutine = True
    i_coh = index_lum[i_repeat][0]
    i_speed = index_lum[i_repeat][1]
    
    stim_img = stimulator.generate_stim_lum(i_coh, i_speed)
    
    # update component parameters for each repeat
    key_resp.keys = []
    _key_resp_allKeys = []
    
    # keep track of which components have finished
    trialComponents = [fixation_point, stim, resp_text, key_resp]
    for thisComponent in trialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
            
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "trial"-------
    while continueRoutine:
        
        t = trialClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=trialClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1
        
        # fixation point --------------------------------------------------------
        
        if fixation_point.status == NOT_STARTED and tThisFlip >= fixation_time_prpty[0]-frameTolerance:
            fixation_point.tStartRefresh = tThisFlipGlobal
            win.timeOnFlip(fixation_point, 'tStartRefresh')
            fixation_point.setAutoDraw(True)
            
        if fixation_point.status == STARTED:
            if tThisFlipGlobal > fixation_point.tStartRefresh + fixation_time_prpty[1]-frameTolerance:
                win.timeOnFlip(fixation_point, 'tStopRefresh')
                fixation_point.setAutoDraw(False)
        
        # -------------- --------------------------------------------------------
    
        
        # luminance stimulus ----------------------------------------------------
        
        if stim.status == NOT_STARTED and tThisFlip >= stim_time_prpty[0]-frameTolerance:
            stim.frameNStart = frameN
            stim.tStartRefresh = tThisFlipGlobal
            win.timeOnFlip(stim, 'tStartRefresh')
            stim.setAutoDraw(True)
            
        if stim.status == STARTED:
            i = frameN - stim.frameNStart
            stim.setImage(stim_img[i])
            
            if tThisFlipGlobal > stim.tStartRefresh + stim_time_prpty[1]-frameTolerance:
                stim.frameNStop = frameN
                win.timeOnFlip(stim, 'tStopRefresh')
                stim.setAutoDraw(False)
        
        # -----------------------------------------------------------------------
        
        # resp_text--------------------------------------------------------------
        
        if resp_text.status == NOT_STARTED and tThisFlip >= resp_time_prpty[0]-frameTolerance:
            resp_text.tStartRefresh = tThisFlipGlobal
            win.timeOnFlip(resp_text, 'tStartRefresh')
            resp_text.setAutoDraw(True)
        
        # -----------------------------------------------------------------------
        
        
        # key_resp---------------------------------------------------------------
        waitOnFlip = False
        if key_resp.status == NOT_STARTED and tThisFlip >= resp_time_prpty[0]-frameTolerance:
            key_resp.tStartRefresh = tThisFlipGlobal
            win.timeOnFlip(key_resp, 'tStartRefresh')
            
            key_resp.status = STARTED
            waitOnFlip = True
            win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            
        if key_resp.status == STARTED and not waitOnFlip:
            theseKeys = key_resp.getKeys(keyList=['left', 'right'], waitRelease=False)
            _key_resp_allKeys.extend(theseKeys)
            
            if len(_key_resp_allKeys):
                key_resp.keys = _key_resp_allKeys[-1].name
                continueRoutine = False
        
        # -----------------------------------------------------------------------
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
            
    # check responses
    if key_resp.keys in ['', [], None]:  # No response was made
        key_resp.keys = None
    
    trials1.addData('coherence', cohs[i_coh])
    trials1.addData('speed[deg/sec]', speeds[i_speed])
    trials1.addData('key_resp.keys',key_resp.keys)
    
    routineTimer.reset()
    thisExp.nextEntry()
    

win.flip()

thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)

logging.flush()
thisExp.abort()

win.close()
core.quit()

