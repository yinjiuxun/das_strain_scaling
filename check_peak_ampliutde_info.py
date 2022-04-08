#%% import modules
import os
import pandas as pd
#from sep_util import read_file
import numpy as np

# import the plotting functions
from plotting_functions import *
# import the utility functions
from utility_functions import *

# %%
# ==============================  Ridgecrest data ========================================
#% Specify the file names
DAS_info_files = '/kuafu/DASdata/DASinfo/DAS_ChannelLocation/DAS_Ridgecrest_ODH3.txt'
catalog_file =  '/home/yinjx/notebooks/strain_scaling/Ridgecrest_das_catalog_M2_M8.txt'
results_output_dir = '/home/yinjx/kuafu/Ridgecrest/Ridgecrest_scaling/peak_amplitude_scaling_results_strain_rate_snr'
das_pick_file_name = '/peak_amplitude_M3+.csv'
peak_df_file = results_output_dir + '/' + das_pick_file_name
# Load the peak amplitude results
peak_amplitude_df = pd.read_csv(peak_df_file)

#  load the information about the Ridgecrest DAS channel
DAS_info = np.genfromtxt(DAS_info_files)
DAS_channel_num = DAS_info.shape[0]
DAS_index = DAS_info[:, 0].astype('int')
DAS_lon = DAS_info[:, 1]
DAS_lat = DAS_info[:, 2]

catalog = pd.read_csv(catalog_file, sep='\s+', header=None, skipfooter=1, engine='python')
# Find events in the pick file
event_id_selected = np.unique(peak_amplitude_df['event_id'])
catalog_select = catalog[catalog[0].isin(event_id_selected)]
num_events = catalog_select.shape[0]
catalog_select

# Add the event label for plotting
peak_amplitude_df = add_event_label(peak_amplitude_df)

#%%
# plot time variation of events
time_list = [obspy.UTCDateTime(time) for time in catalog_select[3]]
time_span = np.array([time-time_list[0] for time in time_list])
time_span_days = time_span/3600/24

fig, ax = plt.subplots(figsize=(10, 8))
ax.plot(time_span_days, catalog_select[7], 'o')
ax.set_xlabel(f'Days from the {time_list[0]}')
ax.set_ylabel('magnitude')
plt.savefig(results_output_dir + '/time_variation_selected_earthquakes.png', bbox_inches='tight')

# plot map
fig, ax = plt.subplots(figsize=(7, 6))
cmp = ax.scatter(DAS_lon, DAS_lat, s=10, c=DAS_index, cmap='jet')
ax.scatter(catalog_select[5], catalog_select[4], s=10**(catalog_select[7]/5), c='k')
fig.colorbar(cmp)
plt.savefig(results_output_dir + '/map_of_earthquakes_not_grouped.png', bbox_inches='tight')

# %%
# ==============================  Mammoth data ========================================
#%% Specify the file names
DAS_info_files1 = '/kuafu/DASdata/DASinfo/DAS_ChannelLocation/DAS_Mammoth_South.txt'
DAS_info_files2 = '/kuafu/DASdata/DASinfo/DAS_ChannelLocation/DAS_Mammoth_North.txt'
catalog_file =  '/home/yinjx/kuafu/Mammoth/catalog_regional.csv'
results_output_dir = '/home/yinjx/kuafu/Mammoth/peak_ampliutde_scaling_results_strain_rate'
das_pick_file_name1 = '/South/Mammoth_South_Scaling_M3.csv'
das_pick_file_name2 = '/North/Mammoth_North_Scaling_M3.csv'

DAS_info1 = pd.read_csv(DAS_info_files1, sep=',', engine='python').dropna()
DAS_info2 = pd.read_csv(DAS_info_files2, sep=',', engine='python').dropna()
DAS_info = pd.concat([DAS_info1, DAS_info2], axis=0)

DAS_channel_num = DAS_info.shape[0]
DAS_index = DAS_info['channel'].astype('int')
DAS_lat = DAS_info['latitude']
DAS_lon = DAS_info['longitude']

