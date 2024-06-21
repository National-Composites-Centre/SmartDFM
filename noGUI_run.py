from runSDFM import sDFM
import win32com.client.dynamic

try: 
    CATIA = win32com.client.Dispatch("CATIA.Application")
    partDocument2 = CATIA.ActiveDocument
    cat_name = CATIA.ActiveDocument.Name
    cat_name = cat_name.split(".CATPart")[0]
except:
    part = "x_test_116"

location = "C:\code\fls_copy_2"

sDFM(part, location)