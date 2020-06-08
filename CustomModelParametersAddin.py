#Author-Justin K
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import json

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
    widthHoles = commandInputs.addIntegerSliderCommandInput('widthHoles', 'Length', 1, 35)
    widthHoles.isVisible = False
    lengthHoles = commandInputs.addIntegerSliderCommandInput('lengthHoles', 'Length', 1, 35)
    lengthHoles.isVisible = False

def hideAllCommandInputs():
    inputs.itemById('widthHoles').isVisible = False
    inputs.itemById('lengthHoles').isVisible = False

def setSomeCommandInputs(parameters):
    for key, value in parameters.items():
        if key == 'lengthHoles':
            thisIndexMP = value['indexMP']
            globalInputIndex[thisIndexMP] = key

            thisInput = inputs.itemById('lengthHoles')
            # thisInput.setText
            # thisInput.setText(value['name'], '')
            thisInput.minimumValue = value['minValue']
            thisInput.maximumValue = value['maxValue']
            # modelParameters.item(1).expression = str(globalSize)
            thisInput.expressionOne = str(globalComp.modelParameters.item(thisIndexMP).expression)
            thisInput.isVisible = True


def updateInputs():
    global globalComp
    global globalParameters

    selectionInput = inputs.itemById('selection')
    if cmdInput.id == 'selection':

        if selectionInput.selectionCount > 0:
            if app.activeProduct.rootComponent != selectionInput.selection(0).entity:
                globalComp = selectionInput.selection(0).entity.component
                if globalComp and globalComp.attributes.count > 0 and globalComp.attributes.itemByName('pVFL', 'part name').isValid:
                    setSomeCommandInputs(json.loads(globalComp.attributes.itemByName('pVFL', 'parameters').value))
                else:
                    selectionInput.clearSelection()
            else:
                selectionInput.clearSelection()

        else:
            hideAllCommandInputs()
            globalParameters.clear()
    else:
        for key, value in globalInputIndex.items():
            globalParameters[key] = inputs.itemById(value).expressionOne

    # sizeInput.isVisible = True
    # if cmdInput.id == 'widthHoles':
    global globalSize
    globalSize = inputs.itemById('lengthHoles')

def updateParameters():
    for key, value in globalParameters.items():
        globalComp.modelParameters.item(key).expression = value
        # globalComp.modelParameters.item(key).expression = inputs.itemById(value).expressionOne
        # global inputs
        # print(str(globalSize.expressionOne))
        # print(str(inputs.itemById('lengthHoles').expressionOne))
        pass




        

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
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


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
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


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
            # tabCmdInput1 = inputs.addTabCommandInput('tab_1', 'Tab 1')
            editParametricInputs = inputs

            # Create a selection input.
            selectionInput = editParametricInputs.addSelectionInput('selection', 'Select Parametric Part', 'Component to select')
            selectionInput.setSelectionLimits(1,1)
            selectionFilter = selectionInput.addSelectionFilter("Occurrences")
            # selectionInput.selectionFilters = selectionFilter

            # Create integer slider input with one slider.
            # sliderOne = editParametricInputs.addIntegerSliderCommandInput('widthHoles', 'Length', 1, 35)
            # sliderOne.isVisible = False

            createAllCommandInputs(editParametricInputs)

        except:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def run(context):
    try:
        global app, ui
        app = adsk.core.Application.get()
        ui = app.userInterface

        # Get the existing command definition or create it if it doesn't already exist.
        cmdDef = ui.commandDefinitions.itemById('cmdInputsSample')
        if not cmdDef:
            cmdDef = ui.commandDefinitions.addButtonDefinition('cmdInputsSample', 'Edit Parametric Part', 'Sample to demonstrate various command inputs.')

        # Connect to the command created event.
        onCommandCreated = MyCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        _handlers.append(onCommandCreated)

        # Execute the command definition.
        cmdDef.execute()

        # Prevent this module from being terminated when the script returns, because we are waiting for event handlers to fire.
        adsk.autoTerminate(False)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    try:
        
        # # ui.messageBox('end')
        # globalComp.modelParameters.item(1).expression = str(globalSize)
        # globalComp.attributes.add('VEX_CAD', 'Name', '2 wide C-Channel')
        # globalComp.attributes.add('VEX_CAD', 'Description', 'Words, words, more words...')
        # globalComp.attributes.add('VEX_CAD', 'Parameters', '1')
        # print('globalComp.attributes.count: ' + str(globalComp.attributes.count))
        # print(str(globalComp.attributes.itemsByGroup('pVFL')[0].name))
        # testAttribute = str(globalComp.attributes.itemByName('VEX_CAD', 'parameters').value)
        # # globalComp.modelParameters.itemByName('Model_Param').expression = testAttribute
        # print(testAttribute)

        updateParameters()

        # print(str(globalComp.attributes.count))
        # print(str(globalComp.attributes.groupNames))
        # print(str(globalComp.attributes.itemByName('pVFL', 'part name').value))
        # print(str(globalComp.attributes.itemByName('pVFL', 'parametric').value))
        # print(str(globalComp.attributes.itemByName('pVFL', 'parameters').value))

        # globalComp.attributes.add('pVFL', 'part name', 'Al 1x2x1x35 C-Channel v1')
        # globalComp.attributes.add('pVFL', 'parametric', '1')
        # globalComp.attributes.add('pVFL', 'parameters', '{"lengthHoles": {"name": "Length", "indexMP": 1, "minValue": 1, "maxValue": 35} }')
        pass

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))