#prerequisistes are relus applied, but not direcly listed in Bryn's rule listed

#to consider...
#3d aspect of layups was barely considered, might affect some of the origin and furthest point finding...

from pydantic import BaseModel, Field, conlist,  validator
import math
from fact_base import FactBase, layup, hole, vert, material
import os
import numpy as np
#import subprocess
import sys
import os
import copy
from scipy import spatial
#from sfd import WS1
from step_features import hole_data, flange_data, MR_data

from CATIA_utils import hole_loc, export_step
from ED import ED

#required to run WS through cmd
import subprocess

#potential rework, for now work with DP OLD database -- replaced

#from IDP_databases import cnt_X,dc_X

class pXX(FactBase):
    #pXX serves as rough template for a pre-rule. This will not be executed. Only numbered rules are executed.

    #Required variables (examples for various types:)
    tool_gender: str = Field("male")
    min_major_radii: float = Field() 
    mmr_location: object = Field()
    layup_sections: conlist(object, min_length=1) #at least one object must exist in this list
    uniform_material: bool = Field()
    #Required variables are important for pre-rules as they dictate the order of pre-rule execution. Commonly pre-rule will
    #have other pre-rules as pre-requisites, which this mechanism accomodates for.


    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        #Typically one overall if-statement should be included that prevents re-runs. Rules keep being checked for having
        #pre-requisites, but to prevent re-running the same rules all the time it is crucial to identify a variable that 
        #only exists after rule has been successfully run once.
        if self.layup_file == None:
            #Main body can include whatever is required to obtain the required information.

            #If this is complex/complicated... the main bulk of code should be housed in dedicated script (e.g. CATIA_utils)
            if os.path.exists(self.path+self.part_name+".txt"):
                #Don't forget to save the obtained information into the FactBase (self.)
                self.layup_file = self.path+self.part_name+".txt"
                #Important to add value ot .ite - this informs the overaching script that a rule has been run, 
                #and FactBase has been adjusted.
                self.ite += 1
            else:
                #Include reporting if it is suspected that lack of informaion might prevent this rule from running.
                self.report.check_issues += "\nLayup file not found, make sure that .txt file with corresponding name is located in specified folder.\n"
            #print out for troubleshooting purposes
            print("pX run")
        return(self)

class p1(FactBase):
    #checks if layup file exists

    #Required variables
    part_name: str = Field()
    path: str = Field()
    #only run this if layup_file == None -- verify this works
    #(eventually change to , run if None or False)


    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        if self.layup_file == None:
            if os.path.exists(self.path+self.part_name+".txt"):
                self.layup_file = self.path+self.part_name+".txt"
                self.ite += 1
            else:
                self.report.check_issues += "\nLayup file not found, make sure that .txt file with corresponding name is located in specified folder.\n"
            print("p1 run")
        return(self)

class p2(FactBase):
    #Variables to be obtained
    step_file: bool = Field(None)

    #Required variables
    part_name: str = Field()
    path: str = Field()

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        #Verify .stp file is available
        if self.step_file == None:
            if os.path.exists(self.path+self.part_name+".stp"):
                self.step_file = True
            else:
                self.step_file = False
            print("p2 run")
            self.ite += 1
        return(self)    

class p3(FactBase):

    #Required variables
    part_name: str = Field()
    path: str = Field()
    layup_file: str = Field()

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        #this takes the layup from file and turns it into list
        print(self.max_ply_layup)
        if self.max_ply_layup == None:
            with open(self.path+self.part_name+".txt", "r") as text_file:
                f = text_file.read()
                
            w = f.split("[LAMINATE]")[1]
            w = w.split("[MATERIALS]")[0]
            ori = w.split('\n')[1]
            ori = ori.replace("[","")
            layup = ori.replace("]","")
            layup = layup.replace(" ","")

            if (layup == None) or (layup == ""):
                self.runtime_error = "Layup is ill defined, please specify layers by numbers corresponding to orientation in degrees."
                return(self)
            else:
                #it also forces all angles to be  between -90 and 90
                l2 = []
                for l in layup.split(",")[:]:
                    #not sure why this is required, but....
                    
                    #to account for non-ASCII "-"
                    if "-" in l:
                        h = l.replace("-","")
                        h = float(h)
                        h = h *-1
                    else:
                        try:
                            h = float(l)
                        except:
                            self.runtime_error = "Layup is ill defined, the values between ',' must be numbers only."
                    
                    #180deg shifts until the layup exits in correct range
                    while h > 90:
                        h = h -180
                    while h < -90:
                        h = h + 180
                        
                    #construct the return string of layer orientations
                    l2.append(h)

                self.max_ply_layup = l2
                print("p3 run")
                self.ite += 1
        return(self)

