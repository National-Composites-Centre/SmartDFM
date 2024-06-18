
import win32com.client.dynamic
import numpy as np
import os
import random
import math
from WS_gen_2 import vertex_list
import time

def xz_curve(x,a=0,b=0,c=0,d=2, e =0):
    #y = a*x**2 + b*x + c
    z = a*(x+e)**d+b*x+c
    return(z)

def extra_edge_cuts(I,documents1,partDocument1,part1,p8arr,ex1, sample,noh,rh,posH,csys):
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

    directions = [dirX,dirY,dir1]




    #prepare for solids modelling
    SF = part1.ShapeFactory
    bodies1 = part1.Bodies
    b1 = bodies1.Item("PartBody")
    part1.InWorkObject = b1
    rfX = part1.CreateReferenceFromName("")




    #creating reference (no-radii) body
    bodies1 = part1.Bodies
    body10 = bodies1.Item("PartBody")

    bodies1 = part1.Bodies
    body100 = bodies1.Add()
    body100.Name="first"

    part1.InWorkObject = body100
    SF = part1.ShapeFactory
    refX = part1.CreateReferenceFromName("")



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




    #hide excess geometry
    selection1 = partDocument1.Selection
    visPropertySet1 = selection1.VisProperties
    selection1.Add(body1)
    selection1.Add(body3)
    selection1.Add(body6)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)

    part1.Update()
    path2 = "D:\\CAD_library_sampling\\sample61\\"
    path3 = "D:\\CAD_library_sampling\\sample61\\no_curves\\"
    #save version without holes and output empty notepad
    partDocument1.SaveAs(path3+sample+"_"+str(I)+".catpart")
    partDocument1.ExportData(path3+sample+"_"+str(I)+".stp", "stp")
    ver_list1 = vertex_list("D:\\CAD_library_sampling\\sample61\\no_curves\\"+sample+"_"+str(I)+".stp")
    #stre = ""
    #with open(path2+sample+"_"+str(I)+"_metadata.txt", "a") as text_file:
    #    text_file.write(stre)





    #hide n seek
    selection1 = partDocument1.Selection
    selection1.Clear()
    visPropertySet1 = selection1.VisProperties
    selection1.Add(body100)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)
    part1.Update()

    #prepare for solids modelling
    SF = part1.ShapeFactory
    bodies1 = part1.Bodies
    b1 = bodies1.Item("PartBody")
    part1.InWorkObject = b1
    rfX = part1.CreateReferenceFromName("")


    #creating reference (no-radii) body
    bodies1 = part1.Bodies
    body10 = bodies1.Item("PartBody")

    bodies1 = part1.Bodies
    body100 = bodies1.Add()
    body100.Name="second"

    part1.InWorkObject = body100
    SF = part1.ShapeFactory
    refX = part1.CreateReferenceFromName("")



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





    #save version with holes
    partDocument1.SaveAs(path2+sample+"_"+str(I)+".catpart")
    partDocument1.ExportData(path2+sample+"_"+str(I)+".stp", "stp")
    ver_list2 = vertex_list("D:\\CAD_library_sampling\\sample61\\"+sample+"_"+str(I)+".stp")

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
    with open(path2+sample+"_"+str(I)+"_metadata.txt", "a") as text_file:
        text_file.write(stre)
    #partDocument1.Close()

'''
#sampling x
i = 0
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

    #csys
    csys = [0,0,0,0,0,0]
    csys[0] = random.randint(0,2000)
    csys[1] = random.randint(0,2000)
    csys[2] = random.randint(0,2000)
    csys[3] = random.randint(0,360)
    csys[4] = random.randint(0,360)
    csys[5] = random.randint(0,360)

    CATIA = win32com.client.Dispatch("CATIA.Application")
    documents1 = CATIA.Documents
    partDocument1 = documents1.Add("Part")
    part1 = partDocument1.Part

    try:
        extra_edge_cuts(i,documents1,partDocument1,part1,p8arr,ex1, "eec",noh,rh,posH,csys)
    except:
        print("number "+str(i)+" not finished, error")

        ee = ee + 1
        if ee > 500:
            break
    
    partDocument1.Close()

    i = i + 1

'''

