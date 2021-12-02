import maya.cmds as mc
import string
import maya.OpenMaya as om


###### ENTIRE CLASS STRUCT BEGINS HERE ########

class SimpleWindow:
    def __init__( self, windowObject ):
        self.windowObject = windowObject
        self.value = 0

    # Scrubs the object name of all extraneous string identifier information.
    # Example usage
    # 'menuWindow|hellokitty|intField57643'
    # 'menuWindow', 'hellokitty', 'intField57643'
    # 'intField57643'
    # 'intField'
    def getType( self ):
        obj = self.windowObject.split("|")
        obj = obj [ len( obj ) - 1 ]
        return ''.join([ i for i in obj if not i.isdigit() ])

    # Creates and 
    def modValue( self, activateSet, newValue ):

        # Stores the pyMel window command as objType
        obj = self.getType()
        objType = {
            'intField':mc.intField,
            'floatField':mc.floatField,
            'floatSlider':mc.floatSlider,
            'intSlider':mc.intSlider,
            'checkBoxValue':mc.checkBox,
            'optionMenu':mc.optionMenu,
            'intFieldGrp':mc.intFieldGrp,
            'floatFieldGrp':mc.floatFieldGrp,
            'checkBoxGrp':mc.checkBoxGrp,
            'textField':mc.textField,
        }
        objType = objType[obj]

        # Sets the flag type for retrieving values
        valType = {
            'intField':0,
            'floatField':0,
            'floatSlider':0,
            'intSlider':0,
            'checkBoxValue':0,
            'optionMenu':1,
            'intFieldGrp':2,
            'floatFieldGrp':2,
            'checkBoxGrp':2,
            'textField':3,
        }

        # Sets the value if activateSet is True, and then gets it regardless.
        # Uses Try because there is no way reliable way to get the number of fields.
        # Pointlessly circuitious, I know, but it works!
        if   valType[obj] == 0:
            if activateSet:
                objType( self.windowObject, edit=True, q=False, v=newValue )
            self.value = objType( self.windowObject, edit=False, q=True, v=True )

        elif valType[obj] == 1:
            if activateSet:
                objType( self.windowObject, edit=True, q=False, sl=newValue )
            self.value = objType( self.windowObject, edit=False, q=True, sl=True )
            
        elif valType[obj] == 2:
            nof = -1
            skip = False

            if not skip:
                try:
                    if activateSet:
                        objType( self.windowObject, edit=True, q=False, v1=newValue[0] )
                    v1 = objType( self.windowObject, edit=False, q=True, v1=True )
                    nof = 1
                except RuntimeError:
                    nof = 0
                    skip = True
                except IndexError:
                    nof = 0
                    skip = True
            if not skip:
                try:
                    if activateSet:
                        objType( self.windowObject, edit=True, q=False, v2=newValue[1] )
                    v2 = objType( self.windowObject, edit=False, q=True, v2=True )
                    nof = 2
                except RuntimeError:
                    nof = 1
                    skip = True
                except IndexError:
                    nof = 1
                    skip = True
            if not skip:
                try:
                    if activateSet:
                        objType( self.windowObject, edit=True, q=False, v3=newValue[2] )
                    v3 = objType( self.windowObject, edit=False, q=True, v3=True )
                    nof = 3
                except RuntimeError:
                    nof = 2
                    skip = True
                except IndexError:
                    nof = 2
                    skip = True
            if not skip:
                try:
                    if activateSet:
                        objType( self.windowObject, edit=True, q=False, v4=newValue[3] )
                    v4 = objType( self.windowObject, edit=False, q=True, v4=True )
                    nof = 4
                except RuntimeError:
                    nof = 3
                    skip = True
                except IndexError:
                    nof = 3
                    skip = True
            
            # Returns the values as a list
            if   nof == 1:
                self.value = v1
            elif nof == 2:
                self.value = v1, v2
            elif nof == 3:
                self.value = v1, v2, v3
            elif nof == 4:
                self.value = v1, v2, v3, v4
        
        elif valType[obj] == 3:
            if activateSet:
                objType( self.windowObject, edit=True, q=False, text=newValue )
            self.value = objType( self.windowObject, edit=False, q=True, text=True )

        else:
            print('WARNING: NOT SUPPORTED OBJECT TYPE, TELL DAVID') 
            return False

        if activateSet:
            newPrint = 'setValue(): '
        else:
            newPrint = 'getValue(): '
        print newPrint, obj, ' - ', self.value
        return self.value

    def getValue( self ):
        return self.modValue( False, "" )
        
    def setValue( self, newValue ):
        return self.modValue ( True, newValue )

    def getWindowObject( self ):
        return self.windowObject

###### ENTIRE CLASS STRUCT ENDS HERE ########

###### DC CODE STARTS HERE ########


#Bellow all the starting values for each of the checkboxes
dc_squared = False
dc_cylindrical = False
dc_prism = False
dc_pipe = False



###### WINDOW ########

