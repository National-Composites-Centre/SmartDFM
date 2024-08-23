#THIS SCRIPT IS COMPLETELY UNUSED IN VERSION 3.0 , in other versions used for UI
#Changes made in 4.3 remove the requirement for CATIA usage

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
#import win32com.client.dynamic

from time import perf_counter
import sys

#Pydantic library is used to validate inputs to pre-rules and rules
from pydantic import ValidationError

#pysimplegui only used to initiate the run and print report
#import PySimpleGUI as sg

###

import os

from runSDFM import sDFM

def TK_FS(self):
    #the random argument is just because kivy passes random stuff during on_press... so...

    #TK file selector
    import tkinter as tk
    from tkinter import filedialog

    filetypes = (
        ('All files', '*.*'),
        ('catiaFiles','*.CATPart'),
        ('STEP files','*.stp'),
    )

    # open-file dialog
    root = tk.Tk()
    filename = tk.filedialog.askopenfilename(
        title='Select a file...',
        filetypes=filetypes,
    )
    self.sef.text = filename

    root.destroy()
    return(self)

#replacing PySimpleGUI by Kivy
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import StringProperty

import subprocess
import os


Builder.load_string('''
<ScrolllabelLabel>:
    Label:
        text: root.text
        font_size: 12
        text_size: self.width, None
        size_hint_y: None
        height: self.texture_size[1]
''')

class ScrolllabelLabel(ScrollView):
    text = StringProperty('')

class MainApp(App):

    Window.size = (500, 700)
    def build(self):
        self.layout = FloatLayout()


        #folder selection
        self.sef = TextInput(text='',size_hint=(0.5,0.05),pos =(120, 650))

        self.b1 = Button(text='Select', on_press=self.TK_FS_,size_hint=(0.22,0.05),pos =(380, 650))
        self.b2 = Button(text='Check my design', on_press=self.submit,size_hint=(0.4,0.05),pos =(15,600))

        #Looks for any file 
        self.l2 = Label(text='Select file:',halign = 'left',pos =(5,650),size_hint=(0.2,0.05))

        #self.t66 = Label(text='If using CATIA file, and .step does not exist yet, make sure CATIA is running!',halign = 'left',size_hint=(0.8,0.05),pos =(5, 550))

        self.scrl = ScrollView(size_hint=(0.95, 0.8), pos =(10,10))
        self.t3 = ScrolllabelLabel(text='If using CATIA file, and .step does not exist yet, make sure CATIA is running!\n',size_hint=(1,1))#,multiline=True)
        self.scrl.add_widget(self.t3)

        self.layout.add_widget(self.l2)
        self.layout.add_widget(self.sef)
        self.layout.add_widget(self.b1)
        #self.layout.add_widget(self.t66)
        self.layout.add_widget(self.b2)
        self.layout.add_widget(self.scrl)
        return(self.layout)
    
    def submit(self,obj):
        self.t3.text = "evaluating"

        #here UI to run with CATIA (or elsewhere)
        input_text = self.sef.text

        if input_text == "":
            print("please select a file")
        else:
            np = os.path.normpath(input_text)
            np = np.split(os.sep)

            part = np[len(np)-1]
            
            extension = part.split(".")[part.count(".")]
            part = part[:-(len(extension)+1)]
     
            folder = input_text[:-(len(part)+len(extension)+1)]

            acceptable_extensions = ["CATPart","stp","STP","STEP",] #here anyone can add acceptable extensions based on their CAD software (that allow for step gen.)
            if extension in acceptable_extensions:
                sDFM(part,folder,extension)
                error = 1
                while error == 1:
                    
                    try:
                        print(folder+"\\"+part+"_report.txt")
                        with open(folder+"\\"+part+"_report.txt", "r") as report:
                            self.t3.text = report.read()
                        error = 2
                    except:
                        pass
            else:
                print("the extension of given file is currently not supported")




    def select(self,obj):
        print("(currently not functional, please edit folder manually)")
        
    
    def TK_FS_(self,obj):
        self = TK_FS(self)
        return(self)
    
MainApp().run()