class p4(FactBase):
    #calculate the numbers of segments with different layup and specify each layup

    #currently ignores cross-overs (implement layup-utils cross-over function later)

    #Required variables
    part_name: str = Field()
    path: str = Field()
    layup_file: str = Field()
    max_ply_layup: list = Field()
    layup_splines: list = Field()
    #layup_splines: conlist(hole, min_length=1)

    #somehow check the layup already exists 
    #layup_sections[0].layup.sequence: list = Field()

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        if self.layup_sections == None:
            #later move major part of this to layup_utils -- keep only rule type stuff here
            
            #obtain the list of delimiting splines 
            #read the file
            with open(self.path+self.part_name+".txt", "r") as text_file:
                f = text_file.read()
                
            w = f.split("[LAMINATE]")[1]
            w = w.split("[MATERIALS]")[0]
            ori = w.split('\n')[2]
            ori = ori.replace("[","")
            lp = ori.replace("]","")

            l2 = []
            for l in lp.split(",")[:]:  
                l2.append(l)

            val, cnt = np.unique(l2, return_counts=True)

            #save edge spline

            spe = f.split("[EDGE SPLINE]")[1]
            spe = spe.split("\n\n")[0]
            pt_list = np.asarray([[0,0,0]])
            ln = 0
            for n,ii in enumerate(spe.split("\n")):

                if n != 0:
                    x = float(ii.split()[0])
                    y = float(ii.split()[1])
                    z = float(ii.split()[2])

                    pt_list = np.concatenate((pt_list, np.asarray([[x,y,z]])),axis=0)

                if n > 1:
                    ln = ln + math.sqrt((pt_list[n,0]-pt_list[n-1,0])**2+(pt_list[n,1]-pt_list[n-1,1])**2+(pt_list[n,2]-pt_list[n-1,2])**2)
            pt_list = np.delete(pt_list, 0,axis=0)
            self.edge_points = pt_list
            self.edge_len = ln


            #print('val',val)
            #pathces allows for number of groups for drop-ffs
            #inside of each patch, sits list of splines (when cross overs come, it is going to be spline amalgamations)
            patches = [[]]

            self.layup_sections = []
            ptch = 0
            for i in val:
                if i != "'f'":
                    #print(i)
                    #collect list of points
                    #
                    #accomodate for random q-marks
                    sp = i.replace("'","")
                    sp = sp.replace('"','')
                    sp = sp.replace(" ","")

                    spx = f.split("[SPLINES]")[1]
                    spx = spx.split(sp)[1]
                    spx = spx.split("spline")[1] #newer - deals with addition closed/open info
                    spx = spx.split("\n\n")[0]

                    ln = 0
                    pt_list = np.asarray([[0,0,0]])
                    for n,ii in enumerate(spx.split("\n")):
                        #print("n",n)
                        #print("ii",ii)
                        if n != 0:
                            x = float(ii.split()[0])
                            #print("x",x)
                            y = float(ii.split()[1])
                            #print("y",y)
                            z = float(ii.split()[2])
                            #print("z",z)
                            pt_list = np.concatenate((pt_list, np.asarray([[x,y,z]])),axis=0)

                        #calculateing circumference by adding points 
                        
                        if n > 1:
                            ln = ln + math.sqrt((pt_list[n,0]-pt_list[n-1,0])**2+(pt_list[n,1]-pt_list[n-1,1])**2+(pt_list[n,2]-pt_list[n-1,2])**2)

                    pt_list = np.delete(pt_list, 0,axis=0)

                    origin = np.asarray([np.average(pt_list[:,0]),np.average(pt_list[:,1]),np.average(pt_list[:,2])])

                    if patches == [[]]:
                        #dont know layup yet, that will come from definition of patches
                        patches[0].append(layup(sp_len = ln,pt_list = pt_list,sp_def = i, origin =origin,patch = ptch))
                        #print(patches[0][0].origin)
                        
                    else:
                        #ok ok , special cases of weird layups will break this BEWARE! 
                        #but the distance of points method should work for most splines that do not cross over...
                        #A last patch origin point
                        #B closest poitn on new spline to A
                        #C furthest point on news spline to B

                        for ii, last_patch in enumerate(patches):
                            A = last_patch[0].origin

                            min_dist = 90000000000
                            iii = 0
                            while iii < np.size(last_patch[0].pt_list,0):
                                dd = math.sqrt((A[0]-pt_list[iii,0])**2+(A[1]-pt_list[iii,1])**2+(A[2]-pt_list[iii,2])**2)
                                if dd < min_dist:
                                    min_dist = dd
                                    B = np.asarray([pt_list[iii,0],pt_list[iii,1],pt_list[iii,2]])
                                iii = iii + 1
                            max_dist = 0
                            iii = 0
                            while iii < np.size(last_patch[0].pt_list,0):
                                dd = math.sqrt((B[0]-pt_list[iii,0])**2+(B[1]-pt_list[iii,1])**2+(B[2]-pt_list[iii,2])**2)
                                if dd > max_dist:
                                    max_dist = dd
                                    C = np.asarray([pt_list[iii,0],pt_list[iii,1],pt_list[iii,2]])
                                iii = iii + 1
                            
                            BA = min_dist
                            BC = max_dist
                            AC = math.sqrt((A[0]-C[0])**2+(A[1]-C[1])**2+(A[2]-C[2])**2)


                            if AC < BC:
                                #otherwise append to current patch
                                patches[ii].append(layup(sp_len = ln,pt_list = pt_list,sp_def = i, origin =origin,patch = ptch)) 
                                patches[ii].sort(key=lambda x: x.sp_len, reverse=True)
                                break
                            else:
                                #the origin of current patch is outside of previous patch
                                
                                if len(patches) - 1 == ii:
                                    #append new patches list of singular object
                                    ptch = ptch + 1
                                    patches.append([layup(sp_len = ln,pt_list = pt_list,sp_def = i, origin =origin,patch = ptch)])
                                    break
                                    #else continue to next for loop  

                            #break when patch allocated
                        #here after adding patch make sure you order patches[ii] from minimum size to maximum

            #add last segment delimited by edge of part
            #append as separate patch, and check if this works
            patches.append([layup(sp_len = self.edge_len,pt_list = self.edge_points,sp_def = "NO SPLINE",patch = 9999)])

            #material list for thickness
            #(check if Max thickness rule still needed)
            #take material information out of layup file
            with open(self.path+self.part_name+".txt", "r") as text_file:
                f = text_file.read()
                
            w = f.split("[MATERIALS]")[1]
            w = w.split("[SPLINES]")[0]

            #establish SQL connection for mat ref
            #cnnC,crrC = cnt_X('NCC')
            ttmax = 0

            mpl = self.max_ply_layup

            for ii, patch in enumerate(patches):
                #reverse the order 
                patch.sort(key=lambda x: x.sp_len, reverse=False)
                local_splines = []

                tt = 0

                for spline in patch:
                    seq = []
                    lrs = []
                    tt = 0

                    for i ,layer in enumerate(mpl):
                        q = True
                        #check if this splien is referenced in other patches
                        for iii, patch2 in enumerate(patches):
                            if iii != ii:
                                for spline2 in patch2:
                                    if spline2.sp_def == l2[i]:
                                        q = False

                        #check if referenced in above splines in this patch
                        if l2[i] in local_splines:
                            q = False

                        #if neither seq.append
                        if q == True:
                            seq.append(layer)
                            lrs.append(self.layup_splines[i])

                            #also calculate local thickness 
                            if "uniform" in w:

                                #if uniform this section does not need to 
                                qw = w.split("[")[1]
                                qw = qw.split("]")[0]
                                
                                lf3 = self.path+"LD_layup_database.txt"

                                try:
                                    with open(lf3, "r") as text_file:

                                        for i ,line in enumerate(text_file.readlines()):
                                            if line.count(",") > 0 and i != 0 and line.split(",")[1] == qw:
                                                #print("yes")
                                                fd = float(line.split(",")[8])
                                                mu = line.split(",")[11]
                                except:
                                    self.runtime_error = "The current folder does not contain LD_layup_database.txt, this"\
                                                        +" is currently required by the standard layup definition."
                                    return(self)
                                #this should be checked, gettign correct thickness values?
                                tt += fd
                                #tt = fd*
                                self.uniform_material = True
                                self.material_u = mu
                            if "variable" in w:
                                #initiate materials list
                                mts = []
                                qw = w.split("[")[1]
                                qw = qw.split("]")[0]
                                
                                #tt = 0

                                #mat = qw.split(",")[i]
                                for mat in qw.split(","):

                                        #print("qw",qw)
                                        lf3 = self.path+"LD_layup_database.txt"
                                        with open(lf3, "r") as text_file:

                                            for i ,line in enumerate(text_file.readlines()):
                                                if line.count(",") > 0 and i != 0 and line.split(",")[1] == mat:
                                                    #print("yes")
                                                    fd = float(line.split(",")[8])
                                                    mts.append(material(mat_name=line.split(",")[1],mat_type =line.split(",")[11],
                                                                        l_thick =float(line.split(",")[8])))



                                tt = tt + fd
                                self.uniform_material = False
                                spline.materials = mts
                                #print(spline.materials) 
                    

                    local_splines.append(spline.sp_def)
                    if ttmax < tt:
                        ttmax = tt
                    spline.local_thickness = tt
                    spline.sequence = seq
                    spline.remaining_splines = lrs
                    
                    #clearer messaging where no delimiting spline is found
                    if spline.sp_def == "NO SPLINE":
                        spline.sp_def = "Edge of part"
                    #save segment of layup
                    self.layup_sections.append(spline)


            self.layup_max_thickness = ttmax


            #once you have 2d table of patches finished go through each spline object specified and define layup 

            #if segments still empty, create a standalone single segment for the full layup

            #use the above to also find distance between any combination of patch splines?? 
            print("p4 run")

            #not to forget database disconnect:
            #dc_X('NCC',cnnC,crrC)
            self.ite += 1


        return(self)


