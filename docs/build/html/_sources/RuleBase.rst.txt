Rule Base
=========

Rule base is Python translation of selected rules from:

https://nationalcompositescentre.sharepoint.com/:x:/s/NCC-CoSinC85/EVnE6qVamgVDs-nZYmMgltwBxFuaKF5oQWwQbED6xMhYzA?e=qVhCUa

To implement new rule it is recommended that template provided as "rXX" is followed. This is included in RuleBase.py and is shown below.


.. _target to code:

.. code-block:: python

	#rXX is an example/template rule, explaining typical features of how the rules are structured
	class rXX(FactBase):
		#Required variables (examples for various types:)
		tool_gender: str = Field("male")
		min_major_radii: float = Field() 
		mmr_location: object = Field()
		layup_sections: conlist(object, min_items=1) #at least one object must exist in this list
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