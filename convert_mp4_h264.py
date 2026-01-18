# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 22:41:20 2022

@author: Nabizadeh
"""
import ffmpeg
import os
import subprocess
import pandas as pd
import glob

# mp4_path = r'D:\Nabizadeh\Uni\Transcoding\transcoding_Video\segment_videos_8M'
# h264_path = r'D:\Nabizadeh\Uni\Transcoding\transcoding_Video\segment_videos_h264_mp4'

def convert_mp4_to_h264(mp4_path,h264_path):
    image_n = sorted(glob.glob(mp4_path+'/*.mp4'))
    k =0
    for k in range(len(image_n)):
        n = image_n[k]
        h,t = os.path.split(n)
        ins = "ffmpeg -i "+image_n[k]+" -c:v copy -an -f h264 "+h264_path+"/"+t[0:-3]+"264"
        a = os.system(ins)