


#FROM CATIA_UTILS.PY 

#############################################
import win32com.client.dynamic
from vecEX2_C import wrmmm
import numpy as np
import win32com.client.dynamic
import os
import statistics

def export_step_old(path,part,thickness):
    #this function takes surface part, adds thickness, and saves result as step file
    CATIA = win32com.client.Dispatch("CATIA.Application")
    

    #location of CATIA file
    try: 
        #try clause checks if the currently open parts
        CATIA = win32com.client.Dispatch("CATIA.Application")
        partDocument2 = CATIA.ActiveDocument
        cat_name = CATIA.ActiveDocument.Name
        #cat_name = cat_name.split(".CATPart")[0]
        if cat_name == part+".catpart":
            #in case the top part is the one specified use this
            partDocument1 = partDocument2
            part1 = partDocument1.Part
        else:
            #in case the top part isnet check this - if this fails except is called
            partDocument1 = CATIA.Documents.Activate(path+part+".catpart")
            part1 = partDocument1.Part
    
    except:
        #this should only happen when the part is not already open, this opens the CATIA part
        #cat_name = ""
        partDocument1 = CATIA.Documents.Open(path+part+".catpart")
        part1 = partDocument1.Part


    #Relies on stanadard naming of geometrical sets
    bodies1 = part1.Bodies
    body1 = bodies1.Item("PartBody")
    part1.InWorkObject = body1
    HSF = part1.ShapeFactory
    reference1 = part1.CreateReferenceFromName("")
    thickSurface1 = HSF.AddNewThickSurface(reference1, 0, thickness, 0.000000)
    hybridBodies1 = part1.HybridBodies
    hybridBody1 = hybridBodies1.Item("main_shape")
    hybridShapes1 = hybridBody1.HybridShapes
    hybridShapeSplit1 = hybridShapes1.Item("MainS")
    reference2 = part1.CreateReferenceFromObject(hybridShapeSplit1)
    thickSurface1.Surface = reference2
    part1.UpdateObject(thickSurface1)

    #export step into defined location, with prescribed name
    partDocument1.ExportData(path+part+""".stp""", "stp")

    partDocument1.Close()

#FAILED ATTEMPT AT SWITCHING BETWEEN EXISTENT WINDOWS:
    '''
    wct = wc.Count
    i = 2
    #wcs = []
    wc_open = False
    while i < wct+1:
        print(wc.Item(i))
        ActWin = wc.Item(i)
        wc_nm = CATIA.ActiveDocument.Name
        #wcs.append(wc_nm)
        print(wc_nm,"wc_nm")
        print(part_name, "part")
        if wc_nm == part_name:
            partDocument1 = CATIA.ActiveDocument
            part1 = partDocument1.Part
            wc_open = True
            break
        i = i + 1

    if wc_open == False:
        partDocument1 = CATIA.Documents.Open(part+".catpart")
        oop = False
        part1 = partDocument1.Part
        print("document was not found open - standrd path is followed")

    '''