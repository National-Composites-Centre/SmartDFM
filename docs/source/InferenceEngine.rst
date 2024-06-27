Inference Engine
================

Inference engine is is the component of SmartDFM that compares the rules against the part currently being designed. In case of SmartDFM this has two steps both driven from `bd_main.py`:

#. Execution of pre-rules:

The functions in pre_base.py are all numbered [p1,p2,p3,....,px]. This is so these can be easily iterated throuhg. The active pre-rules are specified in the 'active_pre' list.

.. code-block:: python

	active_pre = [1,3,4,5,8,9,10,11,12,13,14,15,16] 
	
The pre-rules need to be run in different order based on what information is available in the part. The mechanism for doing this is shown below. The pre-rules list is iterated through. Pre-rule is run if all required pre-requisite parameters are already available in FactBase variable that is being passed in/out. If any pre-rule has been triggered the list is iterated through again. Only once no pre-rule is triggered in cycle the information collection is deemed finished. Each pre-rule has built in features that prevent it from running more than once.

.. code-block:: python
	
	while d.ite > 0:
		#d.ite remains 0 if no change has been done to 'd'
		d.ite = 0

		for i in active_pre:
			if d.runtime_error != None:
				#error handling - displays error that made SmartDFM crash in place of the report
				d.report.design_errors = d.runtime_error
				d.report.warnings = ""
				d.report.suggested_checks = ""
				d.report.check_issues = ""
				d.ite = 0
				break 
				
			#build allows for iteration throuhg pre_base.py functions
			build_func = "problem = pre_base.p"+str(i)+"(d)"
			
			#validation error simply means pre-requisites have not been met
			try:
				exec(build_func)
				d = problem.solve()
			except ValidationError as e:
				#print(e)
				p = 1
		print("d.ite",d.ite)

#. Execution of rules:

Active rules are again specified with a list. However, here the numbers are also used as reference to local NCC rule database.
	
.. code-block:: python

    active_rules =  [35,36,71,83,85,86,91,92,95,128,133,134,135,130,139,144,146,151,166,400,401,402]
	
Rule execution follow similar logic to pre-rules with 2 notable differences. Firstly, the rules list is only iterated through once, as execution of a rule should not affect ability of other rules to be evaluated. Secondly, additional error handling is nested, so that user is informed about rules which were not executed. However, one broken rule does not stop other rules from being executed.
	
.. code-block:: python
	
	#Rules running only once, rule results are text, should not affect the ability of other rules to be checked.
	#temp:
	if d.runtime_error == None:
		for i in active_rules:
			#build function to execute - functions are named according to lists
			build_func = "problem = rule_base.r"+str(i)+"(d)"
			print(build_func)
			#Two levels of error handling, inner loop checks for missing information.
			#Missing information is not technically an error, but intended method for 
			#skipping rules that don't apply.
			#Outter loop error handling actually covers for code errors in individual 
			#rules.
			try:
					#is this too brute force ?
				try:
					exec(build_func)
					d = problem.solve()
					#print("updated, here add some iterator to check when rules triggered")
				except ValidationError as e:
					#print(e)
					#print("Rule "+str(i)+" not checked")
					stre = "Rule "+str(i)+" not checked due to missing information."
					#consider printing some part of the actual error?
					d.report.check_issues += "\n"+stre +"\n"
			except Exception as er:
				#print(er)
				#print("Rule "+str(i)+" not checked")
				stre = "Rule "+str(i)+" not checked due to DFM tool error."
				#consider printing some part of the actual error?
				d.report.check_issues += "\n"+stre +"\n"