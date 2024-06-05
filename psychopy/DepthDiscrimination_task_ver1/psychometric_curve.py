#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import norm
from decimal import Decimal

from stim import StimParameters as stprm

pattern = './data/'
extention = '.csv'
filename = '202406051749_'
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
for rr in stprm.disparity_arr:
    print(rr*3)

#%%
disparity_arr = stprm.disparity_arr        # 刺激の視差リスト

N_repeat = 20
N_LorR = 2
N_disparity = len(disparity_arr)

selected_cnt = np.zeros(N_disparity)

df2 = df.sort_values(['disparity_test'])
key = (df['TestPos_LorR'] == df['key'])

for ii in range(N_disparity):
    extracted_df = df2.loc[
        (df2['disparity_test']==disparity_arr[ii])
    ]
    key = extracted_df['TestPos_LorR'] == extracted_df['key']
    selected_cnt[ii] = sum(key)
        
selection_prop = selected_cnt/(N_repeat*N_LorR)
print(selection_prop)

plt.figure(figsize=(15, 10))
xx = np.linspace(np.min(disparity_arr), np.max(disparity_arr), 100)

y_fit_param_list = []
PSE_shift = []

fitting_N = 10
mu = np.random.uniform(-1,1,fitting_N)
sigma = np.random.uniform(0,3,fitting_N)
for ll in range(N_disparity):
    goodnessfit_best = -9999
    param_best = 0
    fit_ii=0
    while fit_ii < fitting_N:
        # fitting
        init_param = [mu[fit_ii], sigma[fit_ii]]
        fit_param, cov = curve_fit(gauss, disparity_arr, selection_prop, p0=init_param, maxfev=36000)
        y_fit = gauss(disparity_arr, fit_param[0], fit_param[1])

        # goodness fit
        avg_y = np.mean(y_fit)
        goodnessfit = R_square(selection_prop, y_fit, avg_y)

        # save best fit
        if goodnessfit > goodnessfit_best:
            goodnessfit_best = goodnessfit
            param_best = fit_param
            PSE = fit_param[0]
        fit_ii+=1
    print(goodnessfit_best)
    y_fit_param_list.append(fit_param)

y_fit = gauss(xx, y_fit_param_list[0][0], y_fit_param_list[0][1])

plt.scatter(disparity_arr, selection_prop, color='red', marker='^', s=100)
plt.plot(xx, y_fit, color='red', linestyle='dashed', linewidth=3)

plt.plot([np.min(disparity_arr), np.max(disparity_arr)], [0.5, 0.5], color='black', linestyle='dashdot')
plt.title('Subject : HY', fontsize=32)
plt.xlabel('Disparity', fontsize=32)
plt.ylabel('Proportion of \n"Test disk" choice', fontsize=32)
plt.xticks(fontsize=16)
plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], fontsize=16)
# plt.legend(fontsize=22)
# plt.grid()

# plt.savefig('./fitting/curve_fit/{}.png'.format(filename))
# %%
