import numpy as np
class stim_generator:
    """
    ### manual ###

    """
    def __init__(
            self,
            framerate = 45,
            moniSize_pix = [1920, 1080],
            moniSize_cm = [29.44, 16.56],
            eyeOffset_cm = 57.0,
            background_color = [0.5, 0.5,0.5]):
        
        self.framerate = int(framerate)
        self.moniSize_pix = moniSize_pix
        self.moniSize_cm = moniSize_cm
        self.ratio_cm2pix = moniSize_pix[0] / moniSize_cm[0]

        self.eyeOffset_cm = eyeOffset_cm

        self.background_color = background_color

        self.Nrepeat = None
        self.Ndot = None

        self.xStim = None
        self.yStim = None
        self.xyRange = None
        self.patchSize_pix = None
        self.patchCenter_pix = None
        self.dotSize_pix = None
        self.dotDensity = None

        self.disparity_pix = None
        self.corr_Area_pix = None
        self.Leye_monoArea_pix = None
        self.Reye_monoArea_pix = None
        self.uncorr_jitter_pix = None
        

        def deg2rad(self, d_deg):
            d_rad = np.radians(d_deg)
            d_cm = np.tan(d_rad/2) * 2 * self.eyeOffset_cm
            return d_cm
        
        def deg2pix(self, d_deg):
            d_cm = deg2rad(d_deg)
            d_pix = self.ratio_cm2pix * d_cm
            return int(round(d_pix))

        def setStim_prpty(
                self,
                Nrepeat,
                Ndot,
                patchSize_deg,
                patchCenter_deg,
                dotSize_deg,
                dotDensity,
                disparity_deg,
                corrArea_deg,
                Leye_monoArea_deg,
                Reye_monoArea_deg,
                uncorr_jitter_deg):
            
            patchSize_pix = self.deg2pix(patchSize_deg)
            patchCenter_pix = self.deg2pix(patchCenter_deg)
            dotSize_pix = self.deg2pix(dotSize_deg)
            disparity_pix = self.deg2pix(disparity_deg)
            corrArea_pix = self.deg2pix(corrArea_deg)
            Leye_monoArea_pix = self.deg2pix(Leye_monoArea_deg)
            Reye_monoArea_pix = self.deg2pix(Reye_monoArea_deg)
            uncorr_jitter_pix = self.deg2pix(uncorr_jitter_deg)
            
            x = np.arange(patchSize_pix); x -= np.median(x); Nx = len(x)
            y = np.arange(patchSize_pix); y -= np.median(y); Ny = len(y)

            self.Nrepeat = Nrepeat
            self.Ndot = Ndot

            self.xStim = x
            self.yStim = y
            xmin = np.min(self.xStim)
            xmax = np.max(self.xStim)
            ymin = np.min(self.yStim)
            ymax = np.max(self.yStim)
            self.xyRange = (xmin, xmax, ymin, ymax)
            
            self.patchSize_pix = patchSize_pix
            self.patchCenter_pix = patchCenter_pix
            self.dotSize_pix = dotSize_pix

            self.dotDensity = dotDensity
            self.disparity_pix = disparity_pix

            self.corrArea_pix = corrArea_pix
            self.Leye_monoArea_pix = Leye_monoArea_pix
            self.Reye_monoArea_pix = Reye_monoArea_pix
            self.uncorr_jitter_pix = uncorr_jitter_pix

        def circle(self, dotsXY, dist, centerX, centerY):
            r = dist/2
            centerXY = np.array([centerX, centerY])
            select_range_L = np.sqrt(np.sum((dotsXY - centerXY)**2, axis=1)) < r**2
            select_range_R = np.sqrt(np.sum((dotsXY + centerXY)**2, axis=1)) < r**2

            return (select_range_L, select_range_R)
        
        def geneCorrDots(self, ):
            corrDotsXY_l = dotsXY[select_range_L]
            corrDotsXY_r = dotsXY[select_range_R]

            corrDotsXY_lLeye = corrDotsXY_l - centerXY
            corrDotsXY_rLeye = corrDotsXY_r + centerXY

            corrDotsXY_lReye = corrDotsXY_l - centerXY
            corrDotsXY_rReye = corrDotsXY_r + centerXY

        def uncorr