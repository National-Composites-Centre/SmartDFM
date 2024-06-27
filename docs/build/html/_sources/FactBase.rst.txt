Fact Base
=========

Fact base serves as overall storage of variables and references for a part in question. The existence, or non-existence, of information in the FactBase class informs which pre-rules and rules need to be executed. 

The pre-rules focus on updating the FactBase using various mechanisms.

The rules use the FactBase to verify which of the parameters are in conflict with the rules.

The class uses Pydantic definition, which facilitates the rules execution, details are described in :doc:`InferenceEngine`

Usage and parameters
--------------------


fact_base.py includes information on what most variables represent

To create a default list of variables, stored in Pydantic class: ``fact_base.FactBase`` :

.. py:function:: fact_base.FactBase()

	This should list all possible facts in the fact base. For default values see the fact_base.py directly.
	
	:param holes: list - the holes list contains list containing "hole" class members
	:param layup_sections: list - list of "layup_section" objects
	:param max_ply_layup: list - layup with all available plies included (drop-offs considred within layup-sectiosn)
	:param layup_file: str - location of layup file if available
	:param uniform_material: bool - only one material used? True if yes
	:param material_u: object - only for uniform materials
	:param step_file: str - step file path
	:param load_direction: list - [x,y,z] vector (CURRENTLY NOT USED - relevant rules yet to be implemented)
	:param edge_points: object - all spline points for the edge
	:param edge_len: float - lenght of the ege spline
	:param tool_gender: str - male or female tool (only "male" and "female" accepted)
	:param MR_points: list - list of 3d points from WS that correspond to major radii
	:param FL_points: list - list of points relevant to fillets (from WS)
	:param min_major_radii: float - this is the smallest of major radii
	:param mmr_location: object - position of min_major_radius
	:param MR_list: list - list of Major Radii
	:param layup_max_thickness: float - The maximum thickness of laminate anywhere on the part.
	:param major_shape_angle: float - for now just flange angle, but will include any sharp geometry changes
	
	The output report is a string for now
	
	:param report: object - Field(report())
	:param runtime_error: str - Field(None)
	
	For reference:
	
	:param version: str - version of SmartDFM tool
	:param part_name: str - make this unique identifier when storage sorted?
	:param path: str - full path to the main run directory
	:param ite: int
	
	Right now the below is manually edited, it should be replaced by GNN plugin.
	
	:param flange: bool - Field(None)

.. py:function:: fact_base.vert()

	:param x: float 
	:param y: float
	:param z: float
	:param ID: int
	:param NeLi: list - list of neighbouring vertices (connected by some form of line/curve)

			
.. py:function:: fact_base.hole()

	Specialised class to hold information about individual hole.
	
	:param radius: float - describing the radius of the main portion of the hole
	:param type: str - destribes the type of hole, currently only "through_simple" type is used, but more types should be introduced
	:param position: object - 1:3 numpy array consisting x-y-z coordinates of the hole 
	:param direction: object - 1:3 numpy array consisting of x-y-z vector
	:param edge_distance: float - calculated distance from hole to nearest part edge_distance
	:param vert_list: list - list of vertices identified as part of this hole's definition (x-y-z coordinates for each)


.. py:function:: fact_base.material()
	
	:param mat_name: str  - reference name for material in :doc:`layup database`
	:param mat_type: str  - type of material as taken from :doc:`layup database`, eg.: GFRP,CFRP...
	:param l_thick: float - layer thickness in mm
	

.. py:function:: fact_base.layup()

	This class should contain all details regarding layup in specific area delimted by defined spline.
	
	:param balanced: bool - True/False , is laminate balanced?
	:param symmetric: bool - True/False, is laminate symmetric? (This does not duplicate the layup, it is simply an observation on details contained in 'sequence')
	:param sequence: list - simple list of layer primary orientations, should contain all layers. The values should be floats expressed in degrees from -90 to 90. 
	:param sp_def: str - reference name for delimiting spline from CAD system
	:param sp_len: float - calculated lenght/circumference of the delimiting spline 
	:param patch: int - arbitrarily designated patch number. This is used to iterate between zones with different layup.
	:param origin: object - vector definition of average point
	:param pt_list: object - all spline points
	:param mind: float - minimum distance from other drop-off spline
	:param close_other: str - closest drop-offs - corresponds to mind
	:param local_thickness: float - local laminate stack thickness
	:param local_holes: list - list of hole objects relevant for this patch/section/layup
	:param overlap: bool - True if delimiting splines close to or on edges
	:param remaining_splines: list - the corresponding spline delimitations for remianing plies 
	:param materials: list - contains "material" class variables

.. py:function:: fact_base.report()

	This class is used to forms the report, the main output of the DFM package. The default values denote the headings of each of the report sections. The rest of these variables is filled by rules triggered.
	
	:param warnings: str - Default value = "\n             WARNINGS:  \n" - user likely needs to address this
	:param design_errors: str - Default value = "\n             DESIGN ERRORS: \n" - user must address this
	:param suggested_checks: str - Default value = "\n             SUGGESTED CHECKS: \n" - only informs user, might not need to be actioned
	:param check_issues: str - Default value = "\n              DESIGN CHECK ISSUES: \n" - notes on what check was skipped

Reference documents
-------------------
.. toctree::
	layup database

