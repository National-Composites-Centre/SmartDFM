
#there are two types of rules:
# 1: directly taken from Bryn's rules document
# 2: rules that need to be checked as pre-requisites for ^^

from pydantic import BaseModel, Field, conlist
import math
from fact_base import FactBase, layup, report
from layup_utils import symmetry, balance
import numpy as np

#rXX is an example/template rule, explaining typical features of how the rules are structured
class rXX(FactBase):
    #Required variables (examples for various types:)
    tool_gender: str = Field("male")
    min_major_radii: float = Field() 
    mmr_location: object = Field()
    layup_sections: conlist(object, min_length=1) #at least one object must exist in this list
    uniform_material: bool = Field()

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        ###[Explanation of the rule's purpose]
        ###[Typically an if statement that compares a variable obtained by pre-rules to a threshold]
        if self.min_major_radii < 1.5:
            txt = "\n One of the major radii seems below 1.5mm, radius size should be increased.\n"

            #Mechanism to prevent duplication of reporting the same error. Key in cases where multiple 
            #features are being checked for the rule.
            if txt not in self.report.design_errors:
                self.report.design_errors = self.report.design_errors + txt 

        #print("r85 checked")
        return(self)

class r85(FactBase):
    #Required variables
    tool_gender: str = Field("male")
    min_major_radii: float = Field() 

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        ###For male tooling, use 0.06" (~1.5mm) minimum laminate inner radius. Larger is preferable
        if self.min_major_radii < 1.5:
            txt = "\n One of the major radii seems below 1.5mm, radius size should be increased.\n"
            #add a location of the radius??? based WS?

            #avoid duplication
            if txt not in self.report.design_errors:
                self.report.design_errors = self.report.design_errors + txt 

        #print("r85 checked")
        return(self)

class r86(FactBase):
    #Required variables
    min_major_radii: float = Field() 
    #Currently working with max thickness - this rule could be applied with more precision, but matching radii with layup segments is very difficult
    layup_max_thickness: float = Field()
    mmr_location: object = Field()


    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        ###For female tooling, use 0.08"+t (~2mm+t) minimum laminate outer radius
        #this rule is stricter than 85, therefore it is used where tool gender is unknown
        if self.tool_gender != "male":
            if self.tool_gender == "female":
                if self.min_major_radii < self.layup_max_thickness+2:
                    txt = "\n At least one of the major radii seems to be less than 2*thickness,"\
                         +" while female tool is used, radius size should be increased. The radius to"\
                         +" check is at "+str(self.mmr_location)+".\n"
                    #avoid duplication
                    if txt not in self.report.design_errors: 
                        self.report.design_errors = self.report.design_errors + txt 

            elif self.tool_gender == None:
                if self.min_major_radii < self.layup_max_thickness+2:
                    txt = "\n At least one of the major radii seems to be less than 2*thickness, in case female tool is used radius size should be increased.\n"
                    txt +="In case male tool is being used, make sure the radius is above 1.5mm. The radius"\
                        +" to check is at "+str(self.mmr_location)+".\n"
                    #avoid duplication
                    if txt not in self.report.design_errors:
                        self.report.design_errors = self.report.design_errors + txt 


            else:
                print("This is an error: tool_gender was specified as something else than None,male and female")
            
        #print("r86 checked")
        return(self)


class r91(FactBase):
    #Required variables
    layup_sections: list = Field()
    layup_sections: conlist(object, min_length=1)

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        ###Laminates Should Have Greater Than 10% 0° Plies to Avoid Excessive Thermal Coefficients of Expansion
        for l in self.layup_sections:
            c10 = l.sequence.count(0)
            ct = len(l.sequence)
            perc = c10/ct
            if perc < 0.1:
                txt = "\n The layup has less than 10 percent 0 degree plies in location delimited by spline: "+l.sp_def+".\n"
                txt += "To avoid excessive thermal expansion more 0 degree plies should be used.\n"

                #avoid duplication
                if txt not in self.report.suggested_checks:
                    self.report.suggested_checks += txt

        return(self)

