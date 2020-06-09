#Author-Justin K
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import json
import os, sys

app = None
ui  = None
global eventArgs
global inputs
global cmdInput
# selectionInput = None
globalComp = None
globalParameters = {}
globalInputIndex = {}
globalSize = None

# Global set of event handlers to keep them referenced for the duration of the command
_handlers = []

def createAllCommandInputs(commandInputs):
    widthHoles = commandInputs.addIntegerSliderCommandInput("widthHoles", "Width", 1, 35)
    widthHoles.isVisible = False
    lengthHoles = commandInputs.addIntegerSliderCommandInput("lengthHoles", "Length", 1, 35)
    lengthHoles.isVisible = False
    inserts = commandInputs.addDropDownCommandInput("inserts", "Inserts", 0)
    inserts.isVisible = False
    inserts.listItems.add("None", True)
    inserts.listItems.add("Square", False)
    inserts.listItems.add("Round", False)

def hideAllCommandInputs():
    inputs.itemById("widthHoles").isVisible = False
    inputs.itemById("lengthHoles").isVisible = False

def setHoles(key, value):
    thisIndexMP = value["indexMP"]
    globalInputIndex[key] = {"value": "", "indexMP": thisIndexMP}

    thisInput = inputs.itemById(key)
    # thisInput.setText
    # thisInput.setText(value["name"], "")
    thisInput.minimumValue = value["minValue"]
    thisInput.maximumValue = value["maxValue"]
    # modelParameters.item(1).expression = str(globalSize)
    thisInput.expressionOne = str(globalComp.modelParameters.item(thisIndexMP).expression)
    thisInput.isVisible = True

def setInserts(key, value):
    globalInputIndex[key] = {"value": ""}
    # listItems = add
    thisInput = inputs.itemById(key)
    # thisInput.expressionOne = str(globalComp.modelParameters.item(thisIndexMP).expression)
    # globalComp.
    thisInput.isVisible = True

def setSomeCommandInputs(parameters):
    for key, value in parameters.items():
        if key == "lengthHoles":
            setHoles(key, value)
        elif key == "widthHoles":
            setHoles(key, value)
        elif key == "inserts":
            setInserts(key, value)

def updateInputs():
    global globalComp
    global globalParameters

    selectionInput = inputs.itemById("selection")
    if cmdInput.id == "selection":
        hideAllCommandInputs()
        globalParameters.clear()
        if selectionInput.selectionCount > 0:
            if app.activeProduct.rootComponent != selectionInput.selection(0).entity:
                globalComp = selectionInput.selection(0).entity.component
                if globalComp and globalComp.attributes.count > 0 and globalComp.attributes.itemByName("pVFL", "data"):
                    # print(json.loads(globalComp.attributes.itemByName("pVFL", "data").value)["parameters"])
                    setSomeCommandInputs(json.loads(globalComp.attributes.itemByName("pVFL", "data").value)["parameters"])
                else:
                    selectionInput.clearSelection()
            else:
                selectionInput.clearSelection()
    else:
        for key, value in globalInputIndex.items():
            print(globalInputIndex)
            globalParameters[key] = globalInputIndex[key]
            if inputs.itemById(key).classType() == "adsk::core::DropDownCommandInput":
                globalParameters[key] = {"value": inputs.itemById(key).selectedItem.name}
            elif inputs.itemById(key).classType() == "adsk::core::IntegerSliderCommandInput":
                globalParameters[key]["value"] = inputs.itemById(key).expressionOne
            pass
            print(globalParameters)


    # sizeInput.isVisible = True
    # if cmdInput.id == "widthHoles":
    global globalSize
    globalSize = inputs.itemById("lengthHoles")

def updateModelParameter(comp, parameters):
    comp.modelParameters.item(parameters["indexMP"]).expression = parameters["value"]

def updateBodyBulbs(comp, parameters):
    for key, value in parameters.items():
        comp.bRepBodies.itemByName(key).isLightBulbOn = value

def updateInserts(comp, parameters):
    # print(parameters)
    if parameters["value"] == "None":
        updateBodyBulbs(comp, {"Square Insert 1": False, "Square Insert 2": False, "Round Insert 1": False, "Round Insert 2": False})
    elif parameters["value"] == "Square":
        updateBodyBulbs(comp, {"Square Insert 1": True, "Square Insert 2": True, "Round Insert 1": False, "Round Insert 2": False})
    elif parameters["value"] == "Round":
        updateBodyBulbs(comp, {"Square Insert 1": False, "Square Insert 2": False, "Round Insert 1": True, "Round Insert 2": True})


def updatePart(comp, parameterList):
    for key, value in parameterList.items():
        if key == "lengthHoles":
            updateModelParameter(comp, value)
        elif key == "widthHoles":
            updateModelParameter(comp, value)
        elif key == "inserts":
            updateInserts(comp, value)

    # updateModelParameter(globalComp, {"lengthHoles": {"value": "12", "indexMP": 1}})
    # updateModelParameter(globalComp, globalParameters)
    # updateInserts(globalComp, globalParameters)




        

