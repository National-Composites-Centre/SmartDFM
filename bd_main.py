
#backseat designer 1 works with Python only,
#no KE or Expert system library has been used.

#The requirements for CAD setup:
#    1. hidden all construction geometry if .step is created. Hidden all construction geometry except
#       splines if .step is yet to be created.
#    2. gs2 is the default name of geometrical set hosuing drop-off splines
#    3. 
import rule_base
import pre_base
from fact_base import FactBase, layup
import win32com.client.dynamic

from time import perf_counter
import sys

#Pydantic library is used to validate inputs to pre-rules and rules
from pydantic import ValidationError

#pysimplegui only used to initiate the run and print report
#import PySimpleGUI as sg

###

import os

version = str(1.1)

#try: 
CATIA = win32com.client.Dispatch("CATIA.Application")
partDocument2 = CATIA.ActiveDocument
cat_name = CATIA.ActiveDocument.Name
cat_name = cat_name.split(".CATPart")[0]
#except:
#    cat_name = "Enter name here"


#replacing PySimpleGUI by Kivy
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView

import subprocess
import os

class MainApp(App):

    Window.size = (500, 700)
    def build(self):
        self.layout = FloatLayout()

        #txt input
        self.lfn = TextInput(text=cat_name,size_hint=(0.75,0.05),pos =(120, 650))
        #folder selection
        self.sef = TextInput(text='C:\\code\\fls',size_hint=(0.4,0.05),pos =(160, 600))

        self.b1 = Button(text='Select', on_press=self.select,size_hint=(0.20,0.05),pos =(380, 600))
        self.b2 = Button(text='Check my design', on_press=self.submit,size_hint=(0.4,0.05),pos =(15,550))

        self.l1 = Label(text='File name:',halign = 'left',pos =(5,650),size_hint = (0.2,0.05))

        #This is to be resolved, the equivalent functionality to PySImpleGui not easily available
        self.l2 = Label(text='Select folder (TBD!):',halign = 'left',pos =(10,600),size_hint=(0.3,0.05))

        self.scrl = ScrollView(size_hint=(0.95, 0.75), pos =(10,10))
        self.t3 = TextInput(text='xxxxxx\n',size_hint=(1,1))
        self.scrl.add_widget(self.t3)

        self.layout.add_widget(self.l1)
        self.layout.add_widget(self.l2)
        self.layout.add_widget(self.lfn)
        self.layout.add_widget(self.sef)
        self.layout.add_widget(self.b1)
        self.layout.add_widget(self.b2)
        self.layout.add_widget(self.scrl)
        return(self.layout)
    
    def submit(self,obj):
        self.t3.text = "evaluating"

        #here UI to run with CATIA (or elsewhere)

        part_name = self.lfn.text
        part_folder = self.sef.text
        pnf = part_name+"\n"+part_folder

        with open("temp_file.txt","w") as tfl:
            tfl.write(pnf)


        #turn this into cmd....

        #workaround because Kivy checks variables inside it's functions and prevents code that involves exec() from running ... effectively
        #no more reasonable work-around found
        #

        try:
            os.remove(part_folder+"\\"+part_name+"_report.txt")
        except:
            print("new report is being generated")


        #change location!!
        subprocess.run("conda run -n sdc_kivy_3 python C:\\code\\smartdfm_kivy\\runSDFM.py") 



        error = 1
        while error == 1:
            
            try:
                print(part_folder+"\\"+part_name+"_report.txt")
                with open(part_folder+"\\"+part_name+"_report.txt", "r") as report:
                    self.t3.text = report.read()
                error = 2
            except:
                pass

    


        #THIS REQUIRES WAY OF PASSING THE INITIAL INPU (2 TEXT FIELDS) TO THE REST OF THE APP.... #ALSO NEEDS TO PROVIDE OUTPUT BACK - INTO THE APP DISPLAY.....



    def select(self,obj):
        print("(currently not functional, please edit folder manually)")
        

MainApp().run()


