
Main documentation available at : https://national-composites-centre.github.io/SmartDFM/ .


The below is a legacy Readme.


# Introduction 
This repository supports the development of smart DFM design check. Along with the main DFM scripts it also
contains an assortment of standalone scripts used to generate CAD samples for Wild Strawberries project, 
and to extract specific features out of .step files 

# List of important scripts:
[This list has been superceeded by an excel list of scripts included in the repository]:

vecEX2_C.py - extraction of vectors from .wrl files (CATIA export) -- original script taken from https://github.com/Ellutze/sysi
validation.py - plots vertices provided along with .step file over CATIA model to check correct alignment of metadata with CAD
step_utils.py - important set of functions for interogation of .step files -- loop that follow references linked to specific features
step_features.py - extracts attributes from features within step files
prelim_shapes.py - allows for automated creation of specific features in CAD
main.py - governs generation of CAD datasets, heavily uses prelim_shapes.py 
CATIA_utils.py - miscellaneous CATIA scripts
ED.py - attribute extraction for hole distance from closest edge
design_review - takes information from GNN regarding vertex-feature relations and runs appropriate attribute extraction scripts


#other relevant resources

#pythonocc library has been reviewed, the examples trialed are at https://github.com/tpaviot/pythonocc-demos/tree/master/examples
#scripts used for testing:
test2.py
test3.py
step_out.py
edge.py


# Unused, kept for reference:
wp4_utils.py
CAD_libGen.py : generates V spars and pockets. This has not been used for trainig of the GNN in the end.
working_backup.py
unused_features.py
looping_philosophy.py : sidetracked by OCC where unconventional looping method was encountered 


