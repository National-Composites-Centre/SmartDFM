
#replacing all the below for database change:


#from "layup_definition"


#try accessing material database, only try clause in case access to the database not possible.
#Old unused database currently used, for actual deployment a plugin to local data needs to be created.
try:
    from IDP_databases import cnt_X,dc_X

    #retrieve material from the database
    cnnC,crrC = cnt_X('NCC')

    query = """SELECT Material_name FROM fibre_properties"""
    crrC.execute(query)
    #get results
    sd = []
    rows = crrC.fetchall()

    seznam = []
    for m in rows:
        seznam.append(m[0])

    #not to forget database disconnect:
    dc_X('NCC',cnnC,crrC)
except:
    sg.Popup("material list could not be accessed, check access to the material database")
    seznam = []




        #enforce unique spline names
    if event in 'matN':   
           
        #layout for material imports

        layout33 = [[sg.Text('Material name:',size=(s1,1)),sg.InputText("", key='mn',size=(s2, 1))],
        [sg.Text('E1:',size=(s1,1)),sg.InputText("", key='E1',size=(s2, 1))],
        [sg.Text('E2:',size=(s1,1)),sg.InputText("", key='E2',size=(s2, 1))],
        [sg.Text('G12:',size=(s1,1)),sg.InputText("", key='G12',size=(s2, 1))],
        [sg.Text('v12:',size=(s1,1)),sg.InputText("", key='v12',size=(s2, 1))],
        [sg.Text('source:',size=(s1,1)),sg.InputText("", key='source',size=(s2, 1))],
        [sg.Text('fibre diameter:',size=(s1,1)),sg.InputText("", key='fd',size=(s2, 1))],
        [sg.Text('density:',size=(s1,1)),sg.InputText("", key='dens',size=(s2, 1))],
        [sg.Text('permeability cf.:',size=(s1,1)),sg.InputText("", key='perm',size=(s2, 1))],
        [sg.Button('Save material',key='save_mat',size=(15,1))]]

        window33 = sg.Window('Material Definition', layout33, default_element_size=(12,1),size=(400,330))

        while True: 
            #read all potential user inputs
            event33, values33 = window33.read()    
            
            if event33 is None: # way out!    
                break  
            if event33 in 'save_mat':
                rr = True
                #query assembled in two parts
                #input information into SQL
                query1 = "INSERT INTO fibre_properties("
                query2 = ") VALUES("
                if str(values33['mn']) == "":
                    sg.Popup("Please specify 'Material name'")
                else:
                    query1 += "Material_name"
                    query2 += """'"""+str(values33['mn'])+"""'"""

                if str(values33['E1']) == "":
                    sg.Popup("E1 is a compulsory field'")
                    rr = False
                else:
                    try:
                        E1 = float(values33['E1'])
                    except:
                        sg.Popup("E1 must be a number'")
                        rr = False
                    query1 += ",E1"
                    query2 += """,'"""+str(E1)+"""'"""

                if str(values33['E2']) == "":
                    sg.Popup("E2 is a compulsory field'")
                    rr = False
                else:
                    try:
                        E2 = float(values33['E2'])
                    except:
                        sg.Popup("E2 must be a number'")
                        rr = False
                    query1 += ",E2"
                    query2 += """,'"""+str(E2)+"""'"""

                if str(values33['G12']) == "":
                    sg.Popup("G12 is a compulsory field'")
                    rr = False
                else:
                    try:
                        G12 = float(values33['G12'])
                    except:
                        sg.Popup("G12 must be a number'")
                        rr = False
                    query1 += ",G12"
                    query2 += """,'"""+str(G12)+"""'"""
                
                if str(values33['v12']) == "":
                    sg.Popup("v12 is a compulsory field'")
                    rr = False
                else:
                    try:
                        v12 = float(values33['v12'])
                    except:
                        sg.Popup("v12 must be a number'")
                        rr = False
                    query1 += ",v12"
                    query2 += """,'"""+str(v12)+"""'"""

                if str(values33['source']) != "":
                    query1 += ",info_source"
                    query2 += """,'"""+str(values33['source'])+"""'"""

                if str(values33['fd']) == "":
                    sg.Popup("fibre diameter is a compulsory field'")
                    rr = False
                else:
                    try:
                        fd = float(values33['fd'])
                    except:
                        sg.Popup("fibre diameter must be a number'")
                        rr = False
                    query1 += ",fibre_dia"
                    query2 += """,'"""+str(fd)+"""'"""

                if str(values33['dens']) != "":
                    try:
                        dd = float(values33['dens'])
                    except:
                        sg.Popup("density must be a number'")
                        rr = False
                    query1 += ",density"
                    query2 += """,'"""+str(dd)+"""'"""

                
                if str(values33['perm']) != "":
                    try:
                        pcf = float(values33['perm'])
                    except:
                        sg.Popup("permeability coefficient must be a number'")
                        rr = False
                    query1 += ",perme_coeff"
                    query2 += """,'"""+str(pcf)+"""'"""
               
                query2 += """)"""
                query = query1+query2
                

                if rr == True:
                    sg.Popup("Material "+str(values33['mn'])+" stored.")
                    cnnC,crrC = cnt_X('NCC')
                    crrC.execute(query)
                    cnnC.commit()

                    window33.close()

                    seznam.append(values33['mn'])

            
                    dc_X('NCC',cnnC,crrC)  