#function that defines window
def arch_generator_window():
    
    #deletes any previous meshes in the scene in which the name starts with "diogos". if there is any meshes, they will be deleted
    meshes = mc.ls(
        transforms=True,
        geometry=True
    )
    for m in meshes:
        if mc.objExists(m) and "diogos" in m:
            mc.delete(m)


    #deletes any open window which is not Maya's main window
    for w in mc.lsUI(wnd=True):
        if not w == 'MayaWindow':
            mc.deleteUI(w)

    

    #This is the window for the whole tool. The parent of the parent
    arch_generator = mc.window(
        title='Arch Generator',
        width=400,
        height=300,
        sizeable=False,
        resizeToFitChildren=True,
        mainWindow=False,
        maximizeButton=False,
        #closeCommand=lambda x: close_window(), #it did not work. Gonna leave it here so that I can work on it later
    )

    #a child of the arch_generator where everything is going to be layed on. Every single item present in the UI will be a child of the All_All
    All_All = mc.rowColumnLayout(
        parent = arch_generator, 
        numberOfRows=30, 
        rowSpacing=(50,50),
        rowHeight=[(1,20), (2, 30), (3, 30), ],
        columnSpacing=(1,1),
        adjustableColumn=True,
    )

    #Title
    mc.text(
        parent = All_All,
        label = 'Type of Columns',
    )
    mc.separator(
        parent = All_All,
    )

    ###### CHECKBOXES ########


    #a child of the All_All. Here is where the checkboxes will be attached
    column_type = mc.rowColumnLayout(
        parent = All_All,
        numberOfColumns=5, 
        columnAlign=(1, 'left'), 
        rowSpacing=(5,5),
        columnSpacing=(1,1),
        adjustableColumn=True,
    )

    
    #labels the "type:" so the user knows what it is refering to
    typeOfColumn =mc.text( 
        label='Type:',
        )

    #checkbox for the squared arch
    global squared_box
    squared_box = mc.checkBox( 
        parent=column_type,
        label="square        ",
        value=0,
        en=True,
        onc=lambda x: squared_value( True ),
        ofc=lambda x: squared_value( False ),
        )


    #checkbox for the cylindrical arch    
    global cylindrical_box
    cylindrical_box = mc.checkBox(
        parent=column_type,
        label='cylindrical          ',
        value=0,
        en=True,
        onc=lambda x: cylindrical_value( True ),
        ofc=lambda x: cylindrical_value( False ),
        )

    #checkbox for the prism arch
    global prism_box
    prism_box = mc.checkBox( 
        parent=column_type,
        label='prism           ',
        value=0,
        en=True,
        onc=lambda x: prism_value( True ),
        ofc=lambda x: prism_value( False ),
        )

    #checkbox for the pipe arch
    global pipe_box 
    pipe_box = mc.checkBox(
        parent=column_type,
        label='pipe          ',
        value=0,
        en=True,
        onc=lambda x: pipe_value( True ),
        ofc=lambda x: pipe_value( False ),
        )
    
    mc.separator(
        parent = All_All,
    )
    
    mc.text(
        parent = All_All,
        label = '',
    )

    ###### Attributes ########

    #tittle
    mc.text(
        parent = All_All,
        label = 'Attributes',
    )

    mc.text(
        parent = All_All,
        label = '',
    )
    #separator for organization
    mc.separator(
        parent = All_All,
    )



    #a child of All_All. In here you will be able to set various attributes like Height, Width, Depth, Radius, Length
    arch = mc.rowColumnLayout( 
    parent= All_All,    
    numberOfColumns=3, 
    columnWidth=[(1, 40), (2, 40), (3, 300)], 
    adjustableColumn=2, 
    columnAlign=[(1, 'left'), (2, "center"), (3, "right")], 
    columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)] )


    #title for height
    mc.text(
        parent=arch,
        label="Height:",
    )

    #title for the height field. Whatever the user writes in this box wont be taken as user input
    global arch_height_field
    arch_height_field = SimpleWindow(
        mc.intField(
            parent=arch,
        )
    )

    #title for the height slider. Whatever the user slides in this box will be taken as user input
    #includes the roundTo4() function which didnt ended up working. I will keep it regardless since it doesnt break my code and because I plan to come back to study it
    global arch_height_slider
    arch_height_slider = SimpleWindow(
        mc.intSlider(
            parent=arch,
            minValue= 0,
            maxValue=1000,
            value=0,
            en = True,
            dragCommand=lambda x: arch_height_field.setValue(arch_height_slider.getValue()),
            changeCommand=lambda x: roundTo4()
                
        )
    )
     
    #title for width
    mc.text(
        parent=arch,
        label="Width:",
    )

    #title for the width field. Whatever the user writes in this box wont be taken as user input
    global arch_width_field
    arch_width_field = SimpleWindow(
        mc.intField(
            parent=arch,
        )
    )

    #title for the width slider. Whatever the user slides in this box will be taken as user input
    global arch_width_slider
    arch_width_slider = SimpleWindow(
        mc.intSlider(
            parent=arch,
            minValue=0,
            maxValue=1000,
            value=0,
            en=True,
            dragCommand=lambda x: arch_width_field.setValue(arch_width_slider.getValue()),
        )
    )

    #title for Depth
    mc.text(
        parent=arch,
        label="Depth:",
    )

    #title for the depth field. Whatever the user writes in this box wont be taken as user input
    global arch_depth_field
    arch_depth_field = SimpleWindow(
        mc.intField(
            parent=arch,
        )
    )

    #title for the depth slider. Whatever the user slides in this box will be taken as user input
    global arch_depth_slider
    arch_depth_slider = SimpleWindow(
        mc.intSlider(
            parent=arch,
            minValue=0,
            maxValue=4000,
            value=0,
            dragCommand=lambda x: arch_depth_field.setValue(arch_depth_slider.getValue()),
        )
    )

    #title for Radius
    mc.text(
        parent=arch,
        label="Radius:",
    )

    #title for the radius field. Whatever the user writes in this box wont be taken as user input
    global arch_radius_field
    arch_radius_field = SimpleWindow(
        mc.intField(
            parent=arch,
        )
    )

    #title for the radius slider. Whatever the user slides in this box will be taken as user input
    global arch_radius_slider
    arch_radius_slider = SimpleWindow(
        mc.intSlider(
            parent=arch,
            minValue=0,
            maxValue=1000,
            value=0,
            dragCommand=lambda x: arch_radius_field.setValue(arch_radius_slider.getValue()),
        )
    )

    #title for Length
    mc.text(
        parent=arch,
        label="Lenght:",
    )

    #title for the length field. Whatever the user writes in this box wont be taken as user input
    global arch_lenght_field
    arch_lenght_field = SimpleWindow(
        mc.intField(
            parent=arch,
        )
    )

    #title for the lenght slider. Whatever the user slides in this box will be taken as user input
    global arch_lenght_slider
    arch_lenght_slider = SimpleWindow(
        mc.intSlider(
            parent=arch,
            minValue=0,
            maxValue=1000,
            value=0,
            dragCommand=lambda x: arch_lenght_field.setValue(arch_lenght_slider.getValue()),
        )
    )



    mc.separator(
        parent = All_All,
    )

    mc.text(
        parent = All_All,
        label = '',
    )



    ###### Column Height ########


    #title for Column Hieght
    mc.text(
        parent = All_All,
        label = 'Columns Height',
    )

    mc.text(
        parent = All_All,
        label = '',
    )
    
    #separator for organization
    mc.separator(
        parent = All_All,
    )

    #a child of All_All. In here you will be able to set column height
    column = mc.rowColumnLayout(
        parent = All_All,
        numberOfColumns=3,
        columnWidth=[(1, 85), (2, 20), (3, 250)], 
        adjustableColumn=2, 
        columnAlign=[(1, 'left'), (2, "center"), (3, "right")], 
        columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)],
    )

    #title for Column Hieght
    column_text = mc.text( 
        parent=column,
        label='Column Height:',
    )
    
    #title for the column_height field. Whatever the user writes in this box wont be taken as user input
    global column_height_field
    column_height_field = SimpleWindow(
        mc.intField(
            parent=column,
        )
    )
    
    #title for the column_height slider. Whatever the user slides in this box will be taken as user input
    global column_height_slider
    column_height_slider = SimpleWindow(
        mc.intSlider(
            parent=column,
            min=0,
            max=5000,
            value=1,
            step=1.0,
            dragCommand=lambda x: column_height_field.setValue(column_height_slider.getValue()),
        )
    )

    #for organization
    mc.separator(
        parent = All_All,
    )
    #for organization
    mc.text(
        parent = All_All,
        label = '',
    )

    ###### BUTTONS ########

    # 3 Buttons set for the UI
    buttons = mc.rowColumnLayout(
        parent = All_All,
        numberOfColumns=3,
        columnWidth=[(1, 125), (2, 100), (3, 125)], 
        adjustableColumn=2, 
        columnAlign=[(1, 'left'), (2, "center"), (3, "right")], 
        columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)],
    )

    # Cancel button. The command will call for the cancel() function which I will explain later
    mc.button( 
        parent = buttons,
        label='Cancel',
        command=lambda x: cancel()
    )
    # Preview button. The command will call the make_an_arch() function wich I will explain later
    mc.button( 
        parent = buttons,
        label='Preview',
        command=lambda x: make_an_arch()
    )

    # Apply Button . The command will call the mapply_closed() function wich I will explain later
    mc.button( 
        parent = buttons,
        label='Apply',
        command= lambda x: apply_close()
    )

    mc.showWindow()

