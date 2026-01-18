# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 22:46:33 2022

@author: Nabizadeh
"""
import numpy as np
import glob
import ffmpeg
import pandas as pd


# path = r'D:\Nabizadeh\Uni\Transcoding\transcoding_Video\segment_videos_8M'
# txt_path = r'D:\Nabizadeh\software\mv_extractor\segment_videos_h264_mp4'
def parse_twitch_files(path,txt_path):
    
    i_n = sorted(glob.glob(path +'/*.mp4'))
    
    image_n = sorted(glob.glob(txt_path+'/*.txt'))
    video_mb_feature = []
    for k in range(len(image_n)):
        a3 = ffmpeg.probe(i_n[k], cmd='ffprobe')            
        a3 = a3['streams'][0]
        print(image_n[k])
        #print(a3['bit_rate'])
        # if (a3['duration'] !='2.000000') or (int(a3['bit_rate'])/1000 < 7200):
        #     continue
        with open(image_n[k]) as f:
            f = f.readlines()
        firstline = 0
        str_list = [' I:',' P:',' B:',' S:',' MBS:','16x16:',' 16x8:',' 8x16:',' 8x8:',' 4x4:',' AQP:']
        
        
        all_mb_feature = []
        for line in f:
            if firstline == 0:
                firstline = 1
                continue
            # print(line)
            ind_pre = 0
            mb_feature = []
            j = 0
            for i in range(len(str_list)):
                if i ==0:
                    ind = line.find(str_list[i])
                else:
                    # print(ind)
                    ind_pre = ind 
                    ind = line.find(str_list[i])
                    # print(ind)
                    if ind != -1 and ind_pre!=-1:
                        # print(int(line[ind_pre+len(str_list[i-1]):ind]))
                        j = 1
                        if i !=5 and i !=11:
                            mb_feature.append(int(line[ind_pre+len(str_list[i-1]):ind]))
                            j = 1
                    # break
            mb_feature = np.array(mb_feature)
            if j == 1:
                all_mb_feature.append(mb_feature)
            # if j == 1:
            #     break
        all_mb_feature = np.array(all_mb_feature)
        all_mb_feature = np.sum(all_mb_feature,axis=0)
        video_mb_feature.append(all_mb_feature)
        # break
    #print((video_mb_feature))
    video_mb_feature = np.array(video_mb_feature)    
    np.save("twitch_features.npy", video_mb_feature)
    
    video_metafeatures0 = ['I',' P',' B',' S','16x16',' 16x8',' 8x16',' 8x8',' 4x4']
    my_measures = pd.DataFrame()
    my_measures = pd.DataFrame(video_mb_feature, columns =video_metafeatures0)
    my_measures.to_pickle("twitch_features_h264.pkl")
    return my_measures
