CATIA
=================
CATIA plug-in requires several bespoke scripts to function. Most of the bespoke CATIA functions are within CATIA.utils.py. 

For step file exports the function ''CATIA_utils.export_step()'' is used:

.. py:function:: CATIA_utils.export_step()

	This function allows for generation of thicknesses based on tool surface and defined layup. Once the solid was created part will be saved as .CATpart and .stp. For more details refer to annotations in code.
	
	:param d: DesignVariables class, refer to :doc:`FactBase` for details
   
.. py:function:: CATIA_utils.hole_loc()

	This function is only  used when GNN for hole identificaiton is not available. It requires holes geometry to be defined in dedicated geometry set in CATIA.
	
	:param part: path to the part store as string
	
The two functions above are used directly by pre_base.py in specific pre-rules.

.. py:function:: CATIA_utils.GNN_validation()
	
	This is manually  edited function that is used to validate GNN functionality. It collects gemetry identified and displays it in CATIA.