peak_amplitude_df1 = pd.read_csv(results_output_dir + '/' + das_pick_file_name1)
peak_amplitude_df2 = pd.read_csv(results_output_dir + '/' + das_pick_file_name2)
peak_amplitude_df = pd.concat([peak_amplitude_df1, peak_amplitude_df2], axis=0)

catalog = pd.read_csv(catalog_file, sep=',', engine='python')
# Find events in the pick file
event_id_selected = np.unique(peak_amplitude_df['event_id'])
catalog_select = catalog[catalog['ID'].isin(event_id_selected)]
num_events = catalog_select.shape[0]
catalog_select

# Add the event label for plotting
peak_amplitude_df = add_event_label(peak_amplitude_df)

#%%
# plot time variation of events
time_list = [obspy.UTCDateTime(time.replace(' ', 'T')) for time in catalog_select['time']]
time_span = np.array([time-time_list[0] for time in time_list])
time_span_days = time_span/3600/24

fig, ax = plt.subplots(figsize=(10, 8))
ax.plot(time_span_days, catalog_select['mag'], 'o')
ax.set_xlabel(f'Days from the {time_list[0]}')
ax.set_ylabel('magnitude')
plt.savefig(results_output_dir + '/time_variation_selected_earthquakes.png', bbox_inches='tight')

# plot map
fig, ax = plt.subplots(figsize=(7, 6))
cmp = ax.scatter(DAS_lon, DAS_lat, s=10, c=DAS_index, cmap='jet')
ax.scatter(catalog_select['lon'], catalog_select['lat'], s=10**(catalog_select['mag']/5), c='k')
ax.set_title(f'Total event number: {num_events}')
fig.colorbar(cmp)
plt.savefig(results_output_dir + '/map_of_earthquakes_not_grouped.png', bbox_inches='tight')


# %%
# # ==============================  Olancha data ========================================
# #%% Specify the file names
# DAS_info_files = '/kuafu/DASdata/DASinfo/DAS_ChannelLocation/DAS_Olancha_Plexus.txt'
# catalog_file =  '/home/yinjx/notebooks/strain_scaling/Ridgecrest_das_catalog_M2_M8.txt'
# results_output_dir = '/kuafu/yinjx/Olancha_Plexus/Olancha_scaling/peak_ampliutde_scaling_results_strain_rate'
# das_pick_file_name = '/peak_amplitude_M3+.csv'
# peak_df_file = results_output_dir + '/' + das_pick_file_name
# # Load the peak amplitude results
# peak_amplitude_df = pd.read_csv(peak_df_file)

# #  load the information about the Olancha DAS channel (needs to further update)
# DAS_info = np.genfromtxt(DAS_info_files)
# DAS_channel_num = DAS_info.shape[0]
# DAS_index = DAS_info[:, 0].astype('int')
# DAS_lon = DAS_info[:, 1]
# DAS_lat = DAS_info[:, 2]

# %% 
# Show the peak strain rate amplitude variations
plot_magnitude_distance_coverage(peak_amplitude_df, results_output_dir + '/magnitude_distance_distribution.png')
plot_distance_variations(peak_amplitude_df, ['peak_P', 'peak_S'], results_output_dir + '/peak_strain_rate_vs_distance.png')
plot_magnitude_variations(peak_amplitude_df, ['peak_P', 'peak_S'], results_output_dir + '/peak_strain_rate_vs_magnitude.png')
plot_P_S_amplitude_ratio(peak_amplitude_df, ['peak_P', 'peak_S'], results_output_dir + '/peak_strain_rate_P_S_ratio.png')

# %% 
# Show the peak strain amplitude variations
plot_distance_variations(peak_amplitude_df, ['peak_P_strain', 'peak_S_strain'], results_output_dir + '/peak_strain_vs_distance.png')
plot_magnitude_variations(peak_amplitude_df, ['peak_P_strain', 'peak_S_strain'], results_output_dir + '/peak_strain_vs_magnitude.png')
plot_P_S_amplitude_ratio(peak_amplitude_df, ['peak_P_strain', 'peak_S_strain'], results_output_dir + '/peak_strain_P_S_ratio.png')
# %%


