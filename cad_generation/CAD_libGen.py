# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 13:54:04 2022

@author: jakub.kucera
"""
import win32com.client.dynamic
#import sys, os 
import numpy as np
import os
#import win32gui
#import math
#import time
#from datetime import date
import random
import math
#The functions below use the internal functions of CATIA. VBA recording function
#within CATIA was used to develope these scripts.

from WS_gen_2 import vertex_list

def v_spar(iterations, sample_name):
    CATIA = win32com.client.Dispatch("CATIA.Application")
    #record deletion of product....
    
    i = 0 
    
    while i < iterations:
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
        
        
        
        l1 = random.uniform(20, 120)    #50
        l2 = random.uniform(20, 120)
        l3 = random.uniform(-1, 120)
        l4 = random.uniform(20, 120)
        l5 = random.uniform(-5, 20)
        r1 = random.uniform(1, 9)
        r2 = random.uniform(1, 9)
        e1 = random.uniform(10, 500)
        
        angle = math.degrees(math.atan((l1/2-l2/2)/l4))
        print(angle)
        #check removability from mould
        if l1 < l2:
            q1 = 0
        elif angle < 4:
            q1 = 1
        else:
            q1 = 2
        
        #check all radii are above 3mm
        if r1 < 2 or r2 < 2:
            q2 = 0
        else:
            q2 = 1
        
        
        
        #simplify the below into 2 loops (one referring to coordinate matrix, the other just looping numbers)
        
        point=ShFactory.AddNewPointCoord(0,0,0)
        body1.AppendHybridShape(point) 
        point.Name="p1"
        ref1 = part1.CreateReferenceFromObject(point)
        
        point=ShFactory.AddNewPointCoord(l3,l5,0)
        body1.AppendHybridShape(point) 
        point.Name="p2"
        ref2 = part1.CreateReferenceFromObject(point)
        
        point=ShFactory.AddNewPointCoord((l3+0.5*l1-0.5*l2),l4+l5,0)
        body1.AppendHybridShape(point) 
        point.Name="p3"
        ref3 = part1.CreateReferenceFromObject(point)
        
        point=ShFactory.AddNewPointCoord((l3+0.5*l1+0.5*l2),l4+l5,0)
        body1.AppendHybridShape(point) 
        point.Name="p4"
        ref4 = part1.CreateReferenceFromObject(point)
        
        point=ShFactory.AddNewPointCoord(l3+l1,l5,0)
        body1.AppendHybridShape(point)
        point.Name="p5" 
        ref5 = part1.CreateReferenceFromObject(point)
        
        point=ShFactory.AddNewPointCoord(2*l3+l1,0,0)
        body1.AppendHybridShape(point) 
        point.Name="p6"
        ref6 = part1.CreateReferenceFromObject(point)
        
        l1 = ShFactory.AddNewLinePtPt(ref1, ref2)
        body1.AppendHybridShape(l1)
        point.Name="l1"
        ref7 = part1.CreateReferenceFromObject(l1)
        
        l1 = ShFactory.AddNewLinePtPt(ref2, ref3)
        body1.AppendHybridShape(l1)
        point.Name="l2"
        ref8 = part1.CreateReferenceFromObject(l1)
        
        l1 = ShFactory.AddNewLinePtPt(ref3, ref4)
        body1.AppendHybridShape(l1)
        point.Name="l3"
        ref9 = part1.CreateReferenceFromObject(l1)
        
        l1 = ShFactory.AddNewLinePtPt(ref4, ref5)
        body1.AppendHybridShape(l1)
        point.Name="l4"
        ref10 = part1.CreateReferenceFromObject(l1)
        
        l1 = ShFactory.AddNewLinePtPt(ref5, ref6)
        body1.AppendHybridShape(l1)
        point.Name="l5"
        ref11 = part1.CreateReferenceFromObject(l1)
        
        
        #reference direction plane
        OE = part1.OriginElements
        hspe = OE.PlaneXY
        ref111 = part1.CreateReferenceFromObject(hspe)
        
        dir1 = ShFactory.AddNewDirection(ref111)
        
        
        e = ShFactory.AddNewExtrude(ref7, e1, 0.000000, dir1)
        e.SymmetricalExtension = 0
        body1.AppendHybridShape(e)
        point.Name="e1"
        ref12 = part1.CreateReferenceFromObject(e)
        
        e = ShFactory.AddNewExtrude(ref8, e1, 0.000000, dir1)
        e.SymmetricalExtension = 0
        body1.AppendHybridShape(e)
        point.Name="e2"
        ref13 = part1.CreateReferenceFromObject(e)
        
        e = ShFactory.AddNewExtrude(ref9, e1, 0.000000, dir1)
        e.SymmetricalExtension = 0
        body1.AppendHybridShape(e)
        point.Name="e3"
        ref14 = part1.CreateReferenceFromObject(e)
        
        e = ShFactory.AddNewExtrude(ref10, e1, 0.000000, dir1)
        e.SymmetricalExtension = 0
        body1.AppendHybridShape(e)
        point.Name="e4"
        ref15 = part1.CreateReferenceFromObject(e)
        
        e = ShFactory.AddNewExtrude(ref11, e1, 0.000000, dir1)
        e.SymmetricalExtension = 0
        body1.AppendHybridShape(e)
        point.Name="e5"
        ref16 = part1.CreateReferenceFromObject(e)
        
        
        '''
        a1 = ShFactory.AddNewJoin(ref12, ref13)
        body1.AppendHybridShape(a1)
        point.Name="a1"
        ref16 = part1.CreateReferenceFromObject(a1)
        
        a2 = ShFactory.AddNewJoin(ref15, ref16)
        body1.AppendHybridShape(a2)
        point.Name="a2"
        ref16 = part1.CreateReferenceFromObject(a2)
        '''
        
        
        
        f1 = ShFactory.AddNewFilletBiTangent(ref12, ref13, r1, -1, -1, 1, 0)
        body1.AppendHybridShape(f1)
        point.Name="f1"
        ref17 = part1.CreateReferenceFromObject(f1)
        
        
        f2 = ShFactory.AddNewFilletBiTangent(ref17, ref14, r2, 1, 1, 1, 0)
        body1.AppendHybridShape(f2)
        point.Name="f2"
        ref17 = part1.CreateReferenceFromObject(f2)
        
        f3 = ShFactory.AddNewFilletBiTangent(ref17, ref15, r2, 1, 1, 1, 0)
        body1.AppendHybridShape(f3)
        point.Name="f3"
        ref17 = part1.CreateReferenceFromObject(f3)
        
        f4 = ShFactory.AddNewFilletBiTangent(ref17, ref16, r1, -1, -1, 1, 0)
        body3.AppendHybridShape(f4)
        point.Name="f4"
        ref17 = part1.CreateReferenceFromObject(f4)
        
        
        #make construction geometry invisible
        selection1 = partDocument1.Selection
        selection1.Clear()
        visPropertySet1 = selection1.VisProperties
        selection1.Add(body1)
        visPropertySet1 = visPropertySet1.Parent
        visPropertySet1.SetShow(1)
        selection1.Clear()
        
        part1.Update 
        
        
        
        #lPath = os.path.dirname(os.path.abspath(__file__))
        #sample_name = "s3"
        name = sample_name+"-"+str(i)
        silo = "D:\\CAD_library_sampling\\"+name+".CatPart"
        print(silo)
        partDocument1.SaveAs(silo)
        
        
        
        partDocument1.ExportData("""D:\\CAD_library_sampling\\"""+name+""".stp""", "stp")
         
        i = i + 1
        
        #create empty .txt files
        file = "D:\\CAD_library_sampling\\metadata.txt"
        file2 = "D:\\CAD_library_sampling\\metadata_full.txt"
        open(file, 'a').close()
        open(file2, 'a').close()
        
        #PREDICT IF IT IS OK BASED ON NUMBERS!!
        #create a metadata document - just name and de-mouldability 2 = yes, 1 = yes, but... 0 = no
        with open(file, "a") as text_file:
            text_file.write(sample_name+"___"+name+"___"+str(q1)+"___"+str(q2)+"\n")
        
        #second document with the above metadata + variables, for later to check if needed...
        with open(file2, "a") as text_file:
            text_file.write(sample_name+"___"+name+"___"+str(q1)+"___"+str(q2)+"___"+
                            str(l1)+"___"+str(l2)+"___"+str(l3)+"___"+str(l4)+"___"+
                            str(l5)+"___"+str(r1)+"___"+str(r2)+"___"+str(e1)+"___"+str(angle)+"\n")
             
def pocket(i,sample_name):
    CATIA = win32com.client.Dispatch("CATIA.Application")
    #record deletion of product....
    

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
    
    
    
    l1 = random.uniform(20, 120)    #50
    l2 = random.uniform(-15, 10)
    l3 = random.uniform(20,120)
    noh = random.randint(1,20)
    roh = random.randint(2,min(int(l3/2),12))
    t = random.randint(1,40)/10
    
    #better iteration here I believe
    ii = 0
    polar = np.zeros((8,2))
    while ii < 8:
        polar[ii,0] = random.uniform(0,45)
        polar[ii,1] = random.uniform(50,200)
        ii = ii + 1

    r1 = random.uniform(1, 9)
    #r2 = random.uniform(1, 9)
    
    angle = math.atan(l2/l1)*180/math.pi
    if angle > 0:
        q1 = 0
        #this is not manufacturable
    elif angle > -4:
        q1 =1
    else:
        q1 = 2
    
    # Starting the top surface spline
    spline1 = ShFactory.AddNewSpline()
    spline1.SetSplineType(0)
    spline1.SetClosing(1)
    #Add points to splines
    #xmaxT = np.matrix([[-1000,0]])
    #xminT = np.matrix([[1000,0]])
    iii = 0
    while iii < 8:
        x = polar[iii,1]*math.sin((polar[iii,0]+iii*45)*math.pi/180)
        y = polar[iii,1]*math.cos((polar[iii,0]+iii*45)*math.pi/180)
        point=ShFactory.AddNewPointCoord(x,y,0)
        spline1.AddPoint(point)
        #Find the maximum x position for top surface.

        iii = iii + 1     
    #Submit the spline, and create the reference.
    ref111 = part1.CreateReferenceFromObject(spline1) 
    body1.AppendHybridShape(spline1)
    
    # Starting new spline for bottom section.
    spline2 = ShFactory.AddNewSpline()
    spline2.SetSplineType(0)
    spline2.SetClosing(0)        

    oe = part1.OriginElements
    hspe = oe.PlaneXY
    ref222 = part1.CreateReferenceFromObject(hspe)
    par1 = ShFactory.AddNewCurvePar(ref111, ref222, l3, False, False)
    par1.SmoothingType = 0
    body1.AppendHybridShape(par1)

    #for holes placement
    mid_par = ShFactory.AddNewCurvePar(ref111, ref222, l3/2, False, False)
    par1.SmoothingType = 0
    body1.AppendHybridShape(mid_par)        
    rf1 = part1.CreateReferenceFromObject(mid_par)
    
    
    off = ShFactory.AddNewPlaneOffset(ref222, l1, True)

    body1.AppendHybridShape(off)
    ref3 = part1.CreateReferenceFromObject(off)
    proj = ShFactory.AddNewProject(ref111, ref3)
    proj.SolutionType = 0
    proj.Normal = True
    proj.SmoothingType = 0
    proj.ExtrapolationMode = 0
    body1.AppendHybridShape(proj)       
    fill = ShFactory.AddNewFill()
    ref6 = part1.CreateReferenceFromObject(proj)


    ref4 = part1.CreateReferenceFromObject(par1)
    fill.AddBound(ref4)
    fill.Continuity = 1
    fill.Detection = 2
    fill.AdvancedTolerantMode = 2
    body1.AppendHybridShape(fill)


    ref5 = part1.CreateReferenceFromObject(fill)
    splt = ShFactory.AddNewHybridSplit(ref5, ref111, -1)
    splt.ExtrapolationType = 1
    body1.AppendHybridShape(splt)
    ref12 = part1.CreateReferenceFromObject(splt)


    par2 = ShFactory.AddNewCurvePar(ref6, ref3, l2, False, False)
    par2.SmoothingType = 0
    body1.AppendHybridShape(par2)
    ref11 = part1.CreateReferenceFromObject(par2)
    
    loft1 = ShFactory.AddNewLoft()
    loft1.SectionCoupling = 1
    loft1.Relimitation = 1
    loft1.CanonicalDetection = 2

    loft1.AddSectionToLoft(ref111, 1,None)

    loft1.AddSectionToLoft(ref11, 1,None)

    body1.AppendHybridShape(loft1)
    ref13 = part1.CreateReferenceFromObject(loft1)
    
    
    
    flt = ShFactory.AddNewFilletBiTangent(ref12, ref13, r1, 1, 1, 1, 0)
    body3.AppendHybridShape(flt)
    rf4 = part1.CreateReferenceFromObject(flt)
    
    
    #make construction geometry invisible
    selection1 = partDocument1.Selection
    selection1.Clear()
    visPropertySet1 = selection1.VisProperties
    selection1.Add(body1)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)
    selection1.Clear()

    part1.Update 

    #random but consistent reference point
    point=ShFactory.AddNewPointCoord(0,0,0)
    body1.AppendHybridShape(point)
    rf2 = part1.CreateReferenceFromObject(point)

    #create holes geo set
    body8 = bodies1.Add()
    body8.Name="Holes"

    ii = 0
    while ii < noh:
        #add all holes to the mid_par
        pocx = ShFactory.AddNewPointOnCurveWithReferenceFromPercent(rf1, rf2, ii/noh, False)
        body8.AppendHybridShape(pocx)
        rf3 = part1.CreateReferenceFromObject(pocx)
        
        c1 = ShFactory.AddNewCircleCtrRad(rf3, rf4, False, roh)

        c1.SetLimitation(1)

        body8.AppendHybridShape(c1)
        c1.name = "c"+str(ii)
        rf8 = part1.CreateReferenceFromObject(c1)

        ldir = ShFactory.AddNewLineNormal(rf4, rf3, -20.000000, 20.000000, False)
        body8.AppendHybridShape(ldir)
        rf7 = part1.CreateReferenceFromObject(ldir)

        dirx = ShFactory.AddNewDirection(rf7)
        
        ex = ShFactory.AddNewExtrude(rf8, 50.000000, 50.000000, dirx)
        body8.AppendHybridShape(ex)
        ex.Name = "C_X_"+str(ii)
        ii = ii + 1
        

    #solid
    #definition for solid geometries
    SF = part1.ShapeFactory
    bodies5 = part1.Bodies
    body5 = bodies5.Item("PartBody")
    part1.InWorkObject = body5

    #base surface
    rf00 = part1.CreateReferenceFromName("")
    ts1 = SF.AddNewThickSurface(rf00, 0, 1.0000, 0.000000)
    ts1.Surface = rf4
    l1 = ts1.TopOffset
    l1.Value = t
    part1.UpdateObject(ts1)

    #hide excess geometry
    selection1 = partDocument1.Selection
    visPropertySet1 = selection1.VisProperties
    selection1.Add(body1)
    selection1.Add(body3)
    #selection1.Add(body4)
    selection1.Add(body8)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)
    #save v1

    #cut the holes out 

    #save v2

    path2 = "D:\\CAD_library_sampling\\sample13\\"
    #save version without holes and output empty notepad
    partDocument1.SaveAs(path2+"PR_"+str(i)+".catpart")
    partDocument1.ExportData(path2+"PR_"+str(i)+".stp", "stp")
    ver_list1 = vertex_list("D:\CAD_library_sampling\sample13\PR_"+str(i)+".stp")
    stre = ""
    with open(path2+"PR_"+str(i)+"_metadata.txt", "a") as text_file:
        text_file.write(stre)


    #make holes show
    ii = 0
    while ii < noh:
        iii = 1
        while iii < 3:
            split1 = SF.AddNewSplit(rf00,0)#, catPositiveSide)

            bds1 = part1.HybridBodies

            hb1 = bds1.Item("Holes")

            hs1= hb1.HybridShapes

            cyl_str = "C_X_"+str(ii)
            
            cyl1 = hs1.Item(cyl_str)
            
            reference2 = part1.CreateReferenceFromObject(cyl1)

            split1.Surface = reference2

            part1.UpdateObject(split1)

            iii = iii + 1
        ii = ii + 1

    
    part1.Update()

    #save version with holes
    partDocument1.SaveAs(path2+"PR_"+str(i+1)+".catpart")
    partDocument1.ExportData(path2+"PR_"+str(i+1)+".stp", "stp")
    ver_list2 = vertex_list("D:\CAD_library_sampling\sample13\PR_"+str(i+1)+".stp")

    #compare 2 vertex lists
    diff = []
    for l2 in ver_list2:
        ex = True
        for l1 in ver_list1:
            if l1.x == l2.x and l1.y == l2.y and l1.z == l2.z:
                ex = False
            
        if ex == True:
            diff.append(l2)

    #.txt file for training
    iii = 0
    stre = ""
    alo = []
    while iii < len(diff):
        
        if iii not in alo:
            iv = iii+1
            stre += "\n hole\n"
            stre += str(diff[iii].x)+","+str(diff[iii].y)+","+str(diff[iii].z)+"\n"
            while iv < len(diff):
                #print(alo)
                if iv not in alo:
                    #distance only in x y because holes only done in z direction for now
                    ddst = math.sqrt((diff[iv].x-diff[iii].x)**2+(diff[iv].y-diff[iii].y)**2)#(diff[iv].z-diff[iii].z)**2)
                    if ddst < 2.05*roh:
                        stre += str(diff[iv].x)+","+str(diff[iv].y)+","+str(diff[iv].z)+"\n"
                        alo.append(iv)
                iv = iv + 1
        iii = iii + 1

    with open(path2+"PR_"+str(i+1)+"_metadata.txt", "a") as text_file:
        text_file.write(stre)


    partDocument1.Close()    

         
        

        
        #PREDICT IF IT IS OK BASED ON NUMBERS!!
        #create a metadata document - just name and de-mouldability 2 = yes, 1 = yes, but... 0 = no
        #with open(file, "a") as text_file:
        #    text_file.write(sample_name+"___"+name+"___"+str(q1)+"\n")

'''     
#sample_name = "p10"
#iterations = 20
i = 4487
ee = 0
while i < 10000: 
    try:
        pocket(i, "pocket_x")
    except:
        print("number "+str(i)+" not finished, error")

        ee = ee + 1
        if ee > 100:
            break
    i = i + 2
'''

def stiffened_panel(
                    I,                                                   #iteration
                    xmax = 1000,ymax =2000,no_stringer =2,t = 3, ts =2,  #overall panel
                    str_h = 50, str_w = 100,                             #stringer details
                    rh = 3, noh = 10,                                     #holes
                    b2 = 0.01, a2=0.01,e2=100,d2=1.25,c2=0,              #edge 2 para
                    b1 = 0, a1 = 0, e1 = 0, d1= 0, c1= 0                 #edge 1 para
                    ):
    

    #eventually add two more curves for the other 2 edges
    #this will need to take account for elevated points
    #these would be the guide curves for loft

    #Setting up CATIA modelling environment
    CATIA = win32com.client.Dispatch("CATIA.Application")
    #record deletion of product....

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
    body1.Name="Wireframe"
    # Surfaces group
    body3 = bodies1.Add()
    body3.Name="Surfaces"
    body4 = bodies1.Add()
    body4.Name="SourceLoft"

    body6 = bodies1.Add()
    body6.Name = "Holes"

    # Starting new spline f
    spline2 = ShFactory.AddNewSpline()
    spline2.SetSplineType(0)
    spline2.SetClosing(0)

    pts = 20
    i = 0
    while i <= xmax+10:
    #while loop for curve
        z = xz_curve(i,b=b1,a=a1,e=e1,d=d1,c=c1)
        point=ShFactory.AddNewPointCoord(i,0,z)
        spline2.AddPoint(point)
        i = i + xmax/(pts-1)

    #Submit the spline and create reference.
    body1.AppendHybridShape(spline2) 
    rs2 = part1.CreateReferenceFromObject(spline2) 

    # Starting new spline 
    spline3 = ShFactory.AddNewSpline()
    spline3.SetSplineType(0)
    spline3.SetClosing(0)

    pts = 20
    i = 0
    while i <= xmax+10:
    #while loop for curve
        z = xz_curve(i,b=b2,a=a2,e=e2,d=d2,c=c2)
        point=ShFactory.AddNewPointCoord(i,ymax,z)
        spline3.AddPoint(point)
        i = i + xmax/(pts+1)

    #Submit the spline and create reference.
    body1.AppendHybridShape(spline3) 
    rs3 = part1.CreateReferenceFromObject(spline3) 

    #main loft
    loft1 = ShFactory.AddNewLoft()
    loft1.SectionCoupling = 1
    loft1.Relimitation = 1
    loft1.CanonicalDetection = 2
    loft1.AddSectionToLoft(rs2, 1,None)
    loft1.AddSectionToLoft(rs3, 1,None)
    body4.AppendHybridShape(loft1)
    part1.InWorkObject = loft1
    loft1.Name = "MainSurface"

    rfx = part1.CreateReferenceFromObject(loft1) 

    #origin planes for reference
    originElements1 = part1.OriginElements
    origx = originElements1.PlaneYZ
    ref22 = part1.CreateReferenceFromObject(origx)
    origy = originElements1.PlaneZX
    ref33 = part1.CreateReferenceFromObject(origy)

    #standard y-direction offsets for the end of stringers
    lof11 = ShFactory.AddNewPlaneOffset(ref33, ymax*0.1, False) 
    rf201 = part1.CreateReferenceFromObject(lof11)
    lof12 = ShFactory.AddNewPlaneOffset(ref33, ymax*0.9, False) 
    rf202 = part1.CreateReferenceFromObject(lof12)

    #ref pt
    poc1 = ShFactory.AddNewPointCoord(0,0,0)
    ref0 = part1.CreateReferenceFromObject(poc1)

    #definition for solid geometries
    SF = part1.ShapeFactory
    bodies5 = part1.Bodies
    body5 = bodies5.Item("PartBody")
    part1.InWorkObject = body5

    #base surface
    rf00 = part1.CreateReferenceFromName("")
    ts1 = SF.AddNewThickSurface(rf00, 0, 1.0000, 0.000000)
    ts1.Surface = rfx
    l1 = ts1.TopOffset
    l1.Value = t
    part1.UpdateObject(ts1)

    #for each stringer
    i = 0 
    while i < no_stringer:

        #create a new ofset to cut the base stringer from
        sof1 = ShFactory.AddNewOffset(rfx, t+ts, True, 0.010000)
        body3.AppendHybridShape(sof1)
        rf100 = part1.CreateReferenceFromObject(sof1)
        
        #mid location of the stringer
        cp = (i+1)*xmax/(no_stringer+1)

        #planes
        lof1 = ShFactory.AddNewPlaneOffset(ref22, cp-str_w/2, False)
        lof2 = ShFactory.AddNewPlaneOffset(ref22, cp-ts, False)
        lof3 = ShFactory.AddNewPlaneOffset(ref22, cp+ts, False)
        lof4 = ShFactory.AddNewPlaneOffset(ref22, cp+str_w/2, False)
        rf101 = part1.CreateReferenceFromObject(lof1)
        rf102 = part1.CreateReferenceFromObject(lof2)
        rf103 = part1.CreateReferenceFromObject(lof3)
        rf104 = part1.CreateReferenceFromObject(lof4)

        #additional planes for holes
        lof10 = ShFactory.AddNewPlaneOffset(ref22, cp-str_w/4-ts, False)
        lof11 = ShFactory.AddNewPlaneOffset(ref22, cp+str_w/4+ts, False)
        rf110 = part1.CreateReferenceFromObject(lof10)
        rf111 = part1.CreateReferenceFromObject(lof11)

        #ONE LEG
        spl = ShFactory.AddNewHybridSplit(rf100, rf101, 1)
        ShFactory.GSMVisibility(rf100, 0)
        spl.ExtrapolationType = 1
        body3.AppendHybridShape(spl)
        rf105 = part1.CreateReferenceFromObject(spl)

        spl = ShFactory.AddNewHybridSplit(rf105, rf102, -1)
        ShFactory.GSMVisibility(rf105, 0)
        spl.ExtrapolationType = 1
        body3.AppendHybridShape(spl)
        rf105 = part1.CreateReferenceFromObject(spl)

        spl = ShFactory.AddNewHybridSplit(rf105, rf201, 1)
        ShFactory.GSMVisibility(rf105, 0)
        spl.ExtrapolationType = 1
        body3.AppendHybridShape(spl)
        rf105 = part1.CreateReferenceFromObject(spl)

        spl = ShFactory.AddNewHybridSplit(rf105, rf202, -1)
        ShFactory.GSMVisibility(rf105, 0)
        spl.ExtrapolationType = 1
        body3.AppendHybridShape(spl)
        rf206 = part1.CreateReferenceFromObject(spl)

        #TWO LEG
        spl = ShFactory.AddNewHybridSplit(rf100, rf103, 1)
        ShFactory.GSMVisibility(rf100, 0)
        spl.ExtrapolationType = 1
        body3.AppendHybridShape(spl)
        rf105 = part1.CreateReferenceFromObject(spl)

        spl = ShFactory.AddNewHybridSplit(rf105, rf104, -1)
        ShFactory.GSMVisibility(rf105, 0)
        spl.ExtrapolationType = 1
        body3.AppendHybridShape(spl)
        rf105 = part1.CreateReferenceFromObject(spl)

        spl = ShFactory.AddNewHybridSplit(rf105, rf201, 1)
        ShFactory.GSMVisibility(rf105, 0)
        spl.ExtrapolationType = 1
        body3.AppendHybridShape(spl)
        rf105 = part1.CreateReferenceFromObject(spl)

        spl = ShFactory.AddNewHybridSplit(rf105, rf202, -1)
        ShFactory.GSMVisibility(rf105, 0)
        spl.ExtrapolationType = 1
        body3.AppendHybridShape(spl)
        rf207 = part1.CreateReferenceFromObject(spl)

        #intersect 1
        int1 = ShFactory.AddNewIntersection(rf100, rf102)
        int1.PointType = 0
        body1.AppendHybridShape(int1)
        rf301 = part1.CreateReferenceFromObject(int1)

        spl = ShFactory.AddNewHybridSplit(rf301, rf201, -1)
        ShFactory.GSMVisibility(rf105, 0)
        spl.ExtrapolationType = 1
        body1.AppendHybridShape(spl)
        rf105 = part1.CreateReferenceFromObject(spl)

        spl = ShFactory.AddNewHybridSplit(rf105, rf202, 1)
        ShFactory.GSMVisibility(rf105, 0)
        spl.ExtrapolationType = 1
        body1.AppendHybridShape(spl)
        rf301 = part1.CreateReferenceFromObject(spl)

        #intersect 2
        int1 = ShFactory.AddNewIntersection(rf100, rf103)
        int1.PointType = 0
        body1.AppendHybridShape(int1)
        rf302 = part1.CreateReferenceFromObject(int1)

        spl = ShFactory.AddNewHybridSplit(rf302, rf201, -1)
        ShFactory.GSMVisibility(rf105, 0)
        spl.ExtrapolationType = 1
        body1.AppendHybridShape(spl)
        rf105 = part1.CreateReferenceFromObject(spl)

        spl = ShFactory.AddNewHybridSplit(rf105, rf202, 1)
        ShFactory.GSMVisibility(rf105, 0)
        spl.ExtrapolationType = 1
        body1.AppendHybridShape(spl)
        rf302 = part1.CreateReferenceFromObject(spl)

        #intersect 3 and 4 for holes
        int10 = ShFactory.AddNewIntersection(rf100, rf110)
        int10.PointType = 0
        body1.AppendHybridShape(int10)
        rf410 = part1.CreateReferenceFromObject(int10)

        spl = ShFactory.AddNewHybridSplit(rf410, rf201, -1)
        ShFactory.GSMVisibility(rf105, 0)
        spl.ExtrapolationType = 1
        body1.AppendHybridShape(spl)
        rf105 = part1.CreateReferenceFromObject(spl)

        spl = ShFactory.AddNewHybridSplit(rf105, rf202, 1)
        ShFactory.GSMVisibility(rf105, 0)
        spl.ExtrapolationType = 1
        body1.AppendHybridShape(spl)
        rf410 = part1.CreateReferenceFromObject(spl)

        #4
        int11 = ShFactory.AddNewIntersection(rf100, rf111)
        int11.PointType = 0
        body1.AppendHybridShape(int11)
        rf411 = part1.CreateReferenceFromObject(int11)

        spl = ShFactory.AddNewHybridSplit(rf411, rf201, -1)
        ShFactory.GSMVisibility(rf105, 0)
        spl.ExtrapolationType = 1
        body1.AppendHybridShape(spl)
        rf105 = part1.CreateReferenceFromObject(spl)

        spl = ShFactory.AddNewHybridSplit(rf105, rf202, 1)
        ShFactory.GSMVisibility(rf105, 0)
        spl.ExtrapolationType = 1
        body1.AppendHybridShape(spl)
        rf411 = part1.CreateReferenceFromObject(spl)

        #individual holes - define geometry, not cutout 
        ii = 0
        while ii < noh:
            #two holes for each stringer
            #make point
            pox = ShFactory.AddNewPointOnCurveWithReferenceFromPercent(rf410, ref0, (ii+1)/(noh+1), True)
            body6.AppendHybridShape(pox)
            rt1 = part1.CreateReferenceFromObject(pox)

            #make line
            nx = ShFactory.AddNewLineNormal(rf100, rt1, -100, 100.000000, False)
            body6.AppendHybridShape(nx)
            rt2 = part1.CreateReferenceFromObject(nx)
            dirx = ShFactory.AddNewDirection(rt2)

            #make cylinder for cutout
            c2 = ShFactory.AddNewCylinder(rt1, rh, 1, t+ts+1, dirx)
            rt3 = part1.CreateReferenceFromObject(c2)
            body6.AppendHybridShape(c2)
            c2.Name = "C_1_"+str(i)+"_"+str(ii)

            #repeat the 3 steps above for second half of stringer
            pox = ShFactory.AddNewPointOnCurveWithReferenceFromPercent(rf411, ref0, (ii+1)/(noh+1), True)
            body6.AppendHybridShape(pox)
            rt1 = part1.CreateReferenceFromObject(pox)

            nx = ShFactory.AddNewLineNormal(rf100, rt1, -100, 100.000000, False)
            body6.AppendHybridShape(nx)
            rt2 = part1.CreateReferenceFromObject(nx)

            dirx = ShFactory.AddNewDirection(rt2)
            c2 = ShFactory.AddNewCylinder(rt1, rh, 1, t+ts+1, dirx)
            body6.AppendHybridShape(c2)
            rt3 = part1.CreateReferenceFromObject(c2)
            c2.Name = "C_2_"+str(i)+"_"+str(ii)

            ii = ii + 1

        #only one ref point
        poc2 = ShFactory.AddNewPointOnCurveWithReferenceFromPercent(rf301, ref0, 0.000000, False)
        body1.AppendHybridShape(poc2)
        ref300 = part1.CreateReferenceFromObject(poc2)

        #extrude direction 
        n1 = ShFactory.AddNewLineNormal(rf100, ref300, 0.000000, 20.000000, False)
        body1.AppendHybridShape(n1)
        ref303 = part1.CreateReferenceFromObject(n1)

        #two extrudes
        dir1 = ShFactory.AddNewDirection(ref303)
        ex1 = ShFactory.AddNewExtrude(rf301, str_h, 0.000000, dir1)
        body3.AppendHybridShape(ex1)
        rf307 = part1.CreateReferenceFromObject(ex1)

        ex2 = ShFactory.AddNewExtrude(rf302, str_h, 0.000000, dir1)
        body3.AppendHybridShape(ex2)
        rf308 = part1.CreateReferenceFromObject(ex2)

        #radi and asm
        biti = ShFactory.AddNewFilletBiTangent(rf307, rf206, 5.000000, 1, 1, 1, 0)
        body4.AppendHybridShape(biti)
        rf309 = part1.CreateReferenceFromObject(biti)

        biti = ShFactory.AddNewFilletBiTangent(rf308, rf207, 5.000000, -1, 1, 1, 0)
        body4.AppendHybridShape(biti)
        rf310 = part1.CreateReferenceFromObject(biti)

        part1.InWorkObject = body5
        ts2 = SF.AddNewThickSurface(rf00, 0, 1, 0.000000)
        ts2.Surface = rf310
        l2 = ts2.TopOffset
        l2.Value = ts
        part1.UpdateObject(ts2)

        ts3 = SF.AddNewThickSurface(rf00, 0, 1, 0.000000)
        ts3.Surface = rf309
        l3 = ts3.TopOffset
        l3.Value = -ts
        part1.UpdateObject(ts3)

        #hide excess geometry
        selection1 = partDocument1.Selection
        visPropertySet1 = selection1.VisProperties
        selection1.Add(body1)
        selection1.Add(body3)
        selection1.Add(body4)
        selection1.Add(body6)
        visPropertySet1 = visPropertySet1.Parent
        visPropertySet1.SetShow(1)


        i = i + 1


    part1.Update()

    
    path2 = "D:\\CAD_library_sampling\\sample17\\"
    #save version without holes and output empty notepad
    partDocument1.SaveAs(path2+"SP_"+str(I)+".catpart")
    partDocument1.ExportData(path2+"SP_"+str(I)+".stp", "stp")
    ver_list1 = vertex_list("D:\CAD_library_sampling\sample17\SP_"+str(I)+".stp")
    stre = ""
    with open(path2+"SP_"+str(I)+"_metadata.txt", "a") as text_file:
        text_file.write(stre)
    


    #make holes show
    i = 0
    while i < no_stringer:
        ii = 0
        while ii < noh:
            iii = 1
            while iii < 3:
                split1 = SF.AddNewSplit(rf00,0)#, catPositiveSide)

                bds1 = part1.HybridBodies

                hb1 = bds1.Item("Holes")

                hs1= hb1.HybridShapes

                cyl_str = "C_"+str(iii)+"_"+str(i)+"_"+str(ii)
                #print(cyl_str)
                cyl1 = hs1.Item(cyl_str)
                
                reference2 = part1.CreateReferenceFromObject(cyl1)

                split1.Surface = reference2

                part1.UpdateObject(split1)

                iii = iii + 1
            ii = ii + 1
        i = i + 1

    #save version with holes
    partDocument1.SaveAs(path2+"SP_"+str(I+1)+".catpart")
    partDocument1.ExportData(path2+"SP_"+str(I+1)+".stp", "stp")
    ver_list2 = vertex_list("D:\CAD_library_sampling\sample17\SP_"+str(I+1)+".stp")

    #compare 2 vertex lists
    diff = []
    for l2 in ver_list2:
        ex = True
        for l1 in ver_list1:
            if l1.x == l2.x and l1.y == l2.y and l1.z == l2.z:
                ex = False
            
        if ex == True:
            diff.append(l2)

    #.txt file for training
    iii = 0
    stre = ""
    alo = []
    while iii < len(diff):
        
        if iii not in alo:
            iv = iii+1
            stre += "\n hole\n"
            stre += str(diff[iii].x)+","+str(diff[iii].y)+","+str(diff[iii].z)+"\n"
            while iv < len(diff):
                #print(alo)
                if iv not in alo:
                    #distance only in x y because holes only done in z direction for now
                    ddst = math.sqrt((diff[iv].x-diff[iii].x)**2+(diff[iv].y-diff[iii].y)**2)#(diff[iv].z-diff[iii].z)**2)
                    if ddst < 2.05*rh:
                        stre += str(diff[iv].x)+","+str(diff[iv].y)+","+str(diff[iv].z)+"\n"
                        alo.append(iv)
                iv = iv + 1
        iii = iii + 1

    with open(path2+"SP_"+str(I+1)+"_metadata.txt", "a") as text_file:
        text_file.write(stre)


    partDocument1.Close()

def xz_curve(x,a=0,b=0,c=0,d=2, e =0):
    #y = a*x**2 + b*x + c
    z = a*(x+e)**d+b*x+c
    return(z)

def holes_as_defined():
    print("x")
    #takes "holes" geo set and punches through to visualize in 3D

#stiffened pannel run:
'''
import random
I = 3510
while I < 10000:
    xmax = random.randint(800, 1500)
    ymax = random.randint(1400,3000)
    no_stringer = random.randint(1,5)
    t = random.randint(4,15)/2
    ts = random.randint(1,6)
    str_h = random.randint(30,100)
    str_w = random.randint(40,min(int(xmax/no_stringer)-109,280))
    rh = random.randint(100,500)/100
    noh = random.randint(1,10)
    a1 = random.randint(100,5000)/10000
    a2 = random.randint(100,5000)/10000
    d1 = random.randint(0,1250)/1000
    d2 = random.randint(0,1250)/1000
    b1 = random.randint(0,250)/1000
    b2 = random.randint(0,250)/1000
    e1 = random.randint(0,500)
    e2 = random.randint(0,500)
    c1 = random.randint(-50,50)
    c2 = random.randint(-50,50)   


    stiffened_panel(I,xmax,ymax,no_stringer,t,ts,str_h,str_w,rh,noh,
                    a1=a1,a2=a2,b1=b1,b2=b2,c1=c1,c2=c2,d1=d2,e1=e1,e2=e2)
    I = I + 2
'''
def extra_edge_cuts(I,p8arr,ex1, sample,noh,rh,posH):
    #generates holes which are initiated over an edge
    #important to create non-clean holes, but still realistic

    #Setting up CATIA modelling environment
    CATIA = win32com.client.Dispatch("CATIA.Application")
    #record deletion of product....

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
    body1.Name="Wireframe"
    # Surfaces group
    body3 = bodies1.Add()
    body3.Name="Surfaces"
    body4 = bodies1.Add()
    body4.Name="SourceLoft"

    body6 = bodies1.Add()
    body6.Name = "Holes"
    hs1 = body1.HybridShapes
    hs3 = body3.HybridShapes

    #reference direction plane
    OE = part1.OriginElements
    hspe = OE.PlaneXY
    ref111 = part1.CreateReferenceFromObject(hspe)
    dir1 = ShFactory.AddNewDirection(ref111)
    #plane to start second shape on
    off = ShFactory.AddNewPlaneOffset(ref111, -5, True)
    body1.AppendHybridShape(off)
    ref222 = part1.CreateReferenceFromObject(off)
    #limiting ceiling plane
    off2 = ShFactory.AddNewPlaneOffset(ref111, -100, True)
    body1.AppendHybridShape(off2)
    ref444 = part1.CreateReferenceFromObject(off2)


    #create 8 points
    i = 0
    while i < 8:
        point=ShFactory.AddNewPointCoord(p8arr[i,0],p8arr[i,1],p8arr[i,2])
        body1.AppendHybridShape(point)
        i = i + 1
        point.Name = "P"+str(i)

    #additional 4 points for base of second shape
    i = 0
    while i < 4:
        point=ShFactory.AddNewPointCoord(p8arr[i+4,0],p8arr[i+4,1],1)
        body1.AppendHybridShape(point)
        i = i + 1
        point.Name = "P"+str(i+8)        

    #all points above together to generate surfaces
    i = 0
    while i < 12:
        #starting point of each surface initiates new "fill"
        if (i == 0) or (i == 4) or (i == 8):
            fl = ShFactory.AddNewFill()
        
        poc1 = hs1.Item("P"+str(i+1))
        r1 = part1.CreateReferenceFromObject(poc1)

        #each fourth line connects to first point, to create surface
        if i == 3 or i == 7 or i == 11:
            poc2 = hs1.Item("P"+str(i-2))
        else:
            poc2 = hs1.Item("P"+str(i+2))
        r2 = part1.CreateReferenceFromObject(poc2)

        lpt = ShFactory.AddNewLinePtPt(r1, r2)
        body1.AppendHybridShape(lpt)
        r3 = part1.CreateReferenceFromObject(lpt)
        lpt.Name = "L"+str(i)

        #close each section
        fl.AddBound(r3)
        if i == 3 or i ==7 or i == 11:
            fl.Continuity = 1
            fl.Detection = 2
            fl.AdvancedTolerantMode = 2
            body3.AppendHybridShape(fl)
            fl.Name = "FL"+str(i)

        i = i + 1

    #connect wire for extrusion and more clear cut-out
    pt = hs1.Item("L4")
    r10 = part1.CreateReferenceFromObject(pt)
    pt = hs1.Item("L5")
    r11 = part1.CreateReferenceFromObject(pt)
    asm = ShFactory.AddNewJoin(r10, r11)
    pt = hs1.Item("L6")
    r12 = part1.CreateReferenceFromObject(pt)
    asm.AddElement(r12)
    pt = hs1.Item("L7")
    r13 = part1.CreateReferenceFromObject(pt)
    asm.AddElement(r13)
    asm.SetConnex(1)
    asm.SetManifold(1)
    asm.SetSimplify(0)
    asm.SetSuppressMode(0)
    asm.SetDeviation(0.001000)
    asm.SetAngularToleranceMode(0)
    asm.SetAngularTolerance(0.500000)
    asm.SetFederationPropagation(0)
    body1.AppendHybridShape(asm)
    r14 = part1.CreateReferenceFromObject(asm)

    #extrude to accomodate for shapes where 2nd makes cut into the first
    ex = ShFactory.AddNewExtrude(r14, 100.000000, 0.000000, dir1)
    ex.SymmetricalExtension = 0
    body3.AppendHybridShape(ex)
    r15 = part1.CreateReferenceFromObject(ex)

    #assemble the two surfaces
    fllref = hs3.Item("FL7")
    r9 = part1.CreateReferenceFromObject(fllref)
    asm2 = ShFactory.AddNewJoin(r15, r9)
    asm2.SetConnex(1)
    asm2.SetManifold(1)
    asm2.SetSimplify(0)
    asm2.SetSuppressMode(0)
    asm2.SetDeviation(0.001000)
    asm2.SetAngularToleranceMode(0)
    asm2.SetAngularTolerance(0.500000)
    asm2.SetFederationPropagation(0)
    body3.AppendHybridShape(asm2)
    r16 = part1.CreateReferenceFromObject(asm2)

    #prepare for solids modelling
    SF = part1.ShapeFactory
    bodies1 = part1.Bodies
    b1 = bodies1.Item("PartBody")
    part1.InWorkObject = b1
    rfX = part1.CreateReferenceFromName("")

    #main pad
    pad1 = SF.AddNewPadFromRef(rfX, 5)
    fllref = hs3.Item("FL3")
    r7 = part1.CreateReferenceFromObject(fllref)
    pad1.SetProfileElement(r7)
    pad1.SetDirection(ref222)
    limit1 = pad1.FirstLimit
    length1 = limit1.Dimension
    length1.Value = ex1
    part1.UpdateObject(pad1)

    #second pad
    pad1 = SF.AddNewPadFromRef(rfX, 5)
    fllref = hs3.Item("FL11")
    r8 = part1.CreateReferenceFromObject(fllref)
    pad1.SetProfileElement(r8)
    pad1.SetDirection(ref222)
    limit1 = pad1.FirstLimit
    length1 = limit1.Dimension
    length1.Value = 100
    part1.UpdateObject(pad1)

    #adjust the top pad for the appropriate surface
    split1 = SF.AddNewSplit(rfX, 1)
    split1.Surface = r16
    part1.UpdateObject(split1)


    #create hole geometry
    i = 0
    while i < noh:
        poc3 = ShFactory.AddNewPointOnCurveWithReferenceFromPercent(r14, r13, (posH)/noh+i*(1/noh), False)
        body6.AppendHybridShape(poc3)
        r20 = part1.CreateReferenceFromObject(poc3)

        #make cylinder for cutout
        c2 = ShFactory.AddNewCylinder(r20, rh, 100.000000, 100.000000, dir1)
        rt3 = part1.CreateReferenceFromObject(c2)
        body6.AppendHybridShape(c2)
        c2.Name = "C_1_"+str(i)

        i = i + 1

    #hide excess geometry
    selection1 = partDocument1.Selection
    visPropertySet1 = selection1.VisProperties
    selection1.Add(body1)
    selection1.Add(body3)
    selection1.Add(body6)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)

    part1.Update()
    path2 = "D:\\CAD_library_sampling\\sample16\\"
    #save version without holes and output empty notepad
    partDocument1.SaveAs(path2+sample+"_"+str(I)+".catpart")
    partDocument1.ExportData(path2+sample+"_"+str(I)+".stp", "stp")
    ver_list1 = vertex_list("D:\\CAD_library_sampling\\sample16\\"+sample+"_"+str(I)+".stp")
    stre = ""
    with open(path2+sample+"_"+str(I)+"_metadata.txt", "a") as text_file:
        text_file.write(stre)

    #make holes show
    ii = 0
    while ii < noh:
        split1 = SF.AddNewSplit(rfX,0)#, catPositiveSide)
        bds1 = part1.HybridBodies
        hb1 = bds1.Item("Holes")
        hs1= hb1.HybridShapes
        cyl_str = "C_1_"+str(ii)
        cyl1 = hs1.Item(cyl_str)
        
        reference2 = part1.CreateReferenceFromObject(cyl1)
        split1.Surface = reference2
        part1.UpdateObject(split1)

        ii = ii + 1

    part1.Update()
    #save version with holes
    partDocument1.SaveAs(path2+sample+"_"+str(I+1)+".catpart")
    partDocument1.ExportData(path2+sample+"_"+str(I+1)+".stp", "stp")
    ver_list2 = vertex_list("D:\\CAD_library_sampling\\sample16\\"+sample+"_"+str(I+1)+".stp")

    #compare 2 vertex lists
    diff = []
    for l2 in ver_list2:
        ex = True
        for l1 in ver_list1:
            if l1.x == l2.x and l1.y == l2.y and l1.z == l2.z:
                ex = False
            
        if ex == True:
            diff.append(l2)

    #.txt file for training
    iii = 0
    stre = ""
    alo = []
    while iii < len(diff):
        
        if iii not in alo:
            iv = iii+1
            stre += "\n hole\n"
            stre += str(diff[iii].x)+","+str(diff[iii].y)+","+str(diff[iii].z)+"\n"
            while iv < len(diff):
                #print(alo)
                if iv not in alo:
                    #distance only in x y because holes only done in z direction for now
                    ddst = math.sqrt((diff[iv].x-diff[iii].x)**2+(diff[iv].y-diff[iii].y)**2)#(diff[iv].z-diff[iii].z)**2)
                    if ddst < 2.05*rh:
                        stre += str(diff[iv].x)+","+str(diff[iv].y)+","+str(diff[iv].z)+"\n"
                        alo.append(iv)
                iv = iv + 1
        iii = iii + 1

    #hole metadata store
    with open(path2+sample+"_"+str(I+1)+"_metadata.txt", "a") as text_file:
        text_file.write(stre)
    partDocument1.Close()
'''
#sampling x
i = 42
ee = 0
while i < 10000: 

    p8arr = np.zeros((8,3))

    #x_bot
    p8arr[0,0] = 200
    p8arr[1,0] = 200
    p8arr[2,0] = -200
    p8arr[3,0] = -200

    #y_bot
    p8arr[0,1] = 200
    p8arr[1,1] = -200
    p8arr[2,1] = -200
    p8arr[3,1] = 200 

    #x_top
    p8arr[4,0] = random.randint(0,150)
    p8arr[5,0] = random.randint(0,150)
    p8arr[6,0] = random.randint(-150,0)
    p8arr[7,0] = random.randint(-150,0)

    #y_top
    p8arr[4,1] = random.randint(0,150)
    p8arr[5,1] = random.randint(-150,0)
    p8arr[6,1] = random.randint(-150,0)
    p8arr[7,1] = random.randint(0,150)        

    #z_top
    p8arr[4,2] = random.randint(3,70)
    p8arr[5,2] = random.randint(3,70)
    p8arr[6,2] = random.randint(3,70)
    p8arr[7,2] = random.randint(3,70)  

    #bottom extrude 
    ex1 = random.randint(5,15)
    noh = random.randint(1,10)
    rh = random.randint(50,700)/100
    posH = random.randint(0,100)/100

    try:
        extra_edge_cuts(i,p8arr,ex1, "eec",noh,rh,posH)
    except:
        print("number "+str(i)+" not finished, error")

        ee = ee + 1
        if ee > 100:
            break

    i = i + 2
'''

def half_hole(I,p8arr,ex1, sample,noh,rh,posH):
    #generates half hole in edges, not qualifiying as holes`

    #Setting up CATIA modelling environment
    CATIA = win32com.client.Dispatch("CATIA.Application")
    #record deletion of product....

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
    body1.Name="Wireframe"
    # Surfaces group
    body3 = bodies1.Add()
    body3.Name="Surfaces"
    body4 = bodies1.Add()
    body4.Name="SourceLoft"

    body6 = bodies1.Add()
    body6.Name = "Holes"
    hs1 = body1.HybridShapes
    hs3 = body3.HybridShapes

    #reference direction plane
    OE = part1.OriginElements
    hspe = OE.PlaneXY
    ref111 = part1.CreateReferenceFromObject(hspe)
    dir1 = ShFactory.AddNewDirection(ref111)
    #plane to start second shape on
    off = ShFactory.AddNewPlaneOffset(ref111, -5, True)
    body1.AppendHybridShape(off)
    ref222 = part1.CreateReferenceFromObject(off)
    #limiting ceiling plane
    off2 = ShFactory.AddNewPlaneOffset(ref111, -100, True)
    body1.AppendHybridShape(off2)
    ref444 = part1.CreateReferenceFromObject(off2)


    #create 8 points
    i = 0
    while i < 8:
        point=ShFactory.AddNewPointCoord(p8arr[i,0],p8arr[i,1],p8arr[i,2])
        body1.AppendHybridShape(point)
        i = i + 1
        point.Name = "P"+str(i)

    #additional 4 points for base of second shape
    i = 0
    while i < 4:
        point=ShFactory.AddNewPointCoord(p8arr[i+4,0],p8arr[i+4,1],1)
        body1.AppendHybridShape(point)
        i = i + 1
        point.Name = "P"+str(i+8)        

    #all points above together to generate surfaces
    i = 0
    while i < 12:
        #starting point of each surface initiates new "fill"
        if (i == 0) or (i == 4) or (i == 8):
            fl = ShFactory.AddNewFill()
        
        poc1 = hs1.Item("P"+str(i+1))
        r1 = part1.CreateReferenceFromObject(poc1)

        #each fourth line connects to first point, to create surface
        if i == 3 or i == 7 or i == 11:
            poc2 = hs1.Item("P"+str(i-2))
        else:
            poc2 = hs1.Item("P"+str(i+2))
        r2 = part1.CreateReferenceFromObject(poc2)

        lpt = ShFactory.AddNewLinePtPt(r1, r2)
        body1.AppendHybridShape(lpt)
        r3 = part1.CreateReferenceFromObject(lpt)
        lpt.Name = "L"+str(i)

        #close each section
        fl.AddBound(r3)
        if i == 3 or i ==7 or i == 11:
            fl.Continuity = 1
            fl.Detection = 2
            fl.AdvancedTolerantMode = 2
            body3.AppendHybridShape(fl)
            fl.Name = "FL"+str(i)

        i = i + 1

    #connect wire for extrusion and more clear cut-out
    pt = hs1.Item("L4")
    r10 = part1.CreateReferenceFromObject(pt)
    pt = hs1.Item("L5")
    r11 = part1.CreateReferenceFromObject(pt)
    asm = ShFactory.AddNewJoin(r10, r11)
    pt = hs1.Item("L6")
    r12 = part1.CreateReferenceFromObject(pt)
    asm.AddElement(r12)
    pt = hs1.Item("L7")
    r13 = part1.CreateReferenceFromObject(pt)
    asm.AddElement(r13)
    asm.SetConnex(1)
    asm.SetManifold(1)
    asm.SetSimplify(0)
    asm.SetSuppressMode(0)
    asm.SetDeviation(0.001000)
    asm.SetAngularToleranceMode(0)
    asm.SetAngularTolerance(0.500000)
    asm.SetFederationPropagation(0)
    body1.AppendHybridShape(asm)
    r14 = part1.CreateReferenceFromObject(asm)

    #extrude to accomodate for shapes where 2nd makes cut into the first
    ex = ShFactory.AddNewExtrude(r14, 100.000000, 0.000000, dir1)
    ex.SymmetricalExtension = 0
    body3.AppendHybridShape(ex)
    r15 = part1.CreateReferenceFromObject(ex)

    #assemble the two surfaces
    fllref = hs3.Item("FL7")
    r9 = part1.CreateReferenceFromObject(fllref)
    asm2 = ShFactory.AddNewJoin(r15, r9)
    asm2.SetConnex(1)
    asm2.SetManifold(1)
    asm2.SetSimplify(0)
    asm2.SetSuppressMode(0)
    asm2.SetDeviation(0.001000)
    asm2.SetAngularToleranceMode(0)
    asm2.SetAngularTolerance(0.500000)
    asm2.SetFederationPropagation(0)
    body3.AppendHybridShape(asm2)
    r16 = part1.CreateReferenceFromObject(asm2)

    #prepare for solids modelling
    SF = part1.ShapeFactory
    bodies1 = part1.Bodies
    b1 = bodies1.Item("PartBody")
    part1.InWorkObject = b1
    rfX = part1.CreateReferenceFromName("")

    #main pad -- not applicable here
    #pad1 = SF.AddNewPadFromRef(rfX, 5)
    #fllref = hs3.Item("FL3")
    #r7 = part1.CreateReferenceFromObject(fllref)
    #pad1.SetProfileElement(r7)
    #pad1.SetDirection(ref222)
    #limit1 = pad1.FirstLimit
    #length1 = limit1.Dimension
    #length1.Value = ex1
    #part1.UpdateObject(pad1)

    #second pad
    pad1 = SF.AddNewPadFromRef(rfX, 5)
    fllref = hs3.Item("FL11")
    r8 = part1.CreateReferenceFromObject(fllref)
    pad1.SetProfileElement(r8)
    pad1.SetDirection(ref222)
    limit1 = pad1.FirstLimit
    length1 = limit1.Dimension
    length1.Value = 100
    part1.UpdateObject(pad1)

    #adjust the top pad for the appropriate surface
    split1 = SF.AddNewSplit(rfX, 1)
    split1.Surface = r16
    part1.UpdateObject(split1)


    #create hole geometry
    i = 0
    while i < noh:
        poc3 = ShFactory.AddNewPointOnCurveWithReferenceFromPercent(r14, r13, (posH)/noh+i*(1/noh), False)
        body6.AppendHybridShape(poc3)
        r20 = part1.CreateReferenceFromObject(poc3)

        #make cylinder for cutout
        c2 = ShFactory.AddNewCylinder(r20, rh, 100.000000, 100.000000, dir1)
        rt3 = part1.CreateReferenceFromObject(c2)
        body6.AppendHybridShape(c2)
        c2.Name = "C_1_"+str(i)

        i = i + 1

    #hide excess geometry
    selection1 = partDocument1.Selection
    visPropertySet1 = selection1.VisProperties
    selection1.Add(body1)
    selection1.Add(body3)
    selection1.Add(body6)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)

    #make holes show
    ii = 0
    while ii < noh:
        split1 = SF.AddNewSplit(rfX,0)#, catPositiveSide)
        bds1 = part1.HybridBodies
        hb1 = bds1.Item("Holes")
        hs1= hb1.HybridShapes
        cyl_str = "C_1_"+str(ii)
        cyl1 = hs1.Item(cyl_str)
        
        reference2 = part1.CreateReferenceFromObject(cyl1)
        split1.Surface = reference2
        part1.UpdateObject(split1)

        ii = ii + 1

    part1.Update()
    path2 = "D:\\CAD_library_sampling\\sample18\\"
    #save version without holes and output empty notepad
    partDocument1.SaveAs(path2+sample+"_"+str(I)+".catpart")
    partDocument1.ExportData(path2+sample+"_"+str(I)+".stp", "stp")
    stre = ""
    with open(path2+sample+"_"+str(I)+"_metadata.txt", "a") as text_file:
        text_file.write(stre)


    partDocument1.Close()

'''
#sampling x
i = 0
ee = 0
while i < 5000: 

    p8arr = np.zeros((8,3))

    #x_bot
    p8arr[0,0] = 200
    p8arr[1,0] = 200
    p8arr[2,0] = -200
    p8arr[3,0] = -200

    #y_bot
    p8arr[0,1] = 200
    p8arr[1,1] = -200
    p8arr[2,1] = -200
    p8arr[3,1] = 200 

    #x_top
    p8arr[4,0] = random.randint(0,150)
    p8arr[5,0] = random.randint(0,150)
    p8arr[6,0] = random.randint(-150,0)
    p8arr[7,0] = random.randint(-150,0)

    #y_top
    p8arr[4,1] = random.randint(0,150)
    p8arr[5,1] = random.randint(-150,0)
    p8arr[6,1] = random.randint(-150,0)
    p8arr[7,1] = random.randint(0,150)        

    #z_top
    p8arr[4,2] = random.randint(3,70)
    p8arr[5,2] = random.randint(3,70)
    p8arr[6,2] = random.randint(3,70)
    p8arr[7,2] = random.randint(3,70)  

    #bottom extrude 
    ex1 = random.randint(5,15)
    noh = random.randint(1,10)
    rh = random.randint(50,700)/100
    posH = random.randint(0,100)/100

    try:
        half_hole(i,p8arr,ex1, "eec",noh,rh,posH)
    except:
        print("number "+str(i)+" not finished, error")

        ee = ee + 1
        if ee > 100:
            break

    i = i + 1
'''

def major_radii(i,p8arr,radii,ref):
    #first sample of surfaces with major radii 
    #-- straigt surfaces only
    #-- constant radii only

    #Setting up CATIA modelling environment
    CATIA = win32com.client.Dispatch("CATIA.Application")
    #record deletion of product....

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
    body1.Name="Wireframe"
    # Surfaces group
    body3 = bodies1.Add()
    body3.Name="CurvedSurface"
    body4 = bodies1.Add()
    body4.Name="NoCurveAsm"

    #reference direction plane
    OE = part1.OriginElements
    hspe = OE.PlaneXY
    ref111 = part1.CreateReferenceFromObject(hspe)
    dir1 = ShFactory.AddNewDirection(ref111)

    #creating construction points 
    ii = 0
    r4 = []
    while ii < np.size(p8arr,0):
        #create point for each reference
        point1=ShFactory.AddNewPointCoord(p8arr[ii,0],p8arr[ii,1],p8arr[ii,2])
        body1.AppendHybridShape(point1)
        r1 = part1.CreateReferenceFromObject(point1)

        #connect the two points with a line
        if ii > 0:
            lpt = ShFactory.AddNewLinePtPt(r1, r2)
            body1.AppendHybridShape(lpt)
            lpt.Name="cnn_line_"+str(ii)
            r3 = part1.CreateReferenceFromObject(lpt)

            #extrude each line
            ex1 = ShFactory.AddNewExtrude(r3, 75.000000, 0.000000, dir1)
            body1.AppendHybridShape(ex1)
            #lpt.Name="cnn_line_"+str(ii)
            r4 = part1.CreateReferenceFromObject(ex1)

            if ii > 1:
                #joins for alternative build without radii - for .stp comparison
                asm = ShFactory.AddNewJoin(r4, r5)
                body4.AppendHybridShape(asm)
                r5 = part1.CreateReferenceFromObject(asm)

                #try clause so that bi-tangent can be reversed where needed (quite common)
                try:
                    casm = ShFactory.AddNewFilletBiTangent(r4, r6, radii, 1, 1, 1, 0)
                    body3.AppendHybridShape(casm)
                    part1.Update()
                except:          
                    #when bi-tangent is to be reversed - the first bi-tangent needs to be deleted first
                    selection1 = partDocument1.Selection
                    selection1.Clear()
                    selection1.Add(casm)
                    selection1.Delete()

                    #fixing the bi-tangent with oposite direction on both surfaces
                    casm = ShFactory.AddNewFilletBiTangent(r4, r6, radii, -1, -1, 1, 0)
                    body3.AppendHybridShape(casm)  
                    part1.Update()
                r6 = part1.CreateReferenceFromObject(casm) 
            else:
                #in first loop just generate references
                r5 = r4
                r6 = r4

        r2 = r1

        ii += 1

    #hide n seek
    selection1 = partDocument1.Selection
    selection1.Clear()
    visPropertySet1 = selection1.VisProperties
    selection1.Add(body1)
    selection1.Add(body3)
    selection1.Add(body4)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)
    part1.Update()

    #creating reference (no-radii) body
    bodies1 = part1.Bodies
    body10 = bodies1.Item("PartBody")
    part1.InWorkObject = body10
    SF = part1.ShapeFactory
    ref1 = part1.CreateReferenceFromName("")
    tt = SF.AddNewThickSurface(r5, 0, 1.000000, 0.000000)
    part1.Update()

    #save v1
    path2 = "D:\\CAD_library_sampling\\sample30\\"
    partDocument1.SaveAs(path2+"no_curves\\"+ref+"_"+str(i)+".catpart")
    partDocument1.ExportData(path2+"no_curves\\"+ref+"_"+str(i)+".stp", "stp")
    ver_list1 = vertex_list("D:\\CAD_library_sampling\\sample30\\no_curves\\"+ref+"_"+str(i)+".stp")

    #delete existing thickness
    selection1 = partDocument1.Selection
    selection1.Clear()
    part1 = partDocument1.Part
    shapes1 = body10.Shapes
    ts = shapes1.Item("ThickSurface.1")
    selection1.Add(ts)
    selection1.Delete()

    #create thickness from curved surface
    tt = SF.AddNewThickSurface(r6, 0, 1.000000, 0.000000)
    part1.Update()

    #save v2
    path2 = "D:\\CAD_library_sampling\\sample30\\"
    partDocument1.SaveAs(path2+ref+"_"+str(i)+".catpart")
    partDocument1.ExportData(path2+ref+"_"+str(i)+".stp", "stp")
    ver_list2 = vertex_list("D:\\CAD_library_sampling\\sample30\\"+ref+"_"+str(i)+".stp")

    #compare .stp 1 and .stp 2 --- any new vertices in .stp 2 to be stored for training
    diff = []
    for l2 in ver_list2:
        ex = True
        for l1 in ver_list1:
            if l1.x == l2.x and l1.y == l2.y and l1.z == l2.z:
                ex = False
            
        if ex == True:
            diff.append(l2)

    #test that the expected number of vertices exist (4)
    if len(diff) % 4 == 0:

        #.txt file for training
        iii = 0
        stre = ""
        alo = []
        while iii < len(diff):
            
            if iii not in alo:
                iv = iii+1
                stre += "\nMajor_Radii\n"
                stre += str(diff[iii].x)+","+str(diff[iii].y)+","+str(diff[iii].z)+"\n"
                while iv < len(diff):
                    #print(alo)
                    if iv not in alo:
                        stre += str(diff[iv].x)+","+str(diff[iv].y)+","+str(diff[iv].z)+"\n"
                        alo.append(iv)
                    iv = iv + 1
            iii = iii + 1

        #save metadata
        with open(path2+ref+"_"+str(i)+"_metadata.txt", "a") as text_file:
            text_file.write(stre)

        partDocument1.Close()
    
    else:
        #delete the corresponding catia and step file
        os.remove(path2+ref+"_"+str(i)+".catpart")
        os.remove(path2+ref+"_"+str(i)+".stp")
        print("Run "+str(i)+" was removed. Incorrect number of vertices found.")

'''
#sampling x
i = 0
ee = 0
while i < 5000: 

    ptn = random.randint(3,5)

    p8arr = np.zeros((ptn,3))

    ii = 0
    while ii < ptn:

        #x
        p8arr[ii,0] = ii*50
        #y
        p8arr[ii,1] = random.randint(10,100)
        #z stays 0
        ii = ii + 1

    #bottom extrude 
    radii = random.randint(5,25)

    try:
        major_radii(i,p8arr,radii,"MR")
    except:
        print("number "+str(i)+" not finished, error")

        ee = ee + 1
        if ee > 150:
            break

    i = i + 1
'''

def major_radii_2(i,p8arr,radii,h,ref):
    #second sample of surfaces with major radii 
    #-- triangle

    #Setting up CATIA modelling environment
    CATIA = win32com.client.Dispatch("CATIA.Application")
    #record deletion of product....

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
    body1.Name="Wireframe"
    # Surfaces group
    body3 = bodies1.Add()
    body3.Name="CurvedSurface"
    body4 = bodies1.Add()
    body4.Name="NoCurveAsm"

    #reference direction plane
    OE = part1.OriginElements
    hspe = OE.PlaneXY
    ref111 = part1.CreateReferenceFromObject(hspe)
    dir1 = ShFactory.AddNewDirection(ref111)

    #top of the Pyramid point
    point1=ShFactory.AddNewPointCoord(0,0,h)
    body1.AppendHybridShape(point1)
    r0 = part1.CreateReferenceFromObject(point1)

    #creating construction points 
    ii = 0
    r4 = []
    while ii < np.size(p8arr,0)+1:

        if ii < np.size(p8arr,0):
            #create point for each reference
            point1=ShFactory.AddNewPointCoord(p8arr[ii,0],p8arr[ii,1],p8arr[ii,2])
            body1.AppendHybridShape(point1)
            r1 = part1.CreateReferenceFromObject(point1)
            if ii == 0:
                r77 = r1

        
            lpt = ShFactory.AddNewLinePtPt(r1, r0)
            body1.AppendHybridShape(lpt)
            lpt.Name="cnt_line_"+str(ii)
            r10 = part1.CreateReferenceFromObject(lpt)

        #connect the two points with a line
        if ii > 0 and ii < np.size(p8arr,0):
            lpt = ShFactory.AddNewLinePtPt(r1, r2)
            body1.AppendHybridShape(lpt)
            lpt.Name="cnn_line_"+str(ii)
            r3 = part1.CreateReferenceFromObject(lpt)

        elif ii >= np.size(p8arr,0):
            lpt = ShFactory.AddNewLinePtPt(r77, r0)
            body1.AppendHybridShape(lpt)
            lpt.Name="cnt_line_"+str(ii)
            r10 = part1.CreateReferenceFromObject(lpt)

            lpt = ShFactory.AddNewLinePtPt(r77, r2)
            body1.AppendHybridShape(lpt)
            lpt.Name="cnn_line_"+str(ii)
            r3 = part1.CreateReferenceFromObject(lpt)


        if ii > 0:
            fll = ShFactory.AddNewFill()
            fll.AddBound(r10)
            fll.AddBound(r3)
            fll.AddBound(r100)
            fll.Continuity = 1
            fll.Detection = 2
            fll.AdvancedTolerantMode = 2
            body1.AppendHybridShape(fll)
            r4 = part1.CreateReferenceFromObject(fll)

            
            if ii > 1:
                #joins for alternative build without radii - for .stp comparison
                asm = ShFactory.AddNewJoin(r4, r5)
                body4.AppendHybridShape(asm)
                r5 = part1.CreateReferenceFromObject(asm)

                #try clause so that bi-tangent can be reversed where needed (quite common)
                #horrible use of try-except, kids dont try this at home
                try:
                    casm = ShFactory.AddNewFilletBiTangent(r4, r6, radii, 1, 1, 1, 0)
                    body3.AppendHybridShape(casm)
                    part1.Update()
                except:       
                    try:   
                        #when bi-tangent is to be reversed - the first bi-tangent needs to be deleted first
                        selection1 = partDocument1.Selection
                        selection1.Clear()
                        selection1.Add(casm)
                        selection1.Delete()

                        #fixing the bi-tangent with oposite direction on both surfaces
                        casm = ShFactory.AddNewFilletBiTangent(r4, r6, radii, -1, -1, 1, 0)
                        body3.AppendHybridShape(casm)  
                        part1.Update()
                    except:
                        try:
                            #when bi-tangent is to be reversed - the first bi-tangent needs to be deleted first
                            selection1 = partDocument1.Selection
                            selection1.Clear()
                            selection1.Add(casm)
                            selection1.Delete()

                            #fixing the bi-tangent with oposite direction on both surfaces
                            casm = ShFactory.AddNewFilletBiTangent(r4, r6, radii, 1, -1, 1, 0)
                            body3.AppendHybridShape(casm)  
                            part1.Update()
                        except:
                            #when bi-tangent is to be reversed - the first bi-tangent needs to be deleted first
                            selection1 = partDocument1.Selection
                            selection1.Clear()
                            selection1.Add(casm)
                            selection1.Delete()

                            #fixing the bi-tangent with oposite direction on both surfaces
                            casm = ShFactory.AddNewFilletBiTangent(r4, r6, radii, -1, 1, 1, 0)
                            body3.AppendHybridShape(casm)  
                            part1.Update()



                r6 = part1.CreateReferenceFromObject(casm) 
            else:
                #in first loop just generate references
                r5 = r4
                r6 = r4
            

        r100 = r10
        r2 = r1

        ii += 1
    
    #hide n seek
    selection1 = partDocument1.Selection
    selection1.Clear()
    visPropertySet1 = selection1.VisProperties
    selection1.Add(body1)
    selection1.Add(body3)
    selection1.Add(body4)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)
    part1.Update()

    #creating reference (no-radii) body
    bodies1 = part1.Bodies
    body10 = bodies1.Item("PartBody")
    part1.InWorkObject = body10
    SF = part1.ShapeFactory
    ref1 = part1.CreateReferenceFromName("")
    tt = SF.AddNewThickSurface(r5, 0, 1.000000, 0.000000)
    part1.Update()

    #save v1
    path2 = "D:\\CAD_library_sampling\\sample31\\"
    partDocument1.SaveAs(path2+"no_curves\\"+ref+"_"+str(i)+".catpart")
    partDocument1.ExportData(path2+"no_curves\\"+ref+"_"+str(i)+".stp", "stp")
    ver_list1 = vertex_list("D:\\CAD_library_sampling\\sample31\\no_curves\\"+ref+"_"+str(i)+".stp")

    #delete existing thickness
    selection1 = partDocument1.Selection
    selection1.Clear()
    part1 = partDocument1.Part
    shapes1 = body10.Shapes
    ts = shapes1.Item("ThickSurface.1")
    selection1.Add(ts)
    selection1.Delete()

    #create thickness from curved surface
    tt = SF.AddNewThickSurface(r6, 0, 1.000000, 0.000000)
    part1.Update()

    #save v2
    path2 = "D:\\CAD_library_sampling\\sample31\\"
    partDocument1.SaveAs(path2+ref+"_"+str(i)+".catpart")
    partDocument1.ExportData(path2+ref+"_"+str(i)+".stp", "stp")
    ver_list2 = vertex_list("D:\\CAD_library_sampling\\sample31\\"+ref+"_"+str(i)+".stp")

    #compare .stp 1 and .stp 2 --- any new vertices in .stp 2 to be stored for training
    diff = []
    for l2 in ver_list2:
        ex = True
        for l1 in ver_list1:
            if l1.x == l2.x and l1.y == l2.y and l1.z == l2.z:
                ex = False
            
        if ex == True:
            diff.append(l2)



    #.txt file for training
    iii = 0
    stre = ""
    alo = []
    while iii < len(diff):
        
        if iii not in alo:
            iv = iii+1
            stre += "\nMajor_Radii\n"
            stre += str(diff[iii].x)+","+str(diff[iii].y)+","+str(diff[iii].z)+"\n"
            while iv < len(diff):
                #print(alo)
                if iv not in alo:
                    stre += str(diff[iv].x)+","+str(diff[iv].y)+","+str(diff[iv].z)+"\n"
                    alo.append(iv)
                iv = iv + 1
        iii = iii + 1

    #save metadata
    with open(path2+ref+"_"+str(i)+"_metadata.txt", "a") as text_file:
        text_file.write(stre)

    partDocument1.Close()

'''  

#sampling x
i = 0
ee = 0
while i < 2500: 

    #ptn = random.randint(3,5)

    p8arr = np.zeros((3,3))



    p8arr[0,0] = random.randint(0,80)
    p8arr[0,1] = random.randint(0,80)
    p8arr[1,0] = random.randint(0,80)
    p8arr[1,1] = random.randint(-80,0)
    p8arr[2,0] = random.randint(-100,-10)
    p8arr[2,1] = random.randint(-40,40)



    #bottom extrude 
    radii = random.randint(5,120)/10
    h = random.randint(20,60)

    try:
        major_radii_2(i,p8arr,radii,h,"MR2")
    except:
        print("number "+str(i)+" not finished, error")#

        ee = ee + 1
        if ee > 150:
            break

    i = i + 1
'''

def major_radii_3(i,x1,x2,z1,z2,ref):
    #second sample of surfaces with major radii 
    #-- triangle

    #Setting up CATIA modelling environment
    CATIA = win32com.client.Dispatch("CATIA.Application")
    #record deletion of product....

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
    body1.Name="Wireframe"
    # Surfaces group
    body3 = bodies1.Add()
    body3.Name="CurvedSurface"
    body4 = bodies1.Add()
    body4.Name="NoCurveAsm"

    #reference direction plane
    OE = part1.OriginElements
    hspe = OE.PlaneZX
    ref111 = part1.CreateReferenceFromObject(hspe)
    dir1 = ShFactory.AddNewDirection(ref111)

    #base 4 points
    point1=ShFactory.AddNewPointCoord(-100,0,0)
    body1.AppendHybridShape(point1)
    r0 = part1.CreateReferenceFromObject(point1)

    point1=ShFactory.AddNewPointCoord(-100,100,0)
    body1.AppendHybridShape(point1)
    r1 = part1.CreateReferenceFromObject(point1)

    point1=ShFactory.AddNewPointCoord(0,100,0)
    body1.AppendHybridShape(point1)
    r2 = part1.CreateReferenceFromObject(point1)

    point1=ShFactory.AddNewPointCoord(0,0,0)
    body1.AppendHybridShape(point1)
    r3 = part1.CreateReferenceFromObject(point1)

    #wall 4 points 
    point1=ShFactory.AddNewPointCoord(x1,0,z1)
    body1.AppendHybridShape(point1)
    r4 = part1.CreateReferenceFromObject(point1)

    point1=ShFactory.AddNewPointCoord(x2,100,z2)
    body1.AppendHybridShape(point1)
    r5 = part1.CreateReferenceFromObject(point1)

    point1=ShFactory.AddNewPointCoord(x2,100,100)
    body1.AppendHybridShape(point1)
    r6 = part1.CreateReferenceFromObject(point1)

    point1=ShFactory.AddNewPointCoord(x1,0,100)
    body1.AppendHybridShape(point1)
    r7 = part1.CreateReferenceFromObject(point1)

    #bottom 4 lines
    lpt = ShFactory.AddNewLinePtPt(r0, r1)
    body1.AppendHybridShape(lpt)
    r11 = part1.CreateReferenceFromObject(lpt)

    lpt = ShFactory.AddNewLinePtPt(r1, r2)
    body1.AppendHybridShape(lpt)
    r12 = part1.CreateReferenceFromObject(lpt)

    lpt = ShFactory.AddNewLinePtPt(r2, r3)
    body1.AppendHybridShape(lpt)
    r13 = part1.CreateReferenceFromObject(lpt)

    lpt = ShFactory.AddNewLinePtPt(r3, r0)
    body1.AppendHybridShape(lpt)
    r14 = part1.CreateReferenceFromObject(lpt)

    #tob 4 lines
    lpt = ShFactory.AddNewLinePtPt(r4, r5)
    body1.AppendHybridShape(lpt)
    r15 = part1.CreateReferenceFromObject(lpt)

    lpt = ShFactory.AddNewLinePtPt(r5, r6)
    body1.AppendHybridShape(lpt)
    r16 = part1.CreateReferenceFromObject(lpt)

    lpt = ShFactory.AddNewLinePtPt(r6, r7)
    body1.AppendHybridShape(lpt)
    r17 = part1.CreateReferenceFromObject(lpt)

    lpt = ShFactory.AddNewLinePtPt(r7, r4)
    body1.AppendHybridShape(lpt)
    r18 = part1.CreateReferenceFromObject(lpt)

    fll = ShFactory.AddNewFill()
    fll.AddBound(r11)
    fll.AddBound(r12)
    fll.AddBound(r13)
    fll.AddBound(r14)
    fll.Continuity = 1
    fll.Detection = 2
    fll.AdvancedTolerantMode = 2
    body1.AppendHybridShape(fll)
    r20 = part1.CreateReferenceFromObject(fll)

    fll = ShFactory.AddNewFill()
    fll.AddBound(r15)
    fll.AddBound(r16)
    fll.AddBound(r17)
    fll.AddBound(r18)
    fll.Continuity = 1
    fll.Detection = 2
    fll.AdvancedTolerantMode = 2
    body1.AppendHybridShape(fll)
    r21 = part1.CreateReferenceFromObject(fll)

    off = ShFactory.AddNewPlaneOffset(ref111, 100.000000, False) 
    body1.AppendHybridShape(off)
    r30 = part1.CreateReferenceFromObject(off)

    #some try-else will be neede here .... for the 4 circle options....

    rad1 = math.sqrt(x1**2+z1**2)

    c1 = ShFactory.AddNewCircle2PointsRad(r3, r4, ref111, False, rad1, -1) 
    c1.SetLimitation(3)
    body1.AppendHybridShape(c1)
    r31 = part1.CreateReferenceFromObject(c1)

    rad2 = math.sqrt(x2**2+z2**2)

    c1 = ShFactory.AddNewCircle2PointsRad(r2, r5, r30, False, rad2, -1) 
    c1.SetLimitation(3)
    body1.AppendHybridShape(c1)
    r32 = part1.CreateReferenceFromObject(c1)   

    #connect the 2 surfaces
    loft = ShFactory.AddNewLoft()
    loft.SectionCoupling = 1
    loft.Relimitation = 1
    loft.CanonicalDetection = 2

    loft.AddGuide(r31)
    loft.AddGuide(r32)

    loft.AddSectionToLoft(r13, 1, None)
    loft.AddSectionToLoft(r15, -1, None)
    body1.AppendHybridShape(loft)
    r23 = part1.CreateReferenceFromObject(loft)   


    #assemble the surfaces
    asm2 = ShFactory.AddNewJoin(r21, r23)
    asm2.SetConnex(1)
    asm2.SetManifold(1)
    asm2.SetSimplify(0)
    asm2.SetSuppressMode(0)
    asm2.SetDeviation(0.001000)
    asm2.SetAngularToleranceMode(0)
    asm2.SetAngularTolerance(0.500000)
    asm2.SetFederationPropagation(0)
    body3.AppendHybridShape(asm2)
    r23 = part1.CreateReferenceFromObject(asm2)

    asm2 = ShFactory.AddNewJoin(r20, r23)
    asm2.SetConnex(1)
    asm2.SetManifold(1)
    asm2.SetSimplify(0)
    asm2.SetSuppressMode(0)
    asm2.SetDeviation(0.001000)
    asm2.SetAngularToleranceMode(0)
    asm2.SetAngularTolerance(0.500000)
    asm2.SetFederationPropagation(0)
    body4.AppendHybridShape(asm2)
    r50 = part1.CreateReferenceFromObject(asm2)
    
    #hide n seek
    selection1 = partDocument1.Selection
    selection1.Clear()
    visPropertySet1 = selection1.VisProperties
    selection1.Add(body1)
    selection1.Add(body3)
    #selection1.Add(body4)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)
    part1.Update()

    #creating reference (no-radii) body
    #bodies1 = part1.Bodies
    #body10 = bodies1.Item("PartBody")
    #part1.InWorkObject = body10
    #SF = part1.ShapeFactory
    #ref1 = part1.CreateReferenceFromName("")
    #tt = SF.AddNewThickSurface(r50, 0, 1.000000, 0.000000)
    #part1.Update()

    #save v1
    path2 = "D:\\CAD_library_sampling\\sample32\\"
    partDocument1.SaveAs(path2+ref+"_"+str(i)+".catpart")
    partDocument1.ExportData(path2+ref+"_"+str(i)+".stp", "stp")
 
    stre ="\nMajor_Radii\n"
    stre += str(0)+","+str(0)+","+str(0)+"\n"
    stre += str(0)+","+str(100)+","+str(0)+"\n"
    stre += str(x1)+","+str(0)+","+str(z1)+"\n"
    stre += str(x2)+","+str(100)+","+str(z2)+"\n"

    #stre just the 4 points

    #save metadata
    with open(path2+ref+"_"+str(i)+"_metadata.txt", "a") as text_file:
        text_file.write(stre)

    partDocument1.Close()

'''
#sampling x
i = 0
ee = 0
while i < 1000: 

    #ptn = random.randint(3,5)

    x1 = random.randint(10,40)
    x2 = random.randint(10,40)
    #y1
    #y2
    z1 = random.randint(10,40)
    z2 = random.randint(10,40)
    #r1 =
    #r2

    #bottom extrude 
    #radii = random.randint(5,120)/10
    #h = random.randint(20,60)

    try:
        major_radii_3(i,x1,x2,z1,z2,"MR3")
    except:
        print("number "+str(i)+" not finished, error")#

        ee = ee + 1
        if ee > 150:
            break

    i = i + 1
'''

from WS_gen_3 import rand_hole

def major_radii_4(i,p8arr,radii,ref):
    #first sample of surfaces with major radii 
    #-- straigt surfaces only
    #-- constant radii only

    #Setting up CATIA modelling environment
    CATIA = win32com.client.Dispatch("CATIA.Application")
    #record deletion of product....

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
    body1.Name="Wireframe"
    # Surfaces group
    body3 = bodies1.Add()
    body3.Name="CurvedSurface"
    body4 = bodies1.Add()
    body4.Name="NoCurveAsm"

    #reference direction plane
    OE = part1.OriginElements
    hspe = OE.PlaneXY
    ref111 = part1.CreateReferenceFromObject(hspe)
    dir1 = ShFactory.AddNewDirection(ref111)

    #creating construction points 
    ii = 0
    r4 = []
    while ii < np.size(p8arr,0):
        #create point for each reference
        point1=ShFactory.AddNewPointCoord(p8arr[ii,0],p8arr[ii,1],p8arr[ii,2])
        body1.AppendHybridShape(point1)
        r1 = part1.CreateReferenceFromObject(point1)

        #connect the two points with a line
        if ii > 0:
            lpt = ShFactory.AddNewLinePtPt(r1, r2)
            body1.AppendHybridShape(lpt)
            lpt.Name="cnn_line_"+str(ii)
            r3 = part1.CreateReferenceFromObject(lpt)

            #extrude each line
            ex1 = ShFactory.AddNewExtrude(r3, 75.000000, 0.000000, dir1)
            body1.AppendHybridShape(ex1)
            #lpt.Name="cnn_line_"+str(ii)
            r4 = part1.CreateReferenceFromObject(ex1)

            if ii > 1:
                #joins for alternative build without radii - for .stp comparison
                asm = ShFactory.AddNewJoin(r4, r5)
                body4.AppendHybridShape(asm)
                r5 = part1.CreateReferenceFromObject(asm)

                #try clause so that bi-tangent can be reversed where needed (quite common)
                try:
                    casm = ShFactory.AddNewFilletBiTangent(r4, r6, radii, 1, 1, 1, 0)
                    body3.AppendHybridShape(casm)
                    part1.Update()
                except:          
                    #when bi-tangent is to be reversed - the first bi-tangent needs to be deleted first
                    selection1 = partDocument1.Selection
                    selection1.Clear()
                    selection1.Add(casm)
                    selection1.Delete()

                    #fixing the bi-tangent with oposite direction on both surfaces
                    casm = ShFactory.AddNewFilletBiTangent(r4, r6, radii, -1, -1, 1, 0)
                    body3.AppendHybridShape(casm)  
                    part1.Update()
                r6 = part1.CreateReferenceFromObject(casm) 
            else:
                #in first loop just generate references
                r5 = r4
                r6 = r4

        r2 = r1

        ii += 1

    #hide n seek
    selection1 = partDocument1.Selection
    selection1.Clear()
    visPropertySet1 = selection1.VisProperties
    selection1.Add(body1)
    selection1.Add(body3)
    selection1.Add(body4)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)
    part1.Update()

    #creating reference (no-radii) body
    bodies1 = part1.Bodies
    body10 = bodies1.Item("PartBody")
    part1.InWorkObject = body10
    SF = part1.ShapeFactory
    ref1 = part1.CreateReferenceFromName("")
    tt = SF.AddNewThickSurface(r5, 0, 1.000000, 0.000000)
    part1.Update()

    #save v1
    path2 = "D:\\CAD_library_sampling\\sample33\\"
    partDocument1.SaveAs(path2+"no_curves\\"+ref+"_"+str(i)+".catpart")
    partDocument1.ExportData(path2+"no_curves\\"+ref+"_"+str(i)+".stp", "stp")
    ver_list1 = vertex_list("D:\\CAD_library_sampling\\sample33\\no_curves\\"+ref+"_"+str(i)+".stp")

    #delete existing thickness
    selection1 = partDocument1.Selection
    selection1.Clear()
    part1 = partDocument1.Part
    shapes1 = body10.Shapes
    ts = shapes1.Item("ThickSurface.1")
    selection1.Add(ts)
    selection1.Delete()

    #create thickness from curved surface
    tt = SF.AddNewThickSurface(r6, 0, 1.000000, 0.000000)
    part1.Update()

    #save v2
    path2 = "D:\\CAD_library_sampling\\sample33\\"
    partDocument1.SaveAs(path2+ref+"_"+str(i)+".catpart")
    partDocument1.ExportData(path2+ref+"_"+str(i)+".stp", "stp")
    ver_list2 = vertex_list("D:\\CAD_library_sampling\\sample33\\"+ref+"_"+str(i)+".stp")

    #compare .stp 1 and .stp 2 --- any new vertices in .stp 2 to be stored for training
    diff = []
    for l2 in ver_list2:
        ex = True
        for l1 in ver_list1:
            if l1.x == l2.x and l1.y == l2.y and l1.z == l2.z:
                ex = False
            
        if ex == True:
            diff.append(l2)

    #test that the expected number of vertices exist (4)
    if len(diff) % 4 == 0:

        #.txt file for training
        iii = 0
        stre = ""
        alo = []
        while iii < len(diff):
            
            if iii not in alo:
                iv = iii+1
                stre += "\nMajor_Radii\n"
                stre += str(diff[iii].x)+","+str(diff[iii].y)+","+str(diff[iii].z)+"\n"
                while iv < len(diff):
                    #print(alo)
                    if iv not in alo:
                        stre += str(diff[iv].x)+","+str(diff[iv].y)+","+str(diff[iv].z)+"\n"
                        alo.append(iv)
                    iv = iv + 1
            iii = iii + 1

        #save metadata
        with open(path2+ref+"_"+str(i)+"_metadata.txt", "a") as text_file:
            text_file.write(stre)

        #adding untracked holes to make clear holes are not radii

        #step file to be replaced
        os.remove(path2+ref+"_"+str(i)+".catpart")
        os.remove(path2+ref+"_"+str(i)+".stp")

        #random number of holes
        iV = random.randint(0, 5)
        iiV = 0
        prev = []
        while iiV < iV:
            #create a single hole using previously used script
            xyz = [random.randint(10, max(p8arr[:,0])), 0, random.randint(10, 65)]

            run = True

            for xyz2 in prev:
                dist = math.sqrt((xyz[0]-xyz2[0])**2+(xyz[2]-xyz2[2])**2)
                if dist < 10:
                    run = False


            if run == True:

                rand_hole(ShFactory,partDocument1,part1,xyz,iiV,maxhole = 8)
                prev.append(xyz)

            iiV += 1



        partDocument1.SaveAs(path2+ref+"_"+str(i)+".catpart")
        partDocument1.ExportData(path2+ref+"_"+str(i)+".stp", "stp")
        partDocument1.Close()
    
    else:
        #delete the corresponding catia and step file
        os.remove(path2+ref+"_"+str(i)+".catpart")
        os.remove(path2+ref+"_"+str(i)+".stp")
        print("Run "+str(i)+" was removed. Incorrect number of vertices found.")

'''
#sampling x
i = 0
ee = 0
while i < 2000: 

    ptn = random.randint(3,5)

    p8arr = np.zeros((ptn,3))

    ii = 0
    while ii < ptn:

        #x
        p8arr[ii,0] = ii*50
        #y
        p8arr[ii,1] = random.randint(10,100)
        #z stays 0
        ii = ii + 1

    #bottom extrude 
    radii = random.randint(5,25)

    try:
        major_radii_4(i,p8arr,radii,"MR")
    except:
        print("number "+str(i)+" not finished, error")
    

        ee = ee + 1
        if ee > 150:
            break

    i = i + 1
'''

def fillet_basic(I,p8arr,radii,ref,partDocument1):
    #first sample of surfaces with major radii 
    #-- straigt surfaces only
    #-- constant radii only


    #partDocument1.Name = "Part"+str(i)
    part1 = partDocument1.Part
    #Shape factory provides generating of shapes
    ShFactory = part1.HybridShapeFactory
    # Starting new body (geometrical set) in part1
    bodies1 = part1.HybridBodies
    # Adding new body to part1
    body1 = bodies1.Add()
    # Naming new body as "wireframe"
    body1.Name="Wireframe"
    # Surfaces group
    body3 = bodies1.Add()
    body3.Name="Surfaces"
    body4 = bodies1.Add()
    body4.Name="SourceLoft"

    body6 = bodies1.Add()
    body6.Name = "Holes"
    hs1 = body1.HybridShapes
    hs3 = body3.HybridShapes

    #reference direction plane
    OE = part1.OriginElements
    hspe = OE.PlaneXY
    ref111 = part1.CreateReferenceFromObject(hspe)
    dir1 = ShFactory.AddNewDirection(ref111)
    #plane to start second shape on
    off = ShFactory.AddNewPlaneOffset(ref111, -5, True)
    body1.AppendHybridShape(off)
    ref222 = part1.CreateReferenceFromObject(off)
    #limiting ceiling plane
    off2 = ShFactory.AddNewPlaneOffset(ref111, -100, True)
    body1.AppendHybridShape(off2)
    ref444 = part1.CreateReferenceFromObject(off2)


    #create 8 points
    i = 0
    while i < 8:
        point=ShFactory.AddNewPointCoord(p8arr[i,0],p8arr[i,1],p8arr[i,2])
        body1.AppendHybridShape(point)
        i = i + 1
        point.Name = "P"+str(i)





    #all points above together to generate surfaces
    i = 0
    while i < 8:
        #starting point of each surface initiates new "fill"
        if (i == 0) or (i == 4):
            fl = ShFactory.AddNewFill()
        
        poc1 = hs1.Item("P"+str(i+1))
        r1 = part1.CreateReferenceFromObject(poc1)

        #each fourth line connects to first point, to create surface
        if i == 3 or i == 7:
            poc2 = hs1.Item("P"+str(i-2))
        else:
            poc2 = hs1.Item("P"+str(i+2))
        r2 = part1.CreateReferenceFromObject(poc2)

        lpt = ShFactory.AddNewLinePtPt(r1, r2)
        body1.AppendHybridShape(lpt)
        r3 = part1.CreateReferenceFromObject(lpt)
        lpt.Name = "L"+str(i)

        #close each section
        fl.AddBound(r3)
        if i == 3 or i ==7 or i == 11:
            fl.Continuity = 1
            fl.Detection = 2
            fl.AdvancedTolerantMode = 2
            body3.AppendHybridShape(fl)
            fl.Name = "FL"+str(i)

        i = i + 1

    #prepare for solids modelling
    SF = part1.ShapeFactory
    bodies1 = part1.Bodies
    b1 = bodies1.Item("PartBody")
    part1.InWorkObject = b1
    rfX = part1.CreateReferenceFromName("")

    #main pad
    pad1 = SF.AddNewPadFromRef(rfX, 20)
    fllref = hs3.Item("FL3")
    r7 = part1.CreateReferenceFromObject(fllref)
    pad1.SetProfileElement(r7)
    pad1.SetDirection(ref222)
    limit1 = pad1.FirstLimit
    length1 = limit1.Dimension
    length1.Value = 20
    part1.UpdateObject(pad1)


    split1 = SF.AddNewSplit(rfX, 0) #catPositiveSide
    fllref2 = hs3.Item("FL7")
    reference5 = part1.CreateReferenceFromObject(fllref2)
    split1.Surface = reference5

    part1.UpdateObject(split1)


    #hide n seek
    selection1 = partDocument1.Selection
    selection1.Clear()
    visPropertySet1 = selection1.VisProperties
    selection1.Add(body1)
    selection1.Add(body3)
    selection1.Add(body4)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)
    part1.Update()


    #save v1
    path2 = "D:\\CAD_library_sampling\\sample40\\"
    partDocument1.SaveAs(path2+"no_curves\\"+ref+"_"+str(I)+".catpart")
    partDocument1.ExportData(path2+"no_curves\\"+ref+"_"+str(I)+".stp", "stp")
    ver_list1 = vertex_list("D:\\CAD_library_sampling\\sample40\\no_curves\\"+ref+"_"+str(I)+".stp")


    constRadEdgeFillet1 = SF.AddNewSolidEdgeFilletWithConstantRadius(rfX, 0, 0.3) #catTangencyFilletEdgePropagation

    constRadEdgeFillet1.EdgePropagation = 0

    reference2 = part1.CreateReferenceFromBRepName("RSur:(Face:(Brp:(Split.1_ResultOUT);None:();Cf11:());WithTemporaryBody;WithoutBuildError;WithSelectingFeatureSupport;MFBRepVersion_CXR15)", split1)

    constRadEdgeFillet1.AddObjectToFillet(reference2)

    parameters1 = part1.Parameters

    length1 = parameters1.Item("Part1\PartBody\EdgeFillet.1\CstEdgeRibbon.1\Radius")

    length1.Value = radii

    #part1.UpdateObject()

    part1.Update()


    #save v2
    path2 = "D:\\CAD_library_sampling\\sample40\\"
    partDocument1.SaveAs(path2+ref+"_"+str(I)+".catpart")
    partDocument1.ExportData(path2+ref+"_"+str(I)+".stp", "stp")
    ver_list2 = vertex_list("D:\\CAD_library_sampling\\sample40\\"+ref+"_"+str(I)+".stp")

    #compare .stp 1 and .stp 2 --- any new vertices in .stp 2 to be stored for training
    diff = []
    for l2 in ver_list2:
        ex = True
        for l1 in ver_list1:
            if l1.x == l2.x and l1.y == l2.y and l1.z == l2.z:
                ex = False
            
        if ex == True:
            diff.append(l2)



    #.txt file for training
    iii = 0
    stre = ""
    alo = []
    while iii < len(diff):
        
        if iii not in alo:
            iv = iii+1
            stre += "\nFillet\n"
            stre += str(diff[iii].x)+","+str(diff[iii].y)+","+str(diff[iii].z)+"\n"
            while iv < len(diff):
                #print(alo)
                if iv not in alo:
                    stre += str(diff[iv].x)+","+str(diff[iv].y)+","+str(diff[iv].z)+"\n"
                    alo.append(iv)
                iv = iv + 1
        iii = iii + 1

    #save metadata
    with open(path2+ref+"_"+str(I)+"_metadata.txt", "a") as text_file:
        text_file.write(stre)
    
'''

#sampling x
i = 340
ee = 0
while i < 2000: 

    #ptn = random.randint(3,8)

    p8arr = np.zeros((8,3))


    p8arr[0,0] = int(random.randint(0,80))
    p8arr[0,1] = random.randint(0,80)
    p8arr[1,0] = random.randint(0,80)
    p8arr[1,1] = random.randint(-80,0)
    p8arr[2,0] = random.randint(-80,0)
    p8arr[2,1] = random.randint(-80,0)
    p8arr[3,0] = random.randint(-80,0)
    p8arr[3,1] = random.randint(0,80)

    p8arr[4,0] = p8arr[0,0]
    p8arr[4,1] = p8arr[0,1]
    p8arr[4,2] = random.randint(3,10)
    p8arr[5,0] = p8arr[1,0]
    p8arr[5,1] = p8arr[1,1]
    p8arr[5,2] = random.randint(3,10)
    p8arr[6,0] = p8arr[2,0]
    p8arr[6,1] = p8arr[2,1]
    p8arr[6,2] = random.randint(3,10)
    p8arr[7,0] = p8arr[3,0]
    p8arr[7,1] = p8arr[3,1]
    p8arr[7,2] = random.randint(3,10)


    #fillet radius
    radii = random.randint(1,30)/10

    #Setting up CATIA modelling environment
    CATIA = win32com.client.Dispatch("CATIA.Application")
    #record deletion of product....

    documents1 = CATIA.Documents
    partDocument1 = documents1.Add("Part")

    try:
        fillet_basic(i,p8arr,radii,"FL2",partDocument1)
    except:
        print("number "+str(i)+" not finished, error")
    
        ee = ee + 1
        if ee > 150:
            break

    partDocument1.Close()

    i = i + 1
'''

def fillet2(I,p8arr,radii,rad2,ref,poxh,poxz,fr,partDocument1):
    #first sample of surfaces with major radii 
    #-- straigt surfaces only
    #-- constant radii only

    #Setting up CATIA modelling environment
    #CATIA = win32com.client.Dispatch("CATIA.Application")
    #record deletion of product....

    #documents1 = CATIA.Documents
    #partDocument1 = documents1.Add("Part")
    part1 = partDocument1.Part
    #Shape factory provides generating of shapes
    ShFactory = part1.HybridShapeFactory
    # Starting new body (geometrical set) in part1
    bodies1 = part1.HybridBodies
    # Adding new body to part1
    body1 = bodies1.Add()
    # Naming new body as "wireframe"
    body1.Name="Wireframe"
    # Surfaces group
    body3 = bodies1.Add()
    body3.Name="CurvedSurface"
    body4 = bodies1.Add()
    body4.Name="NoCurveAsm"

    #reference direction plane
    OE = part1.OriginElements
    hspe = OE.PlaneXY
    ref111 = part1.CreateReferenceFromObject(hspe)
    dir1 = ShFactory.AddNewDirection(ref111)

    #creating construction points 
    ii = 0
    r4 = []
    while ii < np.size(p8arr,0):
        #create point for each reference
        point1=ShFactory.AddNewPointCoord(p8arr[ii,0],p8arr[ii,1],p8arr[ii,2])
        body1.AppendHybridShape(point1)
        r1 = part1.CreateReferenceFromObject(point1)

        #connect the two points with a line
        if ii > 0:
            lpt = ShFactory.AddNewLinePtPt(r1, r2)
            body1.AppendHybridShape(lpt)
            lpt.Name="cnn_line_"+str(ii)
            r3 = part1.CreateReferenceFromObject(lpt)

            #extrude each line
            ex1 = ShFactory.AddNewExtrude(r3, 75.000000, 0.000000, dir1)
            body1.AppendHybridShape(ex1)
            #lpt.Name="cnn_line_"+str(ii)
            r4 = part1.CreateReferenceFromObject(ex1)

            if ii > 1:
                #joins for alternative build without radii - for .stp comparison
                #asm = ShFactory.AddNewJoin(r4, r5)
                #body4.AppendHybridShape(asm)
                #r5 = part1.CreateReferenceFromObject(asm)

                #try clause so that bi-tangent can be reversed where needed (quite common)
                try:
                    casm = ShFactory.AddNewFilletBiTangent(r4, r6, radii, 1, 1, 1, 0)
                    body3.AppendHybridShape(casm)
                    part1.Update()
                except:          
                    #when bi-tangent is to be reversed - the first bi-tangent needs to be deleted first
                    selection1 = partDocument1.Selection
                    selection1.Clear()
                    selection1.Add(casm)
                    selection1.Delete()

                    #fixing the bi-tangent with oposite direction on both surfaces
                    casm = ShFactory.AddNewFilletBiTangent(r4, r6, radii, -1, -1, 1, 0)
                    body3.AppendHybridShape(casm)  
                    part1.Update()
                r6 = part1.CreateReferenceFromObject(casm) 
            else:
                #in first loop just generate references
                r5 = r4
                r6 = r4

        r2 = r1

        ii += 1

    point1=ShFactory.AddNewPointCoord(poxh,0,poxz)
    body1.AppendHybridShape(point1)
    r1 = part1.CreateReferenceFromObject(point1) 

    proj = ShFactory.AddNewProject(r1, r6)
    proj.SolutionType = 0
    proj.Normal = True
    proj.SmoothingType = 0
    proj.ExtrapolationMode = 0
    body1.AppendHybridShape(proj)       
    r555 = part1.CreateReferenceFromObject(proj)  

    c1 = ShFactory.AddNewCircleCtrRad(r555, r6, False, rad2)
    c1.SetLimitation(1)
    body1.AppendHybridShape(c1)
    r32 = part1.CreateReferenceFromObject(c1)    

    proj = ShFactory.AddNewProject(r32, r6)
    proj.SolutionType = 0
    proj.Normal = True
    proj.SmoothingType = 0
    proj.ExtrapolationMode = 0
    body1.AppendHybridShape(proj)       
    r32 = part1.CreateReferenceFromObject(proj)  

    #split
    spl = ShFactory.AddNewHybridSplit(r6, r32, -1)
    #ShFactory.GSMVisibility(rf100, 0)
    spl.ExtrapolationType = 1
    body3.AppendHybridShape(spl)
    rf105 = part1.CreateReferenceFromObject(spl)

    #hide n seek
    selection1 = partDocument1.Selection
    selection1.Clear()
    visPropertySet1 = selection1.VisProperties
    selection1.Add(body1)
    selection1.Add(body3)
    selection1.Add(body4)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)
    part1.Update()

    #creating reference (no-radii) body
    bodies1 = part1.Bodies
    body10 = bodies1.Item("PartBody")
    part1.InWorkObject = body10
    SF = part1.ShapeFactory
    ref1 = part1.CreateReferenceFromName("")
    #create thickness from curved surface
    tt = SF.AddNewThickSurface(rf105, 0, 3.000000, 0.000000)
    
    part1.Update()


    #save 1 here
    path2 = "D:\\CAD_library_sampling\\sample41\\"
    partDocument1.SaveAs(path2+"no_curves\\"+ref+"_"+str(I)+".catpart")
    partDocument1.ExportData(path2+"no_curves\\"+ref+"_"+str(I)+".stp", "stp")
    ver_list1 = vertex_list("D:\\CAD_library_sampling\\sample41\\no_curves\\"+ref+"_"+str(I)+".stp")



    constRadEdgeFillet1 = SF.AddNewSolidEdgeFilletWithConstantRadius(ref1, 0, fr)

    constRadEdgeFillet1.EdgePropagation = 0

    bodies1 = part1.Bodies


    reference2 = part1.CreateReferenceFromBRepName("RSur:(Face:(Brp:(ThickSurface.1;1:(Brp:(GSMExtrude.1;0:(Brp:(GSMLine.1)))));None:();Cf11:());WithTemporaryBody;WithoutBuildError;WithSelectingFeatureSupport;MFBRepVersion_CXR15)", tt)

    constRadEdgeFillet1.AddObjectToFillet(reference2)

    parameters1 = part1.Parameters

    #length1 = parameters1.Item("Part1\PartBody\EdgeFillet.2\CstEdgeRibbon.2\Radius")

    #length1.Value = fr

    #part1.UpdateObject(constRadEdgeFillet1)
    part1.Update()

    #save 2 here
    path2 = "D:\\CAD_library_sampling\\sample41\\"
    partDocument1.SaveAs(path2+ref+"_"+str(I)+".catpart")
    partDocument1.ExportData(path2+ref+"_"+str(I)+".stp", "stp")
    ver_list2 = vertex_list("D:\\CAD_library_sampling\\sample41\\"+ref+"_"+str(I)+".stp")


    #compare .stp 1 and .stp 2 --- any new vertices in .stp 2 to be stored for training
    diff = []
    for l2 in ver_list2:
        ex = True
        for l1 in ver_list1:
            if l1.x == l2.x and l1.y == l2.y and l1.z == l2.z:
                ex = False
            
        if ex == True:
            diff.append(l2)



    #.txt file for training
    iii = 0
    stre = ""
    alo = []
    while iii < len(diff):
        
        if iii not in alo:
            iv = iii+1
            stre += "\nFillet\n"
            stre += str(diff[iii].x)+","+str(diff[iii].y)+","+str(diff[iii].z)+"\n"
            while iv < len(diff):
                #print(alo)
                if iv not in alo:
                    stre += str(diff[iv].x)+","+str(diff[iv].y)+","+str(diff[iv].z)+"\n"
                    alo.append(iv)
                iv = iv + 1
        iii = iii + 1

    #save metadata
    with open(path2+ref+"_"+str(I)+"_metadata.txt", "a") as text_file:
        text_file.write(stre)

'''
#sampling x
i = 0
ee = 0
while i < 2000: 

    ptn = random.randint(3,5)

    p8arr = np.zeros((ptn,3))

    ii = 0
    while ii < ptn:

        #x
        p8arr[ii,0] = ii*50
        #y
        p8arr[ii,1] = random.randint(10,100)
        #z stays 0
        ii = ii + 1

    #bottom extrude 
    radii = random.randint(5,25)
    r2 = random.randint(5,15)
    poxh = random.randint(20,45)
    poxz = random.randint(20,45)
    fr = random.randint(10,150)/100

    #Setting up CATIA modelling environment
    CATIA = win32com.client.Dispatch("CATIA.Application")
    #record deletion of product....

    documents1 = CATIA.Documents
    partDocument1 = documents1.Add("Part")

    

    try:
        fillet2(i,p8arr,radii,r2,"MR",poxh,poxz,fr,partDocument1)
    except:
        print("number "+str(i)+" not finished, error")

        ee = ee + 1
        if ee > 150:
            break

    partDocument1.Close()

    i = i + 1

'''

def fillet3(I,p8arr,radii,rad2,ref,poxh,poxz,fr,partDocument1):
    #first sample of surfaces with major radii 
    #-- straigt surfaces only
    #-- constant radii only

    #Setting up CATIA modelling environment
    #CATIA = win32com.client.Dispatch("CATIA.Application")
    #record deletion of product....

    #documents1 = CATIA.Documents
    #partDocument1 = documents1.Add("Part")
    part1 = partDocument1.Part
    #Shape factory provides generating of shapes
    ShFactory = part1.HybridShapeFactory
    # Starting new body (geometrical set) in part1
    bodies1 = part1.HybridBodies
    # Adding new body to part1
    body1 = bodies1.Add()
    # Naming new body as "wireframe"
    body1.Name="Wireframe"
    # Surfaces group
    body3 = bodies1.Add()
    body3.Name="CurvedSurface"
    body4 = bodies1.Add()
    body4.Name="NoCurveAsm"

    #reference direction plane
    OE = part1.OriginElements
    hspe = OE.PlaneXY
    ref111 = part1.CreateReferenceFromObject(hspe)
    dir1 = ShFactory.AddNewDirection(ref111)

    #creating construction points 
    ii = 0
    r4 = []
    while ii < np.size(p8arr,0):
        #create point for each reference
        point1=ShFactory.AddNewPointCoord(p8arr[ii,0],p8arr[ii,1],p8arr[ii,2])
        body1.AppendHybridShape(point1)
        r1 = part1.CreateReferenceFromObject(point1)

        #connect the two points with a line
        if ii > 0:
            lpt = ShFactory.AddNewLinePtPt(r1, r2)
            body1.AppendHybridShape(lpt)
            lpt.Name="cnn_line_"+str(ii)
            r3 = part1.CreateReferenceFromObject(lpt)

            #extrude each line
            ex1 = ShFactory.AddNewExtrude(r3, 75.000000, 0.000000, dir1)
            body1.AppendHybridShape(ex1)
            #lpt.Name="cnn_line_"+str(ii)
            r4 = part1.CreateReferenceFromObject(ex1)

            if ii > 1:
                #joins for alternative build without radii - for .stp comparison
                #asm = ShFactory.AddNewJoin(r4, r5)
                #body4.AppendHybridShape(asm)
                #r5 = part1.CreateReferenceFromObject(asm)

                #try clause so that bi-tangent can be reversed where needed (quite common)
                try:
                    casm = ShFactory.AddNewFilletBiTangent(r4, r6, radii, 1, 1, 1, 0)
                    body3.AppendHybridShape(casm)
                    part1.Update()
                except:          
                    #when bi-tangent is to be reversed - the first bi-tangent needs to be deleted first
                    selection1 = partDocument1.Selection
                    selection1.Clear()
                    selection1.Add(casm)
                    selection1.Delete()

                    #fixing the bi-tangent with oposite direction on both surfaces
                    casm = ShFactory.AddNewFilletBiTangent(r4, r6, radii, -1, -1, 1, 0)
                    body3.AppendHybridShape(casm)  
                    part1.Update()
                r6 = part1.CreateReferenceFromObject(casm) 
            else:
                #in first loop just generate references
                r5 = r4
                r6 = r4

        r2 = r1

        ii += 1



    #hide n seek
    selection1 = partDocument1.Selection
    selection1.Clear()
    visPropertySet1 = selection1.VisProperties
    selection1.Add(body1)
    selection1.Add(body3)
    selection1.Add(body4)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)
    part1.Update()

    #creating reference (no-radii) body
    bodies1 = part1.Bodies
    body10 = bodies1.Item("PartBody")
    part1.InWorkObject = body10
    SF = part1.ShapeFactory
    ref1 = part1.CreateReferenceFromName("")
    #create thickness from curved surface
    tt = SF.AddNewThickSurface(r6, 0, 4.000000, 0.000000)
    
    part1.Update()


    #save 1 here
    path2 = "D:\\CAD_library_sampling\\sample42\\"
    partDocument1.SaveAs(path2+"no_curves\\"+ref+"_"+str(I)+".catpart")
    partDocument1.ExportData(path2+"no_curves\\"+ref+"_"+str(I)+".stp", "stp")
    ver_list1 = vertex_list("D:\\CAD_library_sampling\\sample42\\no_curves\\"+ref+"_"+str(I)+".stp")



    constRadEdgeFillet1 = SF.AddNewSolidEdgeFilletWithConstantRadius(ref1, 0, fr)
    constRadEdgeFillet1.EdgePropagation = 0
    bodies1 = part1.Bodies
    reference2 = part1.CreateReferenceFromBRepName("RSur:(Face:(Brp:(ThickSurface.1;1:(Brp:(GSMExtrude.1;0:(Brp:(GSMLine.1)))));None:();Cf11:());WithTemporaryBody;WithoutBuildError;WithSelectingFeatureSupport;MFBRepVersion_CXR15)", tt)
    constRadEdgeFillet1.AddObjectToFillet(reference2)
    parameters1 = part1.Parameters
    part1.Update()

    #save 2 here
    path2 = "D:\\CAD_library_sampling\\sample42\\"
    partDocument1.SaveAs(path2+ref+"_"+str(I)+".catpart")
    partDocument1.ExportData(path2+ref+"_"+str(I)+".stp", "stp")
    ver_list2 = vertex_list("D:\\CAD_library_sampling\\sample42\\"+ref+"_"+str(I)+".stp")


    #compare .stp 1 and .stp 2 --- any new vertices in .stp 2 to be stored for training
    diff = []
    for l2 in ver_list2:
        ex = True
        for l1 in ver_list1:
            if l1.x == l2.x and l1.y == l2.y and l1.z == l2.z:
                ex = False
            
        if ex == True:
            diff.append(l2)



    #.txt file for training
    iii = 0
    stre = ""
    alo = []
    while iii < len(diff):
        
        if iii not in alo:
            iv = iii+1
            stre += "\nFillet\n"
            stre += str(diff[iii].x)+","+str(diff[iii].y)+","+str(diff[iii].z)+"\n"
            while iv < len(diff):
                #print(alo)
                if iv not in alo:
                    stre += str(diff[iv].x)+","+str(diff[iv].y)+","+str(diff[iv].z)+"\n"
                    alo.append(iv)
                iv = iv + 1
        iii = iii + 1

    #save metadata
    with open(path2+ref+"_"+str(I)+"_metadata.txt", "a") as text_file:
        text_file.write(stre)
'''

#sampling x
i = 0
ee = 0
while i < 1000: 

    ptn = random.randint(3,5)

    p8arr = np.zeros((ptn,3))

    ii = 0
    while ii < ptn:

        #x
        p8arr[ii,0] = ii*50
        #y
        p8arr[ii,1] = random.randint(10,100)
        #z stays 0
        ii = ii + 1

    #bottom extrude 
    radii = random.randint(5,25)
    r2 = random.randint(5,15)
    poxh = random.randint(20,45)
    poxz = random.randint(20,45)
    fr = random.randint(10,150)/100

    #Setting up CATIA modelling environment
    CATIA = win32com.client.Dispatch("CATIA.Application")
    #record deletion of product....

    documents1 = CATIA.Documents
    partDocument1 = documents1.Add("Part")

    

    try:
        fillet3(i,p8arr,radii,r2,"MR",poxh,poxz,fr,partDocument1)
    except:
        print("number "+str(i)+" not finished, error")

        ee = ee + 1
        if ee > 150:
            break

    partDocument1.Close()

    i = i + 1

'''

def h_42(I,p8arr,radii,ref,p1,p2,t1,t2,t3):
    #ply drop-offs included - additional hole training

    #Setting up CATIA modelling environment
    CATIA = win32com.client.Dispatch("CATIA.Application")
    #record deletion of product....

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
    body1.Name="Wireframe"
    # Surfaces group
    body3 = bodies1.Add()
    body3.Name="CurvedSurface"
    body4 = bodies1.Add()
    body4.Name="NoCurveAsm"
    body8 = bodies1.Add()
    body8.Name="Steps"

    #reference direction plane
    OE = part1.OriginElements
    hspe = OE.PlaneXY
    ref111 = part1.CreateReferenceFromObject(hspe)
    dir1 = ShFactory.AddNewDirection(ref111)

    #creating construction points 
    ii = 0
    r4 = []
    while ii < np.size(p8arr,0):
        #create point for each reference
        point1=ShFactory.AddNewPointCoord(p8arr[ii,0],p8arr[ii,1],p8arr[ii,2])
        body1.AppendHybridShape(point1)
        r1 = part1.CreateReferenceFromObject(point1)

        #connect the two points with a line
        if ii > 0:
            lpt = ShFactory.AddNewLinePtPt(r1, r2)
            body1.AppendHybridShape(lpt)
            lpt.Name="cnn_line_"+str(ii)
            r3 = part1.CreateReferenceFromObject(lpt)

            #extrude each line
            ex1 = ShFactory.AddNewExtrude(r3, 75.000000, 0.000000, dir1)
            body1.AppendHybridShape(ex1)
            #lpt.Name="cnn_line_"+str(ii)
            r4 = part1.CreateReferenceFromObject(ex1)

            if ii > 1:
                #joins for alternative build without radii - for .stp comparison
                asm = ShFactory.AddNewJoin(r4, r5)
                body4.AppendHybridShape(asm)
                r5 = part1.CreateReferenceFromObject(asm)

                #try clause so that bi-tangent can be reversed where needed (quite common)
                try:
                    casm = ShFactory.AddNewFilletBiTangent(r4, r6, radii, 1, 1, 1, 0)
                    body3.AppendHybridShape(casm)
                    part1.Update()
                except:          
                    #when bi-tangent is to be reversed - the first bi-tangent needs to be deleted first
                    selection1 = partDocument1.Selection
                    selection1.Clear()
                    selection1.Add(casm)
                    selection1.Delete()

                    #fixing the bi-tangent with oposite direction on both surfaces
                    casm = ShFactory.AddNewFilletBiTangent(r4, r6, radii, -1, -1, 1, 0)
                    body3.AppendHybridShape(casm)  
                    part1.Update()
                r6 = part1.CreateReferenceFromObject(casm) 
            else:
                #in first loop just generate references
                r5 = r4
                r6 = r4

        r2 = r1

        ii += 1


    


    bnd = ShFactory.AddNewBoundaryOfSurface(r6)
    body8.AppendHybridShape(bnd)
    r606 = part1.CreateReferenceFromObject(bnd) 
    
    par1 = ShFactory.AddNewCurvePar(r606, r6, p1, False, False)
    par1.SmoothingType = 0
    body8.AppendHybridShape(par1)
    r607 = part1.CreateReferenceFromObject(par1) 


    par2 = ShFactory.AddNewCurvePar(r606, r6, p2, False, False)
    par2.SmoothingType = 0
    body8.AppendHybridShape(par2)
    r608 = part1.CreateReferenceFromObject(par2) 

    #add a split 
    spl1 = ShFactory.AddNewHybridSplit(r6, r607, 1)
    spl1.ExtrapolationType = 1
    body8.AppendHybridShape(spl1)
    r609 = part1.CreateReferenceFromObject(spl1) 

    #add a split 
    spl2 = ShFactory.AddNewHybridSplit(r6, r608, 1)
    spl2.ExtrapolationType = 1
    body8.AppendHybridShape(spl2)
    r610 = part1.CreateReferenceFromObject(spl2) 


    #then 3 thicknesses instead

    #then holes with annotations !


    #hide n seek
    selection1 = partDocument1.Selection
    selection1.Clear()
    visPropertySet1 = selection1.VisProperties
    selection1.Add(body1)
    selection1.Add(body3)
    selection1.Add(body4)
    selection1.Add(body8)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)
    part1.Update()

    #creating reference (no-radii) body
    bodies1 = part1.Bodies
    body10 = bodies1.Item("PartBody")
    part1.InWorkObject = body10
    SF = part1.ShapeFactory
    ref1 = part1.CreateReferenceFromName("")


    #create thickness from curved surface
    tt = SF.AddNewThickSurface(r6, 0, t1, 0.000000)
    tt = SF.AddNewThickSurface(r609, 0, t2, 0.000000)
    tt = SF.AddNewThickSurface(r610, 0, t3, 0.000000)
    part1.Update()

    #save v1
    path2 = "D:\\CAD_library_sampling\\sample50\\"
    partDocument1.SaveAs(path2+"no_curves\\"+ref+"_"+str(I)+".catpart")
    partDocument1.ExportData(path2+"no_curves\\"+ref+"_"+str(I)+".stp", "stp")
    ver_list1 = vertex_list("D:\\CAD_library_sampling\\sample50\\no_curves\\"+ref+"_"+str(I)+".stp")


    #random number of holes
    iV = random.randint(0, 5)
    iiV = 0
    prev = []
    while iiV < iV:
        #create a single hole using previously used script
        xyz = [random.randint(15, max(p8arr[:,0])-15), 0, random.randint(15, 60)]

        run = True

        for xyz2 in prev:
            dist = math.sqrt((xyz[0]-xyz2[0])**2+(xyz[2]-xyz2[2])**2)
            if dist < 10:
                run = False


        if run == True:

            rand_hole(ShFactory,partDocument1,part1,xyz,iiV,maxhole = 8)
            prev.append(xyz)

        iiV += 1

    #save v2
    path2 = "D:\\CAD_library_sampling\\sample50\\"
    partDocument1.SaveAs(path2+ref+"_"+str(I)+".catpart")
    partDocument1.ExportData(path2+ref+"_"+str(I)+".stp", "stp")
    ver_list2 = vertex_list("D:\\CAD_library_sampling\\sample50\\"+ref+"_"+str(I)+".stp")

    #compare .stp 1 and .stp 2 --- any new vertices in .stp 2 to be stored for training
    diff = []
    for l2 in ver_list2:
        ex = True
        for l1 in ver_list1:
            if l1.x == l2.x and l1.y == l2.y and l1.z == l2.z:
                ex = False
            
        if ex == True:
            diff.append(l2)

    #.txt file for training
    iii = 0
    stre = ""
    alo = []
    while iii < len(diff):
        
        if iii not in alo:
            iv = iii+1
            stre += "\n hole\n"
            stre += str(diff[iii].x)+","+str(diff[iii].y)+","+str(diff[iii].z)+"\n"
            while iv < len(diff):

                stre += str(diff[iv].x)+","+str(diff[iv].y)+","+str(diff[iv].z)+"\n"
                alo.append(iv)
                iv = iv + 1
        iii = iii + 1
        


    #save metadata
    with open(path2+ref+"_"+str(I)+"_metadata.txt", "a") as text_file:
        text_file.write(stre)

    partDocument1.Close()

'''

#sampling x
i = 0
ee = 0
while i < 3500: 

    ptn = random.randint(3,5)

    p8arr = np.zeros((ptn,3))

    ii = 0
    while ii < ptn:

        #x
        p8arr[ii,0] = ii*50
        #y
        p8arr[ii,1] = random.randint(10,100)
        #z stays 0
        ii = ii + 1

    p1 = random.randint(10,200)/10
    p2 = random.randint((p1+1)*10,300)/10
    t1 = random.randint(2,20)/10
    t2 = random.randint(5,40)/10
    t3 = random.randint(5,40)/10

    #bottom extrude 
    radii = random.randint(5,25)

    try:
        h_42(i,p8arr,radii,"H",p1,p2,t1,t2,t3)
    except:
        print("number "+str(i)+" not finished, error")
    

        ee = ee + 1
        if ee > 150:
            break

    i = i + 1
'''

def h_60(I,p8arr,radii,ref,p1,p2,t1,t2,t3,csys):
    #h_42 + rotations and translations 

    #ply drop-offs included - additional hole training

    #Setting up CATIA modelling environment
    CATIA = win32com.client.Dispatch("CATIA.Application")
    #record deletion of product....

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
    body1.Name="Wireframe"
    # Surfaces group
    body3 = bodies1.Add()
    body3.Name="CurvedSurface"
    body4 = bodies1.Add()
    body4.Name="NoCurveAsm"
    body8 = bodies1.Add()
    body8.Name="Steps"

    #reference direction plane
    OE = part1.OriginElements
    hspe = OE.PlaneXY
    ref111 = part1.CreateReferenceFromObject(hspe)
    dir1 = ShFactory.AddNewDirection(ref111)

    #reference direction plane
    hspe = OE.PlaneYZ
    ref111 = part1.CreateReferenceFromObject(hspe)
    dirX = ShFactory.AddNewDirection(ref111)

    #reference direction plane
    hspe = OE.PlaneZX
    ref111 = part1.CreateReferenceFromObject(hspe)
    dirY = ShFactory.AddNewDirection(ref111)

    #creating construction points 
    ii = 0
    r4 = []
    while ii < np.size(p8arr,0):
        #create point for each reference
        point1=ShFactory.AddNewPointCoord(p8arr[ii,0],p8arr[ii,1],p8arr[ii,2])
        body1.AppendHybridShape(point1)
        r1 = part1.CreateReferenceFromObject(point1)

        #connect the two points with a line
        if ii > 0:
            lpt = ShFactory.AddNewLinePtPt(r1, r2)
            body1.AppendHybridShape(lpt)
            lpt.Name="cnn_line_"+str(ii)
            r3 = part1.CreateReferenceFromObject(lpt)

            #extrude each line
            ex1 = ShFactory.AddNewExtrude(r3, 75.000000, 0.000000, dir1)
            body1.AppendHybridShape(ex1)
            #lpt.Name="cnn_line_"+str(ii)
            r4 = part1.CreateReferenceFromObject(ex1)

            if ii > 1:
                #joins for alternative build without radii - for .stp comparison
                asm = ShFactory.AddNewJoin(r4, r5)
                body4.AppendHybridShape(asm)
                r5 = part1.CreateReferenceFromObject(asm)

                #try clause so that bi-tangent can be reversed where needed (quite common)
                try:
                    casm = ShFactory.AddNewFilletBiTangent(r4, r6, radii, 1, 1, 1, 0)
                    body3.AppendHybridShape(casm)
                    part1.Update()
                except:          
                    #when bi-tangent is to be reversed - the first bi-tangent needs to be deleted first
                    selection1 = partDocument1.Selection
                    selection1.Clear()
                    selection1.Add(casm)
                    selection1.Delete()

                    #fixing the bi-tangent with oposite direction on both surfaces
                    casm = ShFactory.AddNewFilletBiTangent(r4, r6, radii, -1, -1, 1, 0)
                    body1.AppendHybridShape(casm)  
                    part1.Update()
                r6 = part1.CreateReferenceFromObject(casm) 
            else:
                #in first loop just generate references
                r5 = r4
                r6 = r4

        r2 = r1

        ii += 1

    #rotations and translations
    #dirX, dirY,dir1
    iii = 0
    directions = [dirX,dirY,dir1]

    bnd = ShFactory.AddNewBoundaryOfSurface(r6)
    body8.AppendHybridShape(bnd)
    r606 = part1.CreateReferenceFromObject(bnd) 
    
    par1 = ShFactory.AddNewCurvePar(r606, r6, p1, False, False)
    par1.SmoothingType = 0
    body8.AppendHybridShape(par1)
    r607 = part1.CreateReferenceFromObject(par1) 

    par2 = ShFactory.AddNewCurvePar(r606, r6, p2, False, False)
    par2.SmoothingType = 0
    body8.AppendHybridShape(par2)
    r608 = part1.CreateReferenceFromObject(par2) 

    #add a split 
    spl1 = ShFactory.AddNewHybridSplit(r6, r607, 1)
    spl1.ExtrapolationType = 1
    body8.AppendHybridShape(spl1)
    r609 = part1.CreateReferenceFromObject(spl1) 

    #add a split 
    spl2 = ShFactory.AddNewHybridSplit(r6, r608, 1)
    spl2.ExtrapolationType = 1
    body8.AppendHybridShape(spl2)
    r610 = part1.CreateReferenceFromObject(spl2) 

    #hide n seek
    selection1 = partDocument1.Selection
    selection1.Clear()
    visPropertySet1 = selection1.VisProperties
    selection1.Add(body1)
    selection1.Add(body3)
    selection1.Add(body4)
    selection1.Add(body8)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)
    part1.Update()

    #creating reference (no-radii) body
    bodies1 = part1.Bodies
    body10 = bodies1.Item("PartBody")

    bodies1 = part1.Bodies
    body100 = bodies1.Add()
    body100.Name="xxx"

    part1.InWorkObject = body100
    SF = part1.ShapeFactory
    ref1 = part1.CreateReferenceFromName("")

    #create thickness from curved surface
    tt = SF.AddNewThickSurface(r6, 0, t1, 0.000000)
    tt = SF.AddNewThickSurface(r609, 0, t2, 0.000000)
    tt = SF.AddNewThickSurface(r610, 0, t3, 0.000000)

    part1.InWorkObject = body100

    iii = 0
    while iii < 3:

        tr = SF.AddNewTranslate2(csys[iii])
        tr = tr.HybridShape
        tr.VectorType = 0
        tr.Direction = directions[iii]
        part1.InWorkObject = tr
        part1.Update()
        iii = iii + 1
    iii = 0
    while iii < 3:
        rotate1 = SF.AddNewRotate2(directions[iii], csys[iii+ 3])

        hybridShapeRotate1 = rotate1.HybridShape

        hybridShapeRotate1.RotationType = 0

        hybridShapeRotate1.Axis = directions[iii]
        part1.InWorkObject = hybridShapeRotate1
        part1.Update()
        iii = iii + 1

    #save v1
    path2 = "D:\\CAD_library_sampling\\sample60\\"
    partDocument1.SaveAs(path2+"no_curves\\"+ref+"_"+str(I)+".catpart")
    partDocument1.ExportData(path2+"no_curves\\"+ref+"_"+str(I)+".stp", "stp")
    ver_list1 = vertex_list("D:\\CAD_library_sampling\\sample60\\no_curves\\"+ref+"_"+str(I)+".stp")

    #hide n seek
    selection1 = partDocument1.Selection
    selection1.Clear()
    visPropertySet1 = selection1.VisProperties
    selection1.Add(body100)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)
    part1.Update()

    part1.InWorkObject = body10

    #create thickness from curved surface
    tt = SF.AddNewThickSurface(r6, 0, t1, 0.000000)
    tt = SF.AddNewThickSurface(r609, 0, t2, 0.000000)
    tt = SF.AddNewThickSurface(r610, 0, t3, 0.000000)


    #random number of holes
    iV = random.randint(1, 5)
    iiV = 0
    prev = []
    while iiV < iV:
        #create a single hole using previously used script


        xyz = [random.randint(15, max(p8arr[:,0])-15), 0, random.randint(15, 60)]

        run = True

        for xyz2 in prev:
            dist = math.sqrt((xyz[0]-xyz2[0])**2+(xyz[2]-xyz2[2])**2)
            if dist < 10:
                run = False


        if run == True:

            rand_hole(ShFactory,partDocument1,part1,xyz,iiV,maxhole = 8)
            prev.append(xyz)

        iiV += 1

    part1.InWorkObject = body3

    #rotate translate by random 
    iii = 0
    while iii < 3:

        tr = SF.AddNewTranslate2(csys[iii])
        tr = tr.HybridShape
        tr.VectorType = 0
        tr.Direction = directions[iii]
        part1.InWorkObject = tr
        part1.Update()
        iii = iii + 1
    iii = 0
    while iii < 3:
        rotate1 = SF.AddNewRotate2(directions[iii], csys[iii+ 3])

        hybridShapeRotate1 = rotate1.HybridShape

        hybridShapeRotate1.RotationType = 0

        hybridShapeRotate1.Axis = directions[iii]
        part1.InWorkObject = hybridShapeRotate1
        part1.Update()
        iii = iii + 1

    #save v2
    path2 = "D:\\CAD_library_sampling\\sample60\\"
    partDocument1.SaveAs(path2+ref+"_"+str(I)+".catpart")
    partDocument1.ExportData(path2+ref+"_"+str(I)+".stp", "stp")
    ver_list2 = vertex_list("D:\\CAD_library_sampling\\sample60\\"+ref+"_"+str(I)+".stp")

    #compare .stp 1 and .stp 2 --- any new vertices in .stp 2 to be stored for training
    diff = []
    for l2 in ver_list2:
        ex = True
        for l1 in ver_list1:
            if l1.x == l2.x and l1.y == l2.y and l1.z == l2.z:
                ex = False
            
        if ex == True:
            diff.append(l2)

    #.txt file for training
    iii = 0
    stre = ""
    alo = []
    while iii < len(diff):
        
        if iii not in alo:
            iv = iii+1
            stre += "\n hole\n"
            stre += str(diff[iii].x)+","+str(diff[iii].y)+","+str(diff[iii].z)+"\n"
            while iv < len(diff):

                stre += str(diff[iv].x)+","+str(diff[iv].y)+","+str(diff[iv].z)+"\n"
                alo.append(iv)
                iv = iv + 1
        iii = iii + 1
        


    #save metadata
    with open(path2+ref+"_"+str(I)+"_metadata.txt", "a") as text_file:
        text_file.write(stre)

    partDocument1.Close()


#from math_utils import GlobalToLocal
#sampling x
i = 0
ee = 0
while i < 4000: 

    ptn = random.randint(3,5)

    p8arr = np.zeros((ptn,3))

    ii = 0
    while ii < ptn:

        #x
        p8arr[ii,0] = ii*50
        #y
        p8arr[ii,1] = random.randint(10,100)
        #z stays 0
        ii = ii + 1

    p1 = random.randint(10,200)/10
    p2 = random.randint((p1+1)*10,300)/10
    t1 = random.randint(2,20)/10
    t2 = random.randint(5,40)/10
    t3 = random.randint(5,40)/10

    #bottom extrude 
    radii = random.randint(5,25)

    #csys
    csys = [0,0,0,0,0,0]
    csys[0] = random.randint(0,2000)
    csys[1] = random.randint(0,2000)
    csys[2] = random.randint(0,2000)
    csys[3] = random.randint(0,360)
    csys[4] = random.randint(0,360)
    csys[5] = random.randint(0,360)


    try:
        h_60(i,p8arr,radii,"H",p1,p2,t1,t2,t3,csys)
    except:
        print("number "+str(i)+" not finished, error")
    
        ee = ee + 1
        if ee > 150:
            break

    i = i + 1


