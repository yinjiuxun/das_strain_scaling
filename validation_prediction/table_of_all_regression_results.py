#%% import modules
from cmath import e
import os
import pandas as pd
#from sep_util import read_file
import numpy as np
import statsmodels.formula.api as smf
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

# %matplotlib inline
params = {
    'image.interpolation': 'nearest',
    'image.cmap': 'gray',
    'savefig.dpi': 100,  # to adjust notebook inline plot size
    'axes.labelsize': 18, # fontsize for x and y labels (was 10)
    'axes.titlesize': 18,
    'font.size': 18,
    'legend.fontsize': 18,
    'xtick.labelsize': 18,
    'ytick.labelsize': 18,
    'text.usetex':False,
    'axes.facecolor': 'white',
    'savefig.facecolor': 'white',
    'pdf.fonttype': 42 # Turn off text conversion to outlines
}
#%%
# Next apply to the individual array
data_file_list = ['../data_files/peak_amplitude/peak_amplitude_Ridgecrest.csv',
                    '../data_files/peak_amplitude/peak_amplitude_LongValley_N.csv',
                    '../data_files/peak_amplitude/peak_amplitude_LongValley_S.csv',
                    '../data_files/peak_amplitude/peak_amplitude_Sanriku.csv',
                    '../data_files/peak_amplitude/peak_amplitude_multiple_arrays.csv']  

results_output_dir_list = ['../iter_results_Ridgecrest',
                            '../iter_results_LongValley_N',
                            '../iter_results_LongValley_S',
                            '../iter_results_Sanriku',
                            '../iter_results']  
    
region_list = ['Ridgecrest', 'Long-Valley N', 'Long-Valley S', 'Sanriku', 'combined']
                      
all_results_pd_weighted = pd.DataFrame(columns={'region', 
                                       'mag coef. (P)', 'dist coef. (P)', 'mag coef. uncertainty (P)', 'dist coef. uncertainty (P)',
                                       'mag coef. (S)', 'dist coef. (S)', 'mag coef. uncertainty (S)', 'dist coef. uncertainty (S)'})

#%%
def uncertainty_from_covariance(cov, key):
    return np.sqrt(cov.loc[key, key])

i_row = 0 # used to assign values

all_results_pd = pd.DataFrame(columns=['region',
                                    'mag coef. (P)', 'dist coef. (P)', 'mag coef. uncertainty (P)', 'dist coef. uncertainty (P)',
                                    'mag coef. (S)', 'dist coef. (S)', 'mag coef. uncertainty (S)', 'dist coef. uncertainty (S)'])
                                    
for ii_region, results_output_dir in enumerate(results_output_dir_list):

    if region_list[ii_region] != 'Sanriku':
        regP = sm.load(results_output_dir + "/P_regression_combined_site_terms_iter.pickle")
        regS = sm.load(results_output_dir + "/S_regression_combined_site_terms_iter.pickle")
    else:
        regS = sm.load(results_output_dir + f"/S_regression_combined_site_terms_iter.pickle")
    
    all_results_pd.at[i_row, 'region'] = region_list[ii_region]

    if region_list[ii_region] == 'Sanriku':
        all_results_pd.at[i_row, 'mag coef. (P)'] = np.nan
        all_results_pd.at[i_row, 'dist coef. (P)'] = np.nan
        all_results_pd.at[i_row, 'mag coef. uncertainty (P)'] = np.nan
        all_results_pd.at[i_row, 'dist coef. uncertainty (P)'] = np.nan
    else:
        all_results_pd.at[i_row, 'mag coef. (P)'] = regP.params['magnitude']
        all_results_pd.at[i_row, 'dist coef. (P)'] = regP.params['np.log10(distance_in_km)']
        all_results_pd.at[i_row, 'mag coef. uncertainty (P)'] = uncertainty_from_covariance(regP.cov_params(), 'magnitude')
        all_results_pd.at[i_row, 'dist coef. uncertainty (P)'] = uncertainty_from_covariance(regP.cov_params(), 'np.log10(distance_in_km)')

    all_results_pd.at[i_row, 'mag coef. (S)'] = regS.params['magnitude']
    all_results_pd.at[i_row, 'dist coef. (S)'] = regS.params['np.log10(distance_in_km)']
    all_results_pd.at[i_row, 'mag coef. uncertainty (S)'] = uncertainty_from_covariance(regS.cov_params(), 'magnitude')
    all_results_pd.at[i_row, 'dist coef. uncertainty (S)'] = uncertainty_from_covariance(regS.cov_params(), 'np.log10(distance_in_km)')

    i_row += 1