def stiffened_panel(
                    csys,documents1,partDocument1,part1,I,                                                   #iteration
                    xmax = 1000,ymax =2000,no_stringer =2,t = 3, ts =2,  #overall panel
                    str_h = 50, str_w = 100,                             #stringer details
                    rh = 3, noh = 10,                                     #holes
                    b2 = 0.01, a2=0.01,e2=100,d2=1.25,c2=0,              #edge 2 para
                    b1 = 0, a1 = 0, e1 = 0, d1= 0, c1= 0                #edge 1 para
                    ):
    

    #eventually add two more curves for the other 2 edges
    #this will need to take account for elevated points
    #these would be the guide curves for loft

    #Setting up CATIA modelling environment
    #CATIA = win32com.client.Dispatch("CATIA.Application")
    #record deletion of product....

    #documents1 = CATIA.Documents
    #partDocument1 = documents1.Add("Part")
    #part1 = partDocument1.Part
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
    
    directions = [dirX,dirY,dir1]



    #definition for solid geometries
    SF = part1.ShapeFactory
    bodies5 = part1.Bodies
    body5 = bodies5.Item("PartBody")
    part1.InWorkObject = body5

    #creating reference (no-radii) body
    bodies1 = part1.Bodies
    body10 = bodies1.Item("PartBody")

    bodies1 = part1.Bodies
    body5 = bodies1.Add()
    body5.Name="first"

    part1.InWorkObject = body5
    SF = part1.ShapeFactory
    ref1 = part1.CreateReferenceFromName("")
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

    part1.Update()

    
    path2 = "D:\\CAD_library_sampling\\sample62\\"
    path3 = "D:\\CAD_library_sampling\\sample62\\no_curves\\"
    #save version without holes and output empty notepad
    partDocument1.SaveAs(path3+"SP_"+str(I)+".catpart")
    partDocument1.ExportData(path3+"SP_"+str(I)+".stp", "stp")
    ver_list1 = vertex_list("D:\CAD_library_sampling\sample62\\no_curves\\SP_"+str(I)+".stp")

    #hide excess geometry
    selection1 = partDocument1.Selection
    selection1.Clear()
    visPropertySet1 = selection1.VisProperties
    selection1.Add(body5)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)

    #creating reference (no-radii) body
    bodies1 = part1.Bodies
    body10 = bodies1.Item("PartBody")

    bodies1 = part1.Bodies
    body5 = bodies1.Add()
    body5.Name="second"

    part1.InWorkObject = body5
    SF = part1.ShapeFactory
    ref1 = part1.CreateReferenceFromName("")
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

        i = i + 1

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

    part1.Update()

    #save version with holes
    partDocument1.SaveAs(path2+"SP_"+str(I)+".catpart")
    partDocument1.ExportData(path2+"SP_"+str(I)+".stp", "stp")
    ver_list2 = vertex_list("D:\CAD_library_sampling\sample62\SP_"+str(I)+".stp")

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

    with open(path2+"SP_"+str(I)+"_metadata.txt", "a") as text_file:
        text_file.write(stre)


    #partDocument1.Close()

'''
import random
I = 4880
ee = 0
while I < 6500:
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

    #csys
    csys = [0,0,0,0,0,0]
    csys[0] = random.randint(0,2000)
    csys[1] = random.randint(0,2000)
    csys[2] = random.randint(0,2000)
    csys[3] = random.randint(0,360)
    csys[4] = random.randint(0,360)
    csys[5] = random.randint(0,360)

    CATIA = win32com.client.Dispatch("CATIA.Application")
    documents1 = CATIA.Documents
    partDocument1 = documents1.Add("Part")
    part1 = partDocument1.Part
    try:
        stiffened_panel(csys,documents1,partDocument1,part1,I,xmax,ymax,no_stringer,t,ts,str_h,str_w,rh,noh,
                    a1=a1,a2=a2,b1=b1,b2=b2,c1=c1,c2=c2,d1=d2,e1=e1,e2=e2)
    except:
        print("number "+str(I)+" not finished, error")

        ee = ee + 1
        if ee > 500:
            break

    partDocument1.Close()
    I = I + 1


'''