arch_generator_window()



###### THE CHOICE IS....? ########


#The purpose of the following functions is to give to the user, throw the script editor, feedback on which boxes and choices does he have checked. Each explained bellow


#Serves to give user feedback on the status of the squared checkbox, which can be either True or False
def squared_value(isChecked):
    global dc_squared
    dc_squared = mc.checkBox(squared_box, q=True, v=True)

    print "the choice is squared? " + str(dc_squared)

#Serves to give user feedback on the status of the cylindrical checkbox, which can be either True or False
def cylindrical_value(isChecked):
    global dc_cylindrical
    dc_cylindrical = mc.checkBox(cylindrical_box, q=True, v=True)

    print "the choice is cylindrical? " + str(dc_cylindrical)

#Serves to give user feedback on the status of the prism checkbox, which can be either True or False
def prism_value(isChecked):
    global dc_prism
    dc_prism = mc.checkBox(prism_box, q=True, v=True)

    print "the choice is prism? " + str(dc_prism)

#Serves to give user feedback on the status of the pipe checkbox, which can be either True or False
def pipe_value(isChecked):
    global dc_pipe
    dc_pipe = mc.checkBox(pipe_box, q=True, v=True)

    print "the choice is pipe? " + str(dc_pipe)
    


#Serves the same purpose as the one before. They both work perfectly, although this is a simplicied version. I will keep both here for later since I plan to use this project as a library.
def print_values():
    global squared_value
    global cylindrical_value
    global prism_value
    global pipe_value
    global centimeter_value
    print "the choice is squared? " + str(dc_quared)
    print "the choice is cylindrical? " + str(dc_cylindrical)
    print "the choice is cilindical? " + str(dc_prism)
    print "the choice is pipe? " + str(dc_pipe)


###### TO STUDY ########

#As mentioned previously, this code does not work. However, since it does not break anything I have I will keep it to study it later.
def roundTo4():
    global arch_height_field
    value = arch_height_field.getValue()

    rounded = value - ( value % 4 )

    arch_height_field.setValue( rounded )


###### TO KEEP WORKING ########

# The following function is not being called, which means that it wont break anything. (it doesnt work either) I will keep it since I will know where to continue from when I come back.
def node_boxes():
    global squared_box
    global dc_squared

    global cylindrical_box
    global dc_cylindrical

    global prism_box
    global dc_prism

    global pipe_box
    global dc_pipe



###### MAKE_AN_ARCH ########
###### MAKE_AN_ARCH ########
###### MAKE_AN_ARCH ########
###### MAKE_AN_ARCH ########