class p5(FactBase):
    #finds the nearest distance between splines

    #DOES NOT WORK WITHOUT EDGE DEFINITION -- all the splines overlap
        #currently CATIA needs to be used to obtain this ^^

    #Required variables
    layup_sections: conlist(object, min_length=1)
    edge_points: object = Field()

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        #edge threshold for region where overlapping splines are allowed
        et = 10

        #with check of 1 run per expert system
        if self.layup_sections[0].mind == 999999.0:
            i = 0
            while i < len(self.layup_sections)-1: 
                      
                ii = i+1
                #initiate iteration of mind
                mind = self.layup_sections[i].mind
                change = 0
                while ii < len(self.layup_sections):
                    

                    #SORT OUT WHAT HAPPENS WHEN ONE OF THE SPLINES OVERLAP THE EDGE (SPOILER, THERE WILL BE NO POINTS....)

                    #remove edge points from first spline list
                    sls1 = np.asarray([[0,0,0]])
                    for p1 in self.layup_sections[i].pt_list:
                        dpt1 = 9999
                        for p2 in self.edge_points:
                            dpt = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)
                            if dpt < dpt1:
                                dpt1 = dpt
                        if dpt1 > et:
                            sls1 = np.concatenate((sls1,np.asarray([[p1[0],p1[1],p1[2]]])),axis=0)
                        else:
                            self.layup_sections[i].overlap = True
                    sls1 = np.delete(sls1,0,axis = 0)
                    
                    if np.size(sls1,0) == 0:
                        #if no points were stored it means edge spline is the spline
                        #in such case the spline is kept in full
                        sls1 = self.layup_sections[i].pt_list

                    #remove edge points from second spline list
                    sls2 = np.asarray([[0,0,0]])
                    for p1 in self.layup_sections[ii].pt_list:
                        dpt1 = 9999
                        for p2 in self.edge_points:
                            dpt = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)
                            if dpt < dpt1:
                                dpt1 = dpt
                        if dpt1 > et:
                            sls2 = np.concatenate((sls2,np.asarray([[p1[0],p1[1],p1[2]]])),axis=0)
                        else:
                            self.layup_sections[ii].overlap = True
                    sls2 = np.delete(sls2,0,axis = 0)

                    if np.size(sls2,0) == 0:
                        #if no points were stored it means edge spline is the spline
                        #in such case the spline is kept in full
                        sls2 = self.layup_sections[ii].pt_list



                    #print(self.layup_sections[ii].sp_def)

                    #print(sls2)

                    #CURRENTLY ISSUE WITH WORKING WITH ONE SPLINE ONLY --- DONT THINK IT HAS A WAY OF CALCULATING DISTANCE...

                    for p1 in sls1:
                        for p2 in sls2:
                            dist = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)
                            if dist <= mind:
                                mind = dist
                                i_id = ii
                                change = change + 1

                    ii = ii + 1

                if change > 0:
                    self.layup_sections[i].mind = mind
                    self.layup_sections[i].close_other = self.layup_sections[i_id].sp_def
                
                    #if this is also the closest for the other spline
                    if mind < self.layup_sections[i_id].mind:
                        self.layup_sections[i_id].mind = mind
                        self.layup_sections[i_id].close_other = self.layup_sections[i].sp_def
                i = i + 1

            else:
                #This account for situation where no drop-offs were recorded, prevents
                #re-run of p5
                self.layup_sections[i].mind = 0

            #print(mind)
            print("p5 run")
            self.ite += 1

        return(self)