for ii_column in range(2, 9):
    all_results_pd[all_results_pd.columns[ii_column]] = pd.to_numeric(all_results_pd[all_results_pd.columns[ii_column]])

# 
all_results_pd.iloc[:, 2:] = all_results_pd.iloc[:, 2:].astype('float')

# %%
# Plot all coefficients
custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params, font_scale=1.2)


fig, ax = plt.subplots(2, 2, figsize=(12, 9))


def plot_iter_results(ax, y_key, xtick_labels):
    #ax.plot(iter_x, iter_results_pd_unweighted[y_key], 'rx', markersize=10, markeredgewidth=3, zorder=5, label='ols')
    ax.plot(iter_x, iter_results_pd_weighted[y_key], 'rx', markersize=10, markeredgewidth=3, zorder=5, label='wls')
    ax.set_xticks(range(len(xtick_labels)))
    ax.set_xticklabels(labels=xtick_labels)
    ax.legend()
    ax.grid()
    return ax

# For paper, only present Ridgecrest, Long Valley and Sanriku
iter_results_pd_weighted = all_results_pd
xtick_labels = ['RC', 'LV-N', 'LV-S', 'Sanriku', 'RC+LV']
iter_x = [0.1, 1.1, 2.1, 3.1, 4.1]

# P mag coef.
gca = ax[0, 0]
plot_iter_results(ax=gca, y_key='mag coef. (P)', xtick_labels=xtick_labels)
gca.set_ylabel('mag coef. (P)')
gca.set_ylim(0, 1)

# S mag coef.
gca = ax[0, 1]
plot_iter_results(ax=gca, y_key='mag coef. (S)', xtick_labels=xtick_labels)
gca.set_ylabel('mag coef. (S)')
gca.set_ylim(0, 1)

# P dist coef.
gca = ax[1, 0]
plot_iter_results(ax=gca, y_key='dist coef. (P)', xtick_labels=xtick_labels)
gca.set_ylabel('dist coef. (P)')
gca.set_ylim(-2, 0)

# S dist coef.
gca = ax[1, 1]
gca = plot_iter_results(ax=gca, y_key='dist coef. (S)', xtick_labels=xtick_labels)
gca.set_ylabel('dist coef. (S)')
gca.set_ylim(-2, 0)

# Adding the Barbour et al. (2021) results
# TODO: label the line with the values
barbour_2021_coefficents = [0.92, -1.45]
PGA_coefficients_OLS = [0.583631, -1.793554]
PGA_coefficients_WLS = [0.388142, -1.630351]

for ii in range(2):
    for jj in range(2):
        if (ii == 1) and (jj == 1):
            label_text1 = 'PGA from NGA-West2 (OLS)'
            label_text2 = 'PGA from NGA-West2 (WLS)'
            label_text3 = 'Strainmeter Barbour et al. (2021)'
        else:
            label_text1, label_text2, label_text3 = None, None, None

        #ax[ii, jj].hlines(y=PGA_coefficients_OLS[ii], xmin=0, xmax=5, linestyle='--', color='r', linewidth=2, label=label_text1)
        ax[ii, jj].hlines(y=PGA_coefficients_WLS[ii], xmin=0, xmax=5, linestyle='--', color='b', linewidth=2, label=label_text2)
        ax[ii, jj].hlines(y=barbour_2021_coefficents[ii], xmin=0, xmax=5, linestyle='--', color='orange', linewidth=2, label=label_text3)
        
ax[0, 0].get_legend().remove()
ax[0, 1].get_legend().remove()
ax[1, 0].get_legend().remove()

my_label = ['Peak DAS strain rate (WLS)', 'PGA from NGA-West2 (WLS)', 'Strainmeter Barbour et al. (2021)'] #

L = ax[1, 1].legend(loc='center left', bbox_to_anchor=(-1.4, 2.4), ncol=3, title='Regression Coefficients')
for i_L in range(len(L.get_texts())):
    L.get_texts()[i_L].set_text(my_label[i_L])


letter_list = [str(chr(k+97)) for k in range(0, 20)]
k=0
for gca in ax.flatten():
    if gca is not None:
        gca.annotate(f'({letter_list[k]})', xy=(-0.2, 1.0), xycoords=gca.transAxes, fontsize=18)
        k += 1


plt.savefig('../data_figures/coefficients_comparison_iter.png', bbox_inches='tight', dpi=200)
plt.savefig('../data_figures/coefficients_comparison_iter.pdf', bbox_inches='tight')

# %%