# The function which actually build the arch. called by the Preview button
def make_an_arch():

    # if there is any meshe in the scene with the name "diogos" it will be deleted
    meshes = mc.ls(
        transforms=True,
        geometry=True
    )
    for m in meshes:
        if mc.objExists(m) and "diogos" in m:
            mc.delete(m)


  
    #globals to call values from the attributes
    global arch_height_slider
    global arch_width_slider
    global arch_depth_slider
    global arch_radius_slider  
    global arch_lenght_slider

    #global to call value from column height
    global column_height_slider

    #globals to call bolleans from squared checkbox
    global squared_box
    global dc_squared

    #globals to call bolleans from cylindrical checkbox
    global cylindrical_box
    global dc_cylindrical

    #globals to call bolleans from prism checkbox
    global prism_box
    global dc_prism

    #globals to call bolleans from pipe checkbox
    global pipe_box
    global dc_pipe



    #get the values chosen by the user before and shortening them into a variable to make the code more easily read and understood
    height_value =  arch_height_slider.getValue()
    width_value = arch_width_slider.getValue()
    depth_value = arch_depth_slider.getValue()
    radius_value = arch_radius_slider.getValue()
    length_value = arch_lenght_slider.getValue()
    column_height = column_height_slider.getValue()

    #when function is called by pressing "Apply" the codes bellow will  create all the four primatives with the given attributes that were pre assigned by me
    mc.polyCube(name = 'diogosPolyCube', h=4, w=1, d=1, sx=1, sy=30, sz=1)
    mc.polyCylinder(name = "diogosPolyCylinder", r=1, height=4, sx = 20, sy = 30, sz =1) 
    mc.polyPrism( name= "diogosPolyPrism", l=4, ns = 3, w=2, sc=1, sh=30 )
    mc.polyPipe(name="diogosPolyPipe", h=4, r =1, t=0.5, sh=30, )


    #Sets a value by which the finished archs must be translated upwards
    dc_To_Translate =  height_value * 1.2915
    dc_To_Translate_all = column_height + dc_To_Translate






    #How I intended the following codde to work was that, it would only run if only one given option would be true
    #Hence my emphazis on the "AND"
    #However pyton seems to have other plans. Regardless, the code continues to work.
    #The only coviat will be that if all are turned TRUE, it will be the polyCube to be generated
    #If they are all turned True except for the squared, the polyCylinder will be generated
    #Sounds far more complicated explained here, but once you see it working on the UI, it is actually pretty simple and intuitive. better than otherwise most likely.


    #FIXED THE ERROR MENTIONED ABOVE BY ADDING THIS "FEW" LINES OF CODE

    #So, I will continue