#558 in pre_base


           #establish SQL connection for mat ref
            cnnC,crrC = cnt_X('NCC')
            ttmax = 0
            for ls in self.layup_sections:
                tt = 0
                
                #print("w",w)
                if "uniform" in w:
                    qw = w.split("[")[1]
                    qw = qw.split("]")[0]

                    #print("qw",qw)
                    #
                    query = """SELECT fibre_dia FROM fibre_properties where Material_name = '"""+qw+"""'"""
                    
                    crrC.execute(query)
                    #get results
                    sd = []
                    rows = crrC.fetchall()
                    fd = rows[0][0]
                    fd = float(fd)

                    tt = len(ls.sequence)*fd

                
                elif "variable" in w:
                    qw = w.split("[")[1]
                    qw = qw.split("]")[0]
                    
                    #tt = 0

                    for mat in qw.split(","):
                        query = """SELECT fibre_dia FROM fibre_properties where Material_name = '"""+mat+"""'"""
                        
                        crrC.execute(query)
                        #get results
                        sd = []
                        rows = crrC.fetchall()
                        fd = rows[0][0]
                        fd = float(fd)

                        tt = tt + fd

                    

                else:

                    for l in ls.sequence:
                        print("option not curretnly available -- the only material allocation options are 'uniform' and 'variable'")
                        self.runtime_error = "Materials have to be defined with 'uniform' or 'variable' options."

                if tt > ttmax:
                    ttmax = tt
                    #do I need to know which layup is the max?

                ls.local_thickness = tt

            self.layup_max_thickness = ttmax
            print("p7 run")

            #not to forget database disconnect:
            dc_X('NCC',cnnC,crrC)




#298 line #establish SQL connection for mat ref
            cnnC,crrC = cnt_X('NCC')
            ttmax = 0

            mpl = self.max_ply_layup
            #l2 is the list of 
            for ii, patch in enumerate(patches):
                #reverse the order 
                patch.sort(key=lambda x: x.sp_len, reverse=False)
                local_splines = []

                tt = 0

                for spline in patch:
                    seq = []
                    lrs = []
                    tt = 0

                    for i ,layer in enumerate(mpl):
                        q = True
                        #check if this splien is referenced in other patches
                        for iii, patch2 in enumerate(patches):
                            if iii != ii:
                                for spline2 in patch2:
                                    if spline2.sp_def == l2[i]:
                                        q = False

                        #check if referenced in above splines in this patch
                        if l2[i] in local_splines:
                            q = False

                        #if neither seq.append
                        if q == True:
                            seq.append(layer)
                            lrs.append(self.layup_splines[i])

                            #also calculate local thickness 
                            if "uniform" in w:
                                #if uniform this section does not need to 
                                qw = w.split("[")[1]
                                qw = qw.split("]")[0]

                                #print("qw",qw)
                                #
                                query = """SELECT fibre_dia FROM fibre_properties where Material_name = '"""+qw+"""'"""
                                
                            
                            if "variable" in w:
                                qw = w.split("[")[1]
                                qw = qw.split("]")[0]
                                
                                #tt = 0

                                mat = qw.split(",")[i]
                                query = """SELECT fibre_dia FROM fibre_properties where Material_name = '"""+mat+"""'"""
                                    
                            crrC.execute(query)
                            #get results
                            sd = []
                            rows = crrC.fetchall()
                            fd = rows[0][0]
                            fd = float(fd)

                            tt = tt + fd


                    local_splines.append(spline.sp_def)
                    if ttmax < tt:
                        ttmax = tt
                    spline.local_thickness = tt
                    spline.sequence = seq
                    spline.remaining_splines = lrs
                    
                    #clearer messaging where no delimiting spline is found
                    if spline.sp_def == "NO SPLINE":
                        spline.sp_def = "Edge of part"
                    #save segment of layup
                    self.layup_sections.append(spline)


            self.layup_max_thickness = ttmax


            #once you have 2d table of patches finished go through each spline object specified and define layup 

            #if segments still empty, create a standalone single segment for the full layup

            #use the above to also find distance between any combination of patch splines?? 
            print("p4 run")

            #not to forget database disconnect:
            dc_X('NCC',cnnC,crrC)
            self.ite += 1

