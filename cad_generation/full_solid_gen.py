

from fact_base import FactBase, layup
import win32com.client.dynamic
#import sys, os 
import numpy as np
import statistics

import PySimpleGUI as sg

#Using pre_base, which is life list of pre-rules, might need to isolate the ones 
#used here.
import pre_base
from CATIA_utils import export_step
from pydantic import ValidationError

#UI open
#very simple UI section:        
s2 = 35
s1 = 30

#rework to be browse buttons instead of input fields.....

layout2 = [[sg.Text('Layup file name:',size=(int(s1/2),1)),sg.InputText("", key='name',size=(s2, 1))],
           [sg.Text("Select entire folder:",size=(int(s1/2),1)), sg.Input(key='location',size=(int(s2/3))),sg.FolderBrowse("Select",size=(int(s2/3),1))],
           #[sg.Text('Location:',size=(int(s1/2),1)),sg.InputText("C:\\temp\\", key='location',size=(s2, 1))],
           [sg.Button('Thickness generation', key='b',size=(20,1))]]

window = sg.Window('Solid Generation From Layup', layout2, default_element_size=(12,1),size=(300,120))

print("loading UI...")

#GUI function loop
while True: 
    #read all potential user inputs
    event, values = window.read()    
    
    if event is None: # way out!    
        break  
    
    if event in 'b':

        if values['name'] == "":
            print("please specify layup file")
        else:
            #using the main class from DFM tool
            d =  FactBase()
            d.part_name = values["name"]
            ptemp = values['location']
            ptemp = ptemp.replace("/","\\")+"\\"
            d.path = ptemp

            #Using some pre-rules from main DFM tool

            #list of pre-processor functions that have to be run, as initial fact finding excercise
            active_pre = [1,3,4,13]

            while d.ite > 0:
                d.ite = 0
                #store current version of d in dold
                #dold = d.copy()

                for i in active_pre:
                    if d.runtime_error != None:
                        d.report.design_errors = d.runtime_error
                        d.report.warnings = ""
                        d.report.suggested_checks = ""
                        d.ite = 0
                        break 
                        
                    #build function to execute - functions are named according to lists
                    build_func = "problem = pre_base.p"+str(i)+"(d)"
                    #print(build_func)
                    try:
                        exec(build_func)
                        d = problem.solve()
                    except ValidationError as e:
                        p = 1

            d = export_step(d)

            

