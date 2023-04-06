import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import curve_fit
import pandas as pd


def f(x, mu, sigma):
    return norm.cdf(x, loc = mu, scale = sigma)
    

def get_thre(x, data, PSE, point):
    def detect_point(x, data, thre):
        prev_data = np.append(data[0], data[0 : len(data) - 1])
        return x[np.where((data >= thre) & (prev_data < thre))]
    
    point *= 0.01
    data_84per = detect_point(x, data, point)[0]
    
    return data_84per - PSE

col_name = 'key_resp.keys'
path = "data/"
filenames = ['demo_4.csv']
filenames = [path+filename for filename in filenames]
resp_mean = [[] for _ in filenames]

for i, filename in enumerate(filenames):
    df = pd.read_csv(filename)
    df = df[['coherence', col_name]]
    df = df.replace(['right', 'left'], [1, 0])
    
    for _, g in df.groupby('coherence'):
        resp_mean[i].append(np.mean(g[col_name]))
    
coh = np.array(list(df.groupby('coherence').groups))
resp_mean = np.mean(resp_mean, axis = 0)

param, cov = curve_fit(f, coh, resp_mean, p0=[0, 1])
mu = param[0]
sigma = param[1]

sampling = 1000
Nx = int((np.max(coh) - np.min(coh)) * sampling)
x = np.linspace(np.min(coh), np.max(coh), Nx)
y = f(x, mu, sigma)

PSE = mu
# thre = get_thre(x, y, PSE, 84)
print("PSE : {:.3f}".format(PSE))
# print("threshold : {:.3f}".format(thre))

plt.close('all')
plt.figure(figsize = (7, 5))
plt.rc('legend', fontsize = 16)
plt.scatter(coh, resp_mean, color = 'm', marker = '*', label = 'Empirical')
plt.plot(x, y, 'b-', label = 'Predicted')
plt.xticks(np.append(coh, 0))
plt.yticks([0, 0.25, 0.5, 0.75, 1.0])
plt.hlines(0.5, np.min(coh), np.max(coh), color = 'black', linestyle = 'dashed')
plt.vlines(0, 0, 1, color = 'black', linestyle = 'dashed')
plt.xlabel('Coherence')
plt.ylabel('Proportion of answering\n"dots moveed rightward"')
plt.legend()

plt.savefig('Maryu_curve.png')
plt.show()