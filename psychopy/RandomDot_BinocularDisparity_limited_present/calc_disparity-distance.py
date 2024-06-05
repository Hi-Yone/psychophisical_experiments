#%%
import numpy as np
import matplotlib.pyplot as plt

D = 53  # 視距離[cm]
I = 6.5 # 眼間距離[cm]
stimDiam = 1 # 刺激の大きさ[deg]
S = D*np.tan(stimDiam*np.pi/180) # 視距離53cm，刺激の大きさ6°のときの刺激の大きさ[cm]

disparity = np.arange(-3.0, 3.01, 0.5) # 両眼視差
# disparity = np.arange(-1.2, 1.21, 0.3) # 両眼視差

theta = np.arctan(I/2 / D) * 180/np.pi  # 視距離53cm，眼間距離6.25cm，両眼視差0°の時の対象までの視角

dist = np.zeros(len(disparity))
angle = np.zeros(len(disparity))
for ii in range(len(disparity)):
    dist[ii] = I/2 / np.tan((theta-disparity[ii])*np.pi/180)
    # if ii != 0:
        # print(np.round(dist[ii] - dist[ii-1], 2))
    angle[ii] = np.arctan(S/dist[ii]) * 180/np.pi

# print(dist)
print(np.round(disparity, 2))
print(angle)

plt.figure(figsize=(10, 10))
# plt.plot(disparity, dist)
plt.plot(disparity, angle)
plt.xlabel('Disparity [deg]', fontsize=32); plt.ylabel('Relative size [deg]', fontsize=32)
# yaxis_angle = np.arange(0.7, 1.31, 0.1)*6
# plt.xticks(disparity, fontsize=16); plt.yticks(yaxis_angle, np.round(yaxis_angle/3, 2))
plt.yticks(angle, fontsize=16)
# plt.scatter(disparity, angle, color='black')
# plt.ylim(0.4*6, 1.6*6)
plt.grid()
# %%
