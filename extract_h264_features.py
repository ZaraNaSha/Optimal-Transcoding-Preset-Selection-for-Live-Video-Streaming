# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 10:27:34 2022

@author: Nabizadeh
"""
import subprocess
import os
import ffmpeg
import numpy as np
import pandas as pd
import glob
import time
#%%
def extract_ffprob_features(my_measures,row_no,i_n,frame_data,frame_features):
    my_measures.at[row_no,'video_name'] = os.path.basename(i_n)
    for i in range(len(frame_data)):
        a = frame_data[i]
        command = 'ffprobe -v error -show_entries frame='+a+' -of default=noprint_wrappers=1'
        command = command.split()
        out = subprocess.check_output(command + [i_n]).decode()
        out = out.split()
        tmpi = 0
        tmpb = 0
        tmpp = 0
        for j in range(len(out)):
            tmp = out[j][len(a)+1:]
            # print(tmp)
            if (tmp == 'unknown') or (tmp == 'N/A'):
                tmp = 0
            if (frame_data[i] == 'sample_aspect_ratio') and (tmp != '1:1'):
                # print("aspect_ratio")
                continue
            elif (frame_data[i] == 'sample_aspect_ratio'):
                continue
            if (frame_data[i] == 'color_range'):
                if (tmp == 'tv'):
                    tmp = 1
                elif (tmp == 'pc'):
                    tmp = 2
            if (frame_data[i] == 'color_space'):
                if (tmp == 'bt709'):
                    tmp = 1
                elif (tmp == 'smpte170m'):
                    tmp = 2
                elif (tmp == 'bt2020nc'):
                    tmp = 3
                elif (tmp == 'smpte2084'):
                    tmp = 4
            if (frame_data[i] == 'color_primaries'):
                if (tmp == 'bt709'):
                    tmp = 1
                elif (tmp == 'smpte170m'):
                    tmp = 2
                elif (tmp == 'bt2020'):
                    tmp = 3
                elif (tmp == 'smpte2084'):
                    tmp = 4
            if (frame_data[i] == 'color_transfer'):
                if (tmp == 'bt709'):
                    tmp = 1
                elif (tmp == 'smpte170m'):
                    tmp = 2
                elif (tmp == 'arib-std-b67'):
                    tmp = 3
                elif (tmp == 'smpte2084'):
                    tmp = 4
                elif (tmp == 'bt470m'):
                    tmp = 5
            if (frame_data[i] == 'pict_type'):
                if (tmp == 'I'):
                    tmpi = tmpi+1
                elif (tmp == 'B'):
                    tmpb = tmpb+1
                else:
                    tmpp = tmpp+1
            else:
                print(frame_data[i])
                tmp = float(tmp)
                if j==0:
                    tmp1 = tmp
                else:
                    tmp1 = tmp1 + tmp
        # print(tmp1)
        if (frame_data[i] == 'pict_type'):
            my_measures.at[row_no,frame_features[i]] = tmpi
            my_measures.at[row_no,frame_features[i+1]] = tmpb
            my_measures.at[row_no,frame_features[i+2]] = tmpp
        else:
            my_measures.at[row_no,frame_features[i]] = tmp1
    return my_measures

#%%
def extract_h264_features(mp4_path,h264_path,preset,bit_rate,bit_rate_in,bit_rate_out,linux):
    video_metafeatures = ["video_name","duration","height","width","n_frame", "buffersize",  "features",  "preset", "transcoding_time"]
    frame_features = ['key_frame','pkt_size','sample_aspect_ratio','coded_picture_number','display_picture_number','interlaced_frame','top_field_first','repeat_pict','color_range','color_space','color_primaries','color_transfer','pict_type_I','pict_type_B','pict_type_P']
    frame_data = ['key_frame','pkt_size','sample_aspect_ratio','coded_picture_number','display_picture_number','interlaced_frame','top_field_first','repeat_pict','color_range','color_space','color_primaries','color_transfer','pict_type']
    my_measures = pd.DataFrame()
    my_measures = my_measures.reindex(columns = my_measures.columns.tolist() 
    + video_metafeatures
    + frame_features)
    
    i_n_8 = sorted(glob.glob(mp4_path +'/*.mp4'))
    i_n = sorted(glob.glob(h264_path +'/*.264'))
    row_no = 0
    bitrate_range = bit_rate_in[0]-(bit_rate_in[0]*0.1)
    for k in range(len(bit_rate)):  
        print("extract_h264_features: ",k)
        for j in range(len(preset)):
            if j==0:
                os.mkdir("./"+str(bit_rate_out[k]))
                os.mkdir("./"+str(bit_rate_out[k])+"/"+preset[j])
            else:
                os.mkdir("./"+str(bit_rate_out[k])+"/"+preset[j])
            for i in range(len(i_n)):
                a3 = ffmpeg.probe(i_n_8[i], cmd='ffprobe')            
                a3 = a3['streams'][0]
                # if (a3['duration'] !='4.000000') or (int(a3['bit_rate'])/1000 < bitrate_range):
                #     continue
                if (a3['duration'] !='2.000000') or (int(a3['bit_rate'])/1000 < bitrate_range):
                    continue
               
                my_measures.at[row_no,'video_name'] = i_n[i][-10:]
                my_measures.at[row_no,'height'] = a3['height']
                my_measures.at[row_no,'width'] = a3['width']
                my_measures.at[row_no,'duration'] = a3['duration'] 
                my_measures.at[row_no,'input_bitrate'] = a3['bit_rate']
                my_measures.at[row_no,'output_bitrate'] = bit_rate_out[k]
                my_measures.at[row_no,'buffersize'] = 20500
                my_measures.at[row_no,'preset'] = j
                my_measures.at[row_no,'n_frame'] = a3['has_b_frames']
                
                if linux == 1:
                    myBat = open('./test_transcode.sh','w+')
                    ins = "#!/bin/sh"
                    myBat.write(ins)
                    myBat.write("\n")
                else:
                    print("aaaaaaaaaaaaaaaaaaaaaaaa")
                    myBat = open('./test_transcode.bat','w+') 
                ins = "ffmpeg -y -i "+i_n[i]+" -c:v libx264 -b:v "+bit_rate[k]+" -preset "+preset[j]+" -pass 1 -f h264 NUL && \\"
                myBat.write(ins)
                myBat.write("\n")
                #ins = "ffmpeg -i "+i_n[i]+" -c:v libx264 -b:v "+bit_rate[k]+" -maxrate "+bit_rate[k]+" -bufsize 20500k -preset "+preset[j]+" -pass 2 ./"+str(bit_rate_out[k])+"/"+preset[j]+"/out_y"+str(i)+"_"+str(j)+"_"+str(k)+".264"
                ins = "ffmpeg -i "+i_n[i]+" -c:v libx264 -b:v "+bit_rate[k]+" -maxrate "+bit_rate[k]+" -preset "+preset[j]+" -pass 2 ./"+str(bit_rate_out[k])+"/"+preset[j]+"/out_y"+str(i)+"_"+str(j)+"_"+str(k)+".264"
                myBat.write(ins)
                myBat.close()
                # break
                tic = time.perf_counter()
                if linux == 1:
                    subprocess.call(['./test_transcode.sh'])
                else:
                    print("bbbbbbbbbbbbbbbbbbbbbb")
                    subprocess.call(['test_transcode.bat'])
                toc = time.perf_counter()
                print(toc - tic)
                my_measures.at[row_no,'transcoding_time'] = toc - tic
                print(i_n_8[i])
                my_measures = extract_ffprob_features(my_measures,row_no,i_n[i],frame_data,frame_features)
                my_measures.to_pickle("measures_features_maedeh_"+bit_rate[k]+"_h264.pkl")
                row_no = row_no + 1
                # break
            # break
    return my_measures
#%%