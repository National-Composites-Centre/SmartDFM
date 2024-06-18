# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 15:27:43 2022

@author: jakub.kucera
"""

import math
import time
import numpy as np
from time import perf_counter

class step_edge:
    #edges as defined in step file, belonging to faces
    def __init__(self, ref = 0, vertices = []):
        self.ref = 0
        self.vertices = []
        self.len = 0
    
class step_face:
    #faces as defined in step file
    def __init__(self, ref = 0 ,out_bound_ref = 0 ,edges = [],plane = np.array([0,0,0,0]),circumference = 0):
        self.ref = 0
        self.out_bound_ref = 0
        self.edges = []
        self.plane = np.array([0,0,0,0])
        self.circumference = 0
        self.bol = 0
    
    
class step_vertex:
    #vertices, the lowest level of geometry in step file
    def __init__(self, x = 0,y = 0,z = 0):
        self.x = 0
        self.y = 0
        self.z = 0
        
class step_circle:
    #CIRCLE('generated circle'
    def __init__(self, ref=0, oref=0,centre = [999,999,999], r = 0):
        #reference to lookup in step file
        ref = 0
        oref = 0
        #radius (mm?)
        centre = [999,999,999]
        r = 0

def circ_reclass(step_file):
    t1_start = perf_counter()
    
    with open(step_file, "r") as text_file:
        f = text_file.read()
        #fc = f.count("\n")    
    
    CIRCs = []
    for l1 in f.split("\n"):
        if "CIRCLE('generated circle'" in l1:
            t1 = l1.split('=')[0]
            t1 = t1.split('#')[1]
            
            CIRC = step_circle()
            CIRC.ref = int(t1)
            
            t2 = l1.split('#')[2]
            t2 = t2.split(',')[0]
            CIRC.oref = int(t2)
            
            t3 = l1.split('#')[2]
            t3 = t3.split(',')[1]
            t3 = t3.split(')')[0]
            CIRC.r = float(t3)
            
            t2 = "#"+t2+"="
            
            for l2 in f.split("\n"):
                if t2 in l2:
                    t4 = l2.split("#")[2]
                    t4 = t4.split(',')[0]
                    t4 = "#"+str(t4)+"="
                    #t5 = l2.split('#')[3]
                    #t5 = t5.split(',')[0]
                    
                    for l3 in f.split("\n"):
                        if t4 in l3:
                            t6 = l3.split("Location',(")[1]
                            x = t6.split(",")[0]
                            
                            y = t6.split(",")[1]
                            z = t6.split(",")[2]
                            z = z.split(")")[0]
                            
                            CIRC.centre = [x, y, z]
            CIRCs.append(CIRC)
    t1_stop = perf_counter()
    print("Circles collected in:", t1_stop - t1_start)                    
    return(CIRCs)
                    
                    
            #continue here ... next reference go through, let the nesting begin
    
    

def step_reclassification(step_file):
    t1_start = perf_counter()
    #collect all faces as classess, with nested atribute classes
    with open(step_file, "r") as text_file:
        f = text_file.read()
        #fc = f.count("\n")
    
    circ = 0
    FACES = []
 
    #loops through all lines looking for faces
    #split the document into lines for search
    for line in f.split("\n"):

        #When line contains face reference.
        if "ADVANCED_FACE" in line:
            #reference to point of the outbound_surf_ref

            temp1 = line.split("#")[2]
            temp1 = temp1.split(")")[0]


            FACE = step_face()
            try:
                FACE.out_bound_ref = int(temp1)
            except:
                temp1 = temp1.split(",")[0]
                FACE.out_bound_ref = int(temp1)
            #reference of the actual face
            t1 = line.split("=")[0]
            t1 = t1.split("#")[1]
            FACE.ref = int(t1)
            
            bolXcnt = line.count("#")
            bolX = line.split("#")[bolXcnt]
            bolX = bolX.split(".")[1]
            if bolX == "T":
                FACE.bol = True
            elif bolX == "F":
                FACE.bol = False
            
            #adjust reference for follow up search
            temp1 = "#"+temp1+"="
            
            #loop the document again for lines with follow up face reference
            #ii = 0
            #while ii < fc:
            for l1 in f.split("\n"):
                #l1 = f.split("\n")[ii]
                
                #when the outbound reference is found
                if temp1 in l1:
                    t2 = l1.split("#")[2]
                    t2 = t2.split(",")[0]
                    t2 = "#"+t2+"="
                    
                    #loop using the border reference
                    #iii = 0
                    #while iii < fc:
                    for l2 in f.split("\n"):

                        #l2 = f.split("\n")[iii]
                        #when the list of edges is found
                        if t2 in l2:
                            #loop through the line based on number of edges
                            c1 = l2.count("#")
                            k = 2
                            
                            while k < c1+1:

                                t3 = l2.split("#")[k]
                                #accomodate for end of line string manipulation
                                if k == c1:
                                    t3 = t3.split(")")[0]
                                else:
                                    t3 = t3.split(",")[0]
                                se = step_edge()
                                se.ref = int(t3)
    
                                t3 = "#"+t3+"="
                                #for each edge
                                #v = 0
                                #oriented edge reference
                                #while iv < fc:
                                for l3 in f.split("\n"):

                                    #l3 = f.split("\n")[iv]
                                    #find edge curve line
                                    if t3 in l3:
                                        t4 = l3.split("#")[2]
                                        t4 = t4.split(",")[0]
                                        t4 = "#"+t4+"="
                                        
                                        #v = 0
                                        #for each point referenced on the edge curve
                                        #while v < fc:
                                        for l4 in f.split("\n"):

                                            #l4 = f.split("\n")[v]
                                            
                                            if t4 in l4:
                                                c2 = l4.count("#")
                                                #loop through points relevant to edge
                                                yy = 2
                                                while yy < c2+1:
                                                    
                                                    t5 = l4.split('#')[yy]
                                                    t5 = t5.split(",")[0]
                                                    t5_raw = t5
                                                    t5 = "#"+t5+"="
                                                    
                                                    #vi = 0
                                                    #initial vertex reference
                                                    #while vi < fc:
                                                    for l5 in f.split("\n"):
                                                        #l5 = f.split("\n")[vi]
                                                        if t5 in l5 and "VERTEX_POINT" in l5:
                                                            t6 = l5.split('#')[2]
                                                            t6 = t6.split(")")[0]
                                                            t6 = "#"+t6+"="
                                                            
                                                            #vii = 0
                                                            #looking for lines with specific x,y,z based on vertex ref.
                                                            #while vii < fc:
                                                            for l6 in f.split("\n"):
                                                                #l6 = f.split("\n")[vii]
                                                                if t6 in l6:
                                                                    t7 = l6.split("('Vertex',(")[1]
                                                                    
                                                                    #create vertex class
                                                                    sv = step_vertex()
                                                                    #assign coordinates to vertex
                                                                    sv.x = t7.split(",")[0]
                                                                    sv.y = t7.split(",")[1]
                                                                    z = t7.split(",")[2]
                                                                    sv.z = z.split(")")[0]
                                                                    #assing reference to vertex
                                                                    sv.ref = int(t5_raw) 
                                                                    se.vertices.append(sv)                                                  
                                                                #vii = vii + 1                                                                                                                               
                                                        #vi = vi + 1
                                                    yy = yy + 1
                                            #v = v + 1
                                    #iv = iv + 1  
                                
                                #calculate the distance between vertices
                                se.len = math.sqrt((float(se.vertices[0].x) - float(se.vertices[1].x))**2 +
                                                   (float(se.vertices[0].y) - float(se.vertices[1].y))**2 +
                                                   (float(se.vertices[0].z) - float(se.vertices[1].z))**2)                                      
                                FACE.edges.append(se)  
                                circ = circ + se.len
                                k = k + 1
                        #iii = iii + 1
                #ii = ii + 1
                
                
            
            V1 = np.asarray([[float(FACE.edges[0].vertices[0].x), float(FACE.edges[0].vertices[0].y), float(FACE.edges[0].vertices[0].z)],
                             [float(FACE.edges[0].vertices[1].x), float(FACE.edges[0].vertices[1].y), float(FACE.edges[0].vertices[1].z)],
                             [float(FACE.edges[1].vertices[0].x), float(FACE.edges[1].vertices[0].y), float(FACE.edges[1].vertices[0].z)]])
            #check if 2nd edge point is the same as one of the first:
            
            e = 0
            while (V1[0,:] == V1[2,:]).all() or (V1[1,:] == V1[2,:]).all():
                
                V1[2,:] = np.asarray([float(FACE.edges[e].vertices[1].x), float(FACE.edges[e].vertices[1].y), float(FACE.edges[e].vertices[1].z)])
                e = e + 1         
                            
            #notes from below the else.....
            #find plane equation
            v1 = np.asarray([V1[0,0]-V1[1,0],V1[0,1]-V1[1,1],V1[0,2]-V1[1,2]])
            v2 = np.asarray([V1[0,0]-V1[2,0],V1[0,1]-V1[2,1],V1[0,2]-V1[2,2]])
            x_v1v2 = [v1[1]*v2[2]-v1[2]*v2[1], v1[2]*v2[0]-v1[0]*v2[2], v1[0]*v2[1]-v1[1]*v2[0]]

            d = -V1[0,:].dot(x_v1v2)
            
            pd = np.asarray([x_v1v2[0],x_v1v2[1],x_v1v2[2],d])
            #print(pd)
            
            #second of the same calculation with different point for comparison
            
            V1 = np.asarray([[float(FACE.edges[3].vertices[0].x), float(FACE.edges[3].vertices[0].y), float(FACE.edges[3].vertices[0].z)],
                             [float(FACE.edges[3].vertices[1].x), float(FACE.edges[3].vertices[1].y), float(FACE.edges[3].vertices[1].z)],
                             [float(FACE.edges[0].vertices[0].x), float(FACE.edges[0].vertices[0].y), float(FACE.edges[0].vertices[0].z)]])
            #check if 2nd edge point is the same as one of the first:
            
            e = 0
            while (V1[0,:] == V1[2,:]).all() or (V1[1,:] == V1[2,:]).all():
                
                V1[2,:] = np.asarray([float(FACE.edges[e].vertices[1].x), float(FACE.edges[e].vertices[1].y), float(FACE.edges[e].vertices[1].z)])
                e = e + 1         
                            
            #notes from below the else.....
            #find plane equation
            v1 = np.asarray([V1[0,0]-V1[1,0],V1[0,1]-V1[1,1],V1[0,2]-V1[1,2]])
            v2 = np.asarray([V1[0,0]-V1[2,0],V1[0,1]-V1[2,1],V1[0,2]-V1[2,2]])
            x_v1v2 = [v1[1]*v2[2]-v1[2]*v2[1], v1[2]*v2[0]-v1[0]*v2[2], v1[0]*v2[1]-v1[1]*v2[0]]

            d = -V1[0,:].dot(x_v1v2)
            
            pd2 = np.asarray([x_v1v2[0],x_v1v2[1],x_v1v2[2],d])
            #print(pd2)          
            
            ch1 = pd-pd2
            ch2 = pd+pd2
            
            if (-0.0001 < ch1.all() < 0.0001) or (-0.0001 < ch2.all() < 0.0001) :
                #plane verified by 2 calculations
                #print("plane flat confirmed")
                FACE.plane = pd
            else:
                print("face plane is not flat, or ... bug. FACE.plane not recorded for face reference:" , FACE.ref)
                
                
            #all collected edges summed for face circumference
            FACE.circumference = circ
            #andreset counter
            circ = 0
            
            FACES.append(FACE)


        #i = i + 1
    print("Faces collected")
    # Stop the stopwatch / counter
    t1_stop = perf_counter()
    print("Faces collected in:", t1_stop - t1_start," seconds")
    
    return(FACES)

#step_file ="D:\CoSinC_WP4.2\TestCad\s-5029.stp"
#step_reclassification(step_file)    