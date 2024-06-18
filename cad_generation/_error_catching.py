# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 11:04:57 2022

@author: jakub.kucera
"""

#check for duplicating records 

i = 0
while i < 5000:
    filename = "s-"+str(i)
    # Using readlines()
    file1 = open('D:\\CAD_library_sampling\\sample7\\'+filename+'_metadata.txt', 'r')
    Lines = file1.readlines()
      
    count = 0
    # Strips the newline character
    e = 0
    for line in Lines:
        count += 1
        #(line)
        l = line.split(" /n")[0]
        l = l.strip()
        #print(l)
        if l.isalpha():
            e = e + 1
    #print(e)
    if e == 4:
        
        print("check file no."+str(i))
    i = i + 1
    file1.close()