# Event handler that reacts to any changes the user makes to any of the command inputs.
class MyCommandInputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            global eventArgs
            global inputs
            global cmdInput
            eventArgs = adsk.core.InputChangedEventArgs.cast(args)
            inputs = eventArgs.inputs
            cmdInput = eventArgs.input

            updateInputs()

        except:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))


# Event handler that reacts to when the command is destroyed. This terminates the script.            
class MyCommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # When the command is done, terminate the script
            # This will release all globals which will remove all event handlers
            adsk.terminate()
        except:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))


# Event handler that reacts when the command definition is executed which
# results in the command being created and this event being fired.
class MyCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            
            # Get the command that was created.
            cmd = adsk.core.Command.cast(args.command)

            # Connect to the command destroyed event.
            onDestroy = MyCommandDestroyHandler()
            cmd.destroy.add(onDestroy)
            _handlers.append(onDestroy)

            # Connect to the input changed event.           
            onInputChanged = MyCommandInputChangedHandler()
            cmd.inputChanged.add(onInputChanged)
            _handlers.append(onInputChanged)    

            # Get the CommandInputs collection associated with the command.
            inputs = cmd.commandInputs

            # Create a tab input.
            # tabCmdInput1 = inputs.addTabCommandInput("tab_1", "Tab 1")
            editParametricInputs = inputs

            # Create a selection input.
            selectionInput = editParametricInputs.addSelectionInput("selection", "Select Parametric Part", "Component to select")
            selectionInput.setSelectionLimits(1,1)
            selectionFilter = selectionInput.addSelectionFilter("Occurrences")
            # selectionInput.selectionFilters = selectionFilter

            # Create integer slider input with one slider.
            # sliderOne = editParametricInputs.addIntegerSliderCommandInput("widthHoles", "Length", 1, 35)
            # sliderOne.isVisible = False

            createAllCommandInputs(editParametricInputs)

        except:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))


def run(context):
    try:
        global app, ui
        app = adsk.core.Application.get()
        ui = app.userInterface

        # Get the existing command definition or create it if it doesn"t already exist.
        cmdDef = ui.commandDefinitions.itemById("cmdInputsSample")
        if not cmdDef:
            cmdDef = ui.commandDefinitions.addButtonDefinition("cmdInputsSample", "Edit Parametric Part", "Sample to demonstrate various command inputs.")

        # Connect to the command created event.
        onCommandCreated = MyCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        _handlers.append(onCommandCreated)

        # Execute the command definition.
        cmdDef.execute()

        # Prevent this module from being terminated when the script returns, because we are waiting for event handlers to fire.
        adsk.autoTerminate(False)

        # importManager = app.importManager
        # rootComp = app.activeProduct.rootComponent
        # # Get archive import options
        # archiveFileName = "C:\\library/Test C-Channel.f3d"
        # archiveOptions = importManager.createFusionArchiveImportOptions(archiveFileName)
        
        # # Import archive file to root component
        # importManager.importToTarget(archiveOptions, rootComp)


    except:
        if ui:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))

def stop(context):
    try:
        updatePart(globalComp, globalParameters)

        # print(str(globalComp.attributes.count))
        # print(str(globalComp.attributes.groupNames))
        # print(str(globalComp.attributes.itemByName("pVFL", "part name").value))
        # print(str(globalComp.attributes.itemByName("pVFL", "parametric").value))
        # print(str(globalComp.attributes.itemByName("pVFL", "parameters").value))

        # globalComp.attributes.add("pVFL", "part name", "Al 1x2x1x35 C-Channel v1")
        # globalComp.attributes.add("pVFL", "parametric", "1")
        # globalComp.attributes.add("pVFL", "parameters", "{"lengthHoles": {"name": "Length", "indexMP": 1, "minValue": 1, "maxValue": 35} }")

        # globalComp.attributes.add("pVFL", "part name", "Al 1x25 Plate v1")
        # globalComp.attributes.add("pVFL", "parametric", "1")
        # globalComp.attributes.add("pVFL", "parameters", "{"widthHoles": {"name": "Width", "indexMP": 0, "minValue": 1, "maxValue": 5}, "lengthHoles": {"name": "Length", "indexMP": 1, "minValue": 1, "maxValue": 25} }")
        
        # globalComp.attributes.add("pVFL", "data",
        # """{
        #     "partName": "Al 1x2x1x35 C-Channel v1",
        #     "isParametric": "1",
        #     "parameters": {
        #         "lengthHoles": {
        #             "indexMP": 1,
        #             "minValue": 1,
        #             "maxValue": 35
        #         }
        #     }
        # }""")

        # globalComp.attributes.add("pVFL", "data",
        # """{
        #     "partName": "HS 36t Gear v1",
        #     "isParametric": "1",
        #     "parameters": {
        #         "inserts": {
        #             "squareBodies": ["Square Insert 1", "Square Insert 2"],
        #             "roundBodies": ["Round Insert 1", "Round Insert 2"]
        #         }
        #     }
        # }""")
        pass

    except:
        if ui:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))