class p6(FactBase):

    #calculate flange angle (this one currently not used)
    #calculate major radius radius

    #to be expanded for more shapes eventually - WS currently out of commision

    #Required variables
    step_file: str = Field()
    part_name: str = Field()
    path: str = Field()
    MajorRaius: bool = Field()

    #@validator("flange", pre=True)
    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        #specialized step interogation script does most of the work

        if self.min_major_radii == None:
            sf = self.path + self.part_name+".stp"
            rad, angle = flange_data(sf)
            self.min_major_radii = rad
            self.major_shape_angle = angle
            print("p6 run")
            self.ite += 1
        return(self)

class p7(FactBase):
    #obtain maximum thickness of laminate  and local thicknesses 

    #Required variables
    #max_ply_layup: list = Field()
    layup_sections: conlist(object, min_length=1)
    part_name: str = Field()
    path: str = Field()

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):

        if self.layup_max_thickness == None:

            #take material information out of layup file
            with open(self.path+self.part_name+".txt", "r") as text_file:
                f = text_file.read()
                
            w = f.split("[MATERIALS]")[1]
            w = w.split("[SPLINES]")[0]

            #SQL connection replaced by .txt database
            ttmax = 0
            for ls in self.layup_sections:
                tt = 0
                
                #print("w",w)
                if "uniform" in w:
                    qw = w.split("[")[1]
                    qw = qw.split("]")[0]

                    #print("qw",qw)
                    lf3 = self.path+"LD_layup_database.txt"
                    with open(lf3, "r") as text_file:

                        for i ,line in enumerate(text_file.readlines()):
                            if line.count(",") > 0 and i != 0 and line.split(",")[1] == qw:
                                #print("yes")
                                fd = float(line.split(",")[8])

                    tt = len(ls.sequence)*fd
        
                elif "variable" in w:
                    qw = w.split("[")[1]
                    qw = qw.split("]")[0]
                    
                    #tt = 0

                    for mat in qw.split(","):

                        #print("qw",qw)
                        lf3 = self.path+"LD_layup_database.txt"
                        with open(lf3, "r") as text_file:

                            for i ,line in enumerate(text_file.readlines()):
                                if line.count(",") > 0 and i != 0 and line.split(",")[1] == mat:
                                    #print("yes")
                                    fd = float(line.split(",")[8])

                        tt = tt + fd
                else:

                    for l in ls.sequence:
                        print("option not curretnly available -- the only material allocation options are 'uniform' and 'variable'")
                        self.runtime_error = "Materials have to be defined with 'uniform' or 'variable' options."

                if tt > ttmax:
                    ttmax = tt
                    #do I need to know which layup is the max?

                ls.local_thickness = tt

            self.layup_max_thickness = ttmax
            print("p7 run")
            self.ite += 1
        return(self)

