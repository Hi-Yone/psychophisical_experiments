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
# filename = '202307061953_HY'
filename = '202401092302_HY_rep5'
df = pd.read_csv(pattern + filename + extention)
print(filename)

def gauss(x, mu, sigma):
    y = norm.cdf(x, loc=mu, scale=sigma)
    return y

def R_square(y, f, y_bar):
    y_bar = np.mean(y)
    SSres = np.sum((y - f)**2)
    SStot = np.sum((y - y_bar)**2)
    R2 = 1-(SSres/SStot)
    return R2

#%%
# relative_rr = [0.609, 0.71, 0.829, 0.915, 1, 1.083, 1.169, 1.39, 1.51]
relative_rr = TestDisk_radius_arr = [0.569, 0.727, 0.825, 1, 1.169, 1.340, 1.530]
for rr in relative_rr:
    print(rr*3)

#%%
RefDisk_radius = 3                                 # 相関ありパッチの半径 [deg]
disparity_arr = [-0.3, 0, 0.3]        # 刺激の視差リスト
# TestDisk_radius_arr = [0.461, 0.569, 0.727, 0.825, 1, 1.169, 1.340, 1.530, 1.741] * RefDisk_radius
TestDisk_radius_arr = [1.707, 2.181, 2.475, 3, 3.507, 4.0200000000000005, 4.59]

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
print(selection_prop[0])
print(selection_prop[1])
print(selection_prop[2])

plt.figure(figsize=(10, 7))
xx = np.linspace(np.min(TestDisk_radius_arr), np.max(TestDisk_radius_arr), 100)

y_fit_param_list = []
PSE_shift = []

fitting_N = 1
mu = np.random.uniform(2.7,3.2,fitting_N)
sigma = np.random.uniform(0,4,fitting_N)
for ll in range(N_disparity):
    goodnessfit_best = -9999
    param_best = 0
    fit_ii=0
    while fit_ii < fitting_N:
        # fitting
        init_param = [mu[fit_ii], sigma[fit_ii]]
        fit_param, cov = curve_fit(gauss, TestDisk_radius_arr, selection_prop[ll], p0=init_param, maxfev=12000)
        y_fit = gauss(TestDisk_radius_arr, fit_param[0], fit_param[1])

        # goodness fit
        avg_y = np.mean(y_fit)
        goodnessfit = R_square(selection_prop[ll], y_fit, avg_y)

        # save best fit
        if goodnessfit > goodnessfit_best:
            goodnessfit_best = goodnessfit
            param_best = fit_param
            PSE = fit_param[0]
        fit_ii+=1
    print(goodnessfit_best)
    y_fit_param_list.append(fit_param)
    PSE_shift.append(PSE)

y_fit_0 = gauss(xx, y_fit_param_list[0][0], y_fit_param_list[0][1])
y_fit_1 = gauss(xx, y_fit_param_list[1][0], y_fit_param_list[1][1])
y_fit_2 = gauss(xx, y_fit_param_list[2][0], y_fit_param_list[2][1])

plt.scatter(TestDisk_radius_arr, selection_prop[0], color='red', marker='^', s=100)
plt.plot(xx, y_fit_0, color='red', linestyle='dashed', label=' - 0.3°',linewidth=3)
plt.scatter(TestDisk_radius_arr, selection_prop[1], color='black', s=100)
plt.plot(xx, y_fit_1, color='black', label='0°',linewidth=3)
plt.scatter(TestDisk_radius_arr, selection_prop[2], color='blue',marker='^', s=100)
plt.plot(xx, y_fit_2, color='blue', linestyle='dotted', label='0.3°',linewidth=3)

plt.plot([np.min(TestDisk_radius_arr), np.max(TestDisk_radius_arr)], [0.5, 0.5], color='black', linestyle='dashdot')
# plt.title('Subject : HY', fontsize=32)
plt.xlabel('relative area of Test disk', fontsize=36)
plt.ylabel('proportion of \n"Test disk" choice', fontsize=36)
# plt.xticks(TestDisk_radius_arr, relative_rr, fontsize=18)

