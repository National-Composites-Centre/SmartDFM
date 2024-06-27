
       
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

    version = str(4.1)
        
    t1_start = perf_counter()

    #self.t3.text = "evaluating"
    #initiate fact class
    d =  FactBase()

    #here UI to run with CATIA (or elsewhere)
    d.version = version
    d.part_name =  part #self.lfn.text
    ptemp = location
    ptemp = ptemp.replace("/","\\")+"\\"
    d.path = ptemp

    p = pre_base

    #bit cured #TODO make this auto generate?
    active_pre = [p.p1,p.p3,p.p4,p.p5,p.p6,p.p7,p.p8,p.p9,p.p10,p.p11,p.p12,p.p13,p.p14,p.p15,p.p16] 

    #TODO p6 too flexible - make it into two - one for angle, on for radius

    #TODO 14 will be used for testing- and later adjusted for integration - once WS radius is re-trained

    #these rules are numbered according ty Bryn's design rules document
    r = rule_base
    active_rules =  [r.r35,r.r36,r.r71,r.r83,r.r85,r.r86,r.r91,r.r92,r.r95,r.r128,r.r133,r.r134,r.r135,r.r130,r.r139,r.r144,r.r146,r.r151,r.r166,r.r400,r.r401,r.r402]

    #78 temporarily disabled

    #runs until rules dont make any change to fact base
    #for now just run once....

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
                
            #pydantic validation errors will skip the pre-rule for now
            try:
                d = i(d).solve()
        
            except ValidationError as e:
                #print(e)
                pass
            p = 1
        print("d.ite",d.ite)

    #Rules running only once, rule results are text, should not affect the ability of other rules to be checked.
    #temp:
    if d.runtime_error == None:
        for i in active_rules:
            
            #Two levels of error handling, inner loop checks for missing information.
            #Missing information is not technically an error, but intended method for 
            #skipping rules that don't apply.
            #Outter loop error handling actually covers for code errors in individual 
            #rules.
            try:
                    #is this too brute force ?
                try:
                    d = i(d).solve()

                except ValidationError as e:

                    #print(e)
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

    print(d.report.design_errors)
    print(d.report.warnings)
    print(d.report.suggested_checks)

    f = open(d.path+d.part_name+"_report.txt", "w")
    f.write(d.report.design_errors+d.report.warnings+d.report.suggested_checks+d.report.check_issues+"\n"+"\nSmartDFM "+d.version)
    f.close()



