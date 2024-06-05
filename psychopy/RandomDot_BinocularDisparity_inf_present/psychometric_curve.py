#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import norm
from decimal import Decimal

pattern = './data/'
extention = '.csv'
# filename = glob.glob(pattern+participant+extention)[0]
filename = '202306281836_HY'
df = pd.read_csv(pattern + filename + extention)
print(filename)

def gauss(x, mu, sigma):
    y = norm.cdf(x, loc=mu, scale=sigma)
    return y

def R_square(y, f, y_bar):
    SSres = 0; SStot = 0
    for ii in range(len(y)):
        SSres += (y[ii] - f[ii])**2
        SStot += (y[ii] - y_bar)**2
    R2 = 1 - (SSres / SStot)
    return R2
#%%
RefDisk_radius = 3                                 # 相関ありパッチの半径 [deg]
disparity_arr = [-0.6, -0.3, 0, 0.2999999999999999, 0.6]        # 刺激の視差リスト
TestDisk_radius_arr = [1.827, 2.13, 2.487, 2.745, 3, 3.249, 3.507, 4.17, 4.53]

N_repeat = 5
N_LorR = 2
N_disparity = len(disparity_arr)
N_radius = len(TestDisk_radius_arr)

selected_cnt = np.zeros((N_disparity, N_radius))

df2 = df.sort_values(['disparity_test', 'TestDisk_radius'])
key = (df['TestPos_LorR'] == df['key'])

for ii in range(N_disparity):
    for jj in range(N_radius):
        extracted_df = df2.loc[
            (df2['disparity_test']==disparity_arr[ii])
              & (df2['TestDisk_radius']==TestDisk_radius_arr[jj])
        ]
        key = extracted_df['TestPos_LorR'] == extracted_df['key']
        selected_cnt[ii, jj] = sum(key)
        
selection_prop = selected_cnt/(N_repeat*N_LorR)
print(selection_prop)

plt.figure(figsize=(15, 10))
xx = np.linspace(np.min(TestDisk_radius_arr), np.max(TestDisk_radius_arr), 100)
y_fit_list = []
for ll in range(N_disparity):
    goodnessfit_best = -9999
    y_fit_best = 0
    mu_best = 0
    for mu in np.arange(2.0, 4.1, 0.1):
        # fitting
        init_param = [mu, 1]
        fit_param, cov = curve_fit(gauss, TestDisk_radius_arr, selection_prop[ll], p0=init_param, maxfev=29000)
        y_fit = gauss(xx, fit_param[0], fit_param[1])

        # goodness fit
        avg_y = np.mean(y_fit)
        goodnessfit = R_square(selection_prop[ll], y_fit, avg_y)

        # save best fit
        if goodnessfit >= goodnessfit_best:
            goodnessfit_best = goodnessfit
            y_fit_best = y_fit
            mu_best = mu
    print(mu_best, goodnessfit_best)
    y_fit_list.append(y_fit_best)

plt.scatter(TestDisk_radius_arr, selection_prop[0], color='red')
plt.plot(xx, y_fit_list[0], color='red', linestyle='--', label='-0.6°')
# plt.scatter(TestDisk_radius_arr, selection_prop[1])
# plt.plot(xx, y_fit_list[1], color='red', linestyle='--', label='-0.3°')
plt.scatter(TestDisk_radius_arr, selection_prop[2], color='black')
plt.plot(xx, y_fit_list[2], color='black', label='0°')
# plt.scatter(TestDisk_radius_arr, selection_prop[3])
# plt.plot(xx, y_fit_list[3], color='blue', linestyle='--', label='0.3°')
plt.scatter(TestDisk_radius_arr, selection_prop[4], color='blue')
plt.plot(xx, y_fit_list[4], color='blue', linestyle='--', label='0.6°')
plt.title('Subject : HY')
plt.xlabel('Relative area of cyclopean Test disk')
plt.ylabel('Proportion of \n"Test disk" choice')
plt.xticks(TestDisk_radius_arr, TestDisk_radius_arr)
plt.legend()
plt.grid()

plt.savefig('./fitting/curve_fit/{}.png'.format(filename))
# %%
def linear(xx, a, b):
    yy = a*xx + b
    return yy

D = 53  # 視距離[cm]
I = 6.5 # 眼間距離[cm]
stimDiam = 6 # 刺激の大きさ[deg]
S = D*np.tan(stimDiam*np.pi/180) # 視距離53cm，刺激の大きさ6°のときの刺激の大きさ[cm]

ctr=len(y_fit_list[0])//2
PSE_shift  = [y_fit_list[0][ctr], y_fit_list[1][ctr], y_fit_list[2][ctr], y_fit_list[3][ctr], y_fit_list[4][ctr]]
# disparity = np.arange(-0.3, 0.31, 0.15) # 両眼視差
disparity = np.arange(-1.2, 1.21, 0.3) # 両眼視差
xx = np.linspace(-0.3, 0.31, 30)

theta = np.arctan(I/2 / D) * 180/np.pi  # 視距離53cm，眼間距離6.25cm，両眼視差0°の時の対象までの視角

dist = np.zeros(len(disparity))
angle = np.zeros(len(disparity))
for ii in range(len(disparity)):
    dist[ii] = I/2 / np.tan((theta-disparity[ii])*np.pi/180)
    if ii != 0:
        print(np.round(dist[ii] - dist[ii-1], 2))
    angle[ii] = np.arctan(S/dist[ii]) * 180/np.pi

measuredAngle = np.array(PSE_shift)*6
# fitting
init_param = [1, 1]
fit_param, cov = curve_fit(linear, disparity, measuredAngle, p0=init_param)
y_fit = linear(xx, fit_param[0], fit_param[1])

plt.figure(figsize=(10, 10))
# plt.plot(disparity, dist)
plt.plot(disparity, angle, color='blue', label='geometrical')
plt.scatter(disparity, angle, color='blue')

plt.plot(xx, y_fit, 'red', label='fitted')
plt.scatter(disparity, measuredAngle, color='red')

plt.title('PSE shift subject:HY')
plt.xlabel('disparity'); plt.ylabel('angle')
yaxis_angle = np.arange(0.6, 1.61, 0.2)*6
plt.xticks(disparity); plt.yticks(yaxis_angle, np.round(yaxis_angle/6, 2))
plt.ylim(0.4*6, 1.6*6)
plt.grid()
plt.legend()

plt.savefig('./fitting/PSE/PSE_shift_{}.png'.format(filename))

# %%
y_fit_list[4][50]
# %%