plt.xticks(np.array([0.6, 0.8, 1., 1.2, 1.4, 1.6])*3, [0.6, 0.8, 1., 1.2, 1.4, 1.6], fontsize=18)
plt.yticks([0, 0.25, 0.5, 0.75, 1.0], fontsize=20)
plt.legend(fontsize=22)
# plt.grid()

# plt.savefig('./fitting/curve_fit/{}.jpg'.format(filename))
# %%
def linear(xx, a, b):
    yy = a*xx + b
    return yy

D = 53  # 視距離[cm]
I = 6.5 # 眼間距離[cm]
stimDiam = 6 # 刺激の大きさ[deg]
S = D*np.tan(stimDiam*np.pi/180) # 視距離53cm，刺激の大きさ6°のときの刺激の大きさ[cm]

disparity = np.array([-0.3, 0, 0.3]) # 両眼視差
xx = np.linspace(-0.3, 0.31, 30)

theta = np.arctan(I/2 / D) * 180/np.pi  # 視距離53cm，眼間距離6.25cm，両眼視差0°の時の対象までの視角

dist = np.zeros(len(disparity))
angle = np.zeros(len(disparity))
for ii in range(len(disparity)):
    dist[ii] = I/2 / np.tan((theta-disparity[ii])*np.pi/180)
    angle[ii] = np.arctan(S/dist[ii]) * 180/np.pi

measuredAngle = np.array(PSE_shift)*2
print(measuredAngle/3)

# fitting
init_param = [-1, 1]
fit_param, cov = curve_fit(linear, disparity, measuredAngle, p0=init_param)
y_fit = linear(xx, fit_param[0], fit_param[1])

plt.figure(figsize=(10,8))
# plt.plot(disparity, dist)
# plt.plot(disparity, angle, color='blue', label='geometrical', linewidth=2)
# plt.scatter(disparity, angle, color='blue')

plt.plot(xx, y_fit, label='fitted', linewidth=4)
# plt.plot(disparity, measuredAngle, color='red', label='mesured', linewidth=4)
plt.scatter(disparity, measuredAngle, s=120)

# plt.title('PSE shift subject:HY', fontsize=32)
plt.xlabel('disparity', fontsize=36); plt.ylabel('PSE', fontsize=36)
yaxis_angle = np.arange(0.6, 1.61, 0.2)*6
plt.xticks(disparity, fontsize=24); plt.yticks(yaxis_angle, np.round(yaxis_angle/6, 2), fontsize=24)
plt.ylim(0.6*6, 1.4*6)
plt.grid()
# plt.legend(fontsize=24)

# plt.savefig('./fitting/PSE/PSE_shift_{}.jpg'.format(filename))
# %%
# bootstrap法の適用 
import numpy as np
import matplotlib.pyplot as plt

# サンプルデータの生成（適切なデータに置き換える必要があります）
np.random.seed(42)
data = np.random.normal(loc=5, scale=2, size=100)

# ブートストラップ法による信頼区間の計算
def bootstrap(data, num_samples=1000, alpha=0.95):
    bootstrap_samples = []
    for _ in range(num_samples):
        bootstrap_sample = np.random.choice(data, size=len(data), replace=True)
        bootstrap_samples.append(np.mean(bootstrap_sample))  # ここでは平均を取る例ですが、適切な統計量に変更してください。
    
    lower_bound = np.percentile(bootstrap_samples, (1 - alpha) / 2 * 100)
    upper_bound = np.percentile(bootstrap_samples, (1 + alpha) / 2 * 100)
    return lower_bound, upper_bound

# ブートストラップ法を適用して信頼区間を計算
lower, upper = bootstrap(data)

# 結果の表示
print(f"ブートストラップ法による信頼区間 ({100*(1-0.95)}%): ({lower:.2f}, {upper:.2f})")

# データの可視化
plt.hist(data, bins=20, alpha=0.7, label='実データ')
plt.axvline(lower, color='red', linestyle='dashed', linewidth=2, label='ブートストラップ信頼区間 (下限)')
plt.axvline(upper, color='red', linestyle='dashed', linewidth=2, label='ブートストラップ信頼区間 (上限)')
plt.legend()
plt.show()