

import numpy as np
from numpy.linalg import norm
from CATIA_utils import hole_loc
import math
import time


def dd(p1,p2,p3):
    #distance between pt1-pt2 vector to pt3
    if norm(p2-p1) == 0:
        print(p2)
        print(p1)
        print("0 error")
    d = norm(np.cross(p2-p1, p1-p3))/norm(p2-p1)
    
    #to account for limits on the vector 
    #calcualte the angles p3-p2-p1 and p3-p1-p2
    #if either is more than 90, closest point is p1 or p2
    #(yes, the next 20 lines accomodate for this...)
    
    vector1 = p1-p2
    vector2 = p3-p2
    vector3 = p3-p1
    vector4 = p2-p1

    vector1 = [vector1[0,0], vector1[0,1],vector1[0,2]]
    vector2 = [vector2[0,0], vector2[0,1],vector2[0,2]]
    vector3 = [vector3[0,0], vector3[0,1],vector3[0,2]]
    vector4 = [vector4[0,0], vector4[0,1],vector4[0,2]]
    
    unit_vector1 = vector1 / np.linalg.norm(vector1)
    unit_vector2 = vector2 / np.linalg.norm(vector2)

    dot_product = np.dot(unit_vector1, unit_vector2)

    angle1 = np.arccos(dot_product) #angle in radian
    
    unit_vector1 = vector4 / np.linalg.norm(vector4)
    unit_vector3 = vector3 / np.linalg.norm(vector3)

    dot_product = np.dot(unit_vector1, unit_vector3)

    angle2 = np.arccos(dot_product) #angle in radian   
    
    angle1 = angle1/math.pi*180
    angle2 = angle2/math.pi*180
    
    if min(angle1,angle2) < 0 or max(angle1,angle2) > 90:
        d1 = math.sqrt((p1[0,0]-p3[0,0])**2+(p1[0,1]-p3[0,1])**2+(p1[0,2]-p3[0,2])**2)
        d2 = math.sqrt((p2[0,0]-p3[0,0])**2+(p2[0,1]-p3[0,1])**2+(p2[0,2]-p3[0,2])**2)
        d = min(d1,d2)
    return(d)


#optional inputs:
    #VER - see below --option of providing in source file (from my data) or another?
    #r = radius of the hole (allows for automated removal of hole geometry)
    
    
#Notes and limitations
    #all neighbouring holes need to be listed as input, otherwise they show as other edges
        #hole to hole distance can therefore easily be implemented

#source vertices (this should be an input here)
#ED2 doest check if the vertices used for edges belogn to the correct shape, ED does

