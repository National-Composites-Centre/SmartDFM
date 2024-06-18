Development notes
=================



Preparation
-----------

Currently no fully packaged version exists. 

The developer installation is therefore the same as user installation.

#. Use "git clone" on the "main" branch of https://github.com/JKucera-NCC/SmartDFM . The main branch has the latest tested version.
#. Set up the Python environment from sdc.yml.
#. Basic graph neural network models (GNNs) are cloned with the repo, for alternative feature recognition algorthms please refer to :doc:`FeatureRecognition`.
#. For proper usage of SmartDFM composite definition will also have to be generated. The only composite definition currently integrated is the "layup definition" method, available at https://github.com/JKucera-NCC/LayupDefinition. For installation of this refer to the local documentation. [ref. the LD docs...]


Reworking and adding rules
--------------------------

To rework rules refer to annotations within the respective rules. Any changes should be reflected in the annotations. Refer to :doc:`RuleBase` for rule template with all key aspects. It is good practice to keep local written up rule database that feeds into the Python implemented rules. 

Developers should have good overview of rules already implemented to avoid duplication or conflicts.

When creating new rule developer should think about the information that feeds into the rule. If the pre-requisites to evaluating the rule are already defined in :doc:`FactBase` and obtained through :doc:`PreBase`, the only development required is the rule itself. Otherwise additinal developments might be required.

Pre-rules development
---------------------

The developments to pre_base.py are quite varied, but here are few points that should be followed:

* Highly complicated pre-rules should use external function. For example CAD related manipulation should be in step_utils.py, CATIA_utils.py, or equivalent for other software.
* Way to prevent re-run of the rule should be implemented.
* The run-time of the pre-rule should be considered; if run-time very high the cost vs benefit of the information obtained should be evaluated.



components of the system
------------------------
.. toctree::
	:maxdepth: 1

	FactBase
	
	PreBase
	
	RuleBase
	
	FeatureRecognition

	InferenceEngine
	
	CATIA



