# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 13:54:04 2022

@author: jakub.kucera
"""
import win32com.client.dynamic
#import sys, os 
import numpy as np
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
    #SF = part1.ShapeFactory
    #bodies5 = part1.Bodies
    #body5 = bodies5.Item("PartBody")
    #part1.InWorkObject = body5

    #base surface
    #rf00 = part1.CreateReferenceFromName("")
    #ts1 = SF.AddNewThickSurface(rf00, 0, 1.0000, 0.000000)
    #ts1.Surface = rf4
    #l1 = ts1.TopOffset
    #l1.Value = t
    #part1.UpdateObject(ts1)

    #hide excess geometry
    selection1 = partDocument1.Selection
    visPropertySet1 = selection1.VisProperties
    selection1.Add(body1)
    selection1.Add(body8)
    #selection1.Add(body3)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)

    part1.Update()
    
    #save v2

    path2 = "D:\\CAD_library_sampling\\sample14\\"
    #save version without holes and output empty notepad
    partDocument1.SaveAs(path2+"PR_"+str(i)+".catpart")
    partDocument1.ExportData(path2+"PR_"+str(i)+".stp", "stp")
    ver_list1 = vertex_list("D:\CAD_library_sampling\sample14\PR_"+str(i)+".stp")
    stre = ""
    with open(path2+"PR_"+str(i)+"_metadata.txt", "a") as text_file:
        text_file.write(stre)

    
    selection2 = partDocument1.Selection
    visPropertySet2 = selection2.VisProperties
    selection2.Add(flt)
    #make holes show
    ii = 0
    while ii < noh:


        bds1 = part1.HybridBodies

        hb1 = bds1.Item("Holes")

        hs1= hb1.HybridShapes

        cyl_str = "C_X_"+str(ii)
        
        cyl1 = hs1.Item(cyl_str)

        ref2 = part1.CreateReferenceFromObject(cyl1)

        hss1 = ShFactory.AddNewHybridSplit(rf4, ref2, 1)
        body3.AppendHybridShape(hss1)
        rf4 = part1.CreateReferenceFromObject(hss1)
            

        ii = ii + 1

        if ii != noh:
            selection2.Add(hss1)
        else:
            hss1.name="MainS"
    
    visPropertySet2 = visPropertySet2.Parent
    visPropertySet2.SetShow(1)
    
    part1.Update()

    #save version with holes
    partDocument1.SaveAs(path2+"PR_"+str(i+1)+".catpart")
    partDocument1.ExportData(path2+"PR_"+str(i+1)+".stp", "stp")
    ver_list2 = vertex_list("D:\CAD_library_sampling\sample14\PR_"+str(i+1)+".stp")


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
i = 1898
ee = 0
while i < 5000: 
    try:
        pocket(i, "pocket_x")
    except:
        print("number "+str(i)+" not finished, error")
        ee = ee + 1

    if ee > 250:
        break
    i = i + 2
'''

def stiffened_panel(
                    I,                                                   #iteration
                    xmax = 1000,ymax =2000,no_stringer =2,t = 3, ts =2,  #overall panel
                    str_h = 50, str_w = 100,                             #stringer details
                    rh = 3, noh = 10,                                    #holes
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

    '''
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
    '''

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
            c2 = ShFactory.AddNewCylinder(rt1, rh, 100.000000, 100.000000, dirx)
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
            c2 = ShFactory.AddNewCylinder(rt1, rh, 100.000000, 100.000000, dirx)
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

        body16 = bodies1.Add()
        body16.Name = "P"+str(i)
    

        #radi and asm
        biti = ShFactory.AddNewFilletBiTangent(rf307, rf206, 5.000000, 1, 1, 1, 0)
        body16.AppendHybridShape(biti)
        rf309 = part1.CreateReferenceFromObject(biti)

        biti = ShFactory.AddNewFilletBiTangent(rf308, rf207, 5.000000, -1, 1, 1, 0)
        body16.AppendHybridShape(biti)
        rf310 = part1.CreateReferenceFromObject(biti)

        '''
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


        '''

        

        #hide excess geometry
        selection1 = partDocument1.Selection
        visPropertySet1 = selection1.VisProperties
        selection1.Add(body1)
        selection1.Add(body3)
        selection1.Add(body4)
        selection1.Add(body6)
        visPropertySet1 = visPropertySet1.Parent
        visPropertySet1.SetShow(1)


        




        part1.Update()

        
        path2 = "D:\\CAD_library_sampling\\sample15\\"
        #save version without holes and output empty notepad
        partDocument1.SaveAs(path2+"SP_"+str(I)+".catpart")
        partDocument1.ExportData(path2+"SP_"+str(I)+".stp", "stp")
        ver_list1 = vertex_list("D:\CAD_library_sampling\sample15\SP_"+str(I)+".stp")

        
        stre = ""
        with open(path2+"SP_"+str(I)+"_metadata.txt", "a") as text_file:
            text_file.write(stre)
        
        
        I = I + 1

        #hide excess geometry
        selection6 = partDocument1.Selection
        visPropertySet6 = selection6.VisProperties
        selection6.Add(body16)
        visPropertySet6 = visPropertySet6.Parent
        visPropertySet6.SetShow(1)  

        
        #make holes show

        #iterate through stringers
        
        iii = 1
        #itereate through holes
        while iii < 3:
            #iterate through halfes of stringer
            ii = 0
            if iii == 1:
                rftemp = rf309
            elif iii ==2:
                rftemp = rf310

            while ii < noh:
                #split1 = SF.AddNewSplit(rf00,0)#, catPositiveSide)

                bds1 = part1.HybridBodies

                hb1 = bds1.Item("Holes")

                hs1= hb1.HybridShapes

                cyl_str = "C_"+str(iii)+"_"+str(i)+"_"+str(ii)
                #print(cyl_str)
                cyl1 = hs1.Item(cyl_str)
                
                reference2 = part1.CreateReferenceFromObject(cyl1)

                                    
                splx = ShFactory.AddNewHybridSplit(rftemp, reference2, 1)

                splx.ExtrapolationType = 1

                rftemp = part1.CreateReferenceFromObject(splx)



                ii = ii + 1


            if iii == 1:
                body17 = bodies1.Add()
            body17.Name = "P"+str(i)+"_S"+str(iii)
            body17.AppendHybridShape(splx)
            iii = iii + 1
            
        part1.Update()

        #save version with holes
        partDocument1.SaveAs(path2+"SP_"+str(I)+".catpart")
        partDocument1.ExportData(path2+"SP_"+str(I)+".stp", "stp")
        ver_list2 = vertex_list("D:\CAD_library_sampling\sample15\SP_"+str(I)+".stp")

        #hide excess geometry
        selection6 = partDocument1.Selection
        visPropertySet6 = selection6.VisProperties
        selection6.Add(body17)
        visPropertySet6 = visPropertySet6.Parent
        visPropertySet6.SetShow(1)  


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



        i = i + 1


        
        with open(path2+"SP_"+str(I)+"_metadata.txt", "a") as text_file:
            text_file.write(stre)
        

        I = I + 1


    #also save main surface!!
    I = I + 1
    partDocument1.Close()
        
    return(I)
def xz_curve(x,a=0,b=0,c=0,d=2, e =0):
    #y = a*x**2 + b*x + c
    z = a*(x+e)**d+b*x+c
    return(z)

def holes_as_defined():
    print("x")
    #takes "holes" geo set and punches through to visualize in 3D


#stiffened pannel run:

import random
I = 0
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
    e2= random.randint(0,500)
    c1 = random.randint(-50,50)
    c2 = random.randint(-50,50)   


    I = stiffened_panel(I,xmax,ymax,no_stringer,t,ts,str_h,str_w,rh,noh,
                    a1=a1,a2=a2,b1=b1,b2=b2,c1=c1,c2=c2,d1=d2,e1=e1,e2=e2)
    

