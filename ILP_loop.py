# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pulp
import random
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
path = r'D:\zahra_tuf_pc\Uni\Transcoding\PSNR_Time_Code'
names = glob.glob(path+'/*_PSNR.csv')
w_t = []
w_b = []
v_psnr = []
n = 877
# n = 51 # for games video
num_chunks = 6
num_presets = 5  # Assuming 5 different presets
num_bitrates = 10  # Assuming 10 different bitrates
num_presets_per_chunk = 50
# Constraints
# T_max = 11  # Example cumulative time constraint
T_max = 5
# B_max = 6*(5000)  # Example cumulative bitrate constraint
bitrates = [6000,5000,4000,3000,2000,1000,800,600,400,200]
bit_no = 7
B_max = 6*(bitrates[bit_no]) 

presets = ['veryslow', 'slow', 'fast', 'veryfast', 'ultrafast']
title = [
    'ref_PSNR',
    'ref_birate',
    'ref_time',
    'total_PSNR',
    'total_bitrate',
    'total_time'
]
data_sel = pd.DataFrame()
data_sel = data_sel.reindex(columns = data_sel.columns.tolist() 
+ title)
# video_sel = [646,867,430,733,90,487]
# video_sel = [374,635,414,316,195,478]
# video_sel = [347,348,349,350,351,352] #livemusic8_001.264
# video_sel = [58,59,60,61,62,63]
loop_no = 0
all_selected = []
preset_number = []
while loop_no < n:
    chunks = []
    ref = []
    tmp3 = []
    for l in range(num_chunks):   
        tmp1 = []
        tmp2 = []
        k = np.random.randint(0, n-1,1)
        print(k)
        tmp3.append(k[0])
        # k = video_sel[l]
        for i in range(num_presets):#(len(names)):
            data = pd.read_csv(names[i])
            for j in range(num_bitrates):
                # print(data.loc[j*n+k]['output_bitrate'])
                chunk = {'psnr': float(data.loc[j*n+k]['PSNR']), 'bitrate': int(data.loc[j*n+k]['output_bitrate']), 'time': data.loc[j*n+k]['transcoding_time']}
                # if j==1 and i==3: # bitrate == 5000 and preset == veryfast
                #     ref.append(chunk)
                if j==bit_no and i==3: # bitrate == 5000 and preset == veryfast
                    ref.append(chunk)
                tmp1.append(chunk)
        for x in range(num_presets_per_chunk):
            tmp2.append(tmp1[x]['time'])
        tmp2 = np.array(tmp2)
        tmp2 = np.squeeze(tmp2)
        tmp2 = tmp2 *(2/(np.max(tmp2)))
        for x in range(num_presets_per_chunk):
            tmp1[x]['time'] = tmp2[x]
        chunks.append(tmp1)    
    all_selected.append(tmp3)    
    # break
    ref_psnr = sum(preset['psnr'] for preset in ref)
    ref_bitrate = sum(preset['bitrate'] for preset in ref)
    ref_time = sum(preset['time'] for preset in ref)
    data_sel.at[loop_no,'ref_PSNR'] = ref_psnr
    data_sel.at[loop_no,'ref_birate'] = ref_bitrate
    data_sel.at[loop_no,'ref_time'] = ref_time
    # break
    # Define the problem
    prob = pulp.LpProblem("Maximize_PSNR", pulp.LpMaximize)
    
    # Decision variables
    x = []
    for i in range(6):
        x.append([pulp.LpVariable(f"x_{i+1}_{j+1}", cat="Binary") for j in range(num_presets_per_chunk)])
    
    # Objective function
    prob += pulp.lpSum(chunks[i][j]['psnr'] * x[i][j] for i in range(6) for j in range(num_presets_per_chunk))
    
    # Constraints
    for i in range(6):
        prob += pulp.lpSum(x[i][j] for j in range(num_presets_per_chunk)) == 1  # Each chunk must have exactly one preset selected
    
    prob += pulp.lpSum(chunks[i][j]['bitrate'] * x[i][j] for i in range(6) for j in range(num_presets_per_chunk)) <= B_max  # Total bitrate constraint
    prob += pulp.lpSum(chunks[i][j]['time'] * x[i][j] for i in range(6) for j in range(num_presets_per_chunk)) <= T_max  # Total time constraint
    
    # Solve the problem
    solver = pulp.PULP_CBC_CMD()  # You can use other solvers like Gurobi if available
    prob.solve(solver)
    
    # Print the results
    print("Status:", pulp.LpStatus[prob.status])
    selected_presets = []

    for i in range(6):
        for j in range(num_presets_per_chunk):
            if pulp.value(x[i][j]) == 1:
                selected_presets.append((i+1, j+1, chunks[i][j]))
                preset_number.append(int(j/10))
                # print(f"Chunk {i+1} selects preset {j+1} with PSNR {chunks[i][j]['psnr']}, Bitrate {chunks[i][j]['bitrate']}, Time {chunks[i][j]['time']}")
 
    # Summarize total PSNR, bitrate, and time
    total_psnr = sum(preset[2]['psnr'] for preset in selected_presets)
    total_bitrate = sum(preset[2]['bitrate'] for preset in selected_presets)
    total_time = sum(preset[2]['time'] for preset in selected_presets)
    
    data_sel.at[loop_no,'total_PSNR'] = total_psnr
    data_sel.at[loop_no,'total_bitrate'] = total_bitrate
    data_sel.at[loop_no,'total_time'] = total_time
    # print(f"Total PSNR: {total_psnr}")
    # print(f"Total Bitrate: {total_bitrate}")
    # print(f"Total Time: {total_time}")
    loop_no += 1
    # break