class r92(FactBase):
    #Required variables
    #layup_sections: list = Field()
    #layup_sections[:]: object = Field()
    layup_sections: conlist(object, min_length=1)


    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        ###Laminates Should Have Greater Than 10% 90° Plies to Avoid Excessive Thermal Coefficients of Expansion.
        for l in self.layup_sections:
            c10 = l.sequence.count(90)
            ct = len(l.sequence)
            perc = c10/ct
            if perc < 0.1:
                txt = "\n The layup has less than 10 percent 90 degree plies in location delimited by spline: "+l.sp_def+".\n"
                txt += "To avoid excessive thermal expansion more 90 degree plies should be used.\n"
                #avoid duplication
                if txt not in self.report.suggested_checks:
                    self.report.suggested_checks += txt

        return(self)

class r134(FactBase):

    #Required variables
    layup.sequence: list = Field()

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        #go to rule list to add rule here...
        ### Whenever possible maintain a dispersed stacking sequence and avoid grouping similar plies. 
        # If plies must be grouped, avoid grouping more than 4 plies of the same orientation together.

        for l in self.layup_sections:
            count = 1
            prev = 999
            for i in l.sequence:
                if i == prev:
                    count += 1
                else:
                    count = 1
                    prev = i
                
                if count >= 4:
                    txt = "\n The layup contains group of 4 or more plies grouped together in location delimited by spline: "+l.sp_def+".\n"
                    txt += "This should be avoided.\n"
                    #avoid duplication
                    if txt not in self.report.suggested_checks:
                        self.report.suggested_checks += txt
                    break

        #add clauses for less than 4 but stacking.. suggestion to spread them out

        #also, add advice on how to spread them out?

        return(self) 

class r135(FactBase):

    #Required variables
    layup.sequence: list = Field()

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        ###If possible, avoid grouping 90° plies. Separate 90° plies by a 0° or ±45° plies where 0° is direction of critical load.
        for l in self.layup_sections:
            count = 0
            for i in l.sequence:
                if i == 90:
                    count += 1
                else:
                    count = 0

                if count >= 2:
                    txt = "\n The layup has a stack of 90degree plies in location delimited by spline: "+l.sp_def+".\n"
                    txt += "This should be avoided, place differently oriented plies between the 90 degree plies.\n"
                    if txt not in self.report.suggested_checks:
                        self.report.suggested_checks += txt
                    break

        return(self)    

class r130(FactBase):

    layup_sections: list = Field()
    #layup_sections[:]: object = Field()
    layup_sections: conlist(object, min_length=1)

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):

        ###Stacking order of plies should be balanced and symmetrical about the laminate midplane. 
        # Any unavoidable unsymmetric or unbalanced plies should be placed near the laminate midplane.

        for i in self.layup_sections:
            i.symmetric = symmetry(i.sequence)
            if i.symmetric == False:
                #one assymetric section is enough to trigger warning
                txt = "\nLaminate is asymmetric in the location delimited by "+i.sp_def+".\n"
                txt += "Layup in that location is: "+str(i.sequence)+"\n"
                txt += "Check that laminate is not asymmetric in any major segments, \n"
                txt += "ideally make all local sections symmetric.\n."
                if txt not in self.report.warnings:
                    self.report.warnings = self.report.warnings+txt


        for i in self.layup_sections:
            i.balanced = balance(i.sequence)
            if i.balanced == False:
                #one imbalance section is enough to trigger warning
                txt = "\nLaminate is not balanced in the location delimited by "+i.sp_def+".\n"
                txt += "Layup in that location is: "+str(i.sequence)+"\n"
                txt += "Check that laminate is not imbalanced in any major segments, \n"
                txt += "and consider making even small sections balanced.\n."
                #avoid duplication
                if txt not in self.report.warnings:
                    self.report.warnings = self.report.warnings+txt

                #eventually distinugish between full stack balance and all segments balance
                #break

        return(self)

    
