# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 10:25:28 2022

@author: jakub.kucera
"""

import math
import time
import numpy as np
def flange_data(V,step_file,report = False):

    av = np.size(V,0)

    #thickness used to disregard some planes - source this better eventually
    t = 10

    P = np.zeros([1,8])
    #nested while loop to select 3 unique points from vertices and compare all possible 4ths
    i = 0
    while i < av-3:
        ii = i + 1
        while ii < av:
            iii = ii + 1
            while iii < av:
                
                #plane from 3 points define
                v1 = np.asarray([V[i,0]-V[ii,0],V[i,1]-V[ii,1],V[i,2]-V[ii,2]])
                v2 = np.asarray([V[i,0]-V[iii,0],V[i,1]-V[iii,1],V[i,2]-V[iii,2]])
                x_v1v2 = [v1[1]*v2[2]-v1[2]*v2[1], v1[2]*v2[0]-v1[0]*v2[2], v1[0]*v2[1]-v1[1]*v2[0]]

                d = -V[i,:].dot(x_v1v2)
                iv = iii+1
                while iv < av:

                    a = x_v1v2[0]
                    b = x_v1v2[1]
                    c = x_v1v2[2]
                    dist = abs((a * V[iv,0] + b * V[iv,1] + c * V[iv,2] + d))
                    e = (math.sqrt(a * a + b * b + c * c))
                    #print("Perpendicular distance is", dist/e)
                    #check if 4th point lies on plane
                    #if yes
                    if dist/e < 0.00001:
                        #check if all points are further than a thickness apart
                        
                        ppd = min(math.sqrt((V[i,0]-V[ii,0])**2+(V[i,1]-V[ii,1])**2+(V[i,2]-V[ii,2])**2),
                                    math.sqrt((V[i,0]-V[iii,0])**2+(V[i,1]-V[iii,1])**2+(V[i,2]-V[iii,2])**2),
                                    math.sqrt((V[i,0]-V[iv,0])**2+(V[i,1]-V[iv,1])**2+(V[i,2]-V[iv,2])**2),
                                    math.sqrt((V[ii,0]-V[iii,0])**2+(V[ii,1]-V[iii,1])**2+(V[ii,2]-V[iii,2])**2),
                                    math.sqrt((V[ii,0]-V[iv,0])**2+(V[ii,1]-V[iv,1])**2+(V[ii,2]-V[iv,2])**2),
                                    math.sqrt((V[iii,0]-V[iv,0])**2+(V[iii,1]-V[iv,1])**2+(V[iii,2]-V[iv,2])**2)
                                    )
                        if ppd > t:
                            #print(ppd)
                            #3 points refs, and plane definition recorded
                            temp = np.asarray([[i,ii,iii,iv,a,b,c,d]])
                            P = np.concatenate((P,temp),axis=0)
                        

                        #note down definition of the plane
                    iv = iv + 1
                iii = iii + 1
            ii = ii + 1
        i = i + 1
    P = np.delete(P,0,axis=0)
    print("with thickness limits I still have ",np.size(P,0)," planes")
    '''
    #remove duplicate planes (would break the paralelism check below!)
    i = 0
    while i < np.size(P,0)-1:
        ii = i + 1
        while ii < np.size(P,0):
            if P[ii,4] != 0:
                rat = P[i,4]/P[ii,4]
                Pi = P[ii,:]*rat
            elif P[ii,5] != 0:
                rat = P[i,5]/P[ii,5]
                Pi = P[ii,:]*rat   
            elif P[ii,6] != 0:
                rat = P[i,6]/P[ii,6]
                Pi = P[ii,:]*rat 
            print(rat)
            if  abs(P[i,0] - Pi[0]) < 0.1:
                if abs(P[i,1] - Pi[1]) < 0.1:
                    if abs(P[i,2] - Pi[2]) < 0.1:
                        if abs(P[i,3] - Pi[3]) < 0.1:
                    
                            P = np.delete(P,ii,axis=0)
                            print("duplicate found")
                            ii = ii - 1
            ii = ii + 1
        i = i + 1

    '''
    
    #only keep planes that have parallel plane availabe (only keep 1)
    i = 0
    Pf = np.zeros([1,8])
    while i < np.size(P,0)-1:
        ii = i + 1
        while ii < np.size(P,0):
            if P[i,4] == 0:
                if P[i,5] ==0:
                    #if both a and b are 0 than normal is always the same
                    print("this 1")
                    yc = 0
                    zc = 0
                #yc replacement check addind P[ii,3]=0 as well
                else:
                    print("this 2")
                    rat = P[ii,5]/P[i,5]
                    yc = P[ii,4] 
                    zc = P[i,6]*rat - P[ii,6]
            
            else:
                print("this 3")
                #if x != 0 simply scale x value to be equivalent and compare other members
                rat = P[ii,4]/P[i,4]
                yc = P[i,5]*rat - P[ii,5]
                zc = P[i,6]*rat - P[ii,6]
            if yc < 0.0000001 and zc < 0.000000001:
                
                temp = np.array([P[i,:]])
                Pf = np.concatenate((Pf,temp),axis=0)
                P = np.delete(P,ii,axis=0)
            ii = ii + 1
        i = i + 1
    '''
    #now that all the remaining planes are from parallel origin, all additional parallels and origins need to be removed
    i = 0
    while i < np.size(Pf,0)-1:
        ii = i + 1
        while ii < np.size(Pf,0):
            if Pf[i,4] == 0:
                if Pf[i,5] ==0:
                    #yc replacement check for both a,b being 0
                    yc = Pf[ii,4] + Pf[ii,5]
                    zc = Pf[i,6] - Pf[ii,6]
                #yc replacement check addind P[ii,3]=0 as well
                else:
                    rat = Pf[ii,5]/Pf[i,5]
                    yc = Pf[ii,4] 
                    zc = Pf[i,6]*rat - Pf[ii,6]
            
            else:
                rat = Pf[ii,4]/Pf[i,4]
                yc = Pf[i,5]*rat - Pf[ii,5]
                zc = Pf[i,6]*rat - Pf[ii,6]
            if yc < 0.001 and zc < 0.001:
                Pf = np.delete(Pf,ii,axis=0)
            ii = ii + 1
        i = i + 1
        
    Pf = np.delete(Pf,0,axis=0)
    print(Pf)
    print(np.size(Pf,0))
    '''
    #Pf = P

    #temporary CATIA display fro troubleshooting
    import win32com.client.dynamic
    import os
    CATIA = win32com.client.Dispatch("CATIA.Application")
    #record deletion of product....

    documents1 = CATIA.Documents
    partDocument1 = documents1.Add("Part")
    part1 = partDocument1.Part
    #Shape factory provides generating of shapes
    ShFactory = part1.HybridShapeFactory
    # Starting new body (geometrical set) in part1
    bodies1 = part1.HybridBodies
    i = 0
    while i < np.size(Pf,0):
        # Adding new body to part1
        body1 = bodies1.Add()
        # Naming new body as "wireframe"
        body1.Name="x"+str(i)

        #create 4 base points based on coordinates
        rf = int(Pf[i,0])
        p = V[rf,:]
        point=ShFactory.AddNewPointCoord(p[0],p[1],p[2])
        body1.AppendHybridShape(point) 
        ref1 = part1.CreateReferenceFromObject(point)
        
        rf = int(Pf[i,1])
        p = V[rf,:]
        point=ShFactory.AddNewPointCoord(p[0],p[1],p[2])
        body1.AppendHybridShape(point) 
        ref2 = part1.CreateReferenceFromObject(point)

        rf = int(Pf[i,2])
        p = V[rf,:]
        point=ShFactory.AddNewPointCoord(p[0],p[1],p[2])
        body1.AppendHybridShape(point) 
        ref3 = part1.CreateReferenceFromObject(point)
        
        rf = int(Pf[i,3])
        p = V[rf,:]
        point=ShFactory.AddNewPointCoord(p[0],p[1],p[2])
        body1.AppendHybridShape(point) 
        ref4 = part1.CreateReferenceFromObject(point)
    

        i = i + 1

    # imported vertices split into the two main planes

    #split all imported vertices into plane groups (plane group only works if more than 3 on same plane)

    #only consider planes where all points are further than thickness appart (to eliminate side walls)

    #only consider planes that have matching parallel plane (to eliminate diagonal planes)

    #this should leave you with only 3 planes available

    #here you need some testing to see that the correct planes are getting picked up

    #find the maximum angle between these surfaces - that is the angle

    #find the radii close to the 3rd surface (unused in max angle), that is the fillet radius

    # find angle between planes
    # and how fillet? 

    return(flange)






'''


    #temporary CATIA display fro troubleshooting
    import win32com.client.dynamic
    import os
    CATIA = win32com.client.Dispatch("CATIA.Application")
    #record deletion of product....

    documents1 = CATIA.Documents
    partDocument1 = documents1.Add("Part")
    part1 = partDocument1.Part
    #Shape factory provides generating of shapes
    ShFactory = part1.HybridShapeFactory
    # Starting new body (geometrical set) in part1
    bodies1 = part1.HybridBodies
    i = 0
    while i < len(FACES):
        x = float(FACES[i].edges[0].vertices[0].x)
        y = float(FACES[i].edges[0].vertices[0].y)
        z = float(FACES[i].edges[0].vertices[0].z)
        p = np.asarray([x,y,z])

        # Adding new body to part1
        body1 = bodies1.Add()
        # Naming new body as "wireframe"
        body1.Name="x"+str(i)


        point=ShFactory.AddNewPointCoord(p[0],p[1],p[2])
        body1.AppendHybridShape(point) 
        ref1 = part1.CreateReferenceFromObject(point)
        
        x = float(FACES[i].edges[0].vertices[1].x)
        y = float(FACES[i].edges[0].vertices[1].y)
        z = float(FACES[i].edges[0].vertices[1].z)
        p = np.asarray([x,y,z])
        

        point=ShFactory.AddNewPointCoord(p[0],p[1],p[2])
        body1.AppendHybridShape(point) 
        ref2 = part1.CreateReferenceFromObject(point)
        
        x = float(FACES[i].edges[2].vertices[0].x)
        y = float(FACES[i].edges[2].vertices[0].y)
        z = float(FACES[i].edges[2].vertices[0].z)
        p = np.asarray([x,y,z])

        point=ShFactory.AddNewPointCoord(p[0],p[1],p[2])
        body1.AppendHybridShape(point) 
        ref3 = part1.CreateReferenceFromObject(point)

        x = float(FACES[i].edges[2].vertices[1].x)
        y = float(FACES[i].edges[2].vertices[1].y)
        z = float(FACES[i].edges[2].vertices[1].z)
        p = np.asarray([x,y,z])
        
        
        point=ShFactory.AddNewPointCoord(p[0],p[1],p[2])
        body1.AppendHybridShape(point) 
        ref4 = part1.CreateReferenceFromObject(point)
    

        i = i + 1
        
        
        '''
        
        
      # for assessment of face classes collected  
        
            
    '''
    i = 0
    while i < len(FACES):
        print("face number: "+str(FACES[i].ref))
        print("face plane:", FACES[i].plane)
        

        
        ii = 0
        while ii < len(FACES[i].edges):
            print("edge ref" , FACES[i].edges[ii].ref)
            iii = 0
            while iii < len(FACES[i].edges[ii].vertices):
                print("vertex:",FACES[i].edges[ii].vertices[iii].ref, FACES[i].edges[ii].vertices[iii].x, FACES[i].edges[ii].vertices[iii].y,FACES[i].edges[ii].vertices[iii].z)
                iii = iii + 1
            ii = ii + 1
        i = i + 1
            #continue here, better printouts to check that collection is correct
            #check that unique points are being stored

    '''
    '''
    
def step_reclassification_x(step_file):
    t1_start = perf_counter()
    #collect all faces as classess, with nested atribute classes
    with open(step_file, "r") as text_file:
        f = text_file.read()
        fc = f.count("\n")
    
    circ = 0
    FACES = []
    i = 0 
    #loops through all lines looking for faces
    while i < fc:
        #split the document into lines for search
        line = f.split("\n")[i]
        
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
            ii = 0
            while ii < fc:
                l1 = f.split("\n")[ii]
                
                #when the outbound reference is found
                if temp1 in l1:
                    t2 = l1.split("#")[2]
                    t2 = t2.split(",")[0]
                    t2 = "#"+t2+"="
                    
                    #loop using the border reference
                    iii = 0
                    while iii < fc:

                        l2 = f.split("\n")[iii]
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
                                iv = 0
                                #oriented edge reference
                                while iv < fc:

                                    l3 = f.split("\n")[iv]
                                    #find edge curve line
                                    if t3 in l3:
                                        t4 = l3.split("#")[2]
                                        t4 = t4.split(",")[0]
                                        t4 = "#"+t4+"="
                                        
                                        v = 0
                                        #for each point referenced on the edge curve
                                        while v < fc:

                                            l4 = f.split("\n")[v]
                                            
                                            if t4 in l4:
                                                c2 = l4.count("#")
                                                #loop through points relevant to edge
                                                yy = 2
                                                while yy < c2+1:
                                                    
                                                    t5 = l4.split('#')[yy]
                                                    t5 = t5.split(",")[0]
                                                    t5_raw = t5
                                                    t5 = "#"+t5+"="
                                                    
                                                    vi = 0
                                                    #initial vertex reference
                                                    while vi < fc:
                                                        l5 = f.split("\n")[vi]
                                                        if t5 in l5 and "VERTEX_POINT" in l5:
                                                            t6 = l5.split('#')[2]
                                                            t6 = t6.split(")")[0]
                                                            t6 = "#"+t6+"="
                                                            
                                                            vii = 0
                                                            #looking for lines with specific x,y,z based on vertex ref.
                                                            while vii < fc:
                                                                l6 = f.split("\n")[vii]
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
                                                                vii = vii + 1                                                                                                                               
                                                        vi = vi + 1
                                                    yy = yy + 1
                                            v = v + 1
                                    iv = iv + 1  
                                
                                #calculate the distance between vertices
                                se.len = math.sqrt((float(se.vertices[0].x) - float(se.vertices[1].x))**2 +
                                                   (float(se.vertices[0].y) - float(se.vertices[1].y))**2 +
                                                   (float(se.vertices[0].z) - float(se.vertices[1].z))**2)                                      
                                FACE.edges.append(se)  
                                circ = circ + se.len
                                k = k + 1
                        iii = iii + 1
                ii = ii + 1
                
                
            
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


        i = i + 1
    print("Faces collected")
    # Stop the stopwatch / counter
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start)
    
    return(FACES)
'''