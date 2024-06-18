import random
import os
import os.path
import sys

from typing import Any, Iterable, Iterator, List, Optional, Tuple

from OCC.Core.BRep import BRep_Tool, BRep_Builder
from OCC.Core.BRepTools import BRepTools_WireExplorer
from OCC.Core.gp import gp_Ax2, gp_Dir, gp_Pnt
from OCC.Core.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCC.Core.HLRAlgo import HLRAlgo_Projector
from OCC.Core.TopAbs import (
    TopAbs_VERTEX,
    TopAbs_EDGE,
    TopAbs_FACE,
    TopAbs_WIRE,
    TopAbs_SHELL,
    TopAbs_SOLID,
    TopAbs_COMPOUND,
    TopAbs_COMPSOLID,
    TopAbs_ShapeEnum,
)
from OCC.Core.TopExp import TopExp_Explorer, topexp_MapShapesAndAncestors
from OCC.Core.TopTools import (
    TopTools_ListIteratorOfListOfShape,
    TopTools_IndexedDataMapOfShapeListOfShape,
)
from OCC.Core.TopoDS import (
    topods,
    TopoDS_Wire,
    TopoDS_Vertex,
    TopoDS_Edge,
    TopoDS_Face,
    TopoDS_Shell,
    TopoDS_Solid,
    TopoDS_Shape,
    TopoDS_Compound,
    TopoDS_CompSolid,
    topods_Edge,
    topods_Vertex,
    TopoDS_Iterator,
)
from OCC.Core.GCPnts import (
    GCPnts_UniformAbscissa,
    GCPnts_QuasiUniformDeflection,
    GCPnts_UniformDeflection,
)
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve

from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Display.SimpleGui import init_display

from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Extend.DataExchange import read_step_file
from OCC.Extend.TopologyUtils import dump_topology_to_string

def dtts2(shape: TopoDS_Shape, level: Optional[int] = 0, buffer: Optional[str] = "") -> None:
    """
    Return the details of an object from the top down
    """
    brt = BRep_Tool()
    sss = ""
    s = shape.ShapeType()
    
    if s == TopAbs_VERTEX:
        pnt = brt.Pnt(topods_Vertex(shape))
        #print(".." * level + f"<Vertex {hash(shape)}: {pnt.X()} {pnt.Y()} {pnt.Z()}>\n")
        sss += ".." * level + f"<Vertex {hash(shape)}: {pnt.X()} {pnt.Y()} {pnt.Z()}>\n"
        #print(sss)

    else:
        #print(".." * level, end="")
        #print(shape)
        sss += ".." * level
        #print(sss)
    it = TopoDS_Iterator(shape)
    while it.More() and level < 5:  # LEVEL MAX
        shp = it.Value()
        it.Next()
        with open("D:\\CoSinC_WP4.2\\xxxyyy.txt", "a") as text_file:
            #print(sss)
            text_file.write(str((sss)))
        dtts2(shp, level + 1, buffer)
    
    #with open("D:\\CoSinC_WP4.2\\xxxyyy.txt", "a") as text_file:
    #    #print(sss)
    #    text_file.write(str((sss)))

def dtts3(shape: TopoDS_Shape, level: Optional[int] = 0, buffer: Optional[str] = "") -> None:
    """
    Return the details of an object from the top down
    """
    brt = BRep_Tool()
    sss = ""
    s = shape.ShapeType()
    print(dir(s))
    
    if s == TopAbs_VERTEX:
        print("here")
        pnt = brt.Pnt(topods_Edge(shape))
        #print(".." * level + f"<Vertex {hash(shape)}: {pnt.X()} {pnt.Y()} {pnt.Z()}>\n")
        sss += ".." * level + f"<Edge {hash(shape)}: {pnt.X()} {pnt.Y()} {pnt.Z()}>\n"
        #print(sss)

    else:
        #print(".." * level, end="")
        #print(shape)
        sss += ".." * level
        #print(sss)
    it = TopoDS_Iterator(shape)
    #print(it)
    while it.More() and level < 5:  # LEVEL MAX
        print("here2")
        shp = it.Value()
        it.Next()
        with open("D:\\CoSinC_WP4.2\\xxxEdge.txt", "a") as text_file:
            #print(sss)
            text_file.write(str((sss)))
        dtts2(shp, level + 1, buffer)
    

    


#compound = read_step_file(os.path.join("..", "assets", "models", "D:\CoSinC_WP4.2\s-1.stp"))
compound = read_step_file("D:\CoSinC_WP4.2\s-1.stp")#,return_as_shapes=True)

#x = TopologyExplorer(compound, ignore_orientation=True)

#this basically lits all vretices under appropriate edges, similar to the step file, just a different format...
y = dtts2(compound)
#dtts2 is an adjusted version which allows for saving in .txt files -- should be checked for duplication (inate iteration weird, loops itself)

#with open("D:\\CoSinC_WP4.2\\xxxyyy.txt", "w") as text_file:
#    text_file.write(str((y.value)))

'''
read_step_file(filename, return_as_shapes=False, verbosity=True)
read the STEP file and returns a compound filename: the file path return_as_shapes: optional, False by default. If True returns a list of shapes,

else returns a single compound

verbosity: optional, False by default.
'''





#print(compound)

#print(dir(compound))

#print(hasattr(compound,"Convex"))
#print(hasattr(compound,"Concave"))

#print(compound.Convex())
#print(compound.Convex)

#TopoDS_Vertex
#print(compound.HashCode())

#TopoDS_Vertex()


