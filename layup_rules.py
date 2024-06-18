# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 10:11:57 2022

@author: jakub.kucera
"""
import numpy as np

def force9090(layup):
    #convert all angles to exist between -90 and 90
    l2 = ""
    for l in layup.split(",")[:]:
        #not sure why this is required, but....
        
        #to account for non-ASCII "-"
        if "-" in l:
            h = l.replace("-","")
            h = float(h)
            h = h *-1
        else:
            h = float(l)
        
        #180deg shifts until the layup exits in correct range
        while h > 90:
            h = h -180
        while h < -90:
            h = h + 180
            
        #construct the return string of layer orientations
        if l2 == "":
            l2 = str(int(h))
        else:
            l2 = l2+","+str(int(h))

    return(l2)
            
        
# how about class that holds true/false, and rule in form of if statement


def f130a(layup):
    #check if laminate is symmetric
    
    #read the file
    with open(layup, "r") as text_file:
        f = text_file.read()
        
    w = f.split("[LAMINATE]")[1]
    w = w.split("[SPLINES]")[0]
    ori = w.split('\n')[1]
    ori = ori.replace("[","")
    ori = ori.replace("]","")

    #convert all angles to exist between -90 and 90
    ori = force9090(ori)

    ct = ori.count(",")
    
    i = 0
    sym = True
    while i < ct:
        
        if ori.split(",")[i] != ori.split(",")[ct-i]:
            sym = False
            print(sym)
            print(ori.split(",")[i] , ori.split(",")[ct-i])
            
        
        
        i = i + 1
        
    #Append this to report.
    if sym == False:
        print("Layup is not symmetric. Please make it symmetric, unless there is \n"
              "a very good reason for it not to be.")
    else:
        print("Layup is symmetric.")
    
    #one thing is to check total layup
    #another is to check if any part of layup (taking into accoutn drop-offs) is symmetric
    
def f130b(layup):
    #check if laminate is balanced
    
    #read the file
    with open(layup, "r") as text_file:
        f = text_file.read()
        
    w = f.split("[LAMINATE]")[1]
    w = w.split("[SPLINES]")[0]
    ori = w.split('\n')[1]
    ori = ori.replace("[","")
    layup = ori.replace("]","")
    #enforce 90 -90 range
    layup = force9090(layup)
    
    
    #use list
    u = np.asarray([])
    for i in layup.split(",")[:]:
        u = np.concatenate((u,np.asarray([int(i)])),axis=0)
    

    mau = int(max(u))
    miu = int(min(u))

    max_shift = 90 - mau
    min_shift = -90 - miu
    
    #rotate the laminate for all possible rotations 
    #if laminate balanced arround any, it is considered balanced for all
    shift = max_shift
    
    balance = False
    while shift > min_shift:
        print(shift)
        print(u)
        
        
        # used to be list: u= u + shift...
        tu = u[:].copy()
        for i,ii in enumerate(tu):
            tu[i] = ii + shift
        
        #check if this laminate is balanced
        i = 0
        while i < np.size(tu,0):
            #print(tu)
            #0 and 90 are deleted according to definition of balanced laminate
            if tu[i] == 90:
                #print("deleting", tu[i])
                tu = np.delete(tu,i,axis=0) #u.remove[i]
                
            elif tu[i] == 0:
                #print("deleting", tu[i])
                tu = np.delete(tu,i,axis=0) 
                
            else:
                ii = 1
                #check if there is a matching negative layer for current layer i
                while ii < np.size(tu,0):
                    if i != ii:
                        #print(tu[i],tu[ii])
                        if tu[i] == tu[ii]*-1:
                            #delete both layers that balance out around current 0
                            #print("deletingX", tu[i])
                            tu = np.delete(tu,i,axis=0)
                            
                            if i < ii:
                                #print("deletingY", tu[ii-1])
                                tu = np.delete(tu,ii-1,axis=0)
                                
                            else:
                                #print("deletingZ", tu[ii])
                                tu = np.delete(tu,ii,axis=0)
                            i = -1
                            break
                                
                            
                    
                    ii = ii + 1
                
                i = i + 1
        
        
        #to accomodate for any full degree definition 0.5 degree has to used 
        #to iterate -- for example [-12,3,24,39] is balanced around 13.5, which
        #would not be possible to find if iteration was by full degrees.
        #This is still not bulletproof, but it is assumed nobody uses definition of 
        #layup in a fraction of a degree precision.
        shift = shift - 0.5
    
        print(tu)
        #break
        if len(tu) == 0:
            balance = True
            print("laminate is balanced")
            break
        
            
        
    if balance == False:
        print("laminate is imbalanced")
    
    
    
    
    

layup = "C:\\temp\\xxx2.txt"
f130b(layup)