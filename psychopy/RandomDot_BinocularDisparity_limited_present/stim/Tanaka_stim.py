import numpy as np
class stim_generator:
    """
    ### manual ###

    """
    def __init__(
            self,
            framerate,
            moniSize_pix,
            moniSize_cm,
            eyeOffset_cm,
            background_color):
        
        self.framerate = int(framerate)
        self.moniSize_pix = moniSize_pix
        self.moniSize_cm = moniSize_cm
        self.ratio_cm2pix = moniSize_pix[0] / moniSize_cm

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
        d_cm = self.deg2rad(d_deg)
        d_pix = self.ratio_cm2pix * d_cm
        return int(round(d_pix))
    
    def cm2deg(self, d_cm):
        d_rad = 2*np.arctan(d_cm/(2*self.eyeOffset_cm))
        d_deg = np.degrees(d_rad)
        return d_deg

    def circlePatch(self, Ndots, circle_radius):
        xy_arr = []
        out_of_range_cnt = Ndots                                                    # 円範囲外の判定用
        while out_of_range_cnt != 0:                                                # 相関ありパッチ内に指定したドット数が全て入るまでループ
            x = np.random.uniform(-circle_radius, circle_radius, out_of_range_cnt)  # ドット生成
            y = np.random.uniform(-circle_radius, circle_radius, out_of_range_cnt)  # ドット生成
            xy = np.column_stack((x, y))                                            # Nx2 arrayの生成

            select_range = np.sqrt(np.sum((xy)**2, axis=1)) < circle_radius         # 円の半径内かを判定 True/False
            out_of_range_cnt = len(np.where(select_range == False)[0])              # 範囲外の数をカウント

            xy_arr.append(xy[select_range])                                         # パッチ範囲内の座標を追加
            
        circle_xy = xy_arr[0]
        for ii in range(1, len(xy_arr)):
            circle_xy = np.concatenate([circle_xy, xy_arr[ii]])                     # 縦に結合
        return circle_xy

    def RefTestDisk(self, 
                     Ndots_ref, Ndots_test, 
                     circle_radius_ref, circle_radius_test, 
                     patch_cntrPos, disparity, 
                     RefTest_dist, TestDiskPosLorR):
        
        pos_ref = self.circlePatch(Ndots_ref, circle_radius_ref)                    # reference刺激の作成
        Leye_ref = np.copy(pos_ref)
        Leye_ref += -patch_cntrPos + RefTest_dist/2*TestDiskPosLorR[0]              # 左目
        Reye_ref = np.copy(pos_ref)
        Reye_ref += patch_cntrPos + RefTest_dist/2*TestDiskPosLorR[0]               # 右目

        pos_test = self.circlePatch(Ndots_test, circle_radius_test)                 # test刺激の作成
        Leye_test = np.copy(pos_test)
        Leye_test += -patch_cntrPos + RefTest_dist/2*TestDiskPosLorR[1]             # 左目
        Leye_test[:, 0] -= disparity/2                                              # 視差を与える
        Reye_test = np.copy(pos_test)
        Reye_test += patch_cntrPos + RefTest_dist/2*TestDiskPosLorR[1]              # 右目
        Reye_test[:, 0] += disparity/2                                              # 視差を与える

        Leye_RefTest = np.concatenate([Leye_ref, Leye_test])
        Reye_RefTest = np.concatenate([Reye_ref, Reye_test])
        
        # ここでconcatenateせずに，別々の戻り値とし，mainの方で別々に設定する
        # binocular_RefTest = np.concatenate([Leye_RefTest, Reye_RefTest])
        # return binocular_RefTest
        return Leye_RefTest, Reye_RefTest

    def monoPatch(self, Ndots, patch_range, circle_radius_ref, circle_radius_test, RefTest, TestDiskPosLorR, disparity, eye):
        xy_arr = []
        out_of_range_cnt = Ndots
        while out_of_range_cnt != 0:
            x = np.random.uniform(-patch_range, patch_range, out_of_range_cnt)
            y = np.random.uniform(-patch_range, patch_range, out_of_range_cnt)
            xy = np.column_stack((x, y))
            disparity_xy = np.array([disparity/2, 0])

            select_range_ref = np.sqrt(np.sum((xy - RefTest/2*TestDiskPosLorR[0])**2, axis=1)) > circle_radius_ref
            if eye == "Leye":
                select_range_test = np.sqrt(np.sum((xy - RefTest/2*TestDiskPosLorR[1] + disparity_xy)**2, axis=1)) > circle_radius_test
            if eye == "Reye":
                select_range_test = np.sqrt(np.sum((xy - RefTest/2*TestDiskPosLorR[1] - disparity_xy)**2, axis=1)) > circle_radius_test

            out_of_range_cnt = len(np.where(select_range_ref == False)[0]) + len(np.where(select_range_test == False)[0])

            xy_arr.append(xy[select_range_ref & select_range_test])

        surround_xy = xy_arr[0]
        for ii in range(1, len(xy_arr)):
            surround_xy = np.concatenate([surround_xy, xy_arr[ii]])     # 縦に結合
        return surround_xy

    def surroundPatch(self, Ndots, patch_range, circle_radius_ref, circle_radius_test, patch_centerPos, RefTest, TestDiskPosLorR, disparity):
        Leye_uncorr = self.monoPatch(Ndots, patch_range, circle_radius_ref, circle_radius_test, RefTest, TestDiskPosLorR, disparity, "Leye")
        Leye_uncorr -= patch_centerPos

        Reye_uncorr = self.monoPatch(Ndots, patch_range, circle_radius_ref, circle_radius_test, RefTest, TestDiskPosLorR, disparity, "Reye")
        Reye_uncorr += patch_centerPos

        monocular_patch = np.concatenate([Leye_uncorr, Reye_uncorr])
        return monocular_patch
    
    # 確認用
    # def surroundPatch(self, Ndots, patch_range, circle_radius_ref, circle_radius_test, patch_centerPos, RefTest, TestDiskPosLorR):
    #     uncorr = self.monoPatch(Ndots, patch_range, circle_radius_ref, circle_radius_test, RefTest, TestDiskPosLorR)
    #     Leye_uncorr = np.copy(uncorr) - patch_centerPos
    #     Reye_uncorr = np.copy(uncorr) + patch_centerPos

    #     monocular_patch = np.concatenate([Leye_uncorr, Reye_uncorr])
    #     return monocular_patch
    
    def calc_Ndots(self, circle_radius_ref, circle_radius_test, patch_range, elemSize, dotsDensity):
        corrPatch_Ndots_ref_arr = []
        corrPatch_Ndots_test_arr = []
        uncorrPatch_Ndots_arr = []
        for ii in range(len(circle_radius_test)):
            circleArea_ref = circle_radius_ref**2 * np.pi
            circleArea_test = circle_radius_test[ii]**2 * np.pi
            patchArea = (2*patch_range)**2 - (circleArea_ref + circleArea_test)
            elemArea = (elemSize/2)**2 * np.pi

            corrPatch_Ndots_ref = int(circleArea_ref*(dotsDensity/100)/elemArea)
            corrPatch_Ndots_test = int(circleArea_test*(dotsDensity/100)/elemArea)
            uncorrPatch_Ndots = int(patchArea*(dotsDensity/100)/elemArea)

            corrPatch_Ndots_ref_arr.append(corrPatch_Ndots_ref)
            corrPatch_Ndots_test_arr.append(corrPatch_Ndots_test)
            uncorrPatch_Ndots_arr.append(uncorrPatch_Ndots)

        return corrPatch_Ndots_ref_arr, corrPatch_Ndots_test_arr, uncorrPatch_Ndots_arr