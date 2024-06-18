
import os
import shutil


dir1 = "D:\\CAD_library_sampling\\sample17\\"
dir2 = "D:\CAD_library_sampling\s17_nohole\\"
i = 3510
while i < 5000:
    try:
        filename = "sp_"+str(i)
        shutil.move(dir1+filename+".catpart", dir2+filename+".catpart")
        shutil.move(dir1+filename+".stp", dir2+filename+".stp")
        shutil.move(dir1+filename+"_metadata.txt", dir2+filename+"_metadata.txt")
    except:
        print("guess not number:"+str(i))
    i = i + 2