def pocket(i,sample_name,documents1,partDocument1,part1):
    
    #record deletion of product....
    

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
    
    #csys
    csys = [0,0,0,0,0,0]
    csys[0] = random.randint(0,2000)
    csys[1] = random.randint(0,2000)
    csys[2] = random.randint(0,2000)
    csys[3] = random.randint(0,360)
    csys[4] = random.randint(0,360)
    csys[5] = random.randint(0,360)
    
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
    
    directions = [dirX,dirY,dir1]

    #solid
    #definition for solid geometries
    SF = part1.ShapeFactory
    bodies5 = part1.Bodies
    body5 = bodies5.Item("PartBody")
    part1.InWorkObject = body5



    #creating reference (no-radii) body
    bodies1 = part1.Bodies
    body10 = bodies1.Item("PartBody")

    bodies1 = part1.Bodies
    body5 = bodies1.Add()
    body5.Name="first"

    part1.InWorkObject = body5
    SF = part1.ShapeFactory
    rf00 = part1.CreateReferenceFromName("")

    part1.InWorkObject = body5


    ts1 = SF.AddNewThickSurface(rf00, 0, 1.0000, 0.000000)
    ts1.Surface = rf4
    l1 = ts1.TopOffset
    l1.Value = t
    part1.UpdateObject(ts1)

    part1.Update()
    
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


    part1.Update()


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

    path2 = "D:\\CAD_library_sampling\\sample64\\"
    path3 = "D:\\CAD_library_sampling\\sample64\\no_curves\\"
    #save version without holes and output empty notepad
    partDocument1.SaveAs(path3+"PR_"+str(i)+".catpart")
    partDocument1.ExportData(path3+"PR_"+str(i)+".stp", "stp")
    ver_list1 = vertex_list("D:\\CAD_library_sampling\\sample64\\no_curves\\PR_"+str(i)+".stp")

    #hide excess geometry
    selection1 = partDocument1.Selection
    selection1.Clear()
    visPropertySet1 = selection1.VisProperties
    selection1.Add(body5)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)
  

    bodies1 = part1.Bodies
    body5 = bodies1.Add()
    body5.Name="second"

    part1.InWorkObject = body5
    SF = part1.ShapeFactory
    rf00 = part1.CreateReferenceFromName("")

    part1.InWorkObject = body5


    ts1 = SF.AddNewThickSurface(rf00, 0, 1.0000, 0.000000)
    ts1.Surface = rf4
    l1 = ts1.TopOffset
    l1.Value = t
    part1.UpdateObject(ts1)

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


    part1.Update()

    #save version with holes
    partDocument1.SaveAs(path2+"PR_"+str(i)+".catpart")
    partDocument1.ExportData(path2+"PR_"+str(i)+".stp", "stp")
    ver_list2 = vertex_list("D:\CAD_library_sampling\sample64\PR_"+str(i)+".stp")

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

    with open(path2+"PR_"+str(i)+"_metadata.txt", "a") as text_file:
        text_file.write(stre)

'''
      
ee = 0
i = 0
while i < 10000:

    CATIA = win32com.client.Dispatch("CATIA.Application")
    documents1 = CATIA.Documents
    partDocument1 = documents1.Add("Part")
    part1 = partDocument1.Part

    try:
        pocket(i,"xxxxxx",documents1,partDocument1,part1)
    except:
        print("number "+str(i)+" not finished, error")

        ee = ee + 1
        if ee > 1000:
            break

    partDocument1.Close()  

    i = i +1
'''

from WS_gen_3 import rand_hole
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
'''

#from math_utils import GlobalToLocal
#sampling x
i = 4050
ee = 0
while i < 10000: 

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
        if ee > 300:
            break

    i = i + 1
'''

