#Author-Justin K
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import json
import os, sys

changeAttributesEnabled = False
# changeAttributesEnabled = True
identifyModelParametersEnabled = False
# identifyModelParametersEnabled = True

app = None
ui  = None
global eventArgs
global inputs
global cmdInput
# selectionInput = None
selectedComp = None
selectedCompAttributes = {}
# globalSize = None

manualAttributes = """{
	"partName": "Al 1x2x1x35 C-Channel v1",
	"isParametric": true,
	"parameters": {
		"FloatSpinnerHolesIndex": {
			"indexDistance": 1,
			"indexOffset": 2,
			"minValue": 0.5,
			"maxValue": 35,
			"multiplier": "0.5 in"
		}
	}
}"""

# manualAttributes = """{
# 	"partName": "Al 1x2x1x35 C-Channel v1",
# 	"isParametric": 1,
# 	"parameters": {
# 		"lengthHoles": {
# 			"indexMP": 1,
# 			"minValue": 1,
# 			"maxValue": 35
# 		}
# 	}
# }"""


# Global set of event handlers to keep them referenced for the duration of the command
_handlers = []

def changeAttributes(comp):
    app = adsk.core.Application.get()
    ui = app.userInterface
    design = app.activeProduct
    if changeAttributesEnabled:
        attribute = selectedComp.attributes.add("pVFL", "data", """{
	"partName": "Al 1x2x1x35 C-Channel v1",
	"isParametric": true,
	"parameters": {
		"FloatSpinnerHolesIndex": {
			"indexDistance": 1,
			"indexOffset": 2,
			"minValue": 0.5,
			"maxValue": 35,
			"multiplier": 0.5
		}
	}
}""")
    # print(attribute.value)
    # print(selectedComp.attributes.itemByName("pVFL", "data").value)
        
        # # ui.inputBox("Enter JSON string", "Change attributes")
        #  # Prompt the user for a string and validate it's valid.
        # isValid = False
        # # input = ''  # The initial default value.
        # while not isValid:
        #     # Get a string from the user.
        #     enterJSON = ui.inputBox('Enter JSON string', 'Change Attributes')
        #     # print(enterJSON)
        #     # isCancelled = False
        #     # if enterJSON[0]:
        #     #     (input, isCancelled) = enterJSON
            
        #     # Exit the program if the dialog was cancelled.
        #     if enterJSON[1]:
        #         return
            
        #     # Check that a valid length description was entered.
        #     unitsMgr = design.unitsManager
        #     try:
        #         # realValue = unitsMgr.evaluateExpression(input, unitsMgr.defaultLengthUnits)
        #         json.loads(enterJSON[0])
        #         isValid = True
        #         applyJSON = ui.messageBox(enterJSON[0] + '\n\nis a valid JSON string.' + '\n\nWould you like to apply it?', 'Apply Attributes',
        #               adsk.core.MessageBoxButtonTypes.OKCancelButtonType)
        #         if applyJSON == 0:
        #             comp.attributes.add("pVFL", "data", enterJSON[0])
        #     except:
        #         # Invalid expression so display an error and set the flag to allow them
        #         # to enter a value again.
        #         ui.messageBox(enterJSON[0] + '\n\nis not a valid JSON string.', 'Invalid entry', 
        #                       adsk.core.MessageBoxButtonTypes.OKButtonType, 
        #                       adsk.core.MessageBoxIconTypes.CriticalIconType)
        #         isValid = False

def identifyModelParameters(comp):
    if identifyModelParametersEnabled:
        for index in range(comp.modelParameters.count):
            comp.modelParameters.item(index).expression = str(index)









inputsDict = []

