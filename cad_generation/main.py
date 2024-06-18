# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 16:23:56 2022

@author: jakub.kucera
"""
import win32com.client.dynamic
import numpy as np
import random
import math
import prelim_shapes

#1 = box
#2 = taper
#3 = omega, stringer
#4 = flange
#5 = hole
#6 = pin
lisT = ["-","box","taper","flange","omega","hole","pin"]


CATIA = win32com.client.Dispatch("CATIA.Application")

#naming of the sampled file
sn = "s"

#start this run at number:
i = 7406
#end this run at number:
mi = 10000
while i < mi:
    
    name = sn+"-"+str(i) 
    
    #create empty .txt files
    file = "D:\\CAD_library_sampling\\"+name+"_metadata.txt"
    #second one should include all the randomly generated variables (add when needed)
    #file2 = "D:\\CAD_library_sampling\\"+name+"metadata_full.txt"
    open(file, 'a').close()
    #open(file2, 'a').close()
    
    #default boundary conditions for the first object
    M = np.asarray([[0,0,0],
                   [0,0,0],
                   [0,0,0],
                   [0,0,0],
                   [-120,-140,0],
                   [120,-140,0],
                   [-120,140,0],
                   [120,140,0]])
    
    #ri defines number of shapes required  # default is simply 2
    
    ri = random.randint(2,2)
    instructions = []
    ii = 0
    while ii < ri:
        if ii == 0:
            #adjusting randomness to equalize number of nodes for a shape
            spec = random.random()
            vertices = [1/8,1/8,1/16,1/44]
            n = [0,0,0,0]
            n[0] = vertices[0]/sum(vertices)
            n[1] = (vertices[1]+vertices[0])/sum(vertices)
            n[2] = (vertices[1]+vertices[0]+vertices[2])/sum(vertices)
            n[3] = (vertices[1]+vertices[0]+vertices[2]+vertices[3])/sum(vertices)
            
            uhm = 0
            u1 = 0
            while uhm < 1:
                if spec <= n[u1]:
                    uhm = 2
                    instructions.append(u1+1)
                u1 = u1 + 1

            #instructions.append(random.randint(1,4))
        else:
            #adjusting randomness to equalize number of nodes for a shape
            spec = random.random()
            vertices = [1/8,1/8,1/16,1/44,1/3,1/3]
            n = [0,0,0,0,0,0]
            n[0] = vertices[0]/sum(vertices)
            n[1] = (vertices[1]+vertices[0])/sum(vertices)
            n[2] = (vertices[1]+vertices[0]+vertices[2])/sum(vertices)
            n[3] = (vertices[1]+vertices[0]+vertices[2]+vertices[3])/sum(vertices)
            n[4] = (vertices[1]+vertices[0]+vertices[2]+vertices[3]+vertices[4])/sum(vertices)
            n[5] = (vertices[1]+vertices[0]+vertices[2]+vertices[3]+vertices[4]+vertices[5])/sum(vertices)
            
            
            uhm = 0
            u1 = 0
            while uhm < 1:
                if spec <= n[u1]:
                    uhm = 2
                    instructions.append(u1+1)
                u1 = u1 + 1           
            
            
            
            #instructions.append(random.randint(1,6))
        ii = ii + 1
    #select base component
    #first = random.randint(1, 4)
    #select secondary component (some can only be secondary: 5-6 hole and pin)
    #second = random.randint(1,6)
    
    #temporary overwrite
    #instructions = [4, 4]
    
    
    print(instructions)
    p1_str = ""
    #initial line in the metadata file
    with open(file, "a") as text_file:
        ii = 0
        while ii < ri:
            
            p1 = str(lisT[instructions[ii]])
            p1_str += p1+"," 
            ii = ii + 1
        text_file.write(p1_str+"\n") 
        
    #start CATIA files
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
    
    #currently combining 2 parts to gether - but could be more
    ii = 0
    while ii < ri: # change 2 into np.size(instructions, 1) for more parts included
    

        
        #for the secondary shapre gen. provide list of randomly generated values
        #in prelim_... add if clause for randomly generated values, if values provided, run just that
    
    
        #could the following be condensed into 1 line that pics function?
        if instructions[ii] == 1:
            
            M, VRTs = prelim_shapes.box(body1, ShFactory, body3,part1,bodies1,partDocument1,ii,M,file,instructions,CATIA)
            
            #Individual part creation here for vertex collection
            #vertex = True
            #repeat for each one below
            #M = prelim_shapes.box(body1, ShFactory, body3,part1,bodies1,partDocument1,ii,M,file,instructions)
            
        if instructions[ii] == 2:
            M, VRTs  = prelim_shapes.taper(body1, ShFactory, body3,part1,bodies1,partDocument1,ii,M,file,instructions,CATIA)
        if instructions[ii] == 3:
            #binary df included here, as 2 flanges cannot be oriented in the same direction.
            #If two flanges are required, the other one points away from the first.
            if ii == 0:
                df = 0
            else:
                df = 1
            M, VRTs  = prelim_shapes.flange(body1, ShFactory, body3,part1,bodies1,partDocument1,ii,M,df,file,instructions,CATIA)
        if instructions[ii] == 4:
            M, VRTs  = prelim_shapes.omega(body1, ShFactory, body3,part1,bodies1,partDocument1,ii,M,file,instructions,CATIA)
        if instructions[ii] == 5:
            VRTs = prelim_shapes.hole(body1, ShFactory, body3,part1,bodies1,partDocument1,ii,M,file,instructions,CATIA,VRTs) 
        if instructions[ii] == 6:
            VRTs = prelim_shapes.pin(body1, ShFactory, body3,part1,bodies1,partDocument1,ii,M,file,instructions,CATIA,VRTs)
        
        
        lisT = ["-","box","taper","flange","omega","hole","pin"]
        p1 = lisT[instructions[ii]]
        with open(file, "a") as text_file:
            text_file.write(p1+"\n"+VRTs+"\n")
        
        ii = ii + 1
          
    #save the CAD file, and export it as .stp
    silo = "D:\\CAD_library_sampling\\"+name+".CatPart"
    print(silo)
    partDocument1.SaveAs(silo)
    partDocument1.ExportData("""D:\\CAD_library_sampling\\"""+name+""".stp""", "stp")
    partDocument1.Close()


    #second document with the above metadata + variables, for later to check if needed...
    #with open(file2, "a") as text_file:
    #    text_file.write(str(x)+","+str(y)+","+str(z)+"B"+"\n")
            
    i = i + 1