from WS_gen_3 import rand_hole
def flt_01(i,p8arr,R1,R2,ref,csys,partDocument1):

    #To compensate for CATIA's inability to select edges, the fillet of a singular edge is done in controlled surface manipulation manner

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
    body8 = bodies1.Add()
    body8.Name="Steps"


    # create ground points
    point1=ShFactory.AddNewPointCoord(p8arr[0,0],p8arr[0,1],0)
    body1.AppendHybridShape(point1)
    r11 = part1.CreateReferenceFromObject(point1)

    point1=ShFactory.AddNewPointCoord(p8arr[1,0],p8arr[1,1],0)
    body1.AppendHybridShape(point1)
    r22 = part1.CreateReferenceFromObject(point1)

    point1=ShFactory.AddNewPointCoord(p8arr[2,0],p8arr[2,1],0)
    body1.AppendHybridShape(point1)
    r33 = part1.CreateReferenceFromObject(point1)

    point1=ShFactory.AddNewPointCoord(p8arr[3,0],p8arr[3,1],0)
    body1.AppendHybridShape(point1)
    r44 = part1.CreateReferenceFromObject(point1)


    #connect the points
    lpt = ShFactory.AddNewLinePtPt(r11, r22)
    body1.AppendHybridShape(lpt)
    r5 = part1.CreateReferenceFromObject(lpt)

    lpt = ShFactory.AddNewLinePtPt(r22, r33)
    body1.AppendHybridShape(lpt)
    r6 = part1.CreateReferenceFromObject(lpt)

    lpt = ShFactory.AddNewLinePtPt(r33, r44)
    body1.AppendHybridShape(lpt)
    r7 = part1.CreateReferenceFromObject(lpt)

    lpt = ShFactory.AddNewLinePtPt(r44, r11)
    body1.AppendHybridShape(lpt)
    r8 = part1.CreateReferenceFromObject(lpt)

    #create surface
    hfl = ShFactory.AddNewFill()
    hfl.AddBound(r5)
    hfl.AddBound(r6)
    hfl.AddBound(r7)
    hfl.AddBound(r8)
    hfl.Continuity = 1
    hfl.Detection = 2
    hfl.AdvancedTolerantMode = 2
    body1.AppendHybridShape(hfl)
    r000 = part1.CreateReferenceFromObject(hfl)

    # create ground points
    point1=ShFactory.AddNewPointCoord(p8arr[0,0],p8arr[0,1],p8arr[0,2])
    body1.AppendHybridShape(point1)
    r1 = part1.CreateReferenceFromObject(point1)

    point1=ShFactory.AddNewPointCoord(p8arr[1,0],p8arr[1,1],p8arr[1,2])
    body1.AppendHybridShape(point1)
    r2 = part1.CreateReferenceFromObject(point1)

    point1=ShFactory.AddNewPointCoord(p8arr[2,0],p8arr[2,1],p8arr[2,2])
    body1.AppendHybridShape(point1)
    r3 = part1.CreateReferenceFromObject(point1)

    point1=ShFactory.AddNewPointCoord(p8arr[3,0],p8arr[3,1],p8arr[3,2])
    body1.AppendHybridShape(point1)
    r4 = part1.CreateReferenceFromObject(point1)

    #connect the points
    lpt = ShFactory.AddNewLinePtPt(r1, r2)
    body1.AppendHybridShape(lpt)
    r5 = part1.CreateReferenceFromObject(lpt)

    lpt = ShFactory.AddNewLinePtPt(r2, r3)
    body1.AppendHybridShape(lpt)
    r6 = part1.CreateReferenceFromObject(lpt)

    lpt = ShFactory.AddNewLinePtPt(r3, r4)
    body1.AppendHybridShape(lpt)
    r7 = part1.CreateReferenceFromObject(lpt)

    lpt = ShFactory.AddNewLinePtPt(r4, r1)
    body1.AppendHybridShape(lpt)
    r8 = part1.CreateReferenceFromObject(lpt)

    #create surface
    hfl = ShFactory.AddNewFill()
    hfl.AddBound(r5)
    hfl.AddBound(r6)
    hfl.AddBound(r7)
    hfl.AddBound(r8)
    hfl.Continuity = 1
    hfl.Detection = 2
    hfl.AdvancedTolerantMode = 2

    body1.AppendHybridShape(hfl)
    r100 = part1.CreateReferenceFromObject(hfl)

    lpt = ShFactory.AddNewLinePtPt(r33, r3)
    body1.AppendHybridShape(lpt)
    r10 = part1.CreateReferenceFromObject(lpt)

    lpt = ShFactory.AddNewLinePtPt(r22, r2)
    body1.AppendHybridShape(lpt)
    r11 = part1.CreateReferenceFromObject(lpt)

    #background surface attempt
    p3 = ShFactory.AddNewPlane3Points(r3, r33, r4)
    body1.AppendHybridShape(p3)
    r115 = part1.CreateReferenceFromObject(p3)
    p3 = ShFactory.AddNewPlane3Points(r2, r22, r1)
    body1.AppendHybridShape(p3)
    r116 = part1.CreateReferenceFromObject(p3)

    #Radii done inside CATIA using vba -- error causing CATIA to complain for no reason

    with open("D:\\CoSinC_WP4.2\\temp\\AID1.txt", "r") as text_file:
        tf = text_file.read()
        pa1 = tf.split("(reference1,")[0]
        pa2 = "(reference1, reference2, Nothing,"+str(R1)+", 1, 1)"
        pa3 = tf.split(" 1, 1)")[1]
        stre = pa1 + pa2 + pa3

    with open("C:\\Users\\jakub.kucera\\AppData\\Local\\Temp\\AID1.catvbs", "w") as text_file:
   
        text_file.write(stre) 

    with open("D:\\CoSinC_WP4.2\\temp\\AID2.txt", "r") as text_file:
        tf = text_file.read()
        pa1 = tf.split("(reference1,")[0]
        pa2 = "(reference1, reference2, Nothing,"+str(R2)+", 1, -1)"
        pa3 = tf.split(" 1, -1)")[1]
        stre = pa1 + pa2 + pa3

    with open("C:\\Users\\jakub.kucera\\AppData\\Local\\Temp\\AID2.catvbs", "w") as text_file:
   
        text_file.write(stre)

    CATIA.StartCommand('AID1.catvbs')
    time.sleep(0.5)
    CATIA.StartCommand('AID2.catvbs')

    time.sleep(0.5)
    part1.Update()

    hs1 = body1.HybridShapes
    c = hs1.Item("Circle.1")
    r12 = part1.CreateReferenceFromObject(c)

    c = hs1.Item("Circle.2")
    r13 = part1.CreateReferenceFromObject(c)

    poc = ShFactory.AddNewPointOnCurveFromPercent(r12, 0.000000, False)
    body1.AppendHybridShape(poc)
    r14 = part1.CreateReferenceFromObject(poc)

    poc = ShFactory.AddNewPointOnCurveFromPercent(r13, 0.000000, False)
    body1.AppendHybridShape(poc)
    r15 = part1.CreateReferenceFromObject(poc)

    poc = ShFactory.AddNewPointOnCurveFromPercent(r12, 1.000000, False)
    body1.AppendHybridShape(poc)
    r16 = part1.CreateReferenceFromObject(poc)

    poc = ShFactory.AddNewPointOnCurveFromPercent(r13, 1.000000, False)
    body1.AppendHybridShape(poc)
    r17 = part1.CreateReferenceFromObject(poc)

    #GUIDES
    lpt = ShFactory.AddNewLinePtPt(r14, r15)
    body1.AppendHybridShape(lpt)
    r18 = part1.CreateReferenceFromObject(lpt)

    lpt = ShFactory.AddNewLinePtPt(r16, r17)
    body1.AppendHybridShape(lpt)
    r19 = part1.CreateReferenceFromObject(lpt)

    proj = ShFactory.AddNewProject(r19, r100)
    proj.SolutionType = 0
    proj.Normal = True
    proj.SmoothingType = 0
    proj.ExtrapolationMode = 0
    body1.AppendHybridShape(proj)
    r19 = part1.CreateReferenceFromObject(proj)

    #lof for cutting fillets 
    L = ShFactory.AddNewLoft()
    L.SectionCoupling = 1
    L.Relimitation = 1
    L.CanonicalDetection = 2
    L.AddGuide(r18)
    L.AddGuide(r19)
    L.AddSectionToLoft(r12, 1, None)
    L.AddSectionToLoft(r13, 1, None)
    body1.AppendHybridShape(L)
    r300 = part1.CreateReferenceFromObject(L)

    part1.Update()

    #hide n seek
    selection1 = partDocument1.Selection
    selection1.Clear()
    visPropertySet1 = selection1.VisProperties
    selection1.Add(body1)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)
    part1.Update()

    #direction ref
    OE = part1.OriginElements
    hspe = OE.PlaneXY
    ref1111 = part1.CreateReferenceFromObject(hspe)
    dir1 = ShFactory.AddNewDirection(ref1111)


    #cut the extrude
    SF = part1.ShapeFactory
    bodies5 = part1.Bodies
    body5 = bodies5.Item("PartBody")
    part1.InWorkObject = body5
    ref1 = part1.CreateReferenceFromName("")

    ts1 = SF.AddNewThickSurface(ref1, 0, 1.0000, 0.000000)
    ts1.Surface = r000
    l1 = ts1.TopOffset
    l1.Value = 400
    part1.UpdateObject(ts1)

    #boolean operations required to counteract the split being wrong on default
    bodies1 = part1.Bodies    
    body7 = bodies1.Add()
    part1.InWorkObject = body7
    ref1 = part1.CreateReferenceFromName("")

    ts1 = SF.AddNewThickSurface(ref1, 0, 1.0000, 0.000000)

    ts1.Surface = r000
    l1 = ts1.TopOffset
    l1.Value = 400
    part1.UpdateObject(ts1)

    part1.Update()
    split1 = SF.AddNewSplit(ref1, 0)
    split1.Surface = r100
    part1.Update()
    part1.InWorkObject = body5
    SF.AddNewRemove(body7)
    part1.Update()

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
    
    directions = [dirX,dirY,dir1]

    #rotate translate and whatnot
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

    #save first version of step for later comparison
    #save v1

    path2 = "D:\\CAD_library_sampling\\sample65\\"
    path3 = "D:\\CAD_library_sampling\\sample65\\no_curves\\"
    #save version without holes and output empty notepad
    partDocument1.SaveAs(path3+"FL_"+str(i)+".catpart")
    partDocument1.ExportData(path3+"FL_"+str(i)+".stp", "stp")
    ver_list1 = vertex_list("D:\\CAD_library_sampling\\sample65\\no_curves\\FL_"+str(i)+".stp")

    #create new model
    #hide excess geometry
    selection1 = partDocument1.Selection
    selection1.Clear()
    visPropertySet1 = selection1.VisProperties
    selection1.Add(body5)
    visPropertySet1 = visPropertySet1.Parent
    visPropertySet1.SetShow(1)
  

    #CREATE REF 6
    bodies1 = part1.Bodies
    body6 = bodies1.Add()
    body6.Name="6"

    part1.InWorkObject = body6
    SF = part1.ShapeFactory
    rf00 = part1.CreateReferenceFromName("")
    part1.InWorkObject = body6
    ref1 = part1.CreateReferenceFromName("")

    ts1 = SF.AddNewThickSurface(ref1, 0, 1.0000, 0.000000)
    ts1.Surface = r000
    l1 = ts1.TopOffset
    l1.Value = 400
    part1.UpdateObject(ts1)
    split1 = SF.AddNewSplit(ref1, 0)
    split1.Surface = r100

    part1.Update()

    #CREATE REF 7
    bodies1 = part1.Bodies
    body7 = bodies1.Add()
    body7.Name="7"
    part1.InWorkObject = body7
    ref1 = part1.CreateReferenceFromName("")
    ts1 = SF.AddNewThickSurface(ref1, 0, 1.0000, 0.000000)
    ts1.Surface = r000
    l1 = ts1.TopOffset
    l1.Value = 400
    part1.UpdateObject(ts1)
    SF.AddNewRemove(body6)
    part1.Update()

    #CREATE REF 8
    bodies1 = part1.Bodies
    body8 = bodies1.Add()
    body8.Name="8"
    part1.InWorkObject = body8
    ref1 = part1.CreateReferenceFromName("")
    ts1 = SF.AddNewThickSurface(ref1, 0, 1.0000, 0.000000)
    ts1.Surface = r000
    l1 = ts1.TopOffset
    l1.Value = 400
    part1.UpdateObject(ts1)
    SF.AddNewRemove(body6)
    part1.Update()
    split1 = SF.AddNewSplit(ref1, 0)
    split1.Surface = r300
    part1.Update()
    bodies1 = part1.Bodies
    part1.InWorkObject = body7
    SF.AddNewRemove(body8)
    part1.Update()

    #rotate translate and whatnot
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

    part1.Update()

    #save version with holes
    partDocument1.SaveAs(path2+"FL_"+str(i)+".catpart")
    partDocument1.ExportData(path2+"FL_"+str(i)+".stp", "stp")
    ver_list2 = vertex_list("D:\CAD_library_sampling\sample65\FL_"+str(i)+".stp")

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
    #.txt file for training
    iii = 0
    stre = ""
    alo = []
    while iii < len(diff):
        
        if iii not in alo:
            iv = iii+1
            stre += "\n fll\n"
            stre += str(diff[iii].x)+","+str(diff[iii].y)+","+str(diff[iii].z)+"\n"
            while iv < len(diff):

                stre += str(diff[iv].x)+","+str(diff[iv].y)+","+str(diff[iv].z)+"\n"
                alo.append(iv)
                iv = iv + 1
        iii = iii + 1

    with open(path2+"FL_"+str(i)+"_metadata.txt", "a") as text_file:
        text_file.write(stre)

