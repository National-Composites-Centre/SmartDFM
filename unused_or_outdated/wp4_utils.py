# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 10:13:07 2022

@author: jakub.kucera
"""




def stl_vertex(location):
    #location = "D:\\CAD_library_sampling\\s-62.stp"
    
    with open(location, "r") as tf:
            
        output = ""

        for line in tf:

            if "Vertex" in line:
                y = line.split("""('Vertex',(""")[1]
                x = y.split("""))""")[0]
                output = output+x+" \n"
    
    return(output)


#stl_vertex("cc")