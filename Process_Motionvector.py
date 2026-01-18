# -*- coding: utf-8 -*-

"""

Created on Sun Mar  5 16:26:47 2023



@author: NBZ

"""



import time

import numpy as np

from mvextractor.videocap import VideoCap

import cv2

import glob

import ffmpeg

import matplotlib.pyplot as plt

import pandas as pd

#%%

path = './segment_videos_h264_mp4'

def mv_extractor(path,path_mp4):

    a = sorted(glob.glob(path+'/*.264'))
    b = sorted(glob.glob(path_mp4+'/*.mp4'))

    info = []

    mv_no = []

    mv_hist_all = []

    for i in range(len(a)):

        a3 = ffmpeg.probe(b[i], cmd='ffprobe')            
        a3 = a3['streams'][0]
        if (a3['duration'] !='2.000000') or (int(a3['bit_rate'])/1000 < 7200):
            continue
        # filename of the video file

        url = a[i]

        print(url)

        cap = VideoCap()



        # open the video file

        ret = cap.open(url)

        if not ret:

            raise RuntimeError("Could not open the video url")

        #print("Sucessfully opened video file")

        step = 0

        times = []

        mv = []

        mv1 = []

        mv_n = 0

        mv_hist = np.zeros(30000)

        p_n = 0

        i_n = 0

        b_n = 0
        mv_mean = 0

        # continuously read and display video frames and motion vectors

        while True:

            #print("Frame: ", step, end=" ")

            step += 1
            #print("step:",step)

            tstart = time.perf_counter()



            # read next video frame and corresponding motion vectors

            ret, frame, motion_vectors, frame_type, timestamp = cap.read()



            tend = time.perf_counter()

            telapsed = tend - tstart

            times.append(telapsed)

           

            # if there is an error reading the frame

            if not ret:

                #print("No frame read. Stopping.")

                break;
            #tic = time.perf_counter()

            tmp = abs(motion_vectors[:,3]-motion_vectors[:,5])+abs(motion_vectors[:,4]-motion_vectors[:,6])
            mv_mean = np.sum(tmp) + mv_mean
            #toc = time.perf_counter()
            #print(toc-tic)

            #print(tmp)

            if step==1:

                mv1 = motion_vectors

                mv = tmp

                #mv_move = tmp

            else:

                mv1 = np.concatenate((mv1,motion_vectors),axis=0)

                mv = np.concatenate((mv,tmp),axis=0)

                #mv_move = tmp+mv_move
            #tmp, bins, patches = plt.hist(tmp,bins=100)
            #tmp, bins, patches = plt.hist(tmp,bins=50)
            

            #mv_hist[0:len(bins)-1] = tmp[0:len(bins)-1] + mv_hist[0:len(bins)-1]
            

            # mv_hist[0:motion_vectors.shape[0]] = tmp[0:motion_vectors.shape[0]] + mv_hist[0:motion_vectors.shape[0]]

            mv_n = mv_n + motion_vectors.shape[0]

            if frame_type== 'I':

                i_n = i_n + 1

            elif frame_type == 'P':

                p_n = p_n + 1

            else:

                b_n = b_n + 1

            

            # if user presses "q" key stop program

            if cv2.waitKey(1) & 0xFF == ord('q'):

               break

        mv_no.append(mv_n)

        #mv_hist_all.append(mv_hist)
        mv_hist_all.append(mv_mean)

        print("average dt: ", mv_n)

       

        cap.release()

    mv_no = np.array(mv_no)

    np.save(path+"/mv_no.npy",mv_no)

    

    mv_hist_all = np.array(mv_hist_all)

    np.save(path+"/mv_hist_all.npy",mv_hist_all)

    # close the GUI window

    cv2.destroyAllWindows()

    

def process_mv(path,image_number):

    bins = np.linspace(0, 100, 101)

    aa = np.load(path+'/mv_no.npy') 

    bb = np.load(path+'/mv_hist_all.npy') 

    mv_new = []

    mv_hist = []

    for k in range(image_number):

        tmp, bins, patches = plt.hist(bb[k], bins)

        mv_hist.append(tmp)

        mv_new.append(aa[k])

    mv_new = np.array(mv_new)

    mv_hist = np.array(mv_hist)

    aa = mv_hist[:,1:100] 

    mv_hist = np.mean(aa,axis = 1)   

    mv_new = np.tile(mv_new,9)

    mv_hist = np.tile(mv_hist,9)

    df = pd.DataFrame(mv_new, columns = ['MV'])

    df1 = pd.DataFrame(mv_hist, columns = ['MV_Hist_Mean'])

    # my_measures = pd.read_pickle("measures_features_maedeh_6m_extra_all_preset.pkl")

    frames = [df,df1]

    result = pd.concat(frames,axis=1)

    # result.to_pickle("measures_features_maedeh_6m_extra_all_preset.pkl")### 368 for each preset

    return result