'''
#from math_utils import GlobalToLocal
#sampling x
i = 393
ee = 0
while i < 6000: 

    #ptn = random.randint(3,5)

    p8arr = np.zeros((4,3))
    #ground points equal in x and y to these points


    #x
    p8arr[0,0] = random.randint(20,200)
    #y
    p8arr[0,1] = random.randint(20,200)
    #z stays 0
    p8arr[0,2] = random.randint(20,200)

    #x
    p8arr[1,0] = random.randint(20,200)*(-1)
    #y
    p8arr[1,1] = random.randint(20,200)
    #z stays 0
    p8arr[1,2] = random.randint(20,200)

    #x
    p8arr[2,0] = random.randint(20,200)*(-1)
    #y
    p8arr[2,1] = random.randint(20,200)*(-1)
    #z stays 0
    p8arr[2,2] = random.randint(20,200)

    #x
    p8arr[3,0] = random.randint(20,200)
    #y
    p8arr[3,1] = random.randint(20,200)*(-1)
    #z stays 0
    p8arr[3,2] = random.randint(20,200)
        

    r1 = random.randint(2,80)/10
    r2 = random.randint(r1*10-1,r1*10+10)/10
    #which point starts fillet
    ref = random.randint(0,4)


    #csys
    csys = [0,0,0,0,0,0]
    csys[0] = random.randint(0,2000)
    csys[1] = random.randint(0,2000)
    csys[2] = random.randint(0,2000)
    csys[3] = random.randint(0,360)
    csys[4] = random.randint(0,360)
    csys[5] = random.randint(0,360)

    #Setting up CATIA modelling environment
    CATIA = win32com.client.Dispatch("CATIA.Application")
    #record deletion of product....

    documents1 = CATIA.Documents
    partDocument1 = documents1.Add("Part")

    try:
        flt_01(i,p8arr,r1,r2,ref,csys,partDocument1)
    except:
        print("number "+str(i)+" not finished, error")
    
        ee = ee + 1
        if ee > 300:
            break
    partDocument1.Close()
    i = i + 1

'''

