
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

def rand_hole(HSF,partDocument1,part1,xyz,i,body3,maxhole = 8):
    #this script generates a hole in the available part

    #additional setup, could be outside
    hybridBodies1 = part1.HybridBodies
    body1 = hybridBodies1.Add()
    body1.Name="xxx"

    #random location for point, inside the part box
    poc1 = HSF.AddNewPointCoord(xyz[0],xyz[1],xyz[2])
    body1.AppendHybridShape(poc1)

    #some plane work
    ref1 = part1.CreateReferenceFromObject(poc1)
    originElements1 = part1.OriginElements
    pe1 = originElements1.PlaneXY
    ref2 = part1.CreateReferenceFromObject(pe1)

    #project the point on surface (currently not super important)
    pr1 = HSF.AddNewProject(ref1, ref2)
    pr1.SolutionType = 0
    pr1.Normal = True
    pr1.SmoothingType = 0
    pr1.ExtrapolationMode = 0
    body1.AppendHybridShape(pr1)

    #hole circle
    ref3 = part1.CreateReferenceFromObject(pr1)
    ref4 = part1.CreateReferenceFromObject(pe1)
    c1 = HSF.AddNewCircleCtrRad(ref3, ref4, False, random.randint(1, maxhole))
    c1.SetLimitation(1)
    body1.AppendHybridShape(c1)

    #switch to solids work and create some extrusions
    ref5 = part1.CreateReferenceFromObject(c1)
    part1.InWorkObject = body3
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

    #hide excess geometry
    selection1 = partDocument1.Selection
    visPropertySet1 = selection1.VisProperties
    selection1.Add(body1)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)

  
    #sphere alternative for surfaces, will work a bit better as it is not direction dependent


def vertex_list(stp_file):
    #Open defined step file
    with open(stp_file, "r") as text_file:
        f = text_file.read()
    fc = f.count("\n")

    vert_list = []

    for line in f.split("\n"):
        #lines defining vertices
        if "=VERTEX_POINT" in line:
            xl = line.split(",#")[1]
            xl = xl.split(")")[0]

            #corresponding vertex locations
            for l2 in f.split("\n"):
                if "#"+str(xl)+"=" in l2:
                    xl2 = l2.split("('Vertex',(")[1]
                    xl2 = xl2.split(")")[0]

                    sv = step_vertex()
                    sv.x = float(xl2.split(",")[0])
                    sv.y = float(xl2.split(",")[1])
                    sv.z = float(xl2.split(",")[2])

                    #save as list of objects
                    vert_list.append(sv)
    #return list of vertex objects
    return(vert_list)

#ver_list = vertex_list("D:\CAD_library_sampling\sample9\s-6.stp")

def main():
    #currently specialized for previous set of CAD shapes
    path = "D:\\CAD_library_sampling\\sample9\\"
    path2 ="D:\\CAD_library_sampling\\sample11\\"
    i = 0
    while i < 9999:
        #open file 
        with open(path+"s-"+str(i)+"_metadata.txt", "r") as text_file:
            f = text_file.read()
        if "hole" not in f:
            #check vertex list
            ver_list1 = vertex_list("D:\CAD_library_sampling\sample9\s-"+str(i)+".stp")

            #establish the area, where holes can be created
            xmax = -99999
            xmin = 999999
            ymax = -99999
            ymin = 99999
            zmax = -99999
            zmin = 99999
            for v in ver_list1:
                if v.x > xmax:
                    xmax =v.x
                if v.x < xmin:
                    xmin = v.x
                if v.y > ymax:
                    ymax = v.y
                if v.y < ymin:
                    ymin = v.y
                if v.z > zmax:
                    zmax = v.z
                if v.z < zmin:
                    zmin = v.z


            limr = 5

            CATIA = win32com.client.Dispatch("CATIA.Application")
            
            #location of CATIA file
            partDocument1 = CATIA.Documents.Open(path+"s-"+str(i)+".catpart")
            part1 = partDocument1.Part

            #Relies on stanadard naming of geometrical sets
            bodies1 = part1.Bodies
            body1 = bodies1.Item("PartBody")
            part1.InWorkObject = body1
            HSF = part1.HybridShapeFactory

            body3 = bodies1.Add()

            ii = random.randint(0, 5)
            prev = []
            while ii < 6:
                #make a hole
                xyz = [random.randint(int(xmin+limr), int(xmax-limr)), 
                    random.randint(int(ymin+limr), int(ymax-limr)), 
                    random.randint(int(zmin), int(zmax))]
                
                run = True

                for xyz2 in prev:
                    dist = math.sqrt((xyz[0]-xyz2[0])**2+(xyz[1]-xyz2[1])**2)
                    if dist < limr*2.05:
                        run = False


                if run == True:
                    rand_hole(HSF,partDocument1,part1,xyz,i,body3,maxhole = limr)
                    prev.append(xyz)


                ii = ii + 1

            #inefficient but working boolean
            partDocument1 = CATIA.ActiveDocument
            part1 = partDocument1.Part
            bodies1 = part1.Bodies
            body1 = bodies1.Item("PartBody")
            part1.InWorkObject = body1
            shapeFactory1 = part1.ShapeFactory
            shapeFactory1.AddNewRemove(body3)
            shapes1 = body1.Shapes



            part1.Update()

            partDocument1.SaveAs(path2+"s-"+str(i)+".catpart")
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


            iii = 0
            stre = ""
            alo = []
            while iii < len(diff):
                
                if iii not in alo:
                    iv = iii+1
                    stre += "\n hole\n"
                    stre += str(diff[iii].x)+","+str(diff[iii].y)+","+str(diff[iii].z)+"\n"
                    while iv < len(diff):
                        print(alo)
                        if iv not in alo:
                            #distance only in x y because holes only done in z direction for now
                            ddst = math.sqrt((diff[iv].x-diff[iii].x)**2+(diff[iv].y-diff[iii].y)**2)#(diff[iv].z-diff[iii].z)**2)
                            if ddst < 2.05*limr:
                                stre += str(diff[iv].x)+","+str(diff[iv].y)+","+str(diff[iv].z)+"\n"
                                alo.append(iv)
                        iv = iv + 1
                iii = iii + 1
                            
            with open(path2+"s-"+str(i)+"_metadata.txt", "a") as text_file:
                text_file.write(stre)

            #copy and rename old three files as another data-point 10000+i
            os.link(path+"s-"+str(i)+".catpart", path2+"s-"+str(i+10000)+".catpart")
            os.link(path+"s-"+str(i)+"_metadata.txt", path2+"s-"+str(i+10000)+"_metadata.txt")
            os.link(path+"s-"+str(i)+".stp", path2+"s-"+str(i+10000)+".stp")


        i = i + 1
#main()
            