Pre-Base
=========

pre_base.py is list of functions that help collect facts required for evaluation of rules (in Rule Base).

This includes variety of smaller scripts, and references to larger applications such as the GNNs or step interogation script libraries.

.. _target to code:

.. code-block:: python

	class pXX(FactBase):
		#pXX serves as rough template for a pre-rule. This will not be executed. Only numbered rules are executed.

		#Required variables (examples for various types:)
		tool_gender: str = Field("male")
		min_major_radii: float = Field() 
		mmr_location: object = Field()
		layup_sections: conlist(object, min_items=1) #at least one object must exist in this list
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