class p8(FactBase):
    #Finds hole locations

    #Required variables
    part_name: str = Field()
    path: str = Field()
    step_file: str = Field()

    #and check if step-file is available...

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        if self.holes == None:
            self.holes = []
            #TWO METHODS HERE - decide which one? -- some decision tree based on facts?
            CATIA = False

            #CATIA method - requires holes to be defined by points in "holes" geometrical set
            if CATIA == True:
                part = self.path+self.part_name+".catpart"
                #print(part)
                f_pt = hole_loc(part)

                i = 0
                while i < np.size(f_pt,0):
                    pos = np.asarray([f_pt[i,0],f_pt[i,1],f_pt[i,2]])
                    h = hole(position=pos)

                    self.holes.append(h)
                    i = i + 1
            
            #using WS to identify holes
            #Improvement still required: use connection information, for robust midpoint and grouping of vertices)
            else:
                part_name = self.part_name
                #the below replace by finding local path
                run_path = os.path.dirname(os.path.realpath(__file__))+'''\\WS_2.0\\'''
                path = self.path
                command = '''conda run -n GPU_WS_pyg_retest python '''+run_path+'''single_file_demonstrator.py '''
                command += '''--file_path "'''+path+part_name+'''".stp --out_path "'''
                command += run_path+'''votes_h" --config_path "'''+run_path+'''config_sursol.ini"'''
                process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)

                import time
                time.sleep(20)

                #open csv files
                file1 = open(run_path+'votes_h.csv')
                file2 = open(run_path+'votes_h_adj.csv')

                #read csv files
                Lines1 = file1.readlines()
                Lines2 = file2.readlines()

                #first shorten the .csv to only include hole references
                #and turn into numpy array
                XX = np.asarray([[0,0,0,0]])
                for line1 in Lines1:
                    if "node" in line1:
                        continue
                        
                    if float(line1.split(",")[8]) == float(1.0):
                        #for B
                        ID = line1.split(",")[1]
                        x = line1.split(",")[2]
                        y = line1.split(",")[3]
                        z = line1.split(",")[4]
                        XX = np.concatenate((XX,np.asarray([[ID,x,y,z]])),axis=0)
                XX = np.delete(XX,0,axis=0)

                #if no holes are found at all - skip the rest of this pre-rule
                if np.size(XX,0) != 0:
                    #limit the second file to only connections between nodes above
                    fl2 = ""
                    for line2 in Lines2:
                        if line2.split(",")[1] == "source":
                            continue
                        if (line2.split(",")[1] in XX[:,0]
                            or line2.split(",")[2] in XX[:,0]):
                            fl2 += line2 + "-!-"

                    #initiate iterated vertex objects
                    v1 = vert()
                    v3 = vert() #used to store values of min.dist vert
                    h1 = hole()
                    c = 0

                    #first point randomly selected
                    v1.ID = int(XX[0,0])
                    v1.x = float(XX[0,1])
                    v1.y = float(XX[0,2])
                    v1.z = float(XX[0,3])

                    #create a hole object, and holes list
                    h1.vert_list.append(v1)
                    
                    XX = np.delete(XX,0,axis=0)

                    #loop through the XX matrix, and take away points from it as you go
                    TOT = np.size(XX,0)
                    #print(TOT)
                    while c < TOT:

                        pt = [v1.x,v1.y,v1.z]  # <-- the point to find
                        near = XX[spatial.KDTree(XX[:,1:4]).query(pt)[1]] # <-- the nearest point 
                        distance,index = spatial.KDTree(XX[:,1:4]).query(pt)
                        mind = distance

                        #closest point as v3
                        v3 = vert()
                        v3.ID = int(near[0])
                        v3.x = float(near[1])
                        v3.y = float(near[2])
                        v3.z = float(near[3])

                        #NOT CHECKING FOR CONNECTIONS, issues with connections not showing in list
                        #therefore this will not work for many parts
                        #consider varying the division parameter mind/10? if this is to be used....
                        cnn = False
                        for line3 in fl2.split("-!-")[:-1]:
                            if (
                                (int(line3.split(",")[1]) == v3.ID 
                                or int(line3.split(",")[1]) == v1.ID)
                                and (int(line3.split(",")[2]) == v3.ID
                                or int(line3.split(",")[2]) == v1.ID)
                            ):
                                cnn = True
                            

                        if len(h1.vert_list) == 1:
                            oldist = 9999999
                        else:
                            oldist = math.sqrt((h1.vert_list[0].x-h1.vert_list[1].x)**2
                                            +((h1.vert_list[0].y-h1.vert_list[1].y)**2
                                                +(h1.vert_list[0].z-h1.vert_list[1].z)**2))
                            
                        if cnn == True:
                            #Requires testing, but for now connection means same hole is assumed
                            h1.vert_list.append(v3)
                            
                        
                        else:
                        
                            #if new point is 100x further than previous local cnn
                            if oldist < mind:
                                self.holes.append(h1)
                                h1 = hole()
                                h1.vert_list.append(v3)
                                
                            else:
                                h1.vert_list.append(v3)
                                

                        XX = np.delete(XX,index,axis=0)
                        
                        #turn the current vertex into referencevertex
                        v1 = copy.deepcopy(v3)
                        c += 1
                        #print(c)
                    self.holes.append(h1)

                    #for the time being the hole position is going to be the average of vertices
                    #this should be improved when .stp vertex connections are better understood
                    for hs in self.holes:
                        n = 0
                        xsm = 0
                        ysm = 0
                        zsm = 0
                        for v in hs.vert_list[:]:
                            xsm += v.x
                            ysm += v.y
                            zsm += v.z
                            n += 1

                        hs.position = np.asarray([xsm/n,ysm/n,zsm/n])
            #print(self.holes)
            print("p8 run")

            self.ite += 1

        return(self)