def ED(hole_points,stp_file, hole_rad, VER = None):
    
    #hole points matrix required
    # - can be specified as list of points
    # - can be specified as catPart with "holes" gemetrical set
    #.stp file required
    
    #radius required when hole fully modelled and VER = None
    #if type(hole_points) is str:
    #    if ".CatPart" in hole_points:
    #        #translates CATIA reference hole_points into matrix of hole_points
    #        hole_points = hole_loc(hole_points)

    #Is this now duplicated? Pre-rules already takes hole positions using CATIA...
    
    with open(stp_file, "r") as text_file:
        f = text_file.read()
        fc = f.count("\n")
        #print(fc)
    md = 99999999999  
    d = md + 1 #just sligtly higher until first calc. comes through
    f1 = 0 
    while f1 < fc:
        st118 = time.time()
        
        line = f.split("\n")[f1]
    
        #if parent vertices are provided, only the associated edges are considered
        if VER == None:
            #when no parent vertices are provided all edges are condsidered
            b1 = True
            b2 = True
        else:
            b1 = False
            b2 = False
        #go through all "EDGE_CURVE" lines in the appropriate stl
        if "EDGE_CURVE" in line:
            #extract all references linked, and count how many are listed
            tp = line.split("=")[1]
            c = tp.count('#')

            i = 0 
            j = 0
            #for all references in the Edge_Curve line
            while i < c:
                #adjust the reference for searcheability
                no1 = tp.split("#")[i+1]
                no1 = no1.split(',')[0]
                ex = "#"+no1+"="
                
                f2 = 0
                #loop through document again, finding the reference
                while f2 < fc:
                    l = f.split("\n")[f2]
                    #for l in text_file:
                    if ex in l:
                        #only interested in "VERTEX_POINT" references
                        if "VERTEX_POINT" in l:
                            ex2 = l.split("#")[2]
                            ex2 = ex2.split(")")[0]
                            ex2 = '#'+ex2+"="
                            f3 = 0
                            #find the listed vertex
                            while f3 < fc:
                                l2 = f.split("\n")[f3]
                                
                                if ex2 in l2:
                                    #turn obtained vertex into x,y,z
                                    ex3 = l2.split("""('Vertex',(""")[1]
                                    ex3 = ex3.split("))")[0]
                                    x = float(ex3.split(",")[0])
                                    y = float(ex3.split(",")[1])
                                    z = float(ex3.split(",")[2])
                                    
                                    #if VER parent part vertices are provided
                                    if VER != None:
                                        #find if the edge belongs to the parent
                                        ii = 0
                                        while ii < np.size(VER,0):
                                            #only consider the vertices that belong to parent geometry
                                            if x == VER[ii,0] and y == VER[ii,1] and z == VER[ii,2]:
                                                j = j + 1
                                                if b1 == False:
                                                    b1 = True
                                                else:
                                                    b2 = True
                                            ii = ii + 1
                                    #if the hole rad is specified, hole geometry can be automatically excluded
                                    if hole_rad != 0:
                                        
                                        ii = 0 
                                        while ii < np.size(hole_points, 0):
                                            xmax = hole_points[ii,0] + hole_rad*1.2 # 1.0 does not always cut it 
                                            ymax = hole_points[ii,1] + hole_rad*1.2
                                            zmax = hole_points[ii,2] + hole_rad*1.2
                                            xmin = hole_points[ii,0] - hole_rad*1.2
                                            ymin = hole_points[ii,1] - hole_rad*1.2
                                            zmin = hole_points[ii,2] - hole_rad*1.2
                                            if xmin < x < xmax and ymin < y < ymax and zmin < z < zmax :
                                                b1 = False
                                                b2 = False                                  
                                            ii = ii + 1
                                    
                                    j = j + 1
                                f3 = f3 + 1
                            if j == 1:
                                jm = np.matrix([[x,y,z]])
                            elif j > 1:
                                jm = np.concatenate((jm,np.matrix([[x,y,z]])),axis=0)
                        if j > 1:
                            #accounts for b-splines 
                            #currently not really working
                            #should be segmenting b-splines for closer vectors to the actual- definition of b-spline weird
                            if ("B_SPLINE_CURVE_WITH_KNOTS" in l):
                                
                                #go through the hashes under b-spline
                                c2 = l.count('#')
                                #print(c2)
                                #add rows to jm at the second to last position
                                ii = 1
                                while ii < c2:
                                    ex2 = l.split("#")[ii+1]
                                    ex2 = ex2.split(",")[0]
                                    ex2 = ex2.split(")")[0]
                                    ex2 = '#'+ex2+"="
                                    #print(ex2)
                                    f3 = 0
                                    #find the listed coordinate point
                                    while f3 < fc:
                                        l2 = f.split("\n")[f3]

                                        #add middle points of b-spline 
                                        #These are somewhat offset - need to review ISO-10303-21 to figure out 
                                        if (ex2 in l2) and ("Control Point" in l2):
                                            ex3 = l2.split(",(")[1]
                                            ex3 = ex3.split("))")[0]
                                            x = float(ex3.split(",")[0])
                                            y = float(ex3.split(",")[1])
                                            z = float(ex3.split(",")[2])  
                                            jm = np.insert(jm, np.size(jm,0)-1, np.array((x,y,z)), 0)  
                                        f3 = f3 +1
                                    ii = ii + 1
                              
                    f2 = f2 + 1                        
                i = i + 1
            if b1 == True and b2 == True:
                #find distance between vector and point ...
                iii = 0
                
                while iii < np.size(hole_points,0):
                    iv = 0 
                    while iv < np.size(jm,0)-1:
                        p1 = np.matrix([jm[iv,0], jm[iv,1],jm[iv,2]])
                        p2 = np.matrix([jm[iv+1,0], jm[iv+1,1],jm[iv+1,2]])
                        p3 = np.matrix([hole_points[iii,0], hole_points[iii,1],hole_points[iii,2]])
                        #finds the closest distance to the vector, but takes
                        #into account the points limits 
                        v = math.sqrt((p2[0,0]-p1[0,0])**2+(p2[0,1]-p1[0,1])**2+(p2[0,2]-p1[0,2])**2)
                        #neglects edges smaller than 1 mm
                        if v > 1:
                            d = dd(p1,p2,p3)
                        iv = iv + 1
                        if d < md:
                            md = d
                    iii = iii + 1       
        f1 = f1 + 1  
        #print("line "+str(f1)+" decomposition took:"+str(time.time()-st118)+" seconds")
    print(md)
    
#pts can be imported from a file
#pts can be read from CATIA if dedicated hole part is created
#the parts need not to have actual holes
#pts = np.matrix([[40,6.532,16.01],
#                [40,11.48,46.6]])
#file = "D:\\CAD_library_sampling\\edgeD\\s-w2.stp"

#catPart = "D:\\CAD_library_sampling\\edgeD\\s-w2.CatPart"
#ED(catPart,file,hole_rad = 2) 
    
