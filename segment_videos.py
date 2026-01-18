# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 11:47:30 2023

@author: NBZ
"""
import glob
import ffmpeg
import os
# video_path = r'D:\Nabizadeh\Uni\Transcoding\transcoding_Video'
# segment_path = r'D:\Nabizadeh\Uni\Transcoding\transcoding_Video\segment_videos_8M'
def segment_videos(video_path,segment_path,video_length=4,format_type='mkv'):
    # type_name = ['game','hdr','houto','lecture','livemusic','lyric','music','news','output8mb','sport','tvclip']
    type_name = ['hdr']
    
    for i in range(len(type_name)):
        image_n = sorted(glob.glob(video_path+'/'+type_name[i] +'/*.'+format_type))
        # image_n = glob.glob(path+'/'+type_name[i] +'/*.mp4')
        for k in range(len(image_n)):
            a3 = ffmpeg.probe(image_n[k], cmd='ffprobe')
            if int(a3['format']['bit_rate']) < 7200000:
                print("reject videos")
                continue
        # k=0
            # ins = "ffmpeg -y -i "+image_n[k]+" -g "+str(video_length*30)+" -r 30 -sc_threshold 0 -f segment -segment_time "+str(video_length)+" -b:v 8000k -preset veryslow -reset_timestamps 1 "+segment_path+"/"+type_name[i]+str(k)+"_%03d.mp4"
            ins = 'ffmpeg.exe -i '+ image_n[k]+' -c:v libx264 -pix_fmt yuv420p -b:v '+str(8000)+'K -bufsize '+ str(8000)+'K -minrate '+str(8000)+'K -maxrate '+str(8000)+'K -x264opts keyint=60:min-keyint=60 -preset veryslow -profile:v high -f hls -hls_time 2 -hls_list_size 0 '+segment_path+"/"+type_name[i]+str(k)+"_%03d.mp4"
            print(ins)
            a = os.system(ins)
            break
        break
        

#%%
# path ='./videos_segment'
# a3 = ffmpeg.probe(path + '/hdr0_0022.ts', cmd='ffprobe')
# a4 = ffmpeg.probe(path + '/hdr0_002.mp4', cmd='ffprobe')