class p9(FactBase):
    #Finds the radius of each hole

    #Required variables
    holes: conlist(hole, min_length=1)

    #and check if step-file is available...

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        #collect hole data 
        if self.holes[0].radius == None:
            step_file = self.path+self.part_name+".stp"
            for h in self.holes:
                h = hole_data(h,step_file,report = False)

            print("p9 run")
            #only causes more iterations if radius has been obtained for hole 1
            if self.holes[0].radius != None:
                self.ite += 1


        return(self)

class p10(FactBase):
    #Finds the edge distance of each hole

    #Required variables
    holes: conlist(hole, min_length=1)

    #and check if step-file is available...

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        if self.holes[0].edge_distance == None:

            #if layup file exists - just consider distance from points on edge
            for h in self.holes:
                mind = 9999
                i = 0
                #CHANGE INTO FOR LOOP AT SOME POINT
                while i < np.size(self.edge_points,0):
                    ldist = math.sqrt((self.edge_points[i,0]-h.position[0])**2+(self.edge_points[i,1]-h.position[1])**2+(self.edge_points[i,2]-h.position[2])**2)
                    #print(ldist)
                    if ldist < mind:
                        mind = ldist
                        
                    i = i + 1

                h.edge_distance = mind

            #edge distance from step file currently not run, the edge spline is provided anyway
            '''
            else:
                #only run the .step definition edge distance measurement if spline for
                #edge not available.

                #This is less precise and might need some mroe troubleshooting

                #run the ED for each hole
                step_file = self.path+self.part_name+".stp"
                for h in self.holes:
                    hpos = np.asarray([h.position])
                    md = ED(hpos,step_file,h.radius) 
                    h.edge_distance = md
            '''
            
            #save the min ed in hole classes 

            print("p10 run")
            self.ite += 1
        return(self)