###### DONT EVEN BOTHER WITH THIS SECTION ########
###### TOOK FAR TO LONG FOR SOMETHING IT COULD HAVE BEEN DONE IN ONE LINE, BUT IT WORKS, AND THE OTHER WAY WASNT. ITS NOT PRETTY BUT IT IS FUNCTIONAL ########
###### SKIP TO CHECKBOX ########

    #if more tha one box is checked:
    if mc.checkBox(squared_box, q=True, v=True) and mc.checkBox(cylindrical_box, q=True, v=True) and mc.checkBox(prism_box, q=True, v=True) and mc.checkBox(pipe_box, q=True, v=True):
        #we will delete:
        mc.delete("diogosPolyCube")
        #and...
        mc.delete("diogosPolyCylinder")
        #and:
        mc.delete("diogosPolyPrism")
        #and:
        mc.delete("diogosPolyPipe")

        mc.error("You can only chose 1 option")

    #if more tha one box is checked:
    elif  mc.checkBox(squared_box, q=True, v=True) and mc.checkBox(cylindrical_box, q=True, v=True) and mc.checkBox(prism_box, q=True, v=True) and mc.checkBox(pipe_box, q=False, v=False):
        #we will delete:
        mc.delete("diogosPolyCube")
        #and...
        mc.delete("diogosPolyCylinder")
        #and:
        mc.delete("diogosPolyPrism")
        #and:
        mc.delete("diogosPolyPipe")

        mc.error("You can only chose 1 option")

    #if more tha one box is checked:
    elif  mc.checkBox(squared_box, q=True, v=True) and mc.checkBox(cylindrical_box, q=True, v=True) and mc.checkBox(prism_box, q=False, v=False) and mc.checkBox(pipe_box, q=True, v=True):
        #we will delete:
        mc.delete("diogosPolyCube")
        #and...
        mc.delete("diogosPolyCylinder")
        #and:
        mc.delete("diogosPolyPrism")
        #and:
        mc.delete("diogosPolyPipe")

        mc.error("You can only chose 1 option")

    #if more tha one box is checked:
    elif  mc.checkBox(squared_box, q=True, v=True) and mc.checkBox(cylindrical_box, q=True, v=True) and mc.checkBox(prism_box, q=False, v=False) and mc.checkBox(pipe_box, q=False, v=False):
        #we will delete:
        mc.delete("diogosPolyCube")
        #and...
        mc.delete("diogosPolyCylinder")
        #and:
        mc.delete("diogosPolyPrism")
        #and:
        mc.delete("diogosPolyPipe")

        mc.error("You can only chose 1 option")

    #if more tha one box is checked:
    elif  mc.checkBox(squared_box, q=True, v=True) and mc.checkBox(cylindrical_box, q=False, v=False) and mc.checkBox(prism_box, q=True, v=True) and mc.checkBox(pipe_box, q=False, v=False):
        #we will delete:
        mc.delete("diogosPolyCube")
        #and...
        mc.delete("diogosPolyCylinder")
        #and:
        mc.delete("diogosPolyPrism")
        #and:
        mc.delete("diogosPolyPipe")

        mc.error("You can only chose 1 option")

    #if more tha one box is checked:
    elif  mc.checkBox(squared_box, q=True, v=True) and mc.checkBox(cylindrical_box, q=False, v=False) and mc.checkBox(prism_box, q=False, v=False) and mc.checkBox(pipe_box, q=True, v=True):
        #we will delete:
        mc.delete("diogosPolyCube")
        #and...
        mc.delete("diogosPolyCylinder")
        #and:
        mc.delete("diogosPolyPrism")
        #and:
        mc.delete("diogosPolyPipe")

        mc.error("You can only chose 1 option")

    #if more tha one box is checked:
    elif  mc.checkBox(squared_box, q=False, v=False) and mc.checkBox(cylindrical_box, q=True, v=True) and mc.checkBox(prism_box, q=True, v=True) and mc.checkBox(pipe_box, q=True, v=True):
        #we will delete:
        mc.delete("diogosPolyCube")
        #and...
        mc.delete("diogosPolyCylinder")
        #and:
        mc.delete("diogosPolyPrism")
        #and:
        mc.delete("diogosPolyPipe")

        mc.error("You can only chose 1 option")

    #if more tha one box is checked:
    elif  mc.checkBox(squared_box, q=False, v=False) and mc.checkBox(cylindrical_box, q=False, v=False) and mc.checkBox(prism_box, q=True, v=True) and mc.checkBox(pipe_box, q=True, v=True):
        #we will delete:
        mc.delete("diogosPolyCube")
        #and...
        mc.delete("diogosPolyCylinder")
        #and:
        mc.delete("diogosPolyPrism")
        #and:
        mc.delete("diogosPolyPipe")

        mc.error("You can only chose 1 option")
        
    #if more tha one box is checked:
    elif  mc.checkBox(squared_box, q=False, v=False) and mc.checkBox(cylindrical_box, q=True, v=True) and mc.checkBox(prism_box, q=False, v=False) and mc.checkBox(pipe_box, q=True, v=True):
        #we will delete:
        mc.delete("diogosPolyCube")
        #and...
        mc.delete("diogosPolyCylinder")
        #and:
        mc.delete("diogosPolyPrism")
        #and:
        mc.delete("diogosPolyPipe")

        mc.error("You can only chose 1 option")


    #if more tha one box is checked:
    elif  mc.checkBox(squared_box, q=False, v=False) and mc.checkBox(cylindrical_box, q=True, v=True) and mc.checkBox(prism_box, q=True, v=True) and mc.checkBox(pipe_box, q=False, v=False):
        #we will delete:
        mc.delete("diogosPolyCube")
        #and...
        mc.delete("diogosPolyCylinder")
        #and:
        mc.delete("diogosPolyPrism")
        #and:
        mc.delete("diogosPolyPipe")

        mc.error("You can only chose 1 option")
    



    #If squared checkboc == True and all others False, it will proceede

    ###### Squared_BOX ########

    elif mc.checkBox(squared_box, q=True, v=True) and mc.checkBox(cylindrical_box, q=False, v=False) and mc.checkBox(prism_box, q=False, v=False) and mc.checkBox(pipe_box, q=False, v=False):

        #as I mentioned previously, all the four primative were created as soon as the "Apply" was pressed
        #However, depending  on which checkbox you have selected, primatives will be deleted and other kept. Lets see the example bellow


        #So, since squared box == True, polyCube will stay and...
        #we will delete:
        mc.delete("diogosPolyCylinder")
        #and:
        mc.delete("diogosPolyPrism")
        #and:
        mc.delete("diogosPolyPipe")

        #which will leave us only with the polyCube, which was renamed to "diogosPolyCube"

        #we must check if attributes are greater than 0
        if height_value == 0:
            #if applyable, then we delete the "diogosPolyCube" and...
            mc.delete('diogosPolyCube')
            #... send and error message. This error message explain which is the issue.
            #The error code will also stop the continuation of the programm meaning it will end right here if the values are not correct
            mc.error("Height must be greater than 0")
        elif width_value == 0:
            #if applyable, then we delete the "diogosPolyCube" and...
            mc.delete('diogosPolyCube')
            #... send and error message. This error message explain which is the issue.
            #The error code will also stop the continuation of the programm meaning it will end right here if the values are not correct
            mc.error("Width must be greater than 0")
        elif depth_value == 0:
            #if applyable, then we delete the "diogosPolyCube" and...
            mc.delete('diogosPolyCube')
            #... send and error message. This error message explain which is the issue.
            #The error code will also stop the continuation of the programm meaning it will end right here if the values are not correct
            mc.error("Depth must be greater than 0")

        #This is a treacky part:
        #Since the ratio between height and width AND between height and value cannot be any given one, "parameters" were given.
        #depending on which, the code would go along or not
        #This was done so that the user, by taking advantage of my tool, would never end up with broken geometry or faces inside the mesh or any other issue
        #we check the ratio between height and width TOGETHER WITH height and depth
        elif height_value/1.5 < width_value and height_value*4 < depth_value:
            #if applyable, then we delete the "diogosPolyCube" and...
            mc.delete('diogosPolyCube')
            #... send and error message. This error message explain which is the issue. in this cae, it will be both the height/width ratio and height/deoth radio as explained bellow. 
            #The error code will also stop the continuation of the programm meaning it will end right here if the values are not correct
            mc.error("Height must be 1.5 times greater than the width and depth must be 4 greater than height")
        
        #In this case depth is not an issue since the ratio is correct
        #instead, the problem lies on the height/width ration. One has to be lowered or the other must be increased
        elif height_value/1.5 < width_value:
            #if indeed the ratio is not correct, the same system as above will be applyed
            #"diogosPolyCube" will be deleted
            mc.delete('diogosPolyCube')
            #error code will play  with the specifc message regarding the specific issue
            mc.error("Height must be 1.5 times greater than the width")
        elif height_value*4 < depth_value:
            #in this case its not both, and its not the height/width ration, but the height/depth ration
            #"diogosPolyCube" will be deleted
            mc.delete('diogosPolyCube')
            #error code will play  with the specifc message regarding the specific issue
            mc.error("Depth cannot be 4 times greater than the height")
        else:
            #if all values were correct, well done! 
            #To signal that fact to the user, we will use to inform him
            print "all values are correct"




        #with the setAttr we will change the attributes of the polyCube and substitute them with use imputted (is taht a word?) by the user
        mc.setAttr("diogosPolyCube.scaleY", height_value)
        mc.setAttr("diogosPolyCube.scaleX", width_value)
        mc.setAttr("diogosPolyCube.scaleZ", depth_value)

        #in order to prepare the "diogosPolyCube for the bend, we must first rotate it"
        mc.setAttr("diogosPolyCube.rotate", 0, 0, -90)

        #bend the "diogosPolyCube" with a curvature set at 90º
        mc.nonLinear("diogosPolyCube", type="bend", curvature = 90)

        #selects the faces 61 and 30. 
        #This faces specificly since they are the ones facing down and will be the bases of the arch
        mc.select("diogosPolyCube.f[61]", "diogosPolyCube.f[30]")

        #extrudes the faces downward (they are still selected)
        extrude_faces = mc.polyExtrudeFacet(kft=True, ltz=1, ls= (1.0, 1.0, 1.0))

        #gets the value chosen by the user and, with the faces still selected, turns the value to the negative (so that it can be moved downwards), sets Y=True to move it only on the Y axis and relative to True as well so that it will move the faces relativetly 
        mc.move(-column_height, y=True, relative=True)

        #it will select the entire mesh. Since Bend1Handle is still part of it it will also select it
        mc.select("diogosPolyCube")

        #ducplicates it so that the original can be deleted
        mc.duplicate("diogosPolyCube", n="diogosPolyCube1")

        #original gets deleted. This is due to the fact that if it wasnt, the user would could not interact with it unless it erased the Bend1Handle
        #Trying to avoid the user from doing extra steps (after all, it is the whole purpose of this project), it was all donde here in the code
        mc.delete("diogosPolyCube")
        
        #selects the new meshe. name doesnt matter since it will change later on, or get deleted. It is explained later on
        mc.select("diogosPolyCube1")

        #moves the selected mesh using the calculations done previously
        mc.move(dc_To_Translate_all, y=True, relative=True)

    


    ###### Cylindrical_BOX ########

    #If cylindrical checkboc == True and all others False, it will proceede
    elif mc.checkBox(cylindrical_box, q=True, v=True) and mc.checkBox(squared_box, q=False, v=False) and mc.checkBox(prism_box, q=False, v=False) and mc.checkBox(pipe_box, q=False, v=False):
        #So, since cylindrical box == True, polyCylinder will stay and...
        #we will delete:
        mc.delete('diogosPolyCube')
        #...and
        mc.delete("diogosPolyPrism")
        #... and
        mc.delete("diogosPolyPipe")
        #which will leave us only with the polyCylinder, which was renamed to "diogosPolyCylinder"


        
        
        
        #we must check if attributes are greater than 0
        if height_value == 0:
            #if applyable, then we delete the "diogosPolycylinder" and...
            mc.delete('diogosPolyCylinder')
            #... send and error message. This error message explain which is the issue.
            #The error code will also stop the continuation of the programm meaning it will end right here if the values are not correct
            mc.error("Height must be greater than 0")
        elif radius_value == 0:
            #if applyable, then we delete the "diogosPolycylinder" and...
            mc.delete('diogosPolyCylinder')
            #... send and error message. This error message explain which is the issue.
            #The error code will also stop the continuation of the programm meaning it will end right here if the values are not correct
            mc.error("Radius must be greater than 0")
        #Another treacky part:
        #This time we only have to worry about the ratio between height and radious since those are the only two values that a cylinder takes
        #This was done so that the user, by taking advantage of my tool, would never end up with broken geometry or faces inside the mesh or any other issue
        #To start we check the ratio between height and radius
        elif height_value*1.25 < radius_value:
            #if the ratio is such that the geometry would be broken if printed the:
            #"diogosPolyCylinder" will be deleted
            mc.delete("diogosPolyCylinder")
            #The error code will also stop the continuation of the programm meaning it will end right here if the values are not correct
            mc.error("The ratio betwwen Radius and Height can be no greater than 1.25")
        else:
            #if all values were correct, well done! 
            #To signal that fact to the user, we will use to inform him
            print "all values are correct"

        #with the setAttr we will change the attributes of the polyCylinder and substitute them with use imputted (is taht a word?) by the user
        mc.setAttr("diogosPolyCylinder.scaleY", height_value)
        mc.setAttr("diogosPolyCylinder.scaleX", radius_value)
        mc.setAttr("diogosPolyCylinder.scaleZ", radius_value)

        #in order to prepare the "diogosPolyCylinder for the bend, we must first rotate it"
        mc.setAttr("diogosPolyCylinder.rotate", 0, 0, -90)

        #bend the "diogosPolyCylinder" with a curvature set at 90º
        mc.nonLinear("diogosPolyCylinder", type="bend", curvature = 90)

        #selects the faces 600 to 639 
        #This faces specificly since they are the ones facing down and will be the bases of the arch
        mc.select("diogosPolyCylinder.f[600:619]", "diogosPolyCylinder.f[620:639]" )

        #extrudes the faces downward (they are still selected)
        mc.polyExtrudeFacet(kft=True, ltz=1, ls= (1.0, 1.0, 1.0))

        #gets the value chosen by the user and, with the faces still selected, turns the value to the negative (so that it can be moved downwards), sets Y=True to move it only on the Y axis and relative to True as well so that it will move the faces relativetly 
        mc.move(-column_height, y=True, relative=True)

        #it will select the entire mesh. Since Bend1Handle is still part of it it will also select it
        mc.select("diogosPolyCylinder")

        #ducplicates it so that the original can be deleted
        mc.duplicate("diogosPolyCylinder", n="diogosPolyCylinder1")

        #original gets deleted. This is due to the fact that if it wasnt, the user would could not interact with it unless it erased the Bend1Handle
        #Trying to avoid the user from doing extra steps (after all, it is the whole purpose of this project), it was all donde here in the code
        mc.delete("diogosPolyCylinder")

        #selects the new meshe. name doesnt matter since it will change later on, or get deleted. It is explained later on
        mc.select("diogosPolyCylinder1")

        #moves the selected mesh using the calculations done previously
        mc.move(dc_To_Translate_all, y=True, relative=True)


    

    ###### Prism_BOX ########

    #If prism checkboc == True and all others False, it will proceede
    elif mc.checkBox(prism_box, q=True, v=True) and mc.checkBox(squared_box, q=False, v=False) and mc.checkBox(cylindrical_box, q=False, v=False) and mc.checkBox(pipe_box, q=False, v=False):
        #So, since prism box == True, polyCylinder will stay and...
        #we will delete:
        mc.delete('diogosPolyCube')
        #...and
        mc.delete("diogosPolyCylinder")
        #... and
        mc.delete("diogosPolyPipe")
        #which will leave us only with the polyCylinder, which was renamed to "diogosPolyCylinder"


        #we must check if attributes are greater than 0
        if height_value == 0:
            #if applyable, then we delete the "diogosPolycylinder" and...
            mc.delete('diogosPolyPrism')
            #... send and error message. This error message explain which is the issue.
            #The error code will also stop the continuation of the programm meaning it will end right here if the values are not correct
            mc.error("Height must be greater than 0")
        elif length_value == 0:
                        #if applyable, then we delete the "diogosPolycylinder" and...
            mc.delete('diogosPolyPrism')
            #... send and error message. This error message explain which is the issue.
            #The error code will also stop the continuation of the programm meaning it will end right here if the values are not correct
            mc.error("Lenght must be greater than 0")

        #Another treacky part:
        #This time we only have to worry about the ratio between height and lenght since those are the only two values that a prism takes
        #This was done so that the user, by taking advantage of my tool, would never end up with broken geometry or faces inside the mesh or any other issue
        #To start we check the ratio between height and lenght
        elif height_value*1.25 < length_value:
            #if the ratio is such that the geometry would be broken if printed the:
            #"diogosPolyPrism" will be deleted
            mc.delete("diogosPolyPrism")
            #The error code will also stop the continuation of the programm meaning it will end right here if the values are not correct
            mc.error("The ratio betwwen Lenght and Height can be no greater than 1.25")
        else:
            #if all values were correct, well done! 
            #To signal that fact to the user, we will use to inform him
            print "all values are correct"
        
        #with the setAttr we will change the attributes of the polyCylinder and substitute them with use imputted (is taht a word?) by the user
        mc.setAttr("diogosPolyPrism.scaleY", height_value)
        mc.setAttr("diogosPolyPrism.scaleZ", length_value)
        mc.setAttr("diogosPolyPrism.scaleX", length_value)

        #in order to prepare the "diogosPolyCylinder for the bend, we must first rotate it"
        mc.setAttr("diogosPolyPrism.rotate", 0, 0, -90)

        #bend the "diogosPolyCylinder" with a curvature set at 90º
        mc.nonLinear("diogosPolyPrism", type="bend", curvature = 90)

        #selects the faces 90 to 95 
        #This faces specificly since they are the ones facing down and will be the bases of the arch
        mc.select("diogosPolyPrism.f[90:95]")

        #extrudes the faces downward (they are still selected)
        mc.polyExtrudeFacet(kft=True, ltz=1, ls= (1.0, 1.0, 1.0))

        #gets the value chosen by the user and, with the faces still selected, turns the value to the negative (so that it can be moved downwards), sets Y=True to move it only on the Y axis and relative to True as well so that it will move the faces relativetly 
        mc.move(-column_height, y=True, relative=True)

        #it will select the entire mesh. Since Bend1Handle is still part of it it will also select it
        mc.select("diogosPolyPrism")

        #ducplicates it so that the original can be deleted
        mc.duplicate("diogosPolyPrism", n="diogosPolyPrism1")

        #original gets deleted. This is due to the fact that if it wasnt, the user would could not interact with it unless it erased the Bend1Handle
        #Trying to avoid the user from doing extra steps (after all, it is the whole purpose of this project), it was all donde here in the code
        mc.delete("diogosPolyPrism")

        #selects the new meshe. name doesnt matter since it will change later on, or get deleted. It is explained later on
        mc.select("diogosPolyPrism1")
        
        #moves the selected mesh using the calculations done previously
        mc.move(dc_To_Translate_all, y=True, relative=True)


    ###### PIPE_BOX ########

    #If pipe checkboc == True and all others False, it will proceede
    elif mc.checkBox(pipe_box, q=True, v=True) and mc.checkBox(squared_box, q=False, v=False) and mc.checkBox(cylindrical_box, q=False, v=False) and mc.checkBox(prism_box, q=False, v=False):
        #So, since pipe box == True, polyCylinder will stay and...
        #we will delete:
        mc.delete('diogosPolyCube')
        #...and
        mc.delete("diogosPolyCylinder")
        #...and
        mc.delete("diogosPolyPrism")

        #we must check if attributes are greater than 0
        if height_value == 0:
            #if applyable, then we delete the "diogosPolyPipe" and...
            mc.delete('diogosPolyPipe')
            #... send and error message. This error message explain which is the issue.
            #The error code will also stop the continuation of the programm meaning it will end right here if the values are not correct
            mc.error("Height must be greater than 0")
        elif radius_value == 0:
            #if applyable, then we delete the "diogosPolyPipe" and...
            mc.delete('diogosPolyPipe')
            #... send and error message. This error message explain which is the issue.
            #The error code will also stop the continuation of the programm meaning it will end right here if the values are not correct
            mc.error("Radius must be greater than 0")
            
        #Another treacky part:
        #This time we only have to worry about the ratio between height and radious since those are the only two values that a pipe takes
        #This was done so that the user, by taking advantage of my tool, would never end up with broken geometry or faces inside the mesh or any other issue
        #To start we check the ratio between height and radius        
        elif radius_value*1.5873 > height_value:
            #if the ratio is such that the geometry would be broken if printed the:
            #"diogosPolyPipe" will be deleted
            mc.delete("diogosPolyPipe")
            #The error code will also stop the continuation of the programm meaning it will end right here if the values are not correct
            mc.error("The ratio betwwen Radius and Height can be no greater than 1.(6)7")
        else:
            #if all values were correct, well done! 
            #To signal that fact to the user, we will use to inform him
            print "all values are correct"""

        #with the setAttr we will change the attributes of the PolyPrism and substitute them with use imputted (is taht a word?) by the user
        mc.setAttr("diogosPolyPipe.scaleY", height_value)
        mc.setAttr("diogosPolyPipe.scaleZ", radius_value)
        mc.setAttr("diogosPolyPipe.scaleX", radius_value)

        #in order to prepare the "diogosPolyCylinder for the bend, we must first rotate it"      
        mc.setAttr("diogosPolyPipe.rotate", 0, 0, -90)

        #bend the "diogosPolyCylinder" with a curvature set at 90º
        mc.nonLinear("diogosPolyPipe", type="bend", curvature = 90)

        #selects the faces 1220 to 1239 and 600 to 619 
        #This faces specificly since they are the ones facing down and will be the bases of the arch
        mc.select("diogosPolyPipe.f[1220:1239]", "diogosPolyPipe.f[600:619]")

        #extrudes the faces downward (they are still selected)
        mc.polyExtrudeFacet(kft=True, ltz=1, ls= (1.0, 1.0, 1.0))

        #gets the value chosen by the user and, with the faces still selected, turns the value to the negative (so that it can be moved downwards), sets Y=True to move it only on the Y axis and relative to True as well so that it will move the faces relativetly 
        mc.move(-column_height, y=True, relative=True)

        #it will select the entire mesh. Since Bend1Handle is still part of it it will also select it
        mc.select("diogosPolyPipe")

        #ducplicates it so that the original can be deleted
        mc.duplicate("diogosPolyPipe", n="diogosPolyPipe1")

        #original gets deleted. This is due to the fact that if it wasnt, the user would could not interact with it unless it erased the Bend1Handle
        #Trying to avoid the user from doing extra steps (after all, it is the whole purpose of this project), it was all donde here in the code
        mc.delete("diogosPolyPipe")

        #selects the new meshe. name doesnt matter since it will change later on, or get deleted. It is explained later on
        mc.select("diogosPolyPipe1")

        #calculates needed translation
        Translate_pipe = dc_To_Translate_all - 513.74

        #moves the selected mesh using the calculations done previously       
        mc.move(Translate_pipe, y=True, relative=True)



    ###### ALL FALSE ########

    # If all checkboxes == False then
    elif mc.checkBox(squared_box, q=False, v=False) and mc.checkBox(cylindrical_box, q=False, v=False) and mc.checkBox(prism_box, q=False, v=False) and mc.checkBox(pipe_box, q=False, v=False):
        #we will delete:
        mc.delete('diogosPolyCube')
        #...and
        mc.delete("diogosPolyCylinder")
        #...and
        mc.delete("diogosPolyPrism")
        #...and
        mc.delete("diogosPolyPipe")



        """window = mc.window( title="Error", iconName='Short Name', widthHeight=(300, 40) )
        mc.columnLayout( adjustableColumn=True )
        mc.text(
        label = 'Chose one option',
        )
        mc.button( label='OK', command=('mc.deleteUI(\"' + window + '\", window=True)') )
        mc.setParent( '..' )
        mc.showWindow( window )"""

        #The error code will also stop the continuation of the programm meaning it will end right here if the values are not correct
        mc.error("You must chose 1 option")

    #WHATEVER ELSE HAPPPENS AND IS NOT SUPPOSED TO...   
    else:
        #we will delete:
        mc.delete('diogosPolyCube')
        #...and
        mc.delete("diogosPolyCylinder")
        #...and
        mc.delete("diogosPolyPrism")
        #...and
        mc.delete("diogosPolyPipe")
        #...and
        mc.error("you can only have 1 option")

