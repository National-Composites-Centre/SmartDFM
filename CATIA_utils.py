# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 09:31:17 2022

@author: jakub.kucera
"""
import win32com.client.dynamic
from vecEX2_C import wrmmm
import numpy as np
import win32com.client.dynamic
import os
import statistics


def export_step(d):
    #this function takes surface part, adds thicknesses appropriate to local
    # layup, and saves result as step file
    part = d.path+d.part_name+".CATPart"
    part_name = d.part_name+".CATPart"
    print(part)
    #prerequisites are:
    #   CATIA surface model (open)
    #   layup definition (accessible by folder search)

    #use CATIA to generate solid from a surface and layup definition
    CATIA = win32com.client.Dispatch("CATIA.Application")
    wc = CATIA.Windows

    #oop value defines if CATIA part should be left open at the end
    oop = True

    #looking for open file (without exceptions this time?)
    
    try: 
        #try clause checks if the currently open parts
        partDocument2 = CATIA.ActiveDocument
        cat_name = CATIA.ActiveDocument.Name
        #cat_name = cat_name.split(".CATPart")[0]
        print(cat_name)
        print(part_name, "part")
        if cat_name == part_name:
            #in case the top part is the one specified use this
            partDocument1 = partDocument2
            part1 = partDocument1.Part
            print("DOCUMENT WAS FOUND OPENED 1")
        else:
            #in case the top part isnet check this - if this fails except is called
            ActWin = wc.Item(part_name)
            ActWin.Activate()
            partDocument1 = CATIA.ActiveDocument
            print("does this ever trigger?")
            part1 = partDocument1.Part
    
    except:
        #this should only happen when the part is not already open, this opens the CATIA part
        #cat_name = ""
        partDocument1 = CATIA.Documents.Open(part+".CATPart")
        oop = False
        part1 = partDocument1.Part
        print("document was not found open - standrd path is followed")
    


    #setting up non-solid modelling
    hybridBodies1 = part1.HybridBodies
    hybridBody1 = hybridBodies1.Add()
    part1.UpdateObject(hybridBody1)
    HSF = part1.HybridShapeFactory

    # Adding new body to part1
    body1 = hybridBodies1.Add()
    # Naming new body as "wireframe"
    body1.Name="thickness build"

    text = "MainS"
    body5 = hybridBodies1.Item("main_shape")
    hs5 = body5.HybridShapes
    sp_ref = hs5.Item(text)
    r5 = part1.CreateReferenceFromObject(sp_ref)

    #setting up for solid modelling
    SF = part1.ShapeFactory
    rX = part1.CreateReferenceFromName("")
    bodies1 = part1.Bodies

    # take average of edge-of-part spline
    for s in d.layup_sections:
        if s.sp_def == "edge":
            xt = 0
            yt = 0
            zt = 0
            for pt in s.pt_list:
                xt += pt.x
                yt += pt.y
                zt += pt.z

            xav = xt/len(s.pt_list)
            yav = yt/len(s.pt_list)
            zav = zt/len(s.pt_list)

    #create the point
    point= HSF.AddNewPointCoord(xav,yav,zav)
    body1.AppendHybridShape(point) 
    ref1 = part1.CreateReferenceFromObject(point)

    #project the point on the surface
    proj = HSF.AddNewProject(ref1, r5)
    body1.AppendHybridShape(proj) 
    ref2 = part1.CreateReferenceFromObject(proj)

    #create a normal to the surface a the point
    nor = HSF.AddNewLineNormal(r5, ref2, 0.000000, 100.000000, False)
    body1.AppendHybridShape(nor) 
    ref3 = part1.CreateReferenceFromObject(nor)

    #create a plane on the normal
    pl = HSF.AddNewPlaneNormal(ref3, ref2)
    body1.AppendHybridShape(pl) 
    ref4 = part1.CreateReferenceFromObject(pl)

    ii = 0
    #for each segment
    for s in d.layup_sections:

        #split main surface according to spline and reference
        #if edge of part, use main surface
        if s.sp_def != "edge":
            print("EDGE IDENTIFIED")
            rr = str(s.sp_def)
            rr = rr.replace("'","")
            print(rr)
            body6 = hybridBodies1.Item("gs2")
            hs6 = body6.HybridShapes
            '''
            #accomodating for implicit zone drop-offs
            if "+++" in rr:
                #create spline from points in new geometrical set
                # Adding new body to part1
                body66 = hybridBodies1.Add()
                body66.Name="pts2"

                iii = 0 

                #while loop for each spline
                hss1 = HSF.AddNewSpline()
                hss1.SetSplineType(0)
                hss1.SetClosing(1)
                while iii < np.size(s.pt_list,0):

                    x = s.pt_list[iii,0]
                    y = s.pt_list[iii,1]
                    z = s.pt_list[iii,2]
                    cord1 = HSF.AddNewPointCoord(x, y, z)
                    body1.AppendHybridShape(cord1)
                    ref2 = part1.CreateReferenceFromObject(cord1)
                    hss1.AddPointWithConstraintExplicit(ref2,None,-1,1,None,0)
                            
                    iii += 1
                
                body66.AppendHybridShape(hss1)
                r6 = part1.CreateReferenceFromObject(hss1)
                hss1.Name=s.sp_def.replace("+++","_")
                part1.Update

                print("under development")
            else:
            '''
            sp_ref = hs6.Item(rr)
            r6 = part1.CreateReferenceFromObject(sp_ref)

            #project spline on plane
            proj = HSF.AddNewProject(r6, ref4)
            body1.AppendHybridShape(proj) 
            r6 = part1.CreateReferenceFromObject(proj)

            #booleans only reliable solution

            #create body 1 as thickness of complete
            body10 = bodies1.Add()
            ts = SF.AddNewThickSurface(rX, 0, 1.000000, 0.000000)
            length1 = ts.TopOffset
            length1.Value = s.local_thickness
            ts.Surface = r5
            ts.swap_OffsetSide()
            part1.UpdateObject(ts)

            #create body 2 as pad of local spline
            body20 = bodies1.Add()
            part1.InWorkObject = body20
            pad1 = SF.AddNewPadFromRef(rX, 20.000000)
            hybridBody2 = hybridBodies1.Item("gs2")
            pad1.SetProfileElement(r6)
            pad1.IsSymmetric = True
            limit1 = pad1.FirstLimit
            length2 = limit1.Dimension
            length2.Value = 1000.000000
            part1.UpdateObject(pad1)

            #intersect the two shapes
            ins = SF.AddNewIntersect(body10)
            #rename required to prevent clashes with other intersects
            ins.Name = "Inter."+str(ii+1)
            shapes1 = body20.Shapes
            intersect1 = shapes1.Item("Inter."+str(ii+1))
            part1.UpdateObject(intersect1)
            part1.Update()

            #Add to main part
            body100 = bodies1.Item("PartBody")
            part1.InWorkObject = body100
            SF.AddNewAssemble(body20)
            shapes = body100.Shapes
            assemble1 = shapes.Item("Assemble.1")
            part1.UpdateObject(assemble1)                
        else:
            r42 = r5
            #just do thickness
            body10 = bodies1.Add()
            ts = SF.AddNewThickSurface(rX, 0, 1.000000, 0.000000)
            length1 = ts.TopOffset
            length1.Value = s.local_thickness
            ts.Surface = r5
            ts.swap_OffsetSide()
            part1.UpdateObject(ts)

            #Add to main part 
            body100 = bodies1.Item("PartBody")
            part1.InWorkObject = body100
            SF.AddNewAssemble(body10)
            shapes = body100.Shapes
            assemble1 = shapes.Item("Assemble.1")
            part1.UpdateObject(assemble1)
        
        ii = ii + 1

    #make construction geometry invisible
    selection1 = partDocument1.Selection
    selection1.Clear()
    visPropertySet1 = selection1.VisProperties
    #only can add hb2 if multiple segments
    try:
        selection1.Add(hybridBody2)
    except:
        pass
    selection1.Add(body5)
    selection1.Add(body1)
    #simply adds only when it exists
    try:
        selection1.Add(body66)
    except:
        pass
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)
    selection1.Clear()
    part1.Update()

    #export step into defined location, with prescribed name
    partDocument1.ExportData(d.path+d.part_name+""".stp""", "stp")
    partDocument1.Save()

    #close if it was close, leave open if it was opened
    if oop == False:
        partDocument1.Close()

    return(d)

def hole_loc(part, path = ""):
    part_name = part
    part = path+part_name+".CATpart"

    #collects location of holes
    #Relies on holes being defined by centre-points stored in
    #geometrical set called "holes".
    CATIA = win32com.client.Dispatch("CATIA.Application")
    wc = CATIA.Windows
    #oop value defines if CATIA part should be left open at the end
    oop = True
    
    #location of CATIA file
    try: 
        #try clause checks if the currently open parts
        partDocument2 = CATIA.ActiveDocument
        cat_name = CATIA.ActiveDocument.Name

        if cat_name == part_name:
            #in case the top part is the one specified use this
            partDocument1 = partDocument2
            part1 = partDocument1.Part
        else:
            #in case the top part isnet check this - if this fails except is called
            ActWin = wc.Item(part_name)
            ActWin.Activate()
            partDocument1 = CATIA.ActiveDocument

            part1 = partDocument1.Part
    
    except:
        #this should only happen when the part is not already open, this opens the CATIA part
        #cat_name = ""
        partDocument1 = CATIA.Documents.Open(part+".catpart")
        oop = False
        part1 = partDocument1.Part

    #partDocument1 = CATIA.Documents.Open(part)
    #part1 = partDocument1.Part
    HSF1 = part1.HybridShapeFactory
    #bodies1 = part1.HybridBodies
    bodies1 = part1.HybridBodies

    B2 = bodies1.Item("Hole")
    #hide part - essential for the .wrl generation
    selection1 = partDocument1.Selection
    selection1.Clear() # added recently delete if error
    visPropertySet1 = selection1.VisProperties
    selection1.Add(B2)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(0)
    selection1.Clear()
    
    # = "D:\\CAD_library_sampling\\xxx.wrl"
    #create .wrl
    #import - make sure vecEX2_C saved in same directory
    from vecEX2_C import wrmmm
    partDocument1.ExportData("C:\\temp\\xxx.wrl", "wrl")
    #interogate .wrl - carry over script from SySi 
    NS,f_pt = wrmmm(True)
    if oop == False:
        partDocument1.Close()
    return(f_pt)
    
#hole_loc("D:\\CoSinC_WP4.2\\TestCad\\X\\x_test_2.catpart")

def check_faces(FACES,CAD=[]):
    #This was only used as a check to display points in CATIA - not part of the DFM app

    #step_file = "D:\CoSinC_WP4.2\TestCad\s-1069.stp"
    #from step_utils import step_reclassification
    #import numpy as np
    #FACES = step_reclassification(step_file) 
    
    #temporary CATIA display fro troubleshooting
    CATIA = win32com.client.Dispatch("CATIA.Application")
    
    documents1 = CATIA.Documents
    partDocument1 = documents1.Add("Part")
    part1 = partDocument1.Part
    ShFactory = part1.HybridShapeFactory
    bodies1 = part1.HybridBodies

    for i , F in enumerate(FACES):
        bolX = F.bol
        
        # Adding new body to part1
        body1 = bodies1.Add()
        # Naming new body as "wireframe"
        body1.Name="x"+str(i)+str(bolX)
        
        x = float(F.edges[0].vertices[0].x)
        y = float(F.edges[0].vertices[0].y)
        z = float(F.edges[0].vertices[0].z)
        p = np.asarray([x,y,z])
        
        point=ShFactory.AddNewPointCoord(p[0],p[1],p[2])
        body1.AppendHybridShape(point) 
        ref1 = part1.CreateReferenceFromObject(point)
        
        x = float(F.edges[0].vertices[1].x)
        y = float(F.edges[0].vertices[1].y)
        z = float(F.edges[0].vertices[1].z)
        p = np.asarray([x,y,z])
        
        point=ShFactory.AddNewPointCoord(p[0],p[1],p[2])
        body1.AppendHybridShape(point) 
        ref2 = part1.CreateReferenceFromObject(point)
        
        x = float(F.edges[2].vertices[0].x)
        y = float(F.edges[2].vertices[0].y)
        z = float(F.edges[2].vertices[0].z)
        p = np.asarray([x,y,z])
        
        point=ShFactory.AddNewPointCoord(p[0],p[1],p[2])
        body1.AppendHybridShape(point) 
        ref3 = part1.CreateReferenceFromObject(point)
        
        x = float(F.edges[2].vertices[1].x)
        y = float(F.edges[2].vertices[1].y)
        z = float(F.edges[2].vertices[1].z)
        p = np.asarray([x,y,z])
           
        point=ShFactory.AddNewPointCoord(p[0],p[1],p[2])
        body1.AppendHybridShape(point) 
        ref4 = part1.CreateReferenceFromObject(point)

def GNN_validation():
    #this projects points on current CATIA part, from specified excel

    #open csv files
    file1 = open('D:\\CoSinC_WP4.2\\WS_2.0\\votes_fl.csv')

    #read csv files
    Lines1 = file1.readlines()

    pts = []
    for i, line in enumerate(Lines1):
        if i != 0:
            votes = int(line.split(",")[6])
            if votes > 0:
                #self.MajorRadius = True
                x = float(line.split(",")[2])
                y = float(line.split(",")[3])
                z = float(line.split(",")[4])
                pt = np.asarray([x,y,z])
                pts.append(pt)

    FL_points = pts

    #catia start up
    CATIA = win32com.client.Dispatch("CATIA.Application")
    wc = CATIA.Windows

    #try clause checks if the currently open parts
    partDocument1 = CATIA.ActiveDocument
    part1 = partDocument1.Part
    ShFactory = part1.HybridShapeFactory
    bodies1 = part1.HybridBodies

    body1 = bodies1.Add()

    #iterate adding points 
    for p in FL_points:
        point=ShFactory.AddNewPointCoord(p[0],p[1],p[2])
        body1.AppendHybridShape(point) 
        ref1 = part1.CreateReferenceFromObject(point)

#GNN_validation()
    