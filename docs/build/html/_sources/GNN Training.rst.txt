GNN Training
============

Overview
--------

The goal is to create maximum variation in example parts while mainitainig clear idea what the training feature is supposed to look like.

Originally, large dataset was created for training of multiple features. However, that would requir extreme flexibility of the script to do for parts representative of real enginerring solutions. Therefore the approch was changed to trining for specific feature. Every node is binary: either it corresponds to trained feature, or it doesn't. This requires larger datasets, but the datasets are easier to create with sufficient relevant variation.

The code for the training datast generation is stored in cad_generation sub-folder of this repository.

Metadata 
--------

The metadate identifies nodes corresponding to the feature of interest(show example).

Usually the nodes are identified by comparing .stp file of part without the feature implemented and the .stp file with the feature in place. This is not bulletproof as some nodes generated are very specific and might not be good representation of the feature. However, that is very rare occurance according to current experience.



CAD generation
--------------

CAD generation scripts are available in "cad_generation" sub-folder. The general script components are listed below:

- the standard components 
	- call catia 
	- create part without feature
	- save and save points
	- create feature
	- compare points
	- save + metadata
	- method for keeping the iteration running through error handling when issues arrise

