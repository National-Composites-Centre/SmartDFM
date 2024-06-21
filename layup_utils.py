# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 15:41:48 2023

@author: jakub.kucera
"""
import numpy as np
import math

#this set of functions help understand layup

#the goal is to identify individual layup in all distinct regions

#information such as stepped out drop-offs have to be addresesed

def stringToNumpy(strx):
    #Translates typical coordinates in .txt into numpy object.
    #[change this function for any size array later?]
    
    res = np.zeros([1,3])
    for line in strx.split("\n"):
        try:
            rest = np.asarray([[float(line.split()[0]),float(line.split()[1]),float(line.split()[2])]])
            
            res = np.concatenate((res,rest),axis = 0 )
        except:
            print("1 line not suitable for numpy matrix")
            
    res = np.delete(res, 0, axis=0)
    return(res)
        
        
def cross_over(layup_file):
    #returns number of intersections and positions
    #variable for build up
    co = ""
    con = 0
    
    #open the layup file
    with open(layup_file, "r") as text_file:
        lf = text_file.read()
    
    #cleaning the list of splines
    lf1 = lf.split("[LAMINATE]")[1]
    lf1 = lf1.split("[")[2]
    lf1 = lf1.split("]")[0]
    lf1 = lf1.replace(" ","")
    lf1 = lf1.replace("'","")
    
    #for each combination of splines
    for i, spline1 in enumerate(lf1.split(",")):
        #layers denoted by 'f' are "full-surface", meaning no spline is attached
        if spline1 != 'f':
            for ii, spline2 in enumerate(lf1.split(",")[(i+1):]):
                if spline2 != 'f':
                    
                    #spline one processing into matrix
                    sp1 = lf.split("[SPLINES]")[1]
                    sp1 = sp1.split(spline1)[1]
                    sp1 = sp1.split("___{end_spline}___")[0]
                    sp1 = stringToNumpy(sp1)
                    
                    #spline two processing into matrix
                    sp2 = lf.split("[SPLINES]")[1]
                    sp2 = sp2.split(spline2)[1]
                    sp2 = sp2.split("___{end_spline}___")[0]
                    sp2 = stringToNumpy(sp2)
                    
                    #approximates of the two meshes used for the two splines
                    diff1 = math.sqrt((sp2[0,0]-sp2[1,0])**2+(sp2[0,1]-sp2[1,1])**2+(sp2[0,2]-sp2[1,2])**2)
                    diff2 = math.sqrt((sp1[0,0]-sp1[1,0])**2+(sp1[0,1]-sp1[1,1])**2+(sp1[0,2]-sp1[1,2])**2)
                    
                    #for each combination of points between the two splines
                    for iii in range(0,np.size(sp1,0)):
                        for iv in range(0,np.size(sp2,0)):
                            #find the distance between the two points
                            dist = math.sqrt(((sp1[iii,0]-sp2[iv,0])**2
                                              )+((sp1[iii,1]-sp2[iv,1])**2
                                                 )+((sp1[iii,2]-sp2[iv,2])**2))
                            
                            #if this distance is smaller than the smaller of the two meshes
                            if dist < min(diff2,diff1)*0.99:
                                #likely cross-over
                                #Break closest loop, no need for connection of the same point to multiple
                                #points.
                                co += spline1+" "+spline2+" "+str(sp1[iii,0]
                                      )+" "+str(sp1[iii,1])+" "+str(sp1[iii,2])+"\n"
                                con += 1
                                break
        
    #number of cross-overs collected initially
    cnt = co.count("\n")
    
    #The following section merges cross-overs that are likely just one,
    #for which multiple nodes were collected.
    rew = ""
    #"skip" lists adds lines which have already been merged, as not to duplicate
    #searches.
    skip = []
    for i in range(0,cnt):
        if i not in skip:
            ish = 1
            xx = float(co.split("\n")[i].split()[2])
            yy = float(co.split("\n")[i].split()[3])
            zz = float(co.split("\n")[i].split()[4])
            
            for ii in range((i+1),cnt):
                if ii not in skip:
                    #distance between each 2 points in the 2 lists
                    diff = math.sqrt((float(co.split("\n")[i].split()[2])-float(co.split("\n")[ii].split()[2]))**2
                                     +(float(co.split("\n")[i].split()[3])-float(co.split("\n")[ii].split()[3]))**2
                                     +(float(co.split("\n")[i].split()[4])-float(co.split("\n")[ii].split()[4]))**2)
                    
                    #merging close points
                    if diff < 4*min(diff2,diff1):
                        
                        ish = ish + 1
                        xx = xx + float(co.split("\n")[ii].split()[2])
                        yy = yy + float(co.split("\n")[ii].split()[3])
                        zz = zz + float(co.split("\n")[ii].split()[4])
                        skip.append(ii)
                       
            if ish == 1:
                #if no close points found, current point is recorded on stand-alone line
                rew += co.split("\n")[i]+"\n"
            else:
                #merges close points into one line, with average location.
                x = xx / ish
                y = yy / ish
                z = zz / ish
                rew += co.split("\n")[ii].split()[0]+" "+co.split("\n")[ii].split()[1]
                rew +=" "+str(x)+" "+str(y)+" "+str(z)+"\n"

    return(rew)
                            

def symmetry(lp):
    #check if laminate is symmetric
    ori = lp
    ct = len(ori)
    
    i = 0
    sym = True
    while i < ct-1:

        if ori[i] != ori[ct-1-i]:
            sym = False 
        i = i + 1
    return(sym)

    
def balance(lp):
    #check if laminate is balanced
    
    #use list
    u = np.asarray([])
    for i in lp:
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
                            #print("deleting", tu[i])
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

        #break
        if len(tu) == 0:
            balance = True
            break
                  
    return(balance)
                    
            
           