class p11(FactBase):
    #Creates step file from the surface catpart
    #Required variables
    layup_max_thickness: float = Field()


    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        if (self.step_file == None):

            if os.path.exists(self.path+self.part_name+".stp"):
                self.step_file = self.path+self.part_name+".stp"
            else:
                #if step file does not exist, create a step file
                export_step(self)
                self.step_file = self.path+self.part_name+".stp"

            print("p11 run")
            self.ite += 1
        return(self)

class p12(FactBase):
    #assign holes to layups based on hole location ...

    #Required variables
    layup_sections: conlist(object, min_length=1)
    holes: conlist(hole, min_length=1)


    #and check if step-file is available...

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        test = True
        for ls in self.layup_sections:
            if ls.local_holes != []:
                test = False

        #checks if this rule runs
        if test == True:
            for h in self.holes:
                dist_min = 900000000000000000
                for ii, ls in enumerate(self.layup_sections):
                    dist = 0
                    i = 0
                    while i < np.size(ls.pt_list,0):
                        dt = math.sqrt((ls.pt_list[i,0]-h.position[0])**2+(ls.pt_list[i,1]-h.position[1])**2+(ls.pt_list[i,2]-h.position[2])**2)
                        dist = dist + dt
                        i = i + 1
                    if dist_min > dist:
                        dist_min = dist
                        ref_sec = ii
                
                #the shortest cummulative distance corresponds to hole allocation
                self.layup_sections[ref_sec].local_holes.append(h)

            #for ls in self.layup_sections:
            #    print(ls.local_holes)
            print("p12 run")
            self.ite += 1
        return(self)
    
