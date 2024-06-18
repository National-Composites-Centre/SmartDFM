
import math
import time
import numpy as np

class hole:
    radius = 0
    type = "through_simple"
    #list more options later: throuth_countersunk, through_stepped, partial_simple, partial_countersunk, partial_stepped...
    position = np.asarray([[0,0,0]])
    direction = np.asarray([[0,0,0]])

class flange:
    #One of the largest features available
    def __init__(self, angle = 0, radius =0 ,xyz_limits =np.asarray([[0,0,0],[0,0,0]])):
        self.angle = 0
        self.radius = 0
        self.xyz_limits = np.asarray([[0,0,0],[0,0,0]])
        
class step_edge:
    #edges as defined in step file, belonging to faces
    def __init__(self, ref = 0, vertices = []):
        self.ref = 0
        self.vertices = []
        self.len = 0
    
class step_face:
    #faces as defined in step file
    def __init__(self, ref = 0 ,out_bound_ref = 0 ,edges = [],plane = np.array([0,0,0,0]),circumference = 0):
        self.ref = 0
        self.out_bound_ref = 0
        self.edges = []
        self.plane = np.array([0,0,0,0])
        self.circumference = 0
    
    
class step_vertex:
    #vertices, the lowest level of geometry in step file
    def __init__(self, x = 0,y = 0,z = 0):
        self.x = 0
        self.y = 0
        self.z = 0
    

def hole_data(hole_pos,step_file,report = False):
    #eventually implement types of holes, countersunk etc.... either as input from feature reco. or by logic of nearby circles
    
    #currently works for holes actually modelled in 3D solids

    h = hole()
    #Open defined step file
    with open(step_file, "r") as text_file:
        f = text_file.read()
        fc = f.count("\n")

    #Find the closest "'Axis2P3D" to specified hole position
    dd = 90000
    i = 0 
    while i < fc:       
        line = f.split("\n")[i]
    
         #Initial reference line that corresponds to holes, only works for 3D modelled ones
        if "Circle Axis2P3D" in line:
            #reference to point
            temp1 = line.split("Axis2P3D")[1]
            temp1 = temp1.split("#")[1]
            temp1 = temp1.split(",")[0]

            ii = 0 
            t1 = "#"+str(temp1)+"="
            while ii < fc:
                l2 = f.split("\n")[ii]
                if t1 in l2:
                    #find reference point line
                    temp4 = l2.split("Location',(")[1]
                    x = float(temp4.split(",")[0])
                    y = float(temp4.split(",")[1])
                    temp4 = temp4.split(",")[2]
                    z = float(temp4.split(")")[0])
                    #end local while loop if line found
                    break
                ii = ii + 1
            
            #calculate distance to reference point
            dist = math.sqrt((hole_pos[0,0]-x)**2+(hole_pos[0,1]-y)**2+(hole_pos[0,2]-z)**2)

            #This method is not bullet proof e.g.: in scenario where small hole is placed to large hole, 
            #the small hole centre could be closer to the other holes vertex, than its own centre.

            if dist <= dd:
                #no #3 below add here
                
                ii = 0
                while ii < fc:

                    #below refernces found for the minimal distance circle

                    #reference of the line 
                    temp2 = line.split("=")[0]                    
                    l3 = f.split("\n")[ii]
          
                    if "=CIRCLE" in l3 and temp2 in l3:
                        r = l3.split(temp2)[1]
                        r = r.split(",")[1]
                        r = float(r.split(")")[0])
                        #more will be required for non standard through holes
                        dd = dist

                        #reference of direction (optional)
                        temp3 = line.split("#")[3]
                        temp3 = line.split(",")[0]
                        iii = 0
                        while iii < fc:
                            l4 = f.split("\n")[iii]
                            if "Direction',(" in l4:
                                t5 = l4.split("on',(")[1]
                                xd = float(t5.split(",")[0])
                                yd = float(t5.split(",")[1])
                                t5 = t5.split(",")[2]
                                zd = float(t5.split(")")[0])
                            iii = iii + 1
                        h.radius = r
                        h.position = np.asarray([x,y,z])
                        h.direction = np.asarray([xd,yd,zd])

                        ii = ii  + 9000

                    ii = ii + 1


        i = i + 1
    if report == True:
        print("r:",h.radius)
        print("pos:",h.position)
        print("dir:",h.direction)
        print("type:",h.type)
    return(h)