def defineInputs():
    unitsMgr = app.activeProduct.unitsManager

    def inchesToHolesValue(input):
        return unitsMgr.evaluateExpression(input + '/' + '0.5in', '')
    
    def holesToInchesValue(input):
        return unitsMgr.evaluateExpression(input + '*' + '0.5in', '')

    class Input:
        def __init__(self, id, name):
            self.id = id
            self.name = name
        def hide(self):
            self.input.isVisible = False
    
    class IntSliderTwo(Input):
        def create(self, commandInputs):
            self.input = commandInputs.addIntegerSliderCommandInput(self.id, self.name, 1, 2, True)
        def show(self, parameter):
            self.parameter = parameter
            self.input.minimumValue = self.parameter["minValue"]
            self.input.maximumValue = self.parameter["maxValue"]
            thisIndexMP = self.parameter["indexMP"]
            self.input.expressionTwo = str(selectedComp.modelParameters.item(thisIndexMP).expression)
            self.updateValue()
            self.input.isVisible = True
        def updateValue(self):
            self.expressionOne = self.input.expressionOne
            self.expressionTwo = self.input.expressionTwo
        def updatePart(self, comp):
            # print('IntSliderTwo.updatePart:')
            # print(comp)
            # comp.modelParameters.item(1).expression = '1'
            # print(self.expressionTwo)
            comp.modelParameters.item(self.parameter["indexMP"]).expression = self.expressionTwo

    class FloatSpinnerHolesIndex(Input):
        def create(self, commandInputs):
            self.inputDistance = commandInputs.addFloatSpinnerCommandInput(self.id + 'Distance', self.name, '', 0, 40, 1, 0)
            self.inputOffset = commandInputs.addFloatSpinnerCommandInput(self.id + 'Offset', 'Offset Holes', '', 0, 40, 1, 0)
        def show(self, parameter):
            self.parameter = parameter
            # self.inputDistance.minimumValue = self.parameter["minValue"]
            # self.inputDistance.maximumValue = self.parameter["maxValue"]
            indexDistance = self.parameter["indexDistance"]
            indexOffset = self.parameter["indexOffset"]
            self.inputDistance.expression = str(inchesToHolesValue(selectedComp.modelParameters.item(indexDistance).expression))
            
            self.inputDistance.isVisible = True
            self.inputOffset.isVisible = True
            self.updateValue()
        def hide(self):
            self.inputDistance.isVisible = False
            self.inputOffset.isVisible = False
        def updateValue(self):
            if self.inputDistance.value + self.inputOffset.value > self.parameter["maxValue"]:
                self.inputOffset.value = self.parameter["maxValue"] - self.inputDistance.value

            inputDistanceFloat = unitsMgr.evaluateExpression(self.inputDistance.expression, '')
            # if inputDistanceFloat > inchesToHolesValue(selectedComp.modelParameters.item(indexDistance).expression):
            print(inputDistanceFloat)
            # if inputDistanceFloat > self.parameter["maxValue"]:
            #     self.inputDistance.expression = str(self.parameter["maxValue"])
            #     self.updateValue()
            # if inputDistanceFloat > self.parameter["maxValue"]:
            #     self.inputDistance.expression = str(self.parameter["maxValue"])
            #     self.updateValue()

            self.expressionDistance = self.inputDistance.expression
            self.expressionOffset = self.inputOffset.expression
        def updatePart(self, comp):
            comp.modelParameters.item(self.parameter["indexDistance"]).value = holesToInchesValue(self.expressionDistance)
            comp.modelParameters.item(self.parameter["indexOffset"]).value = holesToInchesValue(self.expressionOffset)
    
    return [
        # IntSliderTwo('widthHoles', 'Width'),
        IntSliderTwo('lengthHoles', 'Length'),
        FloatSpinnerHolesIndex('FloatSpinnerHolesIndex', 'Length Holes')]













def createAllCommandInputs(commandInputs):
    pass

def hideAllCommandInputs():
    for input in inputsDict:
        inputsDict[input].hide()

def showSomeCommandInputs(parameters):
    for parameter in parameters:
        inputsDict[parameter].show(parameters[parameter])

def updateInputs(parameters):
        for parameter in parameters:
            inputsDict[parameter].updateValue()

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


def updatePart(comp, parameters):
    # print('updatePart: ')
    # print(comp)
    for parameter in parameters['parameters']:
        inputsDict[parameter].updatePart(comp)

    # for key, value in parameters.items():
    #     if key == "lengthHoles":
    #         updateModelParameter(comp, value)
    #     elif key == "widthHoles":
    #         updateModelParameter(comp, value)
    #     elif key == "inserts":
    #         updateInserts(comp, value)
        

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
            

            global selectedComp
            global selectedCompAttributes

            selectionInput = inputs.itemById("selection")
            # changeAttributes(selectionInput.selection(0).entity.component)

            if cmdInput.id == "selection":
                # selectionInput.selection(0).entity.component.modelParameters.item(1).expression = '10'
                # print('MyCommandInputChangedHandler: ')
                # print(selectionInput.selection(0).entity.component)
                if selectionInput.selectionCount == 1 and app.activeProduct.rootComponent != selectionInput.selection(0).entity:
                    selectedComp = selectionInput.selection(0).entity.component
                    # print(selectedComp.attributes.itemByName("pVFL", "data").value)
                    changeAttributes(selectedComp)
                    identifyModelParameters(selectedComp)
                    # if selectedComp and selectedComp.attributes.count > 0 and selectedComp.attributes.itemByName("pVFL", "data"):
                        # selectedCompAttributes = json.loads(selectedComp.attributes.itemByName("pVFL", "data").value)
                    # if selectedComp and selectedComp.attributes.count > 0:
                    selectedCompAttributes = json.loads(manualAttributes)
                    showSomeCommandInputs(selectedCompAttributes["parameters"])
                    # else:
                        # selectionInput.clearSelection()
                else:
                    selectionInput.clearSelection()
                    selectedCompAttributes.clear()
                    hideAllCommandInputs()
            else:
                updateInputs(selectedCompAttributes["parameters"])
            # print(selectedComp.attributes.itemByName("pVFL", "data").value)

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
            # inputs = cmd.commandInputs

            # Create a tab input.
            # tabCmdInput1 = inputs.addTabCommandInput("tab_1", "Tab 1")
            selectionInput = cmd.commandInputs.addSelectionInput("selection", "Select Parametric Part", "Component to select")
            selectionInput.setSelectionLimits(1, 0)
            selectionInput.addSelectionFilter("Occurrences")

            global inputsDict
            inputsDict = {inputs.id: inputs for inputs in defineInputs()}
            for input in inputsDict:
                inputsDict[input].create(cmd.commandInputs)
            hideAllCommandInputs()


            # createAllCommandInputs(editParametricInputs)

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
        # print('hi')
        # if not changeAttributesEnabled and identifyModelParametersEnabled:
            # ui.messageBox("Failed:\n{}".format(traceback.format_exc()))
        updatePart(selectedComp, selectedCompAttributes)
        # print(selectedComp.attributes.itemByName("pVFL", "data").value)

    except:
        if ui:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))