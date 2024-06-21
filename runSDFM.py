
       
import rule_base
import pre_base
from fact_base import FactBase, layup
import win32com.client.dynamic

from time import perf_counter
import sys

#Pydantic library is used to validate inputs to pre-rules and rules
from pydantic import ValidationError

import rule_base
import pre_base
from fact_base import FactBase, layup
import win32com.client.dynamic

from time import perf_counter
import sys
import os

def sDFM(part,location):

    version = str(3.0)

    #try: 
    CATIA = win32com.client.Dispatch("CATIA.Application")
    partDocument2 = CATIA.ActiveDocument
    cat_name = CATIA.ActiveDocument.Name
    cat_name = cat_name.split(".CATPart")[0]
    #except:
    #    cat_name = "Enter name here"

        
    t1_start = perf_counter()

    #self.t3.text = "evaluating"
    #initiate fact class
    d =  FactBase()

    #here UI to run with CATIA (or elsewhere)
    d.version = version
    d.part_name = cat_name #self.lfn.text
    ptemp = "C:\\code\\fls"#self.sef.text
    ptemp = ptemp.replace("/","\\")+"\\"
    d.path = ptemp


    active_pre = [1,3,4,5,8,9,10,11,12,13,14,15,16] 

    #d.step_file = "D:\\CoSinC_WP4.2\\TestCad\\AUTO-TESTING\\MR_49_10.stp"
    #d.step_file = "D:\\Kestrel\\conceptual outer pv\\c4\\bulkhead_c4_v0.stp"
    #d.step_file = "D:\\CoSinC_WP4.2\\TestCad\\AUTO-TESTING\\FL_19.stp"
    #active_pre = [16]

    #p6 too flexible - make it into two - one for angle, on for radius

    #7 included in 4

    #14 will be used for testing- and later adjusted for integration - once WS radius is re-trained

    #these rules are numbered according ty Bryn's design rules document
    active_rules =  [35,36,71,83,85,86,91,92,95,128,133,134,135,130,139,144,146,151,166,400,401,402]

    #under construction: 400,401,402

    #78 temporarily disabled

    #runs until rules dont make any change to fact base
    #for now just run once....

    #eventually control the running of rules through pydantic library only!!


    while d.ite > 0:
        d.ite = 0
        #store current version of d in dold
        #dold = d.copy()

        for i in active_pre:
            if d.runtime_error != None:
                #error handling - displays error that made SmartDFM crash in place of the report
                d.report.design_errors = d.runtime_error
                d.report.warnings = ""
                d.report.suggested_checks = ""
                d.report.check_issues = ""
                d.ite = 0
                break 
                

            #build function to execute - functions are named according to lists
            build_func = "problem = pre_base.p"+str(i)+"(d)"
            print(build_func)
            try:
                exec(build_func)
                d = problem.solve()
                print("updated, here add some iterator to check when rules triggered")
            except ValidationError as e:
                print(e)
            p = 1
        print("d.ite",d.ite)

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

                    print(e)
                    #print("Rule "+str(i)+" not checked")
                    stre = "Rule "+str(i)+" not checked due to missing information."
                    #consider printing some part of the actual error?
                    d.report.check_issues += "\n"+stre +"\n"
            
            except Exception as er:

                print(er)
                #print("Rule "+str(i)+" not checked")
                stre = "Rule "+str(i)+" not checked due to DFM tool error."
                #consider printing some part of the actual error?
                d.report.check_issues += "\n"+stre +"\n"
                
    t1_stop = perf_counter()
    lapsed = t1_stop-t1_start


    total_report = d.report.design_errors +"\n"+d.report.warnings+"\n"+\
                    d.report.suggested_checks+"\n"+d.report.check_issues+\
                        "\n This report is also availble at "+d.path+" as a .txt file"+\
                            "\n"+"\nSmartDFM "+d.version+"\n\n"+"Design was checked in "+str(lapsed)+" seconds."
    #window['-INPUT0-'].Update(total_report)
    #self.t3.text = total_report


    print(d.report.design_errors)
    print(d.report.warnings)
    print(d.report.suggested_checks)

    f = open(d.path+d.part_name+"_report.txt", "a")
    f.write(d.report.design_errors+d.report.warnings+d.report.suggested_checks+d.report.check_issues+"\n"+"\nSmartDFM "+d.version)
    f.close()