class p13(FactBase):

    #Required variables
    part_name: str = Field()
    path: str = Field()
    layup_file: str = Field()

    #and check if step-file is available...

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        #generate list of splines from the text file
        if self.layup_splines == None:
            with open(self.path+self.part_name+".txt", "r") as text_file:
                f = text_file.read()
                
            w = f.split("[LAMINATE]")[1]
            w = w.split("[MATERIALS]")[0]
            ori = w.split('\n')[2]
            ori = ori.replace("[","")
            lp = ori.replace("]","")
            i = 0
            xlist = []
            while i < lp.count(",")+1:
                xlist.append(lp.split(",")[i])
                i = i + 1
            self.layup_splines = xlist
            print("p13 run")
            self.ite += 1

        return(self)
    
class p14(FactBase):
    #establish if identifiyinble major radii exist in the part
    #used in 6 to find the smallest of these

    #Required variables
    part_name: str = Field()
    path: str = Field()
    step_file: str = Field()

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        
        if self.MR_points == None:
            part_name = self.part_name
            #the below replace by finding local path
            run_path = os.path.dirname(os.path.realpath(__file__))+'''\\WS_2.0\\'''
            path = self.path
            command = '''conda run -n GPU_WS_pyg_retest python '''+run_path+'''single_file_demonstrator.py '''
            command += '''--file_path "'''+path+part_name+'''".stp --out_path "'''
            command += run_path+'''votes_mr" --config_path "'''+run_path+'''config_rad.ini"'''
            print(command)
            process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)

            import time
            time.sleep(40)
            
            #open csv files
            file1 = open(run_path+'votes_mr.csv')

            #read csv files
            Lines1 = file1.readlines()

            pts = []
            for i, line in enumerate(Lines1):
                if i != 0:

                    prob = int(line.split(",")[7])
                    pred = int(line.split(",")[8])

                    if prob == 1 and pred == 1:
                        #self.MajorRadius = True
                        x = float(line.split(",")[2])
                        y = float(line.split(",")[3])
                        z = float(line.split(",")[4])
                        pt = np.asarray([x,y,z])
                        pts.append(pt)

            self.MR_points = pts
            
            #print("MR_points:")
            #print(pts)
            #print(self.MajorRadius)

            print("p14 run")
            self.ite += 1
            
        
        return(self)

class p15(FactBase):
    #find the radius value for any "major radii" identified by WS

    #Required variables
    part_name: str = Field()
    path: str = Field()
    step_file: str = Field()
    #MR_poitns: conlist(object, min_length=1)
    MR_points: list = Field()

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):

        #step interogation based on points provided by WS
        if self.min_major_radii == None:
            sf = self.path + self.part_name+".stp"
            rad, mmr, CIRCs = MR_data(sf,self.MR_points)
            self.mmr_location = mmr
            self.min_major_radii = rad
            self.MR_list = CIRCs
            print("p15 run")
            self.ite += 1
        return(self)
    
class p16(FactBase):
    #Required variables
    part_name: str = Field()
    path: str = Field()
    step_file: str = Field()

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        
        if self.FL_points == None:
            part_name = self.part_name
            #the below replace by finding local path
            run_path = os.path.dirname(os.path.realpath(__file__))+'''\\WS_2.0\\'''
            path = self.path
            command = '''conda run -n GPU_WS_pyg_retest python '''+run_path+'''single_file_demonstrator.py '''
            command += '''--file_path "'''+path+part_name+'''".stp --out_path "'''
            command += run_path+'''votes_fl" --config_path "'''+run_path+'''config_fl.ini"'''
            process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)

            #cleaner method for this better way for checking subprocess is finished?
            import time
            time.sleep(20)
            
            #open csv files
            file1 = open(run_path+'votes_fl.csv')

            #read csv files
            Lines1 = file1.readlines()

            pts = []
            for i, line in enumerate(Lines1):
                if i != 0:

                    prob = int(line.split(",")[7])
                    pred = int(line.split(",")[8])

                    if prob == 1 and pred == 1:
                        #self.MajorRadius = True
                        x = float(line.split(",")[2])
                        y = float(line.split(",")[3])
                        z = float(line.split(",")[4])
                        pt = np.asarray([x,y,z])
                        pts.append(pt)

            self.FL_points = pts

            print("p16 run")
            self.ite += 1
            
        
        return(self)

