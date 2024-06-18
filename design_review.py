# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 11:33:10 2022

@author: jakub.kucera
"""
import pandas as pd
import numpy as np

from step_features import flange_data


def step_check(step_file,collection):
    #finds lines relevant to the specific part
    
    vert_res = []
    cnt = step_file.count("\\")
    ref = step_file.split("\\")[cnt]
    ref = ref.split(".")[0]
    d = df.to_numpy()
    cnt = 0
    for i, part  in enumerate(d[:,21]):
        #print(part)
        #print(part,d[i,22])
        if (ref in part) and (int(d[i,22])==5):
            if cnt == 0:
                vert_res = np.asarray([d[i,:]])
                cnt = cnt + 1
            else:
                vert_res = np.concatenate((vert_res,np.asarray([d[i,:]])),axis=0)
                
    return(vert_res)

def flange_filter(vr):
    #ref 19 column - for flange binary
    #fl = [x,y,z]
    fl = np.asarray([[0,0,0]])
    for i, dd in enumerate(vr[:,19]):
        if dd == 1:
            fl = np.concatenate((fl,np.asarray([[vr[i,0],vr[i,1],vr[i,2]]])),axis=0)
    fl = np.delete(fl,0,axis=0)
    #return vertices      
    return(fl)
    
    
    
df = pd.read_parquet('D://CoSinC_WP4.2//WS_out//full_votes_for_val_set.parquet')
step_file = "D:\CAD_library_sampling\sample7\s-1069.stp"
vert_res = step_check(step_file,df)
#print(vert_res)
vertices = flange_filter(vert_res)
#print(vertices)
f1 = flange_data(step_file,vertices,report = True)


#print(df.to_numpy())
#print(df["file"])
#pd.DataFrame(df).to_csv("D://CoSinC_WP4.2//WS_out//full_votes_for_val_set.csv")
