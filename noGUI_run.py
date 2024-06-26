from runSDFM import sDFM
import win32com.client.dynamic
import sys

try: 
    CATIA = win32com.client.Dispatch("CATIA.Application")
    partDocument2 = CATIA.ActiveDocument
    cat_name = CATIA.ActiveDocument.Name
    cat_name = cat_name.split(".CATPart")[0]
except:
    print("please open CATIA and corresponding file first, make sure no background CATIA instances are running (one was likely started now)")
    sys.exit(1)

#EDIT THIS:
location = """C:\\code\\fls_copy_2"""
part = cat_name
sDFM(part, location)