def flt_02(i,p8arr,csys,partDocument1):
    #just another way to create fillets ? 

    #learning how to use sketches in CATIA - lol


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
    body8 = bodies1.Add()
    body8.Name="Steps"

    #setting up sketches
    bodies1 = part1.Bodies

    body1 = bodies1.Item("PartBody")
    sketches1 = body1.Sketches
    originElements1 = part1.OriginElements
    r0 = originElements1.PlaneYZ
    sketch1 = sketches1.Add(r0)

    #Dim arrayOfVariantOfDouble1(8)
    avd = [0,0,0,0,1,0,0,0,1]

    sketch1.SetAbsoluteAxisData(avd)

    part1.InWorkObject = sketch1

    factory2D1 = sketch1.OpenEdition()

    geometricElements1 = sketch1.GeometricElements

    axis2D1 = geometricElements1.Item("AbsoluteAxis")

    line2D1 = axis2D1.GetItem("HDirection")

    line2D1.ReportName = 1

    line2D2 = axis2D1.GetItem("VDirection")

    line2D2.ReportName = 2

    ii = 0 
    while ii < np.size(p8arr,0):
        #creating points 
        build = "point2D"+str(ii + 1)+" = factory2D1.CreatePoint(p8arr[ii,0], p8arr[ii,1])"
        exec(build)
        build = "point2D"+str(ii + 1)+".ReportName = str(3 + ii)"
        exec(build)
        build = "point2D"+str(ii + 1)+".Construction = False"
        exec(build)

        ii = ii + 1
    #point2D2 = factory2D1.CreatePoint(120.000000, 30.000000)
    #point2D2.ReportName = 4
    #point2D2.Construction = False
    #point2D3 = factory2D1.CreatePoint(-20.000000, 70.000000)
    #point2D3.ReportName = 5
    #point2D3.Construction = False
    #point2D4 = factory2D1.CreatePoint(-70.000000, -30.000000)
    #point2D4.ReportName = 6
    #point2D4.Construction = False
    #point2D5 = factory2D1.CreatePoint(94.053735, -1.712102)
    #point2D5.ReportName = 7
    ii = 0 
    while ii < np.size(p8arr,0):
        if ii != np.size(p8arr,0)-1:
            build = "line2D"+str(ii + 3)+" = factory2D1.CreateLine("+str(p8arr[ii,0])+", "+str(p8arr[ii,1])+", "+str(p8arr[ii+1,0])+", "+str(p8arr[ii+1,1])+")"
        else:
            build = "line2D"+str(ii + 3)+" = factory2D1.CreateLine("+str(p8arr[ii,0])+", "+str(p8arr[ii,1])+", "+str(p8arr[0,0])+", "+str(p8arr[0,1])+")"
        exec(build)
        build = "line2D"+str(ii + 3)+".ReportName = 8"
        exec(build)
        build = "line2D"+str(ii + 3)+".StartPoint = point2D"+str(ii + 1)
        exec(build)
        if ii != np.size(p8arr,0) - 1:
            build = "line2D"+str(ii + 3)+".EndPoint = point2D"+str(ii + 2)
        else:
            build = "line2D"+str(ii + 3)+".EndPoint = point2D1"
        exec(build)
        ii = ii + 1 


    #point2D6 = factory2D1.CreatePoint(80.602548, 41.256415)
    #point2D6.ReportName = 9
    #line2D4 = factory2D1.CreateLine(80.602548, 41.256415, -20.000000, 70.000000)
    #line2D4.ReportName = 10
    #line2D4.StartPoint = point2D6
    #line2D4.EndPoint = point2D3
    #line2D5 = factory2D1.CreateLine(-20.000000, 70.000000, -70.000000, -30.000000)
    #line2D5.ReportName = 11
    #line2D5.StartPoint = point2D3
    #line2D5.EndPoint = point2D4
    #line2D6 = factory2D1.CreateLine(-70.000000, -30.000000, 30.000000, -80.000000)
    #line2D6.ReportName = 12
    #line2D6.StartPoint = point2D4
    #line2D6.EndPoint = point2D1
    #point2D7 = factory2D1.CreatePoint(73.200590, 15.349562)
    #point2D7.ReportName = 13

    '''
    #this will involve creating extra point for circle center... GOD
    ii = 0 
    while ii < np.size(p8arr,0)-1:

        x = (p8arr[ii,5]-p8arr[ii,3])* math.sin(math.pi*(p8arr[ii,4]+ii*(360/ptn))/180)
        y = (p8arr[ii,5]-p8arr[ii,3])* math.cos(math.pi*(p8arr[ii,4]+ii*(360/ptn))/180)

        build = "point2D"+str(ii + np.size(p8arr,0) + 1)+" = factory2D1.CreatePoint(x, y)"
        exec(build)
        build = "point2D"+str(ii + np.size(p8arr,0) + 1)+".ReportName = str(3 + np.size(p8arr,0)+ ii)"
        exec(build)
        build = "point2D"+str(ii + np.size(p8arr,0) + 1)+".Construction = False"
        exec(build)


        build = "circle2D"+str(ii + 1)+" = factory2D1.CreateCircle(73.200590, 15.349562, 26.943534, 5.597456, 7.575682)"
        exec(build)
        build = "circle2D"+str(ii + 1)+".CenterPoint = point2D"+str(ii + np.size(p8arr,0) + 1)
        exec(build)
        build = "circle2D"+str(ii + 1)+".ReportName = 14"
        exec(build)
        build = "circle2D"+str(ii + 1)+".StartPoint = point2D"+str(ii + 3)
        exec(build)
        build = "circle2D"+str(ii + 1)+".EndPoint = point2D"+str(ii + 4)
        exec(build)
        ii = ii + 1
    '''

    point2D7 = factory2D1.CreatePoint(73.200590, 15.349562)

    point2D7.ReportName = 13

    circle2D1 = factory2D1.CreateCircle(73.200590, 15.349562, 26.943534, 5.597456, 7.575682)

    circle2D1.CenterPoint = point2D7

    circle2D1.ReportName = 14

    circle2D1.StartPoint = point2D5

    circle2D1.EndPoint = point2D6

    constraints1 = sketch1.Constraints

    reference2 = part1.CreateReferenceFromObject(line2D3)

    reference3 = part1.CreateReferenceFromObject(point2D2)

    constraint1 = constraints1.AddBiEltCst(catCstTypeOn, reference2, reference3)

    constraint1.Mode = catCstModeDrivingDimension

    reference4 = part1.CreateReferenceFromObject(line2D4)

    reference5 = part1.CreateReferenceFromObject(point2D2)

    constraint2 = constraints1.AddBiEltCst(catCstTypeOn, reference4, reference5)

    constraint2.Mode = catCstModeDrivingDimension

    reference6 = part1.CreateReferenceFromObject(circle2D1)

    reference7 = part1.CreateReferenceFromObject(line2D3)

    constraint3 = constraints1.AddBiEltCst(catCstTypeTangency, reference6, reference7)

    constraint3.Mode = catCstModeDrivingDimension

    reference8 = part1.CreateReferenceFromObject(circle2D1)

    reference9 = part1.CreateReferenceFromObject(line2D4)
    constraint4 = constraints1.AddBiEltCst(catCstTypeTangency, reference8, reference9)

    constraint4.Mode = catCstModeDrivingDimension

    reference10 = part1.CreateReferenceFromObject(circle2D1)

    constraint5 = constraints1.AddMonoEltCst(catCstTypeRadius, reference10)

    constraint5.Mode = catCstModeDrivingDimension

    length1 = constraint5.Dimension

    length1.Value = 26.943534

    sketch1.CloseEdition()

    part1.InWorkObject = body1

    part1.Update 