def flange_data(step_file,pos = None,report = False):
    # first do this for standalone flanges, then expand on flange within part
    
    # to do this method needs to support both
    
    #first, all faces are collected as classes, with attributes of plane, and 3 points
    #(are the step vertices for plane always also the vertices)-- keep this comment for troubleshooting
    with open(step_file, "r") as text_file:
        f = text_file.read()
        fc = f.count("\n")
        
    #Thickness of flange assumed 2 for now.
    #This will require rework to effectively remove side faces for more variable flanges
    th = 2
    
    FACES = []
    i = 0 
    #loops through all lines looking for faces
    while i < fc:
        #split the document into lines for search
        line = f.split("\n")[i]
        
        #When line contains face reference.
        if "ADVANCED_FACE" in line:
            #reference to point of the outbound_surf_ref
            temp1 = line.split("#")[2]
            temp1 = temp1.split(")")[0]
            TEDGE = False
            FACE = step_face()
            FACE.out_bound_ref = int(temp1)
            #reference of the actual face
            t1 = line.split("=")[0]
            t1 = t1.split("#")[1]
            FACE.ref = int(t1)
            
            #adjust reference for follow up search
            temp1 = "#"+temp1+"="
            
            #loop the document again for lines with follow up face reference
            ii = 0
            while ii < fc:
                l1 = f.split("\n")[ii]
                
                #when the outbound reference is found
                if temp1 in l1:
                    t2 = l1.split("#")[2]
                    t2 = t2.split(",")[0]
                    t2 = "#"+t2+"="
                    
                    #loop using the border reference
                    iii = 0
                    while iii < fc:
                        l2 = f.split("\n")[iii]
                        #when the list of edges is found
                        if t2 in l2:
                            #loop through the line based on number of edges
                            c1 = l2.count("#")
                            k = 2
                            
                            while k < c1+1:
                                t3 = l2.split("#")[k]
                                #accomodate for end of line string manipulation
                                if k == c1:
                                    t3 = t3.split(")")[0]
                                else:
                                    t3 = t3.split(",")[0]
                                se = step_edge()
                                se.ref = int(t3)
    
                                t3 = "#"+t3+"="
                                #for each edge
                                iv = 0
                                #oriented edge reference
                                while iv < fc:
                                    l3 = f.split("\n")[iv]
                                    #find edge curve line
                                    if t3 in l3:
                                        t4 = l3.split("#")[2]
                                        t4 = t4.split(",")[0]
                                        t4 = "#"+t4+"="
                                        
                                        v = 0
                                        #for each point referenced on the edge curve
                                        while v < fc:
                                            l4 = f.split("\n")[v]
                                            
                                            if t4 in l4:
                                                c2 = l4.count("#")
                                                #loop through points relevant to edge
                                                yy = 2
                                                while yy < c2+1:
                                                    
                                                    t5 = l4.split('#')[yy]
                                                    t5 = t5.split(",")[0]
                                                    t5_raw = t5
                                                    t5 = "#"+t5+"="
                                                    
                                                    vi = 0
                                                    #initial vertex reference
                                                    while vi < fc:
                                                        l5 = f.split("\n")[vi]
                                                        if t5 in l5 and "VERTEX_POINT" in l5:
                                                            t6 = l5.split('#')[2]
                                                            t6 = t6.split(")")[0]
                                                            t6 = "#"+t6+"="
                                                            
                                                            vii = 0
                                                            #looking for lines with specific x,y,z based on vertex ref.
                                                            while vii < fc:
                                                                l6 = f.split("\n")[vii]
                                                                if t6 in l6:
                                                                    t7 = l6.split("('Vertex',(")[1]
                                                                    
                                                                    #create vertex class
                                                                    sv = step_vertex()
                                                                    #assign coordinates to vertex
                                                                    sv.x = t7.split(",")[0]
                                                                    sv.y = t7.split(",")[1]
                                                                    z = t7.split(",")[2]
                                                                    sv.z = z.split(")")[0]
                                                                    #assing reference to vertex
                                                                    sv.ref = int(t5_raw) 
                                                                    se.vertices.append(sv)                                                  
                                                                vii = vii + 1                                                                                                                               
                                                        vi = vi + 1
                                                    yy = yy + 1
                                            v = v + 1
                                    iv = iv + 1
                                #calculate the distance between vertices
                                se.len = math.sqrt((float(se.vertices[0].x) - float(se.vertices[1].x))**2 +
                                                   (float(se.vertices[0].y) - float(se.vertices[1].y))**2 +
                                                   (float(se.vertices[0].z) - float(se.vertices[1].z))**2)
                                #check if edge is shorter than thickness, if so, do not append face --- this needs to go out of this loop! loop only to collect all data and attributes
                                if se.len < th:
                                    TEDGE = True                                        
                                FACE.edges.append(se)    
                                k = k + 1
                        iii = iii + 1
                ii = ii + 1
                
            #take all the filters out of the main loop, filter separetly - better code! the FACE ==> vertex classification standalone func plx...
                
            #only append FACE if FACE is not thickness related
            if TEDGE == False:
                
                if len(FACE.edges) == 4:
                   
                    V1 = np.asarray([[float(FACE.edges[0].vertices[0].x), float(FACE.edges[0].vertices[0].y), float(FACE.edges[0].vertices[0].z)],
                                     [float(FACE.edges[0].vertices[1].x), float(FACE.edges[0].vertices[1].y), float(FACE.edges[0].vertices[1].z)],
                                     [float(FACE.edges[1].vertices[0].x), float(FACE.edges[1].vertices[0].y), float(FACE.edges[1].vertices[0].z)]])
                    #check if 2nd edge point is the same as one of the first:
                    
                    e = 0
                    while (V1[0,:] == V1[2,:]).all() or (V1[1,:] == V1[2,:]).all():
                        
                        V1[2,:] = np.asarray([float(FACE.edges[e].vertices[1].x), float(FACE.edges[e].vertices[1].y), float(FACE.edges[e].vertices[1].z)])
                        e = e + 1         
                                    
                    #notes from below the else.....
                    #find plane equation
                    v1 = np.asarray([V1[0,0]-V1[1,0],V1[0,1]-V1[1,1],V1[0,2]-V1[1,2]])
                    v2 = np.asarray([V1[0,0]-V1[2,0],V1[0,1]-V1[2,1],V1[0,2]-V1[2,2]])
                    x_v1v2 = [v1[1]*v2[2]-v1[2]*v2[1], v1[2]*v2[0]-v1[0]*v2[2], v1[0]*v2[1]-v1[1]*v2[0]]

                    d = -V1[0,:].dot(x_v1v2)
                    
                    pd = np.asarray([x_v1v2[0],x_v1v2[1],x_v1v2[2],d])
                    #print(pd)
                    
                    #second of the same calculation with different point for comparison
                    
                    V1 = np.asarray([[float(FACE.edges[3].vertices[0].x), float(FACE.edges[3].vertices[0].y), float(FACE.edges[3].vertices[0].z)],
                                     [float(FACE.edges[3].vertices[1].x), float(FACE.edges[3].vertices[1].y), float(FACE.edges[3].vertices[1].z)],
                                     [float(FACE.edges[0].vertices[0].x), float(FACE.edges[0].vertices[0].y), float(FACE.edges[0].vertices[0].z)]])
                    #check if 2nd edge point is the same as one of the first:
                    
                    e = 0
                    while (V1[0,:] == V1[2,:]).all() or (V1[1,:] == V1[2,:]).all():
                        
                        V1[2,:] = np.asarray([float(FACE.edges[e].vertices[1].x), float(FACE.edges[e].vertices[1].y), float(FACE.edges[e].vertices[1].z)])
                        e = e + 1         
                                    
                    #notes from below the else.....
                    #find plane equation
                    v1 = np.asarray([V1[0,0]-V1[1,0],V1[0,1]-V1[1,1],V1[0,2]-V1[1,2]])
                    v2 = np.asarray([V1[0,0]-V1[2,0],V1[0,1]-V1[2,1],V1[0,2]-V1[2,2]])
                    x_v1v2 = [v1[1]*v2[2]-v1[2]*v2[1], v1[2]*v2[0]-v1[0]*v2[2], v1[0]*v2[1]-v1[1]*v2[0]]

                    d = -V1[0,:].dot(x_v1v2)
                    
                    pd2 = np.asarray([x_v1v2[0],x_v1v2[1],x_v1v2[2],d])
                    #print(pd2)          
                    
                    ch1 = pd-pd2
                    ch2 = pd+pd2
                    
                    if (-0.0001 < ch1.all() < 0.0001) or (-0.0001 < ch2.all() < 0.0001) :
                        #plane verified by 2 calculations
                        #print("plane flat confirmed")
                        FACE.plane = pd
                    else:
                        print("face plane is not flat, or ... bug")
                        
                    #assume 4 edges for now...
                    FACE.circumference = float(FACE.edges[0].len)+float(FACE.edges[1].len)+float(FACE.edges[2].len)+float(FACE.edges[3].len)
                    
                    
                    #comparison plane calculation
                    
                    
                else:
                    print("the face does not have 4 edges, is this an issue?")
                
                #(check that 4 edges surface)
                
                #find 3 unique vertices from the edges
                
                #calculate plane
                
                #find 3 other unique vertices from edges
                
                #check that both equations above are pretty much the same
                
                #if they are not, print error, if they are add attribute np.() to FACE
                
                FACES.append(FACE)
                
        
            
        i = i + 1
        

    i = 0
    mm = 0
    while i < len(FACES):
        
        if float(FACES[i].circumference) > mm:
            mm = float(FACES[i].circumference)
                       
        i = i + 1

    i = 0
    while i < len(FACES):
        if FACES[i].circumference < 0.5*mm:
            del FACES[i]
            #deleting faces which are significantly smaller than the most prominent surfaces
        i = i + 1
             
                       
    angs = []
    i = 0
    while i < len(FACES)-1:
        ii = i + 1
        while ii < len(FACES):
            
            plane1 = FACES[i].plane
            plane2 = FACES[ii].plane
            plane1 = plane1[0:3]

            plane2 = plane2[0:3]

            ang = np.arccos(np.dot(plane1, plane2) / (np.linalg.norm(plane1) * np.linalg.norm(plane2)))
            #work in degrees:
            ang = ang*180/math.pi
            #for now angles smaller than 2 just dont count... 
            #print(ang)
            if 2 < ang < 178:
                round(ang,2)
                angs.append(ang)
            ii = ii + 1
            
        i = i + 1
        
    maxlegal = max(angs)

    
    for i in angs:
        diff = abs(maxlegal) - abs(i)
        if  -1 < diff < 1:
            sm = maxlegal + i
            if 179 < sm < 181:
                print("what the hell is angle ", i ," doing here")
    
    print("flange angle is:", maxlegal) 
    return(maxlegal)

    #Expansions:::::
    
    #filter for vertices that belong to flange (pointless in initial version) !!
    
    

#step_file ="D:\CAD_library_sampling\s-5045.stp"
#pos = np.asarray([[5.4,0,11.5]])
#h1 = hole_data(pos,step_file,report = True)

step_file = "D:\CoSinC_WP4.2\TestCad\s-5029.stp"
pos = np.asarray([[-93.8378515949,-108.148991802,0.], 
                  [-93.8378515949,-108.148991802,1.37573544736 ],
                  [-93.8378515949,107.016864435,1.37573544736 ],
                  [-93.8378515949,107.016864435,0. ],
                  [93.8378515949,-108.148991802,0. ],
                  [93.8378515949,-108.148991802,1.37573544736 ],
                  [93.8378515949,107.016864435,1.37573544736 ],
                  [93.8378515949,108.529941194,1.74047061358 ],
                  [-93.8378515949,108.529941194,1.74047061358 ],
                  [-93.8378515949,109.156774038,0.515836543174 ],
                  [93.8378515949,107.016864435,0. ],
                  [93.8378515949,109.156774038,0.515836543174 ],
                  [93.8378515949,300.690283508,98.5528726074 ],
                  [93.8378515949,300.063450664,99.7775066778 ],
                  [-93.8378515949,300.690283508,98.5528726074 ],
                  [-93.8378515949,300.063450664,99.7775066778 ]])

f1 = flange_data(step_file,pos,report = True)
    