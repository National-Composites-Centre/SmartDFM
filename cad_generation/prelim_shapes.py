# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 16:16:21 2022

@author: jakub.kucera
"""

#collection of CATIA modules that generate simple features
#Library generated feeds into feature recognition algorithm.

import win32com.client.dynamic
import numpy as np
import math
import random
from vecEX2_C import wrmmm
from wp4_utils import stl_vertex
import os

def h1(M):
    #Processing used for most of the shapes
    #central point
    c = (np.asarray([M[4,:]+M[5,:]+M[6,:]+M[7,:]]))/4
    
    # vec3
    ab = np.asarray([[M[5,0]-M[4,0],M[5,1]-M[4,1],M[5,2]-M[4,2]]])
    ac = np.asarray([[M[6,0]-M[4,0],M[6,1]-M[4,1],M[6,2]-M[4,2]]])
    # z vector normal to plane
    vec3 = np.cross(ab,ac)
    u_v3 = vec3 / np.linalg.norm(vec3)
    return(ab,ac,vec3,u_v3,c)

def part2(CATIA):
    #CATIA instance definition, important to output vertices for each feature.
    
    documents1 = CATIA.Documents
    partDocument1 = documents1.Add("Part")
    part1 = partDocument1.Part
    #Shape factory provides generating of shapes
    ShFactory = part1.HybridShapeFactory
    # Starting new body (geometrical set) in part1
    bodies1 = part1.HybridBodies
    # Adding new body to part1
    body1 = bodies1.Add()
    # Naming new body as "wireframe"
    body1.Name="Points n Lines"
    # Surfaces group
    body3 = bodies1.Add()
    body3.Name="Surfaces"
    body007 = bodies1.Add()
    body007.Name="SourceLoft"
    
    #hide the geometric set
    selection1 = partDocument1.Selection
    selection1.Clear() # added recently delete if error
    visPropertySet1 = selection1.VisProperties
    part1 = partDocument1.Part
    hybridBodies1 = part1.HybridBodies
    hybridBody1 = hybridBodies1.Item("Points n Lines")
    #hybridBodies1 = hybridBody1.Parent
    selection1.Add(hybridBody1)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)
    selection1.Clear()
    
    return(body1,ShFactory,body3, part1,bodies1,partDocument1)

def storage(x,y,z,file,ref):
    #saves vertices for current shape, including notes on which shapes each 
    #vertex relates to
    lisT = ["-","box","taper","flange","omega","hole","pin"]
    p1 = lisT[ref[0]]
    p2 = lisT[ref[1]]
    #repeated use of this function keeps closing and opening same file, 
    #might need to rework
    with open(file, "a") as text_file:
        text_file.write(str(x)+","+str(y)+","+str(z)+","+str(p1)+","+str(p2)+"\n")
        
    


def box(body1,ShFactory,body3,part1,bodies1,partDocument1,ii, M,file,instructions,CATIA):
    #simple box with no tapers
    
    iii = 0
    while iii < 2:
        
        if iii == 0:
            #Three variables used to create box:
            #proportional size in x
            o =  random.uniform(0.5, 1)
            #proportional size in y
            p =  random.uniform(0.5, 1)
            #proportional size in z
            q =  random.uniform(0.5, 1) 
            zmax = 20
            z = zmax*q
            
            ab,ac,vec3,u_v3,c = h1(M)
            
        
            #base points
            p1 = c - 0.5*o*ab - 0.5*p*ac
            p2 = c + 0.5*o*ab - 0.5*p*ac 
            p3 = c - 0.5*o*ab + 0.5*p*ac
            p4 = c + 0.5*o*ab + 0.5*p*ac
            
            '''
            #implement 20% chance to use previous 4 points as base
            if ii == 1 and random.uniform(0,1) < 0.2:
              p1 = c - 0.5*ab - 0.5*ac
              p2 = c + 0.5*ab - 0.5*ac 
              p3 = c - 0.5*ab + 0.5*ac
              p4 = c + 0.5*ab + 0.5*ac
              print("20 percent chance active")
            '''
              
        else:
            body1,ShFactory,body3, part1,bodies1,partDocument1 = part2(CATIA)
                
        #create 4 base points based on coordinates
        point=ShFactory.AddNewPointCoord(p1[0,0],p1[0,1],p1[0,2])
        body1.AppendHybridShape(point) 
        ref1 = part1.CreateReferenceFromObject(point)
        
        point=ShFactory.AddNewPointCoord(p2[0,0],p2[0,1],p2[0,2])
        body1.AppendHybridShape(point) 
        ref2 = part1.CreateReferenceFromObject(point)
    
        point=ShFactory.AddNewPointCoord(p3[0,0],p3[0,1],p3[0,2])
        body1.AppendHybridShape(point) 
        ref3 = part1.CreateReferenceFromObject(point)
        
        point=ShFactory.AddNewPointCoord(p4[0,0],p4[0,1],p4[0,2])
        body1.AppendHybridShape(point) 
        ref4 = part1.CreateReferenceFromObject(point)
    
        #create two lines to create base of the box
        l1 = ShFactory.AddNewLinePtPt(ref1, ref2)
        body1.AppendHybridShape(l1)
        ref33 = part1.CreateReferenceFromObject(l1)
        
        l2 = ShFactory.AddNewLinePtPt(ref3, ref4)
        body1.AppendHybridShape(l2)
        ref44 = part1.CreateReferenceFromObject(l2)
    
        #connect the two lines
        loft1 = ShFactory.AddNewLoft()
        loft1.SectionCoupling = 1
        loft1.Relimitation = 1
        loft1.CanonicalDetection = 2
        loft1.AddSectionToLoft(ref33, 1,None)
        loft1.AddSectionToLoft(ref44, 1,None)
        body1.AppendHybridShape(loft1)
        ref5 = part1.CreateReferenceFromObject(loft1)
    
        #setup for working with solids
        bodies1 = part1.Bodies
        B1 = bodies1.Item("PartBody")
        part1.InWorkObject = B1
        ref6 = part1.CreateReferenceFromName("")
        shapeFactory1 = part1.ShapeFactory
        
        #create a solid by adding thickness
        th = shapeFactory1.AddNewThickSurface(ref6, 0, z, 0.000000)
        th.Surface = ref5
        part1.UpdateObject(th)
        if iii == 0:
        #collect points for the top of the box, and add them to passed matrix
            p5 = p1 + z*u_v3
            p6 = p2 + z*u_v3
            p7 = p3 + z*u_v3
            p8 = p4 + z*u_v3
            M = np.concatenate((p1,p2,p3,p4,p5,p6,p7,p8),axis=0)
            
            #No nodes are shared for the first shape
            #if ii == 0:
            #    ref = [1,0]
            #Sharing of nodes of subsequent shapes noted
            #else:
            #    ref = [1,instructions[0]]
            
            #storage(M[0,0],M[0,1],M[0,2],file,ref)
            #storage(M[1,0],M[1,1],M[1,2],file,ref)
            #storage(M[2,0],M[2,1],M[2,2],file,ref)
            #storage(M[3,0],M[3,1],M[3,2],file,ref)
            
            #last 4 vertices never shared between shapes
            #ref = [1,0]
            #storage(M[4,0],M[4,1],M[4,2],file,ref)
            #storage(M[5,0],M[5,1],M[5,2],file,ref)
            #storage(M[6,0],M[6,1],M[6,2],file,ref)
            #storage(M[7,0],M[7,1],M[7,2],file,ref)
            
        else:
                    
            #save the CAD file, and export it as .stp
            #ilo = "D:\\CAD_library_sampling\\temp\\temp.CatPart"
            #partDocument1.SaveAs(silo)
            location = "D:\\CAD_library_sampling\\temp\\temp.stp"
            partDocument1.ExportData(location, "stp")
            partDocument1.Close()
            
            VRTs = stl_vertex(location)
            
            os.remove(location)
    
        iii = iii + 1
    return(M,VRTs)


def taper(body1, ShFactory, body3,part1,bodies1,partDocument1,ii,M,file,instructions,CATIA):
    
    iii = 0
    while iii < 2:
        
        if iii == 0:
            #Four variables used to create box, with taper:
            #proportional size in x
            o =  random.uniform(0.5, 1)
            #proportional size in y
            p =  random.uniform(0.5, 1)
            #proportional size in z
            q =  random.uniform(0.5, 1)
            #maximum thickness
            zmax = 20
            z = zmax*q   
            #relative taper of the two sides
            T = random.uniform(0.01,0.99)
            
            ab,ac,vec3,u_v3,c = h1(M)
        
            #base points
            p1 = c - 0.5*o*ab - 0.5*p*ac
            p2 = c + 0.5*o*ab - 0.5*p*ac 
            p3 = c - 0.5*o*ab + 0.5*p*ac
            p4 = c + 0.5*o*ab + 0.5*p*ac
            '''
            #implement 20% chance to use previous 4 points as base
            if ii == 1 and random.uniform(0,1) < 0.2:
              p1 = c - 0.5*ab - 0.5*ac
              p2 = c + 0.5*ab - 0.5*ac 
              p3 = c - 0.5*ab + 0.5*ac
              p4 = c + 0.5*ab + 0.5*ac
              print("20 percent chance active")
            '''
        else:

            body1,ShFactory,body3, part1,bodies1,partDocument1 = part2(CATIA)
        
        #top surface points
        p5 = p1 + z*u_v3*T
        p6 = p2 + z*u_v3*T
        p7 = p3 + z*u_v3
        p8 = p4 + z*u_v3
        #to pass points for next shape if needed
        M = np.concatenate((p1,p2,p3,p4,p5,p6,p7,p8),axis=0)
    
        #generate 4 point for the side face (including taper)
        point=ShFactory.AddNewPointCoord(p1[0,0],p1[0,1],p1[0,2])
        body1.AppendHybridShape(point) 
        ref1 = part1.CreateReferenceFromObject(point)
        
        point=ShFactory.AddNewPointCoord(p5[0,0],p5[0,1],p5[0,2])
        body1.AppendHybridShape(point) 
        ref2 = part1.CreateReferenceFromObject(point)
    
        point=ShFactory.AddNewPointCoord(p7[0,0],p7[0,1],p7[0,2])
        body1.AppendHybridShape(point) 
        ref3 = part1.CreateReferenceFromObject(point)
        
        point=ShFactory.AddNewPointCoord(p3[0,0],p3[0,1],p3[0,2])
        body1.AppendHybridShape(point) 
        ref4 = part1.CreateReferenceFromObject(point)   
        
        #create 4 lines to create side face
        l1 = ShFactory.AddNewLinePtPt(ref1, ref2)
        body1.AppendHybridShape(l1)
        ref11 = part1.CreateReferenceFromObject(l1)
        
        l1 = ShFactory.AddNewLinePtPt(ref2, ref3)
        body1.AppendHybridShape(l1)
        ref22 = part1.CreateReferenceFromObject(l1)
        
        l1 = ShFactory.AddNewLinePtPt(ref3, ref4)
        body1.AppendHybridShape(l1)
        ref33 = part1.CreateReferenceFromObject(l1)    
        
        l1 = ShFactory.AddNewLinePtPt(ref4, ref1)
        body1.AppendHybridShape(l1)
        ref44 = part1.CreateReferenceFromObject(l1)
        
        #create the side face by connecting the 4 lines into a fill
        f1 = ShFactory.AddNewFill()
        f1.AddBound(ref11)
        f1.AddBound(ref22)
        f1.AddBound(ref33)
        f1.AddBound(ref44)
        f1.Continuity = 1
        f1.Detection = 2 
        f1.AdvancedTolerantMode = 2
        body1.AppendHybridShape(f1)
        part1.InWorkObject = f1
        ref5 = part1.CreateReferenceFromObject(f1)
    
        #setup for solid modelling
        bodies1 = part1.Bodies
        B1 = bodies1.Item("PartBody")
        part1.InWorkObject = B1
        ref6 = part1.CreateReferenceFromName("")
        shapeFactory1 = part1.ShapeFactory
        
        #creating solid by adding thickness to the surface
        pdifx = p2-p1
        x = math.sqrt(pdifx[0,0]**2+pdifx[0,1]**2+pdifx[0,2]**2)
        th = shapeFactory1.AddNewThickSurface(ref6, 1, x, 0.000000)
        th.Surface = ref5
        part1.UpdateObject(th)
        
        
        '''
        #no sharing of vertices for the first shape in a file
        if ii == 0:
            ref = [2,0]
        else:
            ref = [2,instructions[0]]
        storage(M[0,0],M[0,1],M[0,2],file,ref)
        storage(M[1,0],M[1,1],M[1,2],file,ref)
        storage(M[2,0],M[2,1],M[2,2],file,ref)
        storage(M[3,0],M[3,1],M[3,2],file,ref)
        
        #last 4 points not shared between shapes
        ref = [2,0]
        storage(M[4,0],M[4,1],M[4,2],file,ref)
        storage(M[5,0],M[5,1],M[5,2],file,ref)
        storage(M[6,0],M[6,1],M[6,2],file,ref)
        storage(M[7,0],M[7,1],M[7,2],file,ref)
        iii = iii + 1
        '''
        if iii != 0:
            #save the CAD file, and export it as .stp
            #ilo = "D:\\CAD_library_sampling\\temp\\temp.CatPart"
            #partDocument1.SaveAs(silo)
            location = "D:\\CAD_library_sampling\\temp\\temp.stp"
            partDocument1.ExportData(location, "stp")
            partDocument1.Close()
            
            VRTs = stl_vertex(location)
            
            os.remove(location)  
            
        iii = iii + 1  
    return(M,VRTs)


def flange(body1, ShFactory, body3,part1,bodies1,partDocument1,ii,M,df,file,instructions,CATIA):

    iii = 0
    while iii < 2:
        
        if iii == 0:    
            #proportional size in x
            o =  random.uniform(0.2, 1)
            
            #accomodate for flange being secondary to an existent flange,
            #by adjusting the size, and direction by changing the angle
            if df == 0:
                #proportional size in y
                p =  random.uniform(0.2, 1.5)
                #angle of the flange 
                s  = random.uniform(105,180)
            else:
                p =  random.uniform(0.2, 0.9)
                #angle of the flange 
                s  = random.uniform(15,90)
            
            '''
            #20% chance to use maximum base
            if random.uniform(0,1) < 0.2:
              o = 1
              if df == 0:
                  p = 1.5
              else:
                  p = 0.9
            '''      
                  
            #proportional size in z
            q =  random.uniform(0.2, 1)
            zmax = 4
            z = zmax*q   
            
            #radius -- set to be at least equivalent to thickness
            r  = random.uniform(z,10)
        
            
            ab,ac,vec3,u_v3,c = h1(M)
            
            #base points
            p1 = c - 0.5*o*ab - 0.5*p*ac
            p2 = c + 0.5*o*ab - 0.5*p*ac 
            p3 = c - 0.5*o*ab + 0.5*p*ac
            p4 = c + 0.5*o*ab + 0.5*p*ac
            #points on the upper surface of base
            p5 = p1 + z*u_v3
            p6 = p2 + z*u_v3
            p7 = p3 + z*u_v3
            p8 = p4 + z*u_v3
            #for passing the upper surface to further shapes if needed
            M = np.concatenate((p1,p2,p3,p4,p5,p6,p7,p8),axis=0)
        else:
            body1,ShFactory,body3, part1,bodies1,partDocument1 = part2(CATIA)
            
            
        #first point
        point=ShFactory.AddNewPointCoord(p1[0,0],p1[0,1],p1[0,2])
        body1.AppendHybridShape(point) 
        ref1 = part1.CreateReferenceFromObject(point)
    
        #first point shifted in thickness direction, for plane generation
        point=ShFactory.AddNewPointCoord(p5[0,0],p5[0,1],p5[0,2])
        body1.AppendHybridShape(point) 
        ref2 = part1.CreateReferenceFromObject(point)
        
        #point in the direction of flange
        point=ShFactory.AddNewPointCoord(p3[0,0],p3[0,1],p3[0,2])
        body1.AppendHybridShape(point) 
        ref4 = part1.CreateReferenceFromObject(point)  
        
        #base line, in direction of flange
        l1 = ShFactory.AddNewLinePtPt(ref1, ref4)
        body1.AppendHybridShape(l1)
        ref11 = part1.CreateReferenceFromObject(l1)
        
        #plane, requried for line-at-angle generation
        pl1 = ShFactory.AddNewPlane3Points(ref1, ref2, ref4)
        body1.AppendHybridShape(pl1)
        ref3 = part1.CreateReferenceFromObject(pl1)
        
        #calculating the x-y sizes of base (in local coordinate system)
        p1p2 = p2-p1
        dist1 = math.sqrt(p1p2[0,0]**2+p1p2[0,1]**2+p1p2[0,2]**2)
        p1p3 = p3-p1
        dist2 = math.sqrt(p1p3[0,0]**2+p1p3[0,1]**2+p1p3[0,2]**2)
        
        #the angled line is on different side depending on this shape being the 
        #base shape or secondary
        if df == 1:
            l2 = ShFactory.AddNewLineAngle(ref11, ref3, ref1, False, 0.000000, dist2, s, True)
        else:
            l2 = ShFactory.AddNewLineAngle(ref11, ref3, ref4, False, 0.000000, dist2, s, True)
        body1.AppendHybridShape(l2)
        ref22 = part1.CreateReferenceFromObject(l2)
            
        #extrude to create the two main faces
        dir1 = ShFactory.AddNewDirectionByCoord(ab[0,0], ab[0,1], ab[0,2])
        e = ShFactory.AddNewExtrude(ref11, dist1, 0.000000, dir1)
        e.SymmetricalExtension = 0
        body1.AppendHybridShape(e)
        point.Name="e1"
        ref15 = part1.CreateReferenceFromObject(e)
        
        e = ShFactory.AddNewExtrude(ref22, dist1, 0.000000, dir1)
        e.SymmetricalExtension = 0
        body1.AppendHybridShape(e)
        point.Name="e2"
        ref16 = part1.CreateReferenceFromObject(e)
        
        #filet requires different direction based on base/seconday shape generation
        if ii == 0:
            f1 = ShFactory.AddNewFilletBiTangent(ref15, ref16, r, -1, 1, 1, 0)
        else:
            f1 = ShFactory.AddNewFilletBiTangent(ref15, ref16, r, -1, -1, 1, 0)
        body1.AppendHybridShape(f1)
        point.Name="f1"
        ref17 = part1.CreateReferenceFromObject(f1)
        
        #setup for generation of solids
        bodies1 = part1.Bodies
        B1 = bodies1.Item("PartBody")
        part1.InWorkObject = B1
        ref6 = part1.CreateReferenceFromName("")
        shapeFactory1 = part1.ShapeFactory
        
        #add thickness to generated surface
        th = shapeFactory1.AddNewThickSurface(ref6, 1, z, 0.000000)
        th.Surface = ref17
        part1.UpdateObject(th)
        
        '''
        #store relevant reference points
        if ii == 0:
            ref = [3,0]
        else:
            ref = [3,instructions[0]]
        storage(M[0,0],M[0,1],M[0,2],file,ref)
        storage(M[1,0],M[1,1],M[1,2],file,ref)
        storage(M[2,0],M[2,1],M[2,2],file,ref)
        storage(M[3,0],M[3,1],M[3,2],file,ref)
        
        ref = [3,0]
        storage(M[4,0],M[4,1],M[4,2],file,ref)
        storage(M[5,0],M[5,1],M[5,2],file,ref)
        storage(M[6,0],M[6,1],M[6,2],file,ref)
        storage(M[7,0],M[7,1],M[7,2],file,ref)
        '''
        
        #Rest of this script obtains the 3D location of the end-flange vertices
        
        #hide part
        selection1 = partDocument1.Selection
        selection1.Clear() # added recently delete if error
        visPropertySet1 = selection1.VisProperties
        selection1.Add(B1)
        visPropertySet1 = visPropertySet1.Parent
        visPropertySet1.SetShow(1)
        selection1.Clear()
        
        #create 4 points in a different geometrical set
        poc = ShFactory.AddNewPointOnCurveFromPercent(ref22, 1.000000, True)
        bodies1 = part1.HybridBodies
        body5 = bodies1.Item("SourceLoft")
        body5.AppendHybridShape(poc)
        poc.Name="temp_p"
        
        part1.Update()
    
        #use vecx to export in a temporary file
        partDocument1.ExportData("D:\\CAD_library_sampling\\xxx.wrl", "wrl")
        NS,f_pt = wrmmm()
        #print(f_pt)
        
        #delete point after the location was recorded
        hybridShapes1 = body5.HybridShapes
        poc = hybridShapes1.Item("temp_p")
        selection1.Add(poc)
        selection1.Delete()
        selection1.Clear() 
        
        #unhide part
        selection1.Add(B1)
        visPropertySet1 = visPropertySet1.Parent
        visPropertySet1.SetShow(0)
        selection1.Clear()
        
        '''
        #store the 4 points 
        ref = [3,0]
        storage(f_pt[0,0],f_pt[0,1],f_pt[0,2],file,ref)
        f_pt2 =f_pt + ab*o
        storage(f_pt2[0,0],f_pt2[0,1],f_pt2[0,2],file,ref)
        '''
        
        if iii != 0:
            #save the CAD file, and export it as .stp
            #ilo = "D:\\CAD_library_sampling\\temp\\temp.CatPart"
            #partDocument1.SaveAs(silo)
            location = "D:\\CAD_library_sampling\\temp\\temp.stp"
            partDocument1.ExportData(location, "stp")
            partDocument1.Close()
            
            VRTs = stl_vertex(location)
            
            os.remove(location)  
    
        iii = iii + 1
    return(M,VRTs)


def omega(body1, ShFactory, body3,part1,bodies1,partDocument1,ii,M,file,instructions,CATIA):
    
    iii = 0
    while iii < 2:
        
        if iii == 0:  
    
            check = False
            while check == False:
            
                #proportional size in x
                o =  random.uniform(0.5, 1)
                #proportional size in y
                p =  random.uniform(0.5, 1)
                
                #20% chance to use maximum base
                if random.uniform(0,1) < 0.2:
                  o = 1
                  p = 1
            
                #proportional size in z, z is not simply thickness as above, but the 
                #size of the omega profile
                q =  random.uniform(0.2, 1)
                zmax = 30
                z = zmax*q   
                
                #absolute thickness
                th1 = random.uniform(0.5,3)
                
                #percentage of upper section
                pp = random.uniform(0.2,0.5)
                
                ab,ac,vec3,u_v3,c = h1(M)
                
                #p1-p4 are the base points
                p1 = c - 0.5*o*ab - 0.5*p*ac
                p2 = c + 0.5*o*ab - 0.5*p*ac 
                p3 = c - 0.5*o*ab + 0.5*p*ac
                p4 = c + 0.5*o*ab + 0.5*p*ac
                #the upper side of omega, lower surface
                p5 = p1 + z*u_v3 +pp*ac*0.5
                p6 = p2 + z*u_v3 +pp*ac*0.5
                p7 = p3 + z*u_v3 -pp*ac*0.5
                p8 = p4 + z*u_v3 -pp*ac*0.5
                
                #corners at the base of omega
                p9 = p1 +pp*ac*0.5
                p10 = p2 +pp*ac*0.5
                p11 = p3 -pp*ac*0.5
                p12 = p4 -pp*ac*0.5
                
                p1p2 = p2-p1
                dist1 = math.sqrt(p1p2[0,0]**2+p1p2[0,1]**2+p1p2[0,2]**2)
                #radius is adjusted based on space available
                if dist1/10 < 5:
                    #radius has to be larger than thickness either way
                    r  = random.uniform(th1,dist1/10)    
                else:
                    r  = random.uniform(th1,5)
                    
                #check if r is smaller than side flanges, and r is less then half of top surface
                p57 = p7-p5
                dist3 = math.sqrt(p57[0,0]**2+p57[0,1]**2+p57[0,2]**2)
                p19 = p9-p1
                dist4 = math.sqrt(p19[0,0]**2+p19[0,1]**2+p19[0,2]**2)
                
                if dist3 > 2*r + 1:
                    if dist4 > r:
                        if ii == 1 or dist3 > 30:
                            check = True
        else:
            body1,ShFactory,body3, part1,bodies1,partDocument1 = part2(CATIA)
        
        #six points define the omega shape
        point=ShFactory.AddNewPointCoord(p1[0,0],p1[0,1],p1[0,2])
        body1.AppendHybridShape(point) 
        ref1 = part1.CreateReferenceFromObject(point)
        
        point=ShFactory.AddNewPointCoord(p9[0,0],p9[0,1],p9[0,2])
        body1.AppendHybridShape(point) 
        ref9 = part1.CreateReferenceFromObject(point)
        
        point=ShFactory.AddNewPointCoord(p5[0,0],p5[0,1],p5[0,2])
        body1.AppendHybridShape(point) 
        ref5 = part1.CreateReferenceFromObject(point) 
        
        point=ShFactory.AddNewPointCoord(p7[0,0],p7[0,1],p7[0,2])
        body1.AppendHybridShape(point) 
        ref7 = part1.CreateReferenceFromObject(point)
        
        point=ShFactory.AddNewPointCoord(p11[0,0],p11[0,1],p11[0,2])
        body1.AppendHybridShape(point) 
        ref11 = part1.CreateReferenceFromObject(point)
        
        point=ShFactory.AddNewPointCoord(p3[0,0],p3[0,1],p3[0,2])
        body1.AppendHybridShape(point) 
        ref3 = part1.CreateReferenceFromObject(point) 
        
        #5 lines to connect the 6 points
        l1 = ShFactory.AddNewLinePtPt(ref1, ref9)
        body1.AppendHybridShape(l1)
        point.Name="l1"
        ref10 = part1.CreateReferenceFromObject(l1)
        
        l1 = ShFactory.AddNewLinePtPt(ref9, ref5)
        body1.AppendHybridShape(l1)
        point.Name="l2"
        ref20 = part1.CreateReferenceFromObject(l1)
        
        l1 = ShFactory.AddNewLinePtPt(ref5, ref7)
        body1.AppendHybridShape(l1)
        point.Name="l3"
        ref30 = part1.CreateReferenceFromObject(l1)
        
        l1 = ShFactory.AddNewLinePtPt(ref7, ref11)
        body1.AppendHybridShape(l1)
        point.Name="l4"
        ref40 = part1.CreateReferenceFromObject(l1)
        
        l1 = ShFactory.AddNewLinePtPt(ref11, ref3)
        body1.AppendHybridShape(l1)
        point.Name="l5"
        ref50 = part1.CreateReferenceFromObject(l1)
        
        #extrusion from all 5 lines
        dir1 = ShFactory.AddNewDirectionByCoord(ab[0,0], ab[0,1], ab[0,2])
        e = ShFactory.AddNewExtrude(ref10, dist1, 0.000000, dir1)
        e.SymmetricalExtension = 0
        body1.AppendHybridShape(e)
        point.Name="e1"
        ref60 = part1.CreateReferenceFromObject(e)
        
        e = ShFactory.AddNewExtrude(ref20, dist1, 0.000000, dir1)
        e.SymmetricalExtension = 0
        body1.AppendHybridShape(e)
        point.Name="e2"
        ref70 = part1.CreateReferenceFromObject(e)
        
        e = ShFactory.AddNewExtrude(ref30, dist1, 0.000000, dir1)
        e.SymmetricalExtension = 0
        body1.AppendHybridShape(e)
        point.Name="e3"
        ref80 = part1.CreateReferenceFromObject(e)
        
        e = ShFactory.AddNewExtrude(ref40, dist1, 0.000000, dir1)
        e.SymmetricalExtension = 0
        body1.AppendHybridShape(e)
        point.Name="e4"
        ref90 = part1.CreateReferenceFromObject(e)
        
        e = ShFactory.AddNewExtrude(ref50, dist1, 0.000000, dir1)
        e.SymmetricalExtension = 0
        body1.AppendHybridShape(e)
        point.Name="e5"
        ref100 = part1.CreateReferenceFromObject(e)
        
        #connecting all the extrusions using filets
        f1 = ShFactory.AddNewFilletBiTangent(ref60, ref70, r, -1, -1, 1, 0)
        body1.AppendHybridShape(f1)
        point.Name="f1"
        ref61 = part1.CreateReferenceFromObject(f1)
        
        f1 = ShFactory.AddNewFilletBiTangent(ref61, ref80, r, 1, 1, 1, 0)
        body1.AppendHybridShape(f1)
        point.Name="f2"
        ref62 = part1.CreateReferenceFromObject(f1)    
        
        f1 = ShFactory.AddNewFilletBiTangent(ref62, ref90, r, 1, 1, 1, 0)
        body1.AppendHybridShape(f1)
        point.Name="f3"
        ref63 = part1.CreateReferenceFromObject(f1)
        
        f1 = ShFactory.AddNewFilletBiTangent(ref63, ref100, r, -1, -1, 1, 0)
        body1.AppendHybridShape(f1)
        point.Name="f4"
        ref64 = part1.CreateReferenceFromObject(f1)
        
        #set up for creating solids
        bodies1 = part1.Bodies
        B1 = bodies1.Item("PartBody")
        part1.InWorkObject = B1
        ref6 = part1.CreateReferenceFromName("")
        shapeFactory1 = part1.ShapeFactory
        
        #add thickness to generated surface
        th = shapeFactory1.AddNewThickSurface(ref6, 1, th1, 0.000000)
        th.Surface = ref64
        part1.UpdateObject(th)
        
    
    
        uv_ac = ac / np.linalg.norm(ac)
        
        
        if iii != 0:
            #save the CAD file, and export it as .stp
            #ilo = "D:\\CAD_library_sampling\\temp\\temp.CatPart"
            #partDocument1.SaveAs(silo)
            location = "D:\\CAD_library_sampling\\temp\\temp.stp"
            partDocument1.ExportData(location, "stp")
            partDocument1.Close()
            
            VRTs = stl_vertex(location)
            
            #temporary troubleshooting measure
            
            
            #os.rename(location, "D:\\CAD_library_sampling\\temp\\troubleshooting\\temp_"+str(ii)+".stp")
            os.remove(location) 
            
            #shifting the upper omega surface points to the outer side of surface
            #for addition of following shapes
            #the shift also moves all points towards centre, to avoid radii
            p5 = p5 + th1*u_v3 +r*uv_ac
            p6 = p6 + th1*u_v3 +r*uv_ac
            p7 = p7 + th1*u_v3 -r*uv_ac
            p8 = p8 + th1*u_v3 -r*uv_ac
            M = np.concatenate((p1,p2,p3,p4,p5,p6,p7,p8),axis=0)
        
        '''
        #store points in meta-data file
        if ii == 0:
            ref = [4,0]
        else:
            ref = [4,instructions[0]]
            
        storage(M[0,0],M[0,1],M[0,2],file,ref)
        storage(M[1,0],M[1,1],M[1,2],file,ref)
        storage(M[2,0],M[2,1],M[2,2],file,ref)
        storage(M[3,0],M[3,1],M[3,2],file,ref)
        storage(p9[0,0],p9[0,1],p9[0,2],file,ref)
        storage(p10[0,0],p10[0,1],p10[0,2],file,ref)
        storage(p11[0,0],p11[0,1],p11[0,2],file,ref)
        storage(p12[0,0],p12[0,1],p12[0,2],file,ref)
        
        ref = [4,0]
        storage(M[4,0],M[4,1],M[4,2],file,ref)
        storage(M[5,0],M[5,1],M[5,2],file,ref)
        storage(M[6,0],M[6,1],M[6,2],file,ref)
        storage(M[7,0],M[7,1],M[7,2],file,ref)
        '''
        iii = iii + 1
        
    return(M,VRTs)
    
def hole(body1, ShFactory, body3,part1,bodies1,partDocument1,ii,M,file,instructions,CATIA,VRTs):
    #hole can only be a secondary feature
    ab,ac,vec3,u_v3,c = h1(M)
    dir1 = ShFactory.AddNewDirectionByCoord(vec3[0,0], vec3[0,1], vec3[0,2])
    #for now, all holes are central, can be changed later...
    
    #size of the initial surface
    p1p2 = M[5,:]-M[4,:]
    dist1 = math.sqrt(p1p2[0]**2+p1p2[1]**2+p1p2[2]**2)
    p1p3 = M[7,:]-M[4,:]
    dist2 = math.sqrt(p1p3[0]**2+p1p3[1]**2+p1p3[2]**2)  
    
    #find how large hole can be fitted into main surface
    dist1 = dist1/2 - 3
    dist2 = dist2/2 - 3
    lim = min(dist1,dist2,10)

    #hole minimum 1mm, and maximum based on above
    r = random.uniform(1,lim)

    #point for hole centre
    point=ShFactory.AddNewPointCoord(c[0,0],c[0,1],c[0,2])
    body1.AppendHybridShape(point) 
    ref1 = part1.CreateReferenceFromObject(point)    
    
    #three points for the plane definition
    point=ShFactory.AddNewPointCoord(M[5,0],M[5,1],M[5,2])
    body1.AppendHybridShape(point) 
    ref2 = part1.CreateReferenceFromObject(point)  
    point=ShFactory.AddNewPointCoord(M[4,0],M[4,1],M[4,2])
    body1.AppendHybridShape(point) 
    ref3 = part1.CreateReferenceFromObject(point)
    point=ShFactory.AddNewPointCoord(M[6,0],M[6,1],M[6,2])
    body1.AppendHybridShape(point) 
    ref4 = part1.CreateReferenceFromObject(point)

    #plane definition for placement of hole circle
    pl1 = ShFactory.AddNewPlane3Points(ref2, ref3, ref4)
    body1.AppendHybridShape(pl1)
    ref5 = part1.CreateReferenceFromObject(pl1)  
    
    #circle defining the hole
    hl = ShFactory.AddNewCircleCtrRad(ref1, ref5, False, r)
    hl.SetLimitation(1)
    body1.AppendHybridShape(hl)
    ref50 = part1.CreateReferenceFromObject(hl) 
    
    #hole is created by boolean, solid is created and subtracted from main shape
    
    #setup for solid modelling
    bodies1 = part1.Bodies
    body4 = bodies1.Add()
    part1.InWorkObject = body4
    shapeFactory1 = part1.ShapeFactory
    ref6 = part1.CreateReferenceFromName("")
    
    #large extension cylinder created
    pad1 = shapeFactory1.AddNewPadFromRef(ref6, 200.000000)
    pad1.SetProfileElement(ref50)
    pad1.IsSymmetric = True
    part1.UpdateObject(pad1)
    
    #remove cylindder from main body
    body2 = bodies1.Item("PartBody")
    part1.InWorkObject = body2
    shapeFactory1.AddNewRemove(body4)
    shapes1 = body2.Shapes
    remove1 = shapes1.Item("Remove.1")
    part1.UpdateObject(remove1)
    
    # only one vertex stored for hole
    #ref = [5,instructions[0]]
    #storage(c[0,0],c[0,1],c[0,2],file,ref)
    
    location = "D:\\CAD_library_sampling\\temp\\temp.stp"
    partDocument1.ExportData(location, "stp")
    VRTs2 = stl_vertex(location)
    VRTs3 = ""
    
    count = VRTs2.count("\n")
    e = 0
    while e < count:
        snip = VRTs2.split("\n")[e]
        if snip not in VRTs:
            VRTs3 = VRTs3 + snip + "\n"
        
        e = e + 1
    
    os.remove(location) 
    return(VRTs3)


def pin(body1, ShFactory, body3,part1,bodies1,partDocument1,ii,M,file,instructions,CATIA,VRTs):
    #pin can only be a seconddary shape at this moment
    
    ab,ac,vec3,u_v3,c = h1(M)
    dir1 = ShFactory.AddNewDirectionByCoord(vec3[0,0], vec3[0,1], vec3[0,2])
    #for now, all pins are central, can be changed later
    
    p1p2 = M[5,:]-M[4,:]
    #errors due to np.matrix ==> np.asarray --- check some models later
    dist1 = math.sqrt(p1p2[0]**2+p1p2[1]**2+p1p2[2]**2)
    p1p3 = M[7,:]-M[4,:]
    dist2 = math.sqrt(p1p3[0]**2+p1p3[1]**2+p1p3[2]**2)  
    
    #the base circle size limited, to fit the reference surface
    dist1 = dist1/2 - 3
    dist2 = dist2/2 - 3
    lim = min(dist1,dist2,10)
    r = random.uniform(1,lim)
    #absolute lenght of the pin
    L = random.uniform(5,30)

    #point for the base circle
    point=ShFactory.AddNewPointCoord(c[0,0],c[0,1],c[0,2])
    body1.AppendHybridShape(point) 
    ref1 = part1.CreateReferenceFromObject(point)    
    
    #3 points for the base plane
    point=ShFactory.AddNewPointCoord(M[5,0],M[5,1],M[5,2])
    body1.AppendHybridShape(point) 
    ref2 = part1.CreateReferenceFromObject(point)  
    point=ShFactory.AddNewPointCoord(M[4,0],M[4,1],M[4,2])
    body1.AppendHybridShape(point) 
    ref3 = part1.CreateReferenceFromObject(point)
    point=ShFactory.AddNewPointCoord(M[6,0],M[6,1],M[6,2])
    body1.AppendHybridShape(point) 
    ref4 = part1.CreateReferenceFromObject(point)

    #base plane
    pl1 = ShFactory.AddNewPlane3Points(ref2, ref3, ref4)
    body1.AppendHybridShape(pl1)
    ref5 = part1.CreateReferenceFromObject(pl1)  
    
    #base circle
    hl = ShFactory.AddNewCircleCtrRad(ref1, ref5, False, r)
    hl.SetLimitation(1)
    body1.AppendHybridShape(hl)
    ref50 = part1.CreateReferenceFromObject(hl) 
    
    #set up for solid modelling
    bodies1 = part1.Bodies
    body4 = bodies1.Add()
    part1.InWorkObject = body4
    shapeFactory1 = part1.ShapeFactory
    ref6 = part1.CreateReferenceFromName("")
    
    #create the pin
    pad1 = shapeFactory1.AddNewPadFromRef(ref6, L)
    pad1.SetProfileElement(ref50)
    pad1.IsSymmetric = False
    part1.UpdateObject(pad1)
    
    #add the pin to the main body
    body2 = bodies1.Item("PartBody")
    part1.InWorkObject = body2
    shapeFactory1.AddNewAdd(body4)
    shapes1 = body2.Shapes
    add1 = shapes1.Item("Add.1")
    part1.UpdateObject(add1)
    
    #2 points stored for pin, base point and centre point at max extension
    #ref = [6,instructions[0]]
    #storage(c[0,0],c[0,1],c[0,2],file,ref)
    
    #ref = [6,0]
    #cc = c + L*u_v3
    #storage(cc[0,0],cc[0,1],cc[0,2],file,ref)
    
    
        
    location = "D:\\CAD_library_sampling\\temp\\temp.stp"
    partDocument1.ExportData(location, "stp")
    VRTs2 = stl_vertex(location)
    VRTs3 = ""
    
    count = VRTs2.count("\n")
    e = 0
    while e < count:
        snip = VRTs2.split("\n")[e]
        if snip not in VRTs:
            VRTs3 = VRTs3 + snip + "\n"
        
        e = e + 1
    os.remove(location) 
    return(VRTs3)