class r144(FactBase):

    layup_sections: conlist(object, min_length=2)

    #How do I check for attributs of layup? class within list...

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        ###Ply drop-offs should have a minimum spacing of 0.2 inch (5.1 mm) in the major load direction

        #for now load direction not implemented

        #figure our how to implement , and pass in second half of this rule....

        #it would classify as error if loading direction was known


        if self.load_direction == None:

            #if no load direction is suggested 
            for x in self.layup_sections:
                #rule suggests 5.1 mm limit
                if x.mind < 5.1:
                    txt = "\n Distance between 2 drop-offs is smaller than required."
                    txt +="\n Spline "+x.close_other+" and spline "+x.sp_def+" are closer than the recommended 5.1mm minimum."
                    txt +="\n Major loading direction was not identified. The minimum distance should definitely not be undercut in main loading direction!\n"
                    #avoid duplication
                    if txt not in self.report.warnings:
                        self.report.warnings =self.report.warnings + txt

        return(self)

class r35(FactBase):

    #required variables
    holes: conlist(object, min_length=2)

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        ###Minimum fastener pitch (W/D) should be 4.

        for i, h1 in enumerate(self.holes):
            #if h1.radius == None:
            #    stre = "Radius for hole at position "+str(h1.position)+" has not been obtained. Some rules could not be checked."
            #    self.report.check_issues += "\n"+stre +"\n"
            #else:
            for ii, h2 in enumerate(self.holes):
                if i != ii:
                    #for hole to hole distance average diameter considered, summation of the two radii equivalent
                    D = h1.radius + h2.radius
                    W = math.sqrt((h1.position[0]-h2.position[0])**2+(h1.position[1]-h2.position[1])**2+(h1.position[2]-h2.position[2])**2)
                    if W/D < 4:
                        stre = "Distance between hole at position "+str(h1.position)+ "and the hole at position "+str(h2.position)
                        stre += " is inadequate. W/D should be at least 4 (where W is distance between hole centres and D is the average."
                        stre += " diameter.\n W/D is currently :"+str(round(W/D, 2))
                        #avoid duplication
                        if stre not in self.report.design_errors:
                            self.report.design_errors += "\n"+ stre +"\n"    
        

        return(self)
    

#r48 duplicates r35 and r166, so not used for now
'''
class r48(FactBase):

    #required variables


    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):

        return(self)
'''

class r166(FactBase):

    #required variables
    holes: conlist(object, min_length=1)

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        ###Fastener edge distance and pitch: use 3.0D edge distance in direction of major load (D is diameter of fastener.)
        for h in self.holes:
            c = h.edge_distance/(2*h.radius)
            if c < 3:
                stre = "Hole at position "+str(h.position)+" is too close to edge.\n"
                stre += "Hole should be at least the distance 3*D away from edge, where D is the diameter of the hole.\n"
                stre += "Currently the hole is "+str(round(c, 2))+"D away from closest edge."
                #avoid duplication
                if stre not in self.report.design_errors:
                    self.report.design_errors += "\n"+stre+"\n"

        return(self)

class r151(FactBase):

    #required variables
    layup_sections: conlist(object, min_length=1)
    

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        ### If the outermost structural ply material is fabric, 
        # the ply should be oriented in the least structurally 
        # critical direction (generally, but not always, +45°). 
        # If the outermost structural ply material is tape, the 
        # surface plies should consist of two tape plies 
        # oriented in the least critical directions 
        # (generally one +45° and one –45° ply).

        for s in self.layup_sections:

            count = len(s.sequence)
            #if top or bottom layer are not +-45 
            if (s.sequence[0] != 45 and s.sequence[0] != -45) or (s.sequence[count-1] != 45 and s.sequence[count-1] != -45):
                stre = "Outermost plies should typically be +45° or –45° .\n"
                #avoid duplication
                if stre not in self.report.suggested_checks:
                    self.report.suggested_checks += "\n"+stre+"\n"
                #only takes one instance of this to be included in suggestions
                break



        return(self)
    
class r36(FactBase):

    #required variables
    layup_sections: conlist(object, min_length=1)
    holes: conlist(object, min_length=1)  #instead sub-class in layup_section called holes is used (allocated holes)
 

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        ###Use d/t ~ 1. d = bolt diameter t = laminate thickness

        #pre-rule 12 allocates holes to layups

        for l in self.layup_sections:
            for h in l.local_holes:
                #d/t
                dd = h.radius *2 
                t = l.local_thickness
                dt = dd/t

                #two levels depending on ratio
                if (0.5 > dt ) or (dt > 3):
                    stre = "Bolt diameter to laminate thickness ratio (d/t) should be around 1.\n"
                    stre += "This ratio is "+str(dt)+" at the hole location "+str(h.position)+".\n"
                    stre += "Please adjust this if this hole is used for bolted connection.\n"
                    #avoid duplication
                    if stre not in self.report.warnings:
                        self.report.warnings += "\n"+stre+"\n"
                elif (0.8 > dt ) or (dt > 1.2):
                    stre = "Bolt diameter to laminate thickness ratio (d/t) should be around 1.\n"
                    stre += "This ratio is "+str(dt)+" at the hole location "+str(h.position)+".\n"
                    stre += "Consider adjust this if this hole is used for bolted connection.\n"
                    #avoid duplication
                    if stre not in self.report.suggested_checks:
                        self.report.suggested_checks += "\n"+stre+"\n"        

        #print("temp... delete later")

        return(self)

class r78(FactBase):

    #required variables
    layup_sections: conlist(object, min_length=1)

    #78 temporarily disabled

    #slope ratio will be infinite in locations... this requires better definition of slope ratio and how it is calculated in 3D shapes
    

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        ###Maximum slope ratio:
        #1:10 in any other direction (1 mm drop for 10 mm horizontal).
        for l in self.layup_sections:
            distance = l.mind
            n1 = l.local_thickness
            n2_ref = l.close_other
            for l2 in self.layup_sections:
                if l2.sp_def == n2_ref:
                    n2 = l2.local_thickness
                    break
            change_thick = abs(n2-n1)
            slope = change_thick/distance

            if slope > 0.1:
                stre = "Maximum slope ratio: 1:10. "
                stre += "In any other direction only 1 mm drop in thickness for 10 mm horizontal is recommended.\n"
                stre += "The slope obtained between spline "+str(l.sp_def)+" and spline "+str(l2.sp_def)+" is "+str(slope)+".\n"
                #avoid duplication
                if stre not in self.report.warnings:
                    self.report.warnings += "\n"+stre+"\n"
                
        return(self)

class r133(FactBase):

    #required variables
    layup_sections: conlist(object, min_length=1)


    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        #If the structure is mechanically fastened, an excess of 40% of the fibres oriented in any one direction is inadvisable.
        for ls in self.layup_sections:
            #hole means there might be fastener
            if ls.local_holes != []:
                for ua in set(ls.sequence):
                    cnt_same = ls.sequence.count(ua)
                    perc = cnt_same/len(ls.sequence)

                    #40% trigger limit
                    if perc > 0.4:
                        stre = "The layup around hole located at "+str(ls.local_holes[0].position)+" has "+str(int(100*perc))+"""% layers oriented """
                        stre +=" in "+str(ua)+""" direction. If the structure is mechanically fastened, an excess of 40% """
                        stre += "of the fibres oriented in any one direction is inadvisable.\n"
                        #avoid duplication
                        if stre not in self.report.suggested_checks:
                            self.report.suggested_checks += "\n"+stre+"\n" 


        return(self)
    
class r83(FactBase):

    #required variables
    layup_splines: conlist(object, min_length=2)
    
    

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        #At least the two most external plies shall be continuous
        
        stre = "At least the two most external plies shall be continuous. This appears not to be the case.\n"
        #avoid duplication
        if stre not in self.report.design_errors:
            if self.layup_splines[0] != "'f'":
                #print("1")
                self.report.design_errors += "\n"+stre+"\n" 
            elif self.layup_splines[1] != "'f'":
                #print("2")
                self.report.design_errors += "\n"+stre+"\n" 
            elif self.layup_splines[int(len(self.layup_splines)-1)] != "'f'":
                #print("3")
                self.report.design_errors += "\n"+stre+"\n" 
            elif self.layup_splines[int(len(self.layup_splines)-2)] != "'f'":
                #print("4")
                self.report.design_errors += "\n"+stre+"\n" 


        return(self)
    
class r95(FactBase):
    #required variables 
    layup_splines: conlist(object, min_length=1)
    max_ply_layup: conlist(object, min_length=1)

    def __init__(self,d:FactBase):
        self = FactBase.__init__(self, **d.__dict__)
    def solve(self):
        #If two plies are dropped at the same position there should be, at least, four plies between them. 
        #However, dropping several plies at the same position is not recommended for drop offs with ramp in only one side.

        #to only suggest check once
        reported = 0

        #ADD HERE ITERATION THROUGH LAYUP SEGMENTS.... RUN THE BELOW FOR ALL SEPARATELY -- AFTER EDITING "REMIANING_SPLINES"

        #needs to be checked for each segment
        for seg in self.layup_sections:
            SX = seg.remaining_splines

            #run through unique values in splines
            for sp in set(SX):

                #count the number of instances of spline delimitation 
                cnt = SX.count(sp)

                #if more than one of the same spline delimitation used, and excluding edge of part
                if (cnt > 1) and (sp != "'f'"):

                    #excessive count to start
                    min_count = 100
                    #counting the number of other plies between
                    counting = 0
                    start_counting = False

                    #iterating through complete SX, not just unique as above
                    for a in SX:
                        #when the "sp" spline is obtained start counting, or reset counting
                        if sp == a:
                            if (min_count > counting) and start_counting == True:
                                min_count = counting
                            counting = 0
                            start_counting = True
                        else:
                            counting += 1
                    
                    #print-out according to the rule
                    if min_count < 4:
                        stre = "If two plies are dropped at the same position there should be, at least, four plies between them."
                        stre += "There are only "+str(min_count)+" plies between two dropped-off plies at the spline "+str(sp)+".\n"
                        #avoid duplication
                        if stre not in self.report.warnings:
                            self.report.warnings += "\n"+stre+"\n"
                    else:
                        if reported == 0:
                            stre = "Dropping several plies at the same position is not recommended for drop offs with ramp in only one side.\n"
                            #avoid duplication
                            if stre not in self.report.suggested_checks:
                                self.report.suggested_checks += "\n"+stre+"\n" 
                            reported += 1

        return(self)

class r128(FactBase):

    #required variables
    holes: conlist(object, min_length=1)
    layup_sections: conlist(object, min_length=1)


    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        #Never terminate plies in fastener patterns
        for h in self.holes:
            for ls in self.layup_sections:
                i = 0
                while i < np.size(ls.pt_list,0):
                    #if any point on any spline is closer than radius from hole mid-point it is likely ply is being terminated at fastener location
                    dist = math.sqrt((h.position[0]-ls.pt_list[i].x)**2+(h.position[1]-ls.pt_list[i].y)**2+(h.position[2]-ls.pt_list[i].z)**2)
                    #1% larger hole for corner drop-offs
                    if dist < h.radius*1.01:
                        #print(h.radius)
                        #print(dist)
                        #print(h.position)
                        #print(ls.pt_list[i,:])
                        stre = "Never terminate plies in fastener patterns.\n"
                        stre += "Spline "+str(ls.sp_def)+ " crosses through hole located at : "+str(h.position)+".\n"
                        #avoid duplication
                        if stre not in self.report.design_errors:
                            self.report.design_errors += "\n"+stre+"\n" 
                        break
                    i = i + 1


        return(self)

class r146(FactBase):

    #required variables
    layup_sections: conlist(object, min_length=1)

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        #In areas of load introduction there should be equal numbers of +45° and -45° plies on each side of the mid-plane.

        for ls in self.layup_sections:
            cnt = len(ls.sequence)
            i = 0

            #for now taking it as literally +-45 no other similar angles considered here
            sp45_1 = 0
            sp45_2 = 0
            sm45_1 = 0
            sm45_2 = 0
            while i < cnt/2:
                if ls.sequence[i] == 45:
                    sp45_1 += 1
                elif ls.sequence[i] == -45:
                    sm45_1 += 1
                if ls.sequence[cnt-1-i] == 45:
                    sp45_2 += 1
                elif ls.sequence[cnt-1-i] == -45:
                    sm45_2 += 1
                i = i + 1
            
            #classified as suggestions because the tool cannot idenify area of load introduction
            if sp45_1 != sp45_2:
                stre = "In areas of load introduction there should be equal numbers of +45° and -45° plies on each side of the mid-plane."
                stre += "At the area delimited by "+str(ls.sp_def)+" the number of +45s is not even around the midplane.\n"
                #avoid duplication
                if stre not in self.report.suggested_checks:
                    self.report.suggested_checks += "\n"+stre+"\n"
            
            if sm45_1 != sm45_2:
                stre = "In areas of load introduction there should be equal numbers of +45° and -45° plies on each side of the mid-plane."
                stre += "At the area delimited by "+str(ls.sp_def)+" the number of -45s is not even around the midplane.\n"
                #avoid duplication
                if stre not in self.report.suggested_checks:
                    self.report.suggested_checks += "\n"+stre+"\n"

        return(self)

class r71(FactBase):

    #required variables
    layup_sections: conlist(object, min_length=1)

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
    #To minimise coupling effects, it is recommended to group the 45° and 135° plies in pairs 45°/135°. 
    #The following stacking sequence criterion is recommended: (45°/135°/…/135°/45°/…/135°/45°/…/45°/135°/…).
        for ls in self.layup_sections:
            trigger = False
            for i, a in enumerate(ls.sequence):
                #check for edge of layup numbering....

                #accomodate for 3 of these layers together? wont be flagged rn

                if (a == 45) or (a == -45):
                    if i == 0:
                        if (ls.sequence[i+1] != -a):
                            trigger = True
                    elif i == (len(ls.sequence)-1):
                        if ls.sequence[i-1] != -a:
                            trigger = True
                    else:
                        if (ls.sequence[i+1] != -a) and (ls.sequence[i-1] != -a):
                            trigger = True
                    
            if trigger == True:
                stre = "To minimise coupling effects, it is recommended to group the 45° and 135° plies in pairs 45°/135°."
                stre += "It appears that this is not the case in section delimited by "+str(ls.sp_def)+".\n"
                #suggested check as it is minor once balance and symmetry has been considered 
                #avoid duplication
                if stre not in self.report.suggested_checks:
                    self.report.suggested_checks += "\n"+stre+"\n"




        return(self)

class r139(FactBase):

    #required variables
    layup_sections: conlist(object, min_length=1)


    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        #Ply drop-offs should not exceed 0.010 inch (0.25mm) thick per drop for unidirectional. 139
        #Ply drop-offs should not exceed  0.015 inch (0.38 mm) thick per drop for fabric. 141
        
        
        #unique
        ptch  = []
        for ls in self.layup_sections:
            if ls.patch not in ptch:
                ptch.append(ls.patch)


        #assume it is ordered for now

        #self.layup_sections(key=lambda x: x.sp_len)
        #f = sorted(self.layup_sections, key=self.layup_sections[:].sp_len)#,reverse=True)
        for ref in ptch:
            c2 = 0
            c1 = 0
            for ls in self.layup_sections:
                spline_prev = ls.sp_def
                if c1 != 0:
                    c2 = c1
                c1 = ls.local_thickness
                #spline_prev = ls.sp_def

                if c2 != 0:
                    dif = abs(c2-c1)

                    if dif > 0.38:
                        stre = "Drop-off at one location should not exceed 0.38mm."
                        stre += "The drop-off is "+str(dif)+"mm at "+str(spline_prev)+".\n"
                        #suggested check as it is minor once balance and symmetry has been considered 
                        #avoid duplication
                        if stre not in self.report.suggested_checks:
                            self.report.suggested_checks += "\n"+stre+"\n"
                        
                    elif dif > 0.25:
                        #here suggestion only as not sure if UD
                        stre = "Drop-off at one location should not exceed 0.25mm for unidirectional and 0.38 for woven fabric."
                        stre += "The drop-off is "+str(dif)+"mm at "+str(spline_prev)+".\n"
                        #suggested check as it is minor once balance and symmetry has been considered 
                        #avoid duplication
                        if stre not in self.report.suggested_checks:
                            self.report.suggested_checks += "\n"+stre+"\n"

        return(self)
    


class r400(FactBase):
    #required variables
    min_major_radii: float = Field()
    mmr_location: object = Field()

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        #Rads below 3mm are typically not inspected, check with NDT if this is required. 

        if self.min_major_radii < 3:

            stre = "\n Major radius of "+str(self.min_major_radii) \
                                            +" mm was identified at the following location: "+str(self.mmr_location) \
                                            +". Rads below 3mm are typically not inspected,"\
                                            +"check with NDT if this is required. \n \n"
            
            #avoid duplication
            if stre not in self.report.suggested_checks:
                self.report.suggested_checks += stre
        
        return(self)

class r401(FactBase):

    #required variables

    #the below or curvature
    min_major_radii: float = Field()
    MR_list: list = Field()
    FL_points: list = Field()


    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        #If 2 or more radii of different values below 125mm are present in the design. : Check your curvatures, 
        #it is recommended that similar curvatures are used when below 125mm, as bespoke probes will likely be required.

        rad_list = []
        for circ in self.MR_list:
            #remove points that are tagged as fillets - not relevant (fillet search need more testing!)
            FL_tagged = False
            for FL_any in self.FL_points:
                dist = math.sqrt((circ.centre[0]-FL_any[0])**2+(circ.centre[1]-FL_any[1])**2+(circ.centre[2]-FL_any[2])**2)
                if dist == 0:
                    FL_tagged = True

            if FL_tagged == False:
                #Potentially add some tolerance 
                #e.g. 1mm and 1.01mm can be considered same radius for practical puproses, but where is the treshold? 
                if circ.r < 125:
                    if circ.r not in rad_list:
                        #fillets don't count!
                        #But this might required some checking -- do I trust "fillet" gnn enought? 
                        #Maybe compare votes if in conflict -- i.e. both MR and fillet?
                        rad_list.append(circ.r)

        #check if .step file exits - if step file exists 1 radius is effectively 2 due to thickness.
        #Therefore in case of solid step file ">2" is equal to ">1" for surfaces
        
        #this ^^ check is currently disabled as solids are created when they dont exist before
        
        #if (((len(rad_list) > 1) and (self.step_file == None))
        #    or ((len(rad_list) > 2) and (self.step_file != None))):
        if (len(rad_list) > 2):
            ####
            stre = str(len(rad_list))+" major radii are different size."\
                    + " If multiple different radii values below 125mm are present"\
                    + " multiple probes will likely be required  for inspection. \n"\
                    + " For more information seek feedback from NDT/metrology team.\n \n"
            #avoid duplication
            if stre not in self.report.suggested_checks:
                self.report.suggested_checks += stre
        #Potentially fix: this sometimes considers other side of same radius different radius
        #^^ add a proximity fileter?
        #print(self.uniform_material, "uniform material")
        return(self)
    
class r402(FactBase):

    #required variables
    #materials in database require type column: GFRP/CFRP/....


    #layup_sections: conlist(object, min_length=1)

    
    uniform_material: bool = Field()

    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):
        #Potential issues with attenuation from GRP layers. 
        #If GRP involved in the stack is over 1mm, check the attenuation charts for your specific frequency used. 
        #https://nationalcompositescentre.sharepoint.com/:b:/s/NCC-CoSinC85/EdLNWUUuXDNLj6UFZSBgDHoB0RAMPedN4cfktxJb563r1Q?e=yAWqAN 
        stre = "If GRP involved in the stack is over 1mm, check the attenuation "\
                +"charts for your specific frequency used at :"\
                +"https://nationalcompositescentre.sharepoint.com/:b:/s/NCC-CoSinC85/EdLNWUUuXDNLj6UFZSBgDHoB0RAMPedN4cfktxJb563r1Q?e=yAWqAN.\n \n"
        
        if self.uniform_material == True:
            if ("GRP" in self.material_u) or ("GFRP" in self.material_u):
                self.report.warnings += stre
        else:
            #check if there is more then 1mm of GRP
            GFRP = 0
            for ls in self.layup_sections:
                #print(ls.materials)
                for mat in ls.materials:
                    #GFRP?
                    if ("GRP" in mat.mat_type) or ("GFRP" in mat.mat_type):
                        GFRP += mat.l_thick
                #print(GFRP, " GFRP thickness")
                #if so, instruct to check and give link to attenuation charts 
                if GFRP > 1:
                    self.report.warnings += stre
                    break
                

        
        return(self)   



'''
class r35(FactBase):

    #required variables


    def __init__(self, d: FactBase):
        self = FactBase.__init__(self, **d.__dict__)

    def solve(self):

        return(self)


'''