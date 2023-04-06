import numpy as np
import itertools

class Stimulator :
    """
    Handle functions which generates stimulus and converts between degree, cm and pixel.
    
    Attributes
    -------------
    frame_rate : int (or float)
        Frame rate of monitor.
    
    moni_size_pix : (int, int)
        Monitor size in pixel.
        Values are [horizontal, vertival].
    
    moni_size_cm : (float, float)
        Monitor size in cm.
        Values are [horizontal, vertival].
    
    eye_ofst_cm : float
        Distance between eye and monitor in cm.
    
    vmin : float
        Minimum value of RGB.
    
    vmin : float
        Maximum value of RGB.
    
    vmean : float
        Average value of RGB.
    
    noise_dark : float
        Minimum value of noise on stimulus patch.
    
    noise_bright : float
        Maximum value of noise on stimulus patch.
    
    backgound_color : (float, float, float)
        Background color of experimental window.
        Values are (R, G, B).
    
    ratio_cm2pix : float
        Ratio for converting cm to pixel.
    
    x_stim : np.ndarray
        X axis of stimulus array.
    
    y_stim : np.ndarray
        Y axis of stimulus array.
    
    xy_range : (float, float, float, float)
        Range of x axis and y axis.
        Values are (xMin, xMax, yMin, yMax).
    
    patch_size_pix : int
        Patch size of stimulus window in pixel.
    
    dot_size_pix : int
        Dot size of stimulus in pixel.
    
    cohs : list of float
        Coherences of 0 to 1.
    
    speeds : list of float
        Speeds of stimulus [deg/sec].
    
    n_repeat : int
        Number of repetitions under the same condition consisting of combination of stimulus coherence and speed.
    
    n_dot : int
        Number of stimulus dots.
    
    lifetime_frame : int
        Lifetime of stimulus dot in frame.
    
    stim_shape : (int, int, int, 1)
        Templete for generating stimulus seed.
        Values are (n_frame, len(y), len(x), 1).
    
    stim_cont : float
        Contrast of contrast-stimulus
    """
    
    def __init__(
        self, 
        frame_rate = 60,
        moni_size_pix = [1920, 1080],
        moni_size_cm = [29.44, 16.56], 
        eye_ofst_cm = 57.0,
        vmin = 0,
        vmax = 1,
        background_color = [0.5, 0.5, 0.5]):
            self.frame_rate = int(frame_rate)
            self.moni_size_cm = moni_size_cm
            self.moni_size_pix = moni_size_pix
            self.eye_ofst_cm = eye_ofst_cm
            self.vmin = vmin
            self.vmax = vmax
            self.vmean = (self.vmax + self.vmin) / 2
            
            self.background_color = background_color
            self.ratio_cm2pix = moni_size_pix[0] / moni_size_cm[0]
            
            self.x_stim = None
            self.y_stim = None
            self.xy_range = None
            self.patch_size_pix = None
            self.dot_size_pix = None
            self.cohs = None
            self.speeds = None
            self.n_repeat = None
            self.n_dot = None
            self.lifetime_frame = None
            self.stim_shape = None
            self.stim_cont = None
    
    def deg2cm(self, d_deg):
        d_rad = np.deg2rad(d_deg)
        d_cm = np.tan(d_rad / 2) * 2 * self.eye_ofst_cm
        return d_cm
    
    def deg2pix(self, d_deg):
        d_cm = self.deg2cm(d_deg)
        d_pix = self.ratio_cm2pix * d_cm
        return int(round(d_pix))
        
    def gray2RGB(self, arr):
        return np.tile(arr, (1, 3))
    
    # contrast value to range of luminance value
    def contrast2vRange(self, contrast):
        # Definition : Lmax = L + a,  Lmin = L - a, L = vmean
        # Michelson contrast : c = (Lmax - Lmin) / (Lmax + Lmin)
        # c = (L+a - L-a) / (L+a + L-a) = a / L
        # a = c * L
        
        a = contrast * self.vmean
        Lmin = self.vmean - a
        Lmax = self.vmean + a
        if Lmin < self.vmin:    Lmin = self.vmin
        if Lmax > self.vmax:    Lmax = self.vmax
        
        return (Lmin, Lmax)
        
    
    # set the stimulus properties
    def set_stim_prpty(
        self,
        patch_size_deg,
        dot_size_deg,
        n_repeat,
        stim_time_sec,
        speeds,
        cohs,
        n_dot,
        lifetime_frame,
        noise_cont,
        stim_cont):
            patch_size_pix = self.deg2pix(patch_size_deg)
            dot_size_pix = self.deg2pix(dot_size_deg)
            x = np.arange(patch_size_pix);  x = x - np.median(x);   Nx = len(x)
            y = np.arange(patch_size_pix);  y = y - np.median(y);   Ny = len(y)
            
            cohs = np.append([], cohs)
            speeds = np.append([], speeds)
            
            n_frame = round(self.frame_rate * stim_time_sec) + 5
            
            stim_shape = (n_frame, Ny, Nx, 1)
            
            self.patch_size_pix = patch_size_pix
            self.dot_size_pix = dot_size_pix
            self.cohs = cohs
            self.speeds = speeds
            self.x_stim = x
            self.y_stim = y
            self.stim_shape = stim_shape
            self.n_repeat = n_repeat
            self.n_frame = n_frame
            self.n_dot = n_dot
            self.lifetime_frame = lifetime_frame
            
            noise_vrange = self.contrast2vRange(noise_cont)
            self.noise_dark = noise_vrange[0]
            self.noise_bright = noise_vrange[1]
            
            self.stim_cont = stim_cont
            
            xmin = np.min(self.x_stim)
            xmax = np.max(self.x_stim)
            ymin = np.min(self.y_stim)
            ymax = np.max(self.y_stim)
            self.xy_range = (xmin, xmax, ymin, ymax)
            

    def circle(self, x, y, d, center_x, center_y):
        r = d / 2
        [X, Y] = np.meshgrid(x, y)
        patch = np.where(
            (X - center_x)**2 + (Y - center_y)**2 <= r**2,
            True, False)
        
        return patch

    def patch_mono(self, color, size_deg = None):
        d_pix = self.deg2pix(size_deg)
        plane = np.tile(self.background_color, (d_pix, d_pix, 1))
        
        x = np.arange(d_pix);   x = x - np.median(x)
        y = np.arange(d_pix);   y = y - np.median(y)
        patch = self.circle(x, y, d_pix, 0, 0)
        
        plane[patch] = color
        return plane

    def move(self, pos, speed, direction):
        dx = speed * np.cos(np.radians(direction))
        dy = speed * np.sin(np.radians(direction))
        pos[:, 0] += dx
        pos[:, 1] += dy

    def get_ori(self, n_dot, coh):
        coh_ori = 0 if coh >= 0 else 180
        coh = np.abs(coh)
        
        theta_seed = np.random.uniform(0, 360, n_dot)
        theta_seed = np.append(coh_ori, theta_seed)
        
        p_random_motion = (1 - coh) / n_dot
        p_arr = np.tile(p_random_motion, n_dot)
        p_arr = np.append(coh, p_arr)
        
        theta = np.random.choice(theta_seed, size = n_dot, replace = True, p = p_arr)
        return theta, coh_ori
    
    # generate stimulus sequence combinated coherences and speeds
    def generate_stim_seq(self):
        coh_seq_seed = np.arange(len(self.cohs))
        speed_seq_seed = np.arange(len(self.speeds))
        
        comb = list(itertools.product(coh_seq_seed, speed_seq_seed))
        comb_repeat = np.tile(comb, (self.n_repeat, 1))
        comb_repeat_seq = np.arange(len(comb_repeat))
        
        random_seq = np.random.choice(
            comb_repeat_seq,
            size = len(comb_repeat_seq),
            replace = False)
        
        return comb_repeat[random_seq]
    
    # generate dot positions
    def generate_dot_pos(self, n_dot_ = None):
        if n_dot_ == None:
            n_dot_ = self.n_dot
        
        dot_pos_x = np.random.uniform(self.xy_range[0], self.xy_range[1], (n_dot_, 1))
        dot_pos_y = np.random.uniform(self.xy_range[2], self.xy_range[3], (n_dot_, 1))
        dot_pos = np.append(dot_pos_x, dot_pos_y, axis = 1)
        return dot_pos
        
    def generate_stim_lum(self, i_coh, i_speed):
        coh = self.cohs[i_coh]
        speed = self.speeds[i_speed]
        ori_arr, ori = self.get_ori(self.n_dot, coh)
        dot_pos = self.generate_dot_pos()
        dot_lifetime = np.zeros(self.n_dot)
        
        frames = np.tile(self.vmean, self.stim_shape)
        frames = self.gray2RGB(frames)
        
        patch = self.circle(self.x_stim, self.y_stim, self.patch_size_pix, 0, 0)
        
        i_random_ori = np.where((ori_arr != ori), True, False)
        
        for i_frame in range(self.n_frame):
            for i_dot, pos in enumerate(dot_pos):
                dot_area = self.circle(self.x_stim, self.y_stim, self.dot_size_pix, pos[0], pos[1])
                frames[i_frame, dot_area] = self.vmax
            
            frames[i_frame, ~patch] = self.background_color
            
            self.move(dot_pos, speed, ori_arr)
            
            dot_lifetime = dot_lifetime + 1
            timeout = np.where(dot_lifetime >= self.lifetime_frame, True, False)
            x_frameout = np.where(
                (dot_pos[:, 0] <= self.xy_range[0]) | (dot_pos[:, 0] >= self.xy_range[1]),
                True, False)
            y_frameout = np.where(
                (dot_pos[:, 1] <= self.xy_range[2]) | (dot_pos[:, 1] >= self.xy_range[3]),
                True, False)
            
            reset = timeout | x_frameout | y_frameout | i_random_ori
            n_reset = len(dot_lifetime[reset])
            
            if n_reset != 0:
                dot_pos[reset] = self.generate_dot_pos(n_dot_ = n_reset)
                dot_lifetime[reset] = np.zeros(n_reset)
        
        return frames
     
    def generate_stim_cont(self, i_coh, i_speed):
         coh = self.cohs[i_coh]
         speed = self.speeds[i_speed]
         ori_arr, ori = self.get_ori(self.n_dot, coh)
         dot_pos = self.generate_dot_pos()
         dot_lifetime = np.zeros(self.n_dot)
         
         cont_vmin, cont_vmax = self.contrast2vRange(self.stim_cont)
         cont_band = cont_vmax - cont_vmin
         
         LowPath = self.circle(self.x_stim, self.y_stim, 100, 0, 0)
         
         frames = np.random.uniform(self.noise_dark, self.noise_bright, self.stim_shape[:-1])
         F_frames = np.fft.fft2(frames)
         F_frames = np.fft.fftshift(F_frames)
         F_frames[:, ~LowPath] = 0
         F_frames = np.fft.ifftshift(F_frames)
         frames = np.fft.ifft2(F_frames).real
         frames = np.reshape(frames, frames.shape + (1,))
         frames = self.gray2RGB(frames)
         
         patch = self.circle(self.x_stim, self.y_stim, self.patch_size_pix, 0, 0)
         
         i_random_ori = np.where((ori_arr != ori), True, False)
         
         for i_frame in range(self.n_frame):
             for i_dot, pos in enumerate(dot_pos):
                 dot_area = self.circle(self.x_stim, self.y_stim, self.dot_size_pix, pos[0], pos[1])
                 vmin_dot = np.min(frames[i_frame][dot_area])
                 vmax_dot = np.max(frames[i_frame][dot_area])
                 frames[i_frame][dot_area] = (frames[i_frame][dot_area] - vmin_dot) / (vmax_dot - vmin_dot)                 
             
             frames[i_frame, ~patch] = self.background_color
             
             self.move(dot_pos, speed, ori_arr)
             
             dot_lifetime = dot_lifetime + 1
             timeout = np.where(dot_lifetime >= self.lifetime_frame, True, False)
             x_frameout = np.where(
                 (dot_pos[:, 0] <= self.xy_range[0]) | (dot_pos[:, 0] >= self.xy_range[1]),
                 True, False)
             y_frameout = np.where(
                 (dot_pos[:, 1] <= self.xy_range[2]) | (dot_pos[:, 1] >= self.xy_range[3]),
                 True, False)
             
             reset = timeout | x_frameout | y_frameout | i_random_ori
             n_reset = len(dot_lifetime[reset])
             
             if n_reset != 0:
                 dot_pos[reset] = self.generate_dot_pos(n_dot_ = n_reset)
                 dot_lifetime[reset] = np.zeros(n_reset)
         
         return frames