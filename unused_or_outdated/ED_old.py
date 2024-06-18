# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 10:31:01 2022

@author: jakub.kucera
"""

import numpy as np
from numpy.linalg import norm

#location of hole
def dd(p1,p2,p3):
    #distance between pt1-pt2 vector to pt3
    d = norm(np.cross(p2-p1, p1-p3))/norm(p2-p1)
    return(d)

pts = np.matrix([[75,80,0],
                [75,80,2]])
#source vertices (this should be an input here)
VER = np.matrix([[0.0,0.0,0.0],
                [0.0,100.0,0.0],
                [100.0,100.0,0.0],
                [100.0,0.0,0.0],
                [0.0,0.0,2.0],
                [0.0,100.0,2.0],
                [100.0,100.0,2.0],
                [100.0,0.0,2.0]])

#jm =0
#ED2 doest check if the vertices used for edges belogn to the correct shape, ED does
with open("D:\\CAD_library_sampling\\special cases\\s_1_he.stp", "r") as text_file:
    f = text_file.read()
    fc = f.count("\n")
    print(fc)
md = 99999999999    
f1 = 0 
while f1 < fc:
    line = f.split("\n")[f1]


#for line in text_file:
    b1 = False
    b2 = False
    if "EDGE_CURVE" in line:
        
        tp = line.split("=")[1]
        c = tp.count('#')
        #print(c)
        i = 0 
        j = 0
        while i < c:
            no1 = tp.split("#")[i+1]
            no1 = no1.split(',')[0]
            
            ex = "#"+no1+"="
            
            f2 = 0
            while f2 < fc:
                l = f.split("\n")[f2]
            #for l in text_file:
                if ex in l:

                    if "VERTEX_POINT" in l:

                        ex2 = l.split("#")[2]
                        ex2 = ex2.split(")")[0]
                        
                        ex2 = '#'+ex2+"="
                        
                        f3 = 0
                        while f3 < fc:
                            l2 = f.split("\n")[f3]
                        #for l2 in text_file:
                            
                            if ex2 in l2:

                                ex3 = l2.split("""('Vertex',(""")[1]
                                ex3 = ex3.split("))")[0]
                                x = float(ex3.split(",")[0])
                                y = float(ex3.split(",")[1])
                                z = float(ex3.split(",")[2])
                                
                                ii = 0
                                
                                while ii < np.size(VER,0):
                                    #print(np.matrix([[x,y,z]]))
                                    #print(VER[ii,:])
                                    if x == VER[ii,0] and y == VER[ii,1] and z == VER[ii,2]:
                                        j = j + 1
                                        if b1 == False:
                                            b1 = True
                                        else:
                                            b2 = True
                                    ii = ii + 1
                            f3 = f3 + 1
                        if j == 1:
                            jm = np.matrix([[x,y,z]])
                        elif j > 1:
                            jm = np.concatenate((jm,np.matrix([[x,y,z]])),axis=0)
                            
                                    
                                    
                                # compare this x,y,z to vertices provided
                                                                                           
                f2 = f2 + 1                        
            i = i + 1
        if b1 == True and b2 == True:
            #print(jm)
            #find distance between vector and point ...
            iii = 0
            
            while iii < np.size(pts,0):
                p1 = np.matrix([jm[0,0], jm[0,1],jm[0,2]])
                p2 = np.matrix([jm[1,0], jm[1,1],jm[1,2]])
                p3 = np.matrix([pts[iii,0], pts[iii,1],pts[iii,2]])
                d = dd(p1,p2,p3)
                iii = iii + 1
                if d < md:
                    md = d
        
    f1 = f1 + 1  

print(md)
#go through all "EDGE_CURVE" lines in the appropriate stl
    #for each line
        #check references, if all vertex references correspond to the list
            #obtain the vector
            #find closest distance between vector and point
            #is this the shortest distance?
            
#compare distance to what is allowed (given hole dia and material)