# -*- coding: utf-8 -*-

"""

Created on Tue Oct  4 09:27:55 2022



@author: Nabizadeh

"""

import os 

import glob

import ffmpeg



# path = './segment_videos_h264_mp4'

def extract_twitch_features(path,path_mp4):

    image_n = sorted(glob.glob(path+'/*.264'))

    b = sorted(glob.glob(path_mp4+'/*.mp4'))

    for k in range(len(image_n)):
        a3 = ffmpeg.probe(b[k], cmd='ffprobe')
        a3 = a3['streams'][0]
        if (a3['duration'] !='2.000000') or (int(a3['bit_rate'])/1000 < 7200):
            continue
        n = image_n[k]
        str1 = './ldecod_static -p Silent=0 -i '+image_n[k]+' -o "" >'+n[0:-3]+'txt'
        os.system (str1)
