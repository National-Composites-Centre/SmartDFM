
import random

import win32com.client.dynamic
from vecEX2_C import wrmmm
import numpy as np
import win32com.client.dynamic
import os
import math

class step_vertex:
    #vertices, the lowest level of geometry in step file
    def __init__(self, x = 0,y = 0,z = 0):
        self.x = 0
        self.y = 0
        self.z = 0

def rand_hole(HSF,partDocument1,part1,xyz,i,maxhole = 8):
    #this script generates a hole in the available part

    hybridBodies1 = part1.HybridBodies

    body1 = hybridBodies1.Add()
    body1.Name="xxx"

    poc1 = HSF.AddNewPointCoord(xyz[0],xyz[1],xyz[2])

    body1.AppendHybridShape(poc1)

    ref1 = part1.CreateReferenceFromObject(poc1)

    originElements1 = part1.OriginElements

    pe1 = originElements1.PlaneZX

    ref2 = part1.CreateReferenceFromObject(pe1)

    pr1 = HSF.AddNewProject(ref1, ref2)

    pr1.SolutionType = 0

    pr1.Normal = True

    pr1.SmoothingType = 0

    pr1.ExtrapolationMode = 0

    body1.AppendHybridShape(pr1)

    ref3 = part1.CreateReferenceFromObject(pr1)

    ref4 = part1.CreateReferenceFromObject(pe1)

    c1 = HSF.AddNewCircleCtrRad(ref3, ref4, False, random.randint(1, maxhole))

    c1.SetLimitation(1)

    body1.AppendHybridShape(c1)

    #dir1 = HSF.AddNewDirectionByCoord(0.000000, 0.000000, 1.000000)

    ref5 = part1.CreateReferenceFromObject(c1)

    #ex = HSF.AddNewExtrude(ref5, 200.000000, 200.000000, dir1)

    #ex.SymmetricalExtension = 0

    #body1.AppendHybridShape(ex)
    bodies1 = part1.Bodies


    body2 = bodies1.Add()

    part1.InWorkObject = body2


    part1.Update()

    SF = part1.ShapeFactory



    ref1 = part1.CreateReferenceFromName("")

    pad1 = SF.AddNewPadFromRef(ref1, 20.000000)



    pad1.SetProfileElement(ref5)

    pad1.IsSymmetric = True

    limit1 = pad1.FirstLimit

    length1 = limit1.Dimension

    length1.Value = 200.000000

    part1.UpdateObject(pad1)
    body3 = bodies1.Item("PartBody")
    part1.InWorkObject = body3


    SF.AddNewRemove(body2)



    shapes1 = body3.Shapes

    #remove1 = shapes1.Item("Remove."+str(i))

    part1.Update()




    #ref6 = part1.CreateReferenceFromName("")

    #split1 = SF.AddNewSplit(ref6)#, 1)#, catPositiveSide)

    #ref7 = part1.CreateReferenceFromObject(ex)

    #split1.Surface = ref7

    #split1.SplitSide = 0

    #part1.UpdateObject(split1)
    #part1.Update()

    selection1 = partDocument1.Selection
    visPropertySet1 = selection1.VisProperties
    selection1.Add(body1)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)

  




    #generate a point in random location in set 3d space

    #project said point onto main surface (how identify?)


    #hide everything

    #unhide the projection

    #export projection location


    #(need the other vertex?) -- maybe get from point at extremity? on the edge?


    #save the vertices


    #create a full shere 


    #cut the sphere out of main part
    





#check .step file before hole

#add hole

#check added vertices ... that's what you give to Tim



def vertex_list(stp_file):
    #Open defined step file
    with open(stp_file, "r") as text_file:
        f = text_file.read()
    fc = f.count("\n")

    vert_list = []

    for line in f.split("\n"):
        if "=VERTEX_POINT" in line:
            xl = line.split(",#")[1]
            xl = xl.split(")")[0]

            for l2 in f.split("\n"):
                if "#"+str(xl)+"=" in l2:
                    xl2 = l2.split("('Vertex',(")[1]
                    xl2 = xl2.split(")")[0]

                    sv = step_vertex()
                    sv.x = xl2.split(",")[0]
                    sv.y = xl2.split(",")[1]
                    sv.z = xl2.split(",")[2]

                    vert_list.append(sv)
    for d in vert_list:
        print(d.x)
    
    return(vert_list)

#ver_list = vertex_list("D:\CAD_library_sampling\sample9\s-6.stp")

def poke_holes():

    path = "D:\\CAD_library_sampling\\sample9\\"
    path2 ="D:\\CAD_library_sampling\\sample11\\"
    i = 0
    while i < 5: #9999:
        #open file 
        with open(path+"s-"+str(i)+"_metadata.txt", "r") as text_file:
            f = text_file.read()
        if "hole" not in f:
            #check vertex list
            ver_list1 = vertex_list("D:\CAD_library_sampling\sample9\s-"+str(i)+".stp")

        CATIA = win32com.client.Dispatch("CATIA.Application")
        
        #location of CATIA file
        partDocument1 = CATIA.Documents.Open(path+"s-"+str(i)+".catpart")
        part1 = partDocument1.Part

        #Relies on stanadard naming of geometrical sets
        bodies1 = part1.Bodies
        body1 = bodies1.Item("PartBody")
        part1.InWorkObject = body1
        HSF = part1.HybridShapeFactory

        ii = random.randint(0, 5)
        prev = []
        while ii < 6:
            #make a hole
            xyz = [random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)]
            
            run = True

            for xyz2 in prev:
                dist = math.sqrt((xyz[0]-xyz2[0])**2+(xyz[1]-xyz2[1])**2)


            if run == True:
                rand_hole(HSF,partDocument1,part1,xyz,i)
                prev.append(xyz)

                ii = 50

            ii = ii + 1

        partDocument1.SaveAs=(path2+"s-"+str(i)+".catpart")
        partDocument1.ExportData(path2+"s-"+str(i)+".stp", "stp")
        ver_list2 = vertex_list("D:\CAD_library_sampling\sample11\s-"+str(i)+".stp")

        partDocument1.Close()

        #compare 2 vertex lists
        diff = []
        for l2 in ver_list2:
            ex = True
            for l1 in ver_list1:
                if l1.x == l2.x and l1.y == l2.y and l1.z == l2.z:
                    ex = False
                
            if ex == True:
                diff.append(l2)

        print("diff")
        print(diff)
        stre = "hole\n"
        for h in diff:
            stre += str(h.x)+","+str(h.y)+","+str(h.z)+"\n"
                        
        with open(path2+"s-"+str(i)+"_metadata.txt", "a") as text_file:
            text_file.write(stre)

        #copy and rename old three files as another data-point 10000+i
        os.link(path+"s-"+str(i)+".catpart", path2+"s-"+str(i+10000)+".catpart")
        os.link(path+"s-"+str(i)+"_metadata.txt", path2+"s-"+str(i+10000)+"_metadata.txt")
        os.link(path+"s-"+str(i)+".stp", path2+"s-"+str(i+10000)+".stp")

        i = i + 1

        

    #make hole (random number of holes at random location - avoiding too close holes -- this dist can be used below for distinguish)

    #save .stp 2 -- proper name

    #save .catpart 2

    #check vert list 2

    #compare vert lists

    #distinguish between individual holes

    #save extra locations as holes

    #