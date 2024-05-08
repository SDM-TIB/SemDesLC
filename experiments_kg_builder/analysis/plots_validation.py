import matplotlib as mpl
import matplotlib.pyplot as plt
import scienceplots
from numpy import genfromtxt
import os
from statistics import mean
from statistics import stdev as std

plt.style.use(['science', 'ieee', 'high-contrast'])

mpl.rcParams['xtick.top'] = False
mpl.rcParams['xtick.major.size'] = 0
mpl.rcParams['xtick.minor.size'] = 0
mpl.rcParams['ytick.right'] = False

BASE_PATH = '/results/'
RES_PATH = os.path.join(BASE_PATH, 'validation')
PLOT_PATH = os.path.join(BASE_PATH, 'plots')

approaches = ['SHACL2SPARQL', 'shaclex', 'Trav-SHACL']


def stdev(data):
    if len(data) < 2:
        return 0.0
    else:
        return std(data)


def get_data(filename):
    res = genfromtxt(os.path.join(RES_PATH, filename), dtype=None, encoding='utf8', ndmin=1)
    res = [r/1000.0 for r in res]  # convert ms to s
    res_mean = mean(res)
    res_stdev = stdev(res)
    return res_mean, res_stdev


if not os.path.exists(PLOT_PATH):
    os.makedirs(PLOT_PATH)


s2s_mean, s2s_stdev = get_data('SHACL2SPARQL.csv')
shaclex_mean, shaclex_stdev = get_data('shaclex.csv')
trav_mean, trav_stdev = get_data('Trav-SHACL.csv')

fig, ax = plt.subplots()
plt.bar(0, s2s_mean, label='SHACL2SPARQL', yerr=s2s_stdev)
plt.bar(1, shaclex_mean, label='shaclex', yerr=shaclex_stdev)
plt.bar(2, trav_mean, label='Trav-SHACL', yerr=trav_stdev)
plt.xticks(range(0, len(approaches)), approaches)
ax.set_xlabel('Validation Engine')
ax.set_ylabel('Validation Time [s]')
ax.set_yscale('log')
fig.savefig(os.path.join(PLOT_PATH, 'evaluation_validation.png'))
plt.close(fig)
