#ply by ply modelling from standard layup definition
#currently using CATIA to create the solids.... how hard elsewhere?


import win32com.client.dynamic
import numpy as np

#got through each spline, start to finish

#create number of offsets equivalent to the number of layers 

def pbp_solids(filename):
    #Takes a layup file and generates splines and points in CATIA
    #CATIA start
    CATIA = win32com.client.Dispatch("CATIA.Application")
    partDocument2 = CATIA.ActiveDocument
    part1 = partDocument2.Part
    HSF = part1.HybridShapeFactory
    hbs = part1.HybridBodies

    b1 = hbs.Item("main_shape")
    hs1 = b1.HybridShapes
    hss1 = hs1.Item("MainS")
    ref1 = part1.CreateReferenceFromObject(hss1)
    
    # Adding new body to part1
    body2 = hbs.Add()
    # Naming new body as "wireframe"
    body2.Name="pbp_build"

    #read the file
    with open(filename+".txt", "r") as text_file:
        f = text_file.read()

    w = f.split("[LAMINATE]")[1]
    w = w.split("[MATERIALS]")[0]
    spls = w.split('\n')[2]
    spls = spls.replace("[","")
    spls = spls.replace("]","")
    #print(spls)
    cnt = spls.count(",")
    #print(cnt)
    i = 1 
    while i < cnt+1:

        #adjust the offset value based on thickness

        hybridShapeOffset1 = HSF.AddNewOffset(ref1, i, False, 0.010000)
        body2.AppendHybridShape(hybridShapeOffset1)
        hybridShapeOffset1.Name = "off"+str(i)
        i = i + 1

    for l in spls.split(","):

        ll = f.split("[SPLINES]")[1]
        ls = l.replace("'","")
        if ls == 'f':
            ll = ll.split("[EDGE SPLINE]")[1]
        else:
            ll = ll.split(ls)[1]

        ll = ll.split("\n\n")[0]

        pt_list = np.asarray([[0,0,0]])
        ln = 0
        for n,ii in enumerate(ll.split("\n")):

            if n != 0:
                x = float(ii.split()[0])
                y = float(ii.split()[1])
                z = float(ii.split()[2])

                pt_list = np.concatenate((pt_list, np.asarray([[x,y,z]])),axis=0)
        pt_list = np.delete(pt_list,0,axis=0)
        print(pt_list)

        i = 0
        while i < np.size(pt_list,0):
            #based on notes below 

            i = i + 1

        


pbp_solids("D:\\CoSinC_WP4.2\\TestCad\\X\\x_test_4")

#for each spline'

    #for each spline point
    
    #find the if inside or ouside previous splines, sum of splines choses offset
    #based on this find the offset on which to project the point


    #transitions?? when next point on higher offset, change this point to average of previous and future


    #experiment with fitting surface....



    #adjust what the top layer is 