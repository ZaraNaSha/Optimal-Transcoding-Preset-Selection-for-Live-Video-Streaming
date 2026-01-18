# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 11:31:08 2023

@author: NBZ
"""
from segment_videos import segment_videos
from convert_mp4_h264 import convert_mp4_to_h264
from extract_h264_features import extract_h264_features
from extract_features_twitch import extract_twitch_features
from twitch_features_parse import parse_twitch_files
from Process_Motionvector import mv_extractor,process_mv
import glob
########################################## this is the file that all fuctions for extracting features are invoked #########################################################
def main_preset_time_prediction(segment_video=1,convert_mp4_h264=1,extract_features=1):
    # step one segment the videos
    print("segment_video:",segment_video)
    # video_path = './videos'
    video_path = r'D:\Nabizadeh\Uni\Transcoding\transcoding_Video\videos'
    segment_path = './videos_segment'
    h264_path = './videos_segment_h264'
    if segment_video == 1:
        # video_path = r'D:\Nabizadeh\Uni\Transcoding\transcoding_Video'
        # segment_path = r'D:\Nabizadeh\Uni\Transcoding\transcoding_Video\segment_videos_8M'
        
        print("segment_videos")
        segment_videos(video_path,segment_path,video_length=2,format_type='mkv')
    # step two convert mp4 to h264
    if convert_mp4_h264 == 1:
        # segment_path = r'D:\Nabizadeh\Uni\Transcoding\transcoding_Video\segment_videos_8M'
        # h264_path = r'D:\Nabizadeh\Uni\Transcoding\transcoding_Video\segment_videos_h264_mp4'
        segment_path = segment_path
        
        convert_mp4_to_h264(segment_path,h264_path)
    if extract_features:
        #preset = ["veryslow","slower","slow","medium","fast","faster","veryfast","superfast","ultrafast"]
        preset = ["veryslow","slow","fast","veryfast","ultrafast"]
        # # bit_rate = ['8000k','6000k','4000k','2000k']
        bit_rate = ['6000k','5000k','4000k','3000k','2000k','1000k','800k','600k','400k','200k']
        #bit_rate = ['4000k','3000k','2000k','1000k','800k','600k','400k','200k']
        bit_rate_in = [8000]
        bit_rate_out = [6000,5000,4000,3000,2000,1000,800,600,400,200]
        #bit_rate_out = [2000,1000,800,600,400,200]
        #bit_rate_out = [3000]
        mp4_path = segment_path
        h264_path = h264_path
        linux = 1
        h264_measures = extract_h264_features(mp4_path,h264_path,preset,bit_rate,bit_rate_in,bit_rate_out,linux)
        
        # ##################### this function is run in docker or linux the path should be in the directory of docker for example in my system D:\Nabizadeh\software\mv_extractor#####################
        # path = './segment_videos_h264_mp4'
        
        #extract_twitch_features(h264_path,segment_path)
        txt_path = h264_path
        twitch_measures = parse_twitch_files(mp4_path,txt_path)
        mv_extractor(h264_path,segment_path)
        
        #mv_extractor(segment_path)
        # i_n = glob.glob(segment_path +'/*.mp4')
        # process_mv(h264_path,len(i_n))


main_preset_time_prediction(segment_video=1,convert_mp4_h264=0,extract_features=0)        
        
    
