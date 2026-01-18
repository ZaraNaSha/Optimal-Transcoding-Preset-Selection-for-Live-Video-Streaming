# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 11:22:29 2023

@author: NBZ
"""

import pandas as pd
import numpy as np
import scipy.stats
#%%    split features for tarin #############################
path = r'D:\Nabizadeh\Uni\Transcoding\PSNR_Time_Code'
data = pd.read_pickle(path + '/all_features_PSNR_Time_Windows.pkl')
number_video = 877

for preset in range(5):
    df = pd.DataFrame()
    for i in range(10): # number of bitrate
        tmp = data[i*5*number_video+preset*number_video:(i*5+1)*number_video+preset*number_video]
        tmp = tmp.drop(['video_name','duration','features','preset'], axis=1)
        frames = [df,tmp]
        df = pd.concat(frames,axis=0)
        df = df.reset_index(drop=True)
    df.to_csv(path + "/preset"+str(preset)+"features.csv")