# The function will appply the changes done in preview. called by the Apply button
def apply_close():



    meshes = mc.ls(
        transforms=True,
        geometry=True
    )
    

    
    
    #It will rename the mesh into arch once the button will clicked.
    #This is so that, later on, if the user decided to re use the tool, it wont ever delete the arch that he has already created


    #renames any "diogos" meshes that may exist into arch
    for m in meshes:
        if mc.objExists(m) and "diogos" in m:
            mc.rename(m, "arch")


    #closes windows
    for w in mc.lsUI(wnd=True):
        if not w == 'MayaWindow':
            mc.deleteUI(w)


# The function will cancel whatever changes were done and close the window. called by the cancel button
def cancel():

    #deletes any "diogos" meshes that may exist
    meshes = mc.ls(
        transforms=True,
        geometry=True
    )

    for m in meshes:
        if mc.objExists(m) and "diogos" in m:
            mc.delete(m)

    #closes windows
    for w in mc.lsUI(wnd=True):
        if not w == 'MayaWindow':
            mc.deleteUI(w)



#failed attempt. Will leave it here to continue to work on it later
#def close_window(self):

    #meshes = mc.ls(
        #transforms=True,
        #geometry=True
    #)

    #for m in meshes:
        #if mc.objExists(m) and "diogos" in m:
            #mc.delete(m)


    #for w in mc.lsUI(wnd=True):
        #if not w == 'MayaWindow':
            #mc.deleteUI(w)
    
    #close_window()