#WORKING WITH SKETCHES IN CATIA - PYTHON - IS ABSOLUTELY NOT VIABLE !! - NO DOC, RANDOM REFs, RANDOM RECORDING

#from math_utils import GlobalToLocal
#sampling x
i = 0
ee = 0
while i < 1: 

    ptn = random.randint(3,7)

    p8arr = np.zeros((ptn,6))
    #ground points equal in x and y to these points

    ii = 0
    while ii < ptn:
        #Polar definition of point - to have points in appropriate segments
        #ang 
        p8arr[ii,4] = random.randint(0,int(360/ptn))
        #R
        p8arr[ii,5]  = random.randint(50,250)
        #y
        p8arr[ii,1] = p8arr[ii,5]* math.sin(math.pi*(p8arr[ii,4]+ii*(360/ptn))/180)
        #x
        p8arr[ii,0] = p8arr[ii,5]* math.cos(math.pi*(p8arr[ii,4]+ii*(360/ptn))/180)
   
        #chance of radius
        p8arr[ii,2] = random.randint(1,10)

        #trashold for fillet
        if p8arr[ii,2] > 6:
            p8arr[ii,3] = random.randint(1,10)
        ii = ii + 1

    #csys
    csys = [0,0,0,0,0,0]
    csys[0] = random.randint(0,2000)
    csys[1] = random.randint(0,2000)
    csys[2] = random.randint(0,2000)
    csys[3] = random.randint(0,360)
    csys[4] = random.randint(0,360)
    csys[5] = random.randint(0,360)

    #Setting up CATIA modelling environment
    CATIA = win32com.client.Dispatch("CATIA.Application")
    #record deletion of product....

    documents1 = CATIA.Documents
    partDocument1 = documents1.Add("Part")

    #try:
    flt_02(i,p8arr,csys,partDocument1)
    #except:
    #    print("number "+str(i)+" not finished, error")
    # 
    #     ee = ee + 1
    #     if ee > 300:
    #         break
    #partDocument1.Close()
    i = i + 1