Development notes
=================



Preparation
-----------

Currently no fully packaged version exists. 

The developer installation is therefore the same as user installation.

#. Use "git clone" on https://github.com/National-Composites-Centre/SmartDFM , to understand diefference between version and branches please navigate to :doc:`Versions`. The main branch has the latest tested version.
#. Set up the Python environment from sdc.yml.
#. Basic graph neural network models (GNNs) are cloned with the repo. However, please refer to :doc:`GNN usage` for setup. For alternative feature recognition algorthms please refer to :doc:`FeatureRecognition`.
#. For proper usage of SmartDFM composite definition will also have to be generated. The only composite definition currently integrated is the "layup definition" method, available at https://github.com/National-Composites-Centre/LayupDefinition. For installation of this refer to the local documentation. [ref. the LD docs...]


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



Components of the system
------------------------
.. toctree::
	:maxdepth: 1

	FactBase
	
	PreBase
	
	RuleBase
	
	FeatureRecognition

	InferenceEngine
	
	CAD


Error handling
--------------

It is undesirable for the whole SmartDFM to fail when specific rule or pre-rule fails. However, user should know that an error occured, as not to asume certain rules were followed correctly.

Therefore when running rules 'try' clauses are used, and when error occurs the likely cause of the error along with the rule number are recorded. This is later provided as part of the SmartDFM report.

The following code shows the implementation of this for rules, for pre-rules this is simpler as the result of an error will be missing information, which is flagged under rules errors.

.. code-block:: Python

	try:
		try:
			d = i(d).solve()

		except ValidationError as e:

			stre = "Rule "+str(i)+" not checked due to missing information."
			d.report.check_issues += "\n"+stre +"\n"
	
	except Exception as er:
		stre = "Rule "+str(i)+" not checked due to DFM tool error."
		d.report.check_issues += "\n"+stre +"\n"