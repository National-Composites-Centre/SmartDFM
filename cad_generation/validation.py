# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 16:36:57 2022

@author: jakub.kucera
"""

import win32com.client.dynamic
#import numpy as np


#adds all the vertices stored to the CAD file, can be reviewed in opened CATIA 
#window

#CATIA should be running before running this script

def standard_validation():
    i = 911

    while i < 912:
        filename = "SP_"+str(i)
        
        CATIA = win32com.client.Dispatch("CATIA.Application")
        CATIA.RefreshDisplay = False
        
        #Location of CATIA file to be meshed.
        str15 = "D:\\CAD_library_sampling\\sample12\\"+filename+".catpart"
        partDocument1 = CATIA.Documents.Open(str15)
        part1 = partDocument1.Part
        ShFactory = part1.HybridShapeFactory
        hbs1 = part1.HybridBodies
        bodies1 = part1.HybridBodies
        # Adding new body to part1
        body1 = bodies1.Add()
        # Naming new body as "wireframe"
        body1.Name="validation"
        # Surfaces group
        
        
        #just an option to manually edit to chose between validation and other checks
        validation = False 
        if validation == True:
            # Using readlines()
            file1 = open('D:\\CAD_library_sampling\\sample12\\'+filename+'_metadata.txt', 'r')
        elif validation == False:
            file1 = open('D:\\CoSinC_WP4.2\\temp\\temp.csv')

        
        Lines = file1.readlines()
        
        count = 0
        # Strips the newline character
        for line in Lines:
            count += 1
            print("Line{}: {}".format(count, line.strip()))
            
            if count > 1:
                ct = line.count(",")
                if ct > 1:
                    x = line.split(",")[0]
                    y = line.split(",")[1]
                    z = line.split(",")[2]
            
                    point=ShFactory.AddNewPointCoord(x,y,z)
                    body1.AppendHybridShape(point) 
                    
        i = i + 1
        file1.close()

def validation_ws():
    filename = "D:\CAD_library_sampling\sample17\\SP_9.catpart"
    
    CATIA = win32com.client.Dispatch("CATIA.Application")
    CATIA.RefreshDisplay = False
    
    #Location of CATIA file to be meshed.

    partDocument1 = CATIA.Documents.Open(filename)
    part1 = partDocument1.Part
    ShFactory = part1.HybridShapeFactory
    hbs1 = part1.HybridBodies
    bodies1 = part1.HybridBodies
    # Adding new body to part1
    body1 = bodies1.Add()
    # Naming new body as "wireframe"
    body1.Name="validation"
    # Surfaces group
    

    file1 = open('D:\\CoSinC_WP4.2\\WS_2.0\\votes.csv')

    
    Lines = file1.readlines()
    
    count = 0
    # Strips the newline character
    for line in Lines:
        count += 1
        print("Line{}: {}".format(count, line.strip()))
        if count > 1:
            ct = line.count(",")
            if ct > 1:
                if float(line.split(",")[6]) == 1.0:
                    print("x")
                    x = line.split(",")[1]
                    y = line.split(",")[2]
                    z = line.split(",")[3]
            
                    point=ShFactory.AddNewPointCoord(x,y,z)
                    body1.AppendHybridShape(point) 
                
    
    file1.close()

validation_ws()
