import matplotlib as mpl
import matplotlib.pyplot as plt
import scienceplots
import pandas as pd
import numpy as np
import os
from statistics import mean
from statistics import stdev as std

plt.style.use(['science', 'ieee', 'high-contrast'])

mpl.rcParams['xtick.top'] = False
mpl.rcParams['xtick.major.size'] = 0
mpl.rcParams['xtick.minor.size'] = 0
mpl.rcParams['ytick.right'] = False
mpl.rcParams['figure.figsize'] = (6.6, 2.5)

BASE_PATH = '/results/'
RES_PATH = os.path.join(BASE_PATH, 'querying')
PLOT_PATH = os.path.join(BASE_PATH, 'plots')

approaches = ['ANAPSID', 'DeTrusty', 'FedX']


def stdev(data):
    if len(data) < 2:
        return 0.0
    else:
        return std(data)


def get_data(filename):
    # res = genfromtxt(os.path.join(RES_PATH, filename), dtype=None, encoding='utf8', ndmin=1)
    res = pd.read_csv(os.path.join(RES_PATH, filename), dtype=None, header=None)
    res = res.dropna(subset=[1, 2])
    if 'fedx' in filename:
        res[1] = res[1].apply(lambda x: x/1000.0)
    return res


def stats(df, query):
    query_data = df[df[0] == query][1].to_list()
    if len(query_data) > 0:
        res_mean = mean(query_data)
        res_stdev = stdev(query_data)
        return res_mean, res_stdev
    else:
        return 0.0, 0.0


def get_measurement(df_anapsid, df_detrusty, df_fedx, query):
    anapsid_mean, anapsid_stdev = stats(df_anapsid, query)
    detrusty_mean, detrusty_stdev = stats(df_detrusty, query)
    fedx_mean, fedx_stdev = stats(df_fedx, query)
    return (anapsid_mean, detrusty_mean, fedx_mean), (anapsid_stdev, detrusty_stdev, fedx_stdev)


def approach_stats(df):
    means = []
    stdevs = []
    for query in queries:
        mean, stdev = stats(df, query)
        means.append(mean)
        stdevs.append(stdev)
    return means, stdevs


if not os.path.exists(PLOT_PATH):
    os.makedirs(PLOT_PATH)


anapsid = get_data('anapsid.csv')
detrusty = get_data('detrusty.csv')
fedx = get_data('fedx.csv')

queries = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10']
x = np.arange(len(queries))
width = 0.25
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

# for query in queries:
#     offset = width * multiplier
#     pos = x + offset
#     print(pos)
#     means, stdevs = get_measurement(anapsid, detrusty, fedx, query)
#     rects = ax.bar(pos, means, width, label=query)
#     # ax.bar_label(rects, padding=3)
#     multiplier += 1

for approach in approaches:
    offset = width * multiplier
    pos = x + offset
    if approach == 'ANAPSID':
        means, stdevs = approach_stats(anapsid)
    elif approach == 'DeTrusty':
        means, stdevs = approach_stats(detrusty)
    else:
        means, stdevs = approach_stats(fedx)
    rects = ax.bar(pos, means, width, label=approach, yerr=stdevs)
    multiplier += 1



#plt.bar(0, anapsid_mean, label='ANAPSID', yerr=anapsid_stdev)
#plt.bar(1, detrusty_mean, label='DeTrusty', yerr=detrusty_stdev)
#plt.bar(2, fedx_mean, label='FedX', yerr=fedx_stdev)
ax.set_xticks(x + width, queries)
ax.set_xlabel('Query')
ax.set_ylabel('Execution Time [s]')
ax.set_yscale('log')
ax.legend(loc='upper right', ncols=1)
fig.savefig(os.path.join(PLOT_PATH, 'evaluation_querying.png'))
plt.close(fig)
