# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 22:03:34 2023

@author: NBZ
"""
import glob
import pandas as pd
import os
import ffmpeg
import numpy as np
import matplotlib.pyplot as plt
#%%
number_video = 877
path = r'D:\Nabizadeh\Uni\Transcoding\PSNR_Time_Code'
my_measures = pd.read_pickle(path + "/measures_features_maedeh_200k_h264.pkl")
# time = my_measures['transcoding_time']
# time1 = (time*4)/(np.max(time))
# my_measures['transcoding_time_scaled']=time1
# m1 = my_measures[0:3924].reset_index(drop=True)
# m2 = my_measures[3924:].reset_index(drop=True)
# m1['transcoding_time_4m']=m2['transcoding_time']
# m1['transcoding_time_scaled_4m']=m2['transcoding_time_scaled']
# my_measures = m1
#%%
mv_new = np.load(path + '/mv_no.npy') 
mv_hist = np.load(path +'/mv_hist_all.npy') 
mv_new1 = np.tile(mv_new,5*10) # only 5 preset is used ["veryslow","slow","fast","veryfast","ultrafast"] and 10 bitrate
df = pd.DataFrame(mv_new1, columns = ['MV_new'])
mv_hist1 = np.tile(mv_hist,5*10) # only 5 preset is used ["veryslow","slow","fast","veryfast","ultrafast"] and 10 bitrate
df1 = pd.DataFrame(mv_hist1, columns = ['MV_Hist_Mean'])
my_measures = my_measures.reset_index(drop=True)
#%%
my_measures0 = pd.read_pickle(path +"/twitch_features_h264.pkl")
twitch_features = np.array(my_measures0)
twitch_features = np.tile(twitch_features,(5*10,1)) # only 5 preset is used ["veryslow","slow","fast","veryfast","ultrafast"] and 10 bitrate
my_measures0 = pd.DataFrame(twitch_features, columns = my_measures0.columns)
my_measures0 = my_measures0.loc[~my_measures0.index.duplicated(keep='first')]
#%%

frames = [my_measures,df,df1,my_measures0]
result = pd.concat(frames,axis=1)
# result.to_pickle(path+"/measures_features_all_features_Ryzen_WSL.pkl")### 436 for each preset
result.to_pickle(path+"/all_features_PSNR_Time_Windows.pkl")### 436 for each preset