df = pd.DataFrame(data_sel)
data_sel.to_csv('output_sel_'+str(bitrates[bit_no])+'_2.csv', index=False)
all_selected = np.array(all_selected)
df = pd.DataFrame(all_selected)
df.to_csv('chunk_sel_'+str(bitrates[bit_no])+'_2.csv', index=False)
#%%
preset_number = np.array(preset_number)
bin_width = 0.1

# Calculate the number of bins based on the range of data and desired bin width
# bins = np.arange(-0.05, 4 + bin_width/2, bin_width)
fig, axs = plt.subplots(1, 1, figsize=(10, 8))
fig.suptitle("Distribution of Presets")
axs.hist(preset_number[:], bins=5)
#%%
# import numpy as np
# import scipy.interpolate

# def BD_PSNR(R1, PSNR1, R2, PSNR2, piecewise=0):
#     lR1 = np.log(R1)
#     lR2 = np.log(R2)

#     PSNR1 = np.array(PSNR1)
#     PSNR2 = np.array(PSNR2)

#     p1 = np.polyfit(lR1, PSNR1, 3)
#     p2 = np.polyfit(lR2, PSNR2, 3)

#     # integration interval
#     min_int = max(min(lR1), min(lR2))
#     max_int = min(max(lR1), max(lR2))

#     # find integral
#     if piecewise == 0:
#         p_int1 = np.polyint(p1)
#         p_int2 = np.polyint(p2)

#         int1 = np.polyval(p_int1, max_int) - np.polyval(p_int1, min_int)
#         int2 = np.polyval(p_int2, max_int) - np.polyval(p_int2, min_int)
#     else:
#         # See https://chromium.googlesource.com/webm/contributor-guide/+/master/scripts/visual_metrics.py
#         lin = np.linspace(min_int, max_int, num=100, retstep=True)
#         interval = lin[1]
#         samples = lin[0]
#         v1 = scipy.interpolate.pchip_interpolate(np.sort(lR1), PSNR1[np.argsort(lR1)], samples)
#         v2 = scipy.interpolate.pchip_interpolate(np.sort(lR2), PSNR2[np.argsort(lR2)], samples)
#         # Calculate the integral using the trapezoid method on the samples.
#         int1 = np.trapz(v1, dx=interval)
#         int2 = np.trapz(v2, dx=interval)

#     # find avg diff
#     avg_diff = (int2-int1)/(max_int-min_int)

#     return avg_diff
# #%%
# import matplotlib.pyplot as plt
# p_s = []
# p_r = []
# for preset in selected_presets:
#     p_s.append(preset[2]['psnr'])
# for preset in ref:
#     p_r.append(preset['psnr'])
# plt.plot(p_s,label = 'selected')
# plt.plot(p_r,label = 'ref')
# plt.legend(loc="upper left")
# # plt.ylim(-1.5, 2.0)
# plt.show()
# #%%
# BD_PSNR([1,2,3,4,5,6], p_s, [1,2,3,4,5,6], p_r)