from pydantic import BaseModel, Field, conlist
import numpy as np
from typing import Optional

import CompositeStandard

#Some of the classes below might be obsolete due to usage of CompositeStandard which houses many of these variables

class vert(BaseModel):
    x: float = Field(None)
    y: float = Field(None)
    z: float = Field(None)
    ID: Optional[int] = Field(None)
    NeLi: Optional[list] = Field([]) # Neighbour list
    #min_dist: float = Field([]) #minimum found distance to another vertex on same hole

class hole(BaseModel):
    #fits into "holes" list in main FactBase
    radius: Optional[float] = Field(None,ge=0) 
    type: Optional[str] = Field("through_simple") #currently unused
    #list more options later: throuth_countersunk, through_stepped, partial_simple, partial_countersunk, partial_stepped...
    position: Optional[object] = Field(np.asarray([[0,0,0]]))
    direction: Optional[object] = Field(np.asarray([[0,0,0]]))
    edge_distance: Optional[float] = Field(None,ge=0)
    vert_list: Optional[list] = Field([]) #list of vertices identified for this hole
    
class material(BaseModel):
    mat_name: str = Field(None) #identification of material as present in LD_layup_database.txt
    mat_type: str = Field(None) # GFRP/CFRP/...
    l_thick: Optional[float] = Field(None) #layer thickness

class layup(BaseModel):

    balanced: Optional[bool] = Field(None)
    symmetric: Optional[bool] = Field(None)
    sequence: Optional[list] = Field(None) #eg [90,45,45,90]
    sp_def: Optional[str] = Field(None) #delimiting spline
    sp_len: Optional[float] = Field(None) #length of delimiting spline in mm
    #unbalanced_ply: int = Field(None)
    patch: Optional[int] = Field() #arbitrarily designated patch number
    origin: Optional[object] = Field(np.asarray([[0,0,0]])) #vector definition of average point
    pt_list: Optional[object] = Field() # all spline points
    mind: Optional[float] = Field(999999.0,ge=0) #minimum distance from other drop-off spline
    close_other: Optional[str] = Field(None) # closest drop-offs - corresponds to mind
    local_thickness: Optional[float] = Field(None)
    local_holes: Optional[list] = Field([])
    overlap: Optional[bool] = Field(True) #delimiting splines close to or on edges
    remaining_splines: Optional[list] = Field([]) #the corresponding spline delimitations for remianing plies 
    materials: Optional[list] = Field([]) # contains "material" class variables

class report(BaseModel):
    #this class forms the main output of the DFM package
    warnings: str = Field("\n             WARNINGS:  \n") #user likely needs to address this
    design_errors: str = Field("\n             DESIGN ERRORS: \n") #user must address this
    suggested_checks: str = Field("\n             SUGGESTED CHECKS: \n") #only informs user, might not need to be actioned
    check_issues: str = Field("\n              DESIGN CHECK ISSUES: \n") #notes on what check was skipped

class FactBase(BaseModel):
    """
    This should list all possible facts in the fact base.
    Default values can be included.
    """
    StandardLayup: Optional[object] = Field(None)

    refFileExt: Optional[str] = Field(None) #source file extension
    holes: Optional[list] = Field(None) #empty list of holes on default - is fitted with hole class
    layup_sections: Optional[list] = Field(None) #default value is empty class 
    max_ply_layup: Optional[list] = Field(None) #layup with all available plies included (drop-offs considred within layup-sectiosn)
    all_relimitations: Optional[list] = Field(None)
    layup_file: Optional[str] = Field(None) #is layup file available?
    uniform_material: Optional[bool] = Field(None) # only one material used? True if yes
    material_u: Optional[object] = Field(None) #only for uniform materials
    step_file: Optional[str] = Field(None) #step file
    load_direction: Optional[list] = Field(None) # [x,y,z] vector 
    edge_points: Optional[object] = Field(None)# all spline points for the edge
    edge_len: Optional[float] = Field(None) #lenght of the ege spline
    tool_gender: Optional[str] = Field(None) # male or female tool (only "male" and "female" accepted) -----#force this in pydantic?
    
    #MajorRadius: bool = Field(None) #True if at least 1 MR relevant vertex was identified from WS
    MR_points: Optional[list] = Field(None) #list of 3d points from WS that correspond to major radii
    FL_points: Optional[list] = Field(None) #list of points relevant to fillets (from WS)
    min_major_radii: Optional[float] = Field(None) #this is the smallest of major radii
    mmr_location: Optional[object] = Field(None) #position of min_major_radius
    MR_list: Optional[list] = Field(None) # list of Major Radii
    layup_max_thickness: Optional[float] = Field(None) 
    major_shape_angle: Optional[float] = Field(None) #for now just flange angle, but will include any sharp geometry changes
    layup_splines: Optional[list] = Field(None)

    #the output report is a string for now
    report: object = Field(report())
    runtime_error: Optional[str] = Field(None)

    #is defined?
    #layup_sections: holes(hole, min_items=0) #this is how verified in rules and pre-rules
    #layup_sections: conlist(layup, min_items=1)

    #For reference
    version: str = Field(None) #version of SmartDFM tool
    part_name: str = Field(None) #make this unique identifier when storage sorted?
    path: Optional[str] = Field(None) #full path to the main run directory
    ite: int = Field(1)


    #right now the below is manually edited, it should be replaced by WS plugin 

    #contains features
    flange: Optional[bool] = Field(None)
    
    