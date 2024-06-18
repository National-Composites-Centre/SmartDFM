# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 13:54:04 2022

@author: jakub.kucera
"""
import win32com.client.dynamic
import sys, os 
import numpy as np
import win32gui
import math
import time
from datetime import date

#The functions below use the internal functions of CATIA. VBA recording function
#within CATIA was used to develope these scripts.

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



l1 = 50
l2 = 50
l3 = 50 
l4 = 50
l5 = 5
r1 = 10
r2 = 10
e1 = 200



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


oEl1 = part1.OriginElements
hspe = oEl1.PlaneXY
ref78 = part1.CreateReferenceFromObject(hspe)

rad1 = ShFactory.AddNewCircleBitangentRadius(ref7, ref8, ref78, r1, 1, 1)
rad1.DiscriminationIndex = 1
rad1.BeginOfCircle = 1
rad1.TangentOrientation1 = 1
rad1.TangentOrientation2 = 1
rad1.SetLimitation(2)
rad1.TrimMode = 0
body1.AppendHybridShape(rad1)
rad1.Name="r1"
ref12 = part1.CreateReferenceFromObject(rad1)


rad1 = ShFactory.AddNewCircleBitangentRadius(ref8, ref9, ref78, r2, 1, 1)
rad1.DiscriminationIndex = 1
rad1.BeginOfCircle = 1
rad1.TangentOrientation1 = 1
rad1.TangentOrientation2 = 1
rad1.SetLimitation(2)
rad1.TrimMode = 0
body1.AppendHybridShape(rad1)
rad1.Name="r2"
ref13 = part1.CreateReferenceFromObject(rad1)


rad1 = ShFactory.AddNewCircleBitangentRadius(ref9, ref10, ref78, r2, 1, 1)
rad1.DiscriminationIndex = 1
rad1.BeginOfCircle = 1
rad1.TangentOrientation1 = 1
rad1.TangentOrientation2 = 1
rad1.SetLimitation(2)
rad1.TrimMode = 0
body1.AppendHybridShape(rad1)
rad1.Name="r3"
ref14 = part1.CreateReferenceFromObject(rad1)

rad1 = ShFactory.AddNewCircleBitangentRadius(ref10, ref11, ref78, r1, 1, 1)
rad1.DiscriminationIndex = 1
rad1.BeginOfCircle = 1
rad1.TangentOrientation1 = 1
rad1.TangentOrientation2 = 1
rad1.SetLimitation(2)
rad1.TrimMode = 0
body1.AppendHybridShape(rad1)
rad1.Name="r4"
ref15 = part1.CreateReferenceFromObject(rad1)




t1 = ShFactory.AddNewHybridTrim(ref7, -1, ref12, 1)

t1.Mode = 1



t1.SetElem(0, ref8)
t1.SetPreviousOrientation(2, 1)
t1.SetNextOrientation(2, -1)

t1.SetElem(0, ref13)
t1.SetPreviousOrientation(2, 1)
t1.SetNextOrientation(2, -1)

t1.SetElem(0, ref9)
t1.SetPreviousOrientation(2, 1)
t1.SetNextOrientation(2, -1)

t1.SetElem(0, ref14)
t1.SetPreviousOrientation(2, 1)
t1.SetNextOrientation(2, -1)

t1.SetElem(0, ref10)
t1.SetPreviousOrientation(2, 1)
t1.SetNextOrientation(2, -1)

t1.SetElem(0, ref15)
t1.SetPreviousOrientation(2, 1)
t1.SetNextOrientation(2, -1)

t1.SetElem(0, ref11)
t1.SetPreviousOrientation(2, 1)
t1.SetNextOrientation(2, -1)

body1.AppendHybridShape(t1)






#lPath = os.path.dirname(os.path.abspath(__file__))
name = "testx"
silo = "D:\\CAD_library_sampling\\"+name+".CatPart"
print(silo)
partDocument1.SaveAs(silo)