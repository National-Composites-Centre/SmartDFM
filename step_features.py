import math
import time
import numpy as np
from step_utils import step_reclassification, circ_reclass, step_circle
from time import perf_counter
from fact_base import hole

    

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
    

def hole_data(h,step_file,report = False):
    #eventually implement types of holes, countersunk etc.... either as input from feature reco. or by logic of nearby circles
    
    #currently works for holes actually modelled in 3D solids

    
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
            dist = math.sqrt((h.position[0]-x)**2+(h.position[1]-y)**2+(h.position[2]-z)**2)

            #This method is not bullet proof e.g.: in scenario where small hole is placed close to large hole, 
            #the small hole centre could be closer to the other holes vertex, than its own centre.

            if dist <= dd:

                
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
                        

                        #reference of direction (optional)
                        temp3 = line.split("#")[3]
                        temp3 = line.split(",")[0]
                        #not sure why unused? -- check that extraction below is correct?
                        
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

                        #if the two distances are the same assume co-centric circles and take smaller one
                        if abs(dist-dd) < 2:
                            #if new radius is smaller, then replace 
                            if r < h.radius:
                                dd = dist
                                h.radius = r
                        else:
                            dd = dist
                            h.radius = r
                        #h.position = np.asarray([x,y,z]) # position already known
                        h.direction = np.asarray([xd,yd,zd])

                        ii = ii  + 9000

                    ii = ii + 1


        i = i + 1
    if report == True:
        print("r:",h.radius)
        print("pos:",h.position)
        print("dir:",h.direction)
        print("type:",h.type)


    #not sure if direction correct .... verify
    return(h)

#from fact_base import FactBase, layup
#d =  FactBase()
#d.part_name = "D:\CoSinC_WP4.2\TestCad\X\x_ufo_1.catpart"
#ptemp = values['-IN2-']
#ptemp = ptemp.replace("/","\\")+"\\"
#d.path = ptemp
#hole_data(d,d.step_file,report = True)


def flange_data(step_file,pos = None,report = False):
    # first do this for standalone flanges, then expand on flange within part
    
    # to do this method needs to support both
    
    #first, all faces are collected as classes, with attributes of plane, and 3 points
    #(are the step vertices for plane always also the vertices)-- keep this comment for troubleshooting
    #with open(step_file, "r") as text_file:
    #    f = text_file.read()
    #    fc = f.count("\n")
        
    FACES = step_reclassification(step_file) 
    #print(len(FACES))

    #Thickness of flange assumed 2 for now.
    #This will require rework to effectively remove side faces for more variable flanges
    th = 5
    
    
    #only include faces that belong to pos list if it is available
    isin = True

    deletions = []
    if type(pos) != type(None):
        for i, F in enumerate(FACES):
            #check if all vertices relevant for a face are in pos list
            for ii, E in enumerate(F.edges):
                for iii, V in enumerate(E.vertices):
                    iv = 0
                    isin = False
                    while iv < np.size(pos,0):
                        
                        x = float(V.x)
                        y = float(V.y)
                        z = float(V.z)
                        
                        if -0.1 < (x - pos[iv,0]) < 0.1 and -0.1 < (y - pos[iv,1]) < 0.1 and -0.1 < (z - pos[iv,2]) < 0.1:
                            isin = True
                            #print("verified vertex for face:",i)
                            
                        iv = iv + 1
                    
                    #interupt iteration through vertices if one is not on list
                    if isin == False:
                        #vertex was not found on the list
                        deletions.append(i)
                        break
                #interup iteration through edges if one vertex is not in
                if isin == False:
                    break
  
    cnt = len(deletions)-1
    while cnt >= 0:
        del FACES[deletions[cnt]]
        cnt = cnt - 1
    
    #print(len(FACES)," after adjusting for reference nodes")
    
    i = 1
    while i == 1: 
        #i forces recheck in case FACES were missed due to renumbering
        i = 0
        for face in FACES:
            for edge in face.edges:
                if edge.len < th:
                    FACES.remove(face)
                    i = 1
                    break
                
    #print(len(FACES)," after removing thickness faces")

    #change the 4 below to "for" loops, should be ezy
    
    #finding the largest circumference 
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
    #print(len(FACES)," after removing relatively small faces")
                       
    angs = []
    i = 0
    maxlegal = 0
    while i < len(FACES)-1:
        ii = i + 1
        while ii < len(FACES):
            
            plane1 = FACES[i].plane
            plane2 = FACES[ii].plane
            plane1 = plane1[0:3]
            plane2 = plane2[0:3]
            try:
                ang = np.arccos(np.dot(plane1, plane2) / (np.linalg.norm(plane1) * np.linalg.norm(plane2)))
            except RuntimeWarning:
                print("runtime error TShoot: plane1: "+plane1+" plane2: "+plane2)
            #work in degrees:
            ang = ang*180/math.pi
            #for now angles smaller than 2 just dont count... 
            #print(ang)
            if 2 < ang < 178:
                round(ang,2)
                angs.append(ang)
                if abs(ang) > maxlegal:
                    maxlegal = abs(ang)
                    f1 = i
                    f2 = ii
                    
            ii = ii + 1
            
        i = i + 1
        
    
    #temporary troubleshooting show faces in CATIA
    #from CATIA_utils import check_faces
    #check_faces(FACES)
    

    
    for i in angs:
        diff = abs(maxlegal) - abs(i)
        if  -1 < diff < 1:
            sm = maxlegal + i
            if 179 < sm < 181:
                print("angle ", i ," is not supposed to be here, is it?")
                
              
    #run circle util
    CIRCs = circ_reclass(step_file)
    #print(CIRCs)
    mind = 999999
    for i, c in enumerate(CIRCs):
        mindT = [9999999,9999999]
      
        #compare centre point to the 2 surface used above
        for e in FACES[f1].edges:
            for v in e.vertices:
                d = math.sqrt((float(v.x)-float(c.centre[0]))**2 + 
                              (float(v.y)-float(c.centre[1]))**2 +
                              (float(v.z)-float(c.centre[2]))**2)
                if d < mindT[0]:
                    mindT[0] = d

                    
        #compare centre point to the 2 surface used above
        for e in FACES[f2].edges:
            for v in e.vertices:
                d = math.sqrt((float(v.x)-float(c.centre[0]))**2 + 
                              (float(v.y)-float(c.centre[1]))**2 +
                              (float(v.z)-float(c.centre[2]))**2)
                if d < mindT[1]:
                    mindT[1] = d
            
        
        sm = sum(mindT)
        if sm < mind:
            mind = sm
            f3 = i
        elif sm == mind:
            if CIRCs[i].r < CIRCs[f3].r:
                f3 = i
            
    radius = CIRCs[f3].r
    #print("inner radius used for flange is :",radius)
       
    
    #the shortest minimum distance (centre-to face point), is the one 
    
    
    #for all centre points this distance away collect radii
    
    #find the smallest of those ^^
    
    # done?
    
    print("flange angle is:", maxlegal) 
    return(radius,maxlegal)

    #Expansions:::::
    
    #filter for vertices that belong to flange (pointless in initial version) !!
    

#step_file ="D:\CAD_library_sampling\s-5045.stp"
#pos = np.asarray([[5.4,0,11.5]])
'''
step_file = "D:\CoSinC_WP4.2\TestCad\s-5029_2.stp"
#step_file = "D:\CoSinC_WP4.2\TestCad\s-5029.stp"
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
'''


'''
step_file = "D:\\CoSinC_WP4.2\\TestCad\\X\\x_test_2.stp"
f1 = flange_data(step_file)
'''


def MR_data(step_file,pos,report = False):
    # first do this for standalone flanges, then expand on flange within part
    
    # 
    
    #Go through step file and find all radii with link to points in "pos"

    with open(step_file, "r") as text_file:
        f = text_file.read()
        
    
    #empty return in case no circles are found
    mmr_pos = []
    CIRCs = []
    for l1 in f.split("\n"):
        if "CIRCLE('generated circle'" in l1:
            #go through circle references
            t1 = l1.split('=')[0]
            t1 = t1.split('#')[1]
            
            CIRC = step_circle()
            CIRC.ref = int(t1)
            
            t2 = l1.split('#')[2]
            t2 = t2.split(',')[0]
            CIRC.oref = int(t2)
            
            t3 = l1.split('#')[2]
            t3 = t3.split(',')[1]
            t3 = t3.split(')')[0]
            CIRC.r = float(t3)
            
            t2 = "#"+t2+"="
            for l2 in f.split("\n"):
                if t2 in l2:
                    #print("level 2")
                    #find axis location
                    t4 = l2.split('#')[2]
                    t4 = t4.split(',')[0]
                    t4 = "#"+t4+"="
                    for l3 in f.split("\n"):
                        if t4 in l3:
                            #print("level 3")
                            t5 = l3.split("('Axis2P3D Location',(")[1]
                            t5 = t5.split(")")[0]
                            xr = float(t5.split(",")[0])
                            yr = float(t5.split(",")[1])
                            zr = float(t5.split(",")[2])
                            CIRC.centre = [round(xr,2),round(yr,2),round(zr,2)]
                            
                            for i,p in enumerate(pos):
                                #print(p)
                                ldis = math.sqrt((xr-p[0])**2+(yr-p[1])**2+(zr-p[2])**2)

                                #consider point in radius range
                                if ldis < CIRC.r*1.2:
                                    CIRCs.append(CIRC)
    minr = 999999
    for CIRC in CIRCs:
        if CIRC.r < minr:
            minr = CIRC.r
            mmr_pos = CIRC.centre


                    #go all the way down to point level

                    #check point against list availalbe 

                    #if appropriate save the cirecle details

        #if "=EDGE_CURVE(" in l1:
        #    #go through point on curve #

        #    #if two points on curve are on "pos" list obtain circle
        #    print("something")
    
    print("min radius",minr)
    return(minr,mmr_pos,CIRCs)

    