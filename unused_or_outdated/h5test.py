# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 14:40:28 2022

@author: jakub.kucera
"""
import h5py

#f = h5py.File('D:\\CoSinC_WP4.2\\TestCad\\LAM004.h5', 'r')
#print(f)

#print(list(f.keys()))


#dset = f['composite_cae']

#print(list(dset.keys()))

#keys_1 = list(dset.keys())

#msh = dset['meshes']

#print(list(msh.keys()))


import h5py
#general hdf5 extractor
#lists all stuff stored in the tree, noting the level of the tree
def regres(f,level):
    
    try:
        ff = list(f.keys())
    except:
        ff = 0
    
    if ff != 0:
        ff = list(f.keys())
        for ks in ff:
            print(level, "level:", ks)
            level = level +1
            try:
                level = regres(f[ks],level)
            except:
                print(level, "level:", ks," not found")
            level = level -1
            
    else:
        
        print("Total members in this directory:",f.shape[0])
    return(level)
        


f = h5py.File('D:\\HDF5_examples\\FromDan\\ConeMDB_20mmResultMesh.h5')
#f = h5py.File('D:\\CoSinC_WP4.2\\TestCad\\LAM004.h5', 'r')
level = 0
regres(f,level)


'''
md = dset['material_data']
stu = md['fabrics']
fa = stu['f0']

#print(list(stu.keys()))

#print(list(fa.keys()))

mech = fa['mechanical']

#print(list(mech.keys()))

#print(dir(mech))


x = dset['meshes']

print(list(x['m1'].keys()))

m1 = (x['m1'])
nodes = m1['nodes']

eln = m1['element_nodes']
print(eln[88])

print(list(dir(eln)))

elt = m1['element_types']

print(elt)


comps = dset['components']

print(list(comps))


c1 = comps['component0']

print(list(c1.keys()))

print(c1['rosettes'])


'''