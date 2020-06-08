#Author-Justin K
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

app = None
ui  = None
global eventArgs
global inputs
global cmdInput
# selectionInput = None
globalComp = None
globalSize = None

# Global set of event handlers to keep them referenced for the duration of the command
_handlers = []

def updateParameters():
    sizeInput = inputs.itemById('intSlider')
    selectionInput = inputs.itemById('selection')

    if cmdInput.id == 'selection':
        sizeInput.isVisible = bool(selectionInput.selectionCount)
        if selectionInput.selectionCount > 0:
            global globalComp
            globalComp = selectionInput.selection(0).entity.component
            sizeInput.expressionOne = str(int(globalComp.modelParameters.item(1).value))

    # sizeInput.isVisible = True
    # if cmdInput.id == 'intSlider':
    global globalSize
    globalSize = sizeInput.valueOne



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

            updateParameters()

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
            tab1ChildInputs = inputs
            
            # # Create a message that spans the entire width of the dialog by leaving out the "name" argument.
            # message = '<div align="center">A "full width" message using <a href="http:fusion360.autodesk.com">html.</a></div>'
            # tab1ChildInputs.addTextBoxCommandInput('fullWidth_textBox', '', message, 1, True)            

            # Create a selection input.
            selectionInput = tab1ChildInputs.addSelectionInput('selection', 'Select Parametric Part', 'Component to select')
            selectionInput.setSelectionLimits(1,1)
            selectionFilter = selectionInput.addSelectionFilter("Occurrences")
            # selectionInput.selectionFilters = selectionFilter

            # Create integer slider input with one slider.
            sliderOne = tab1ChildInputs.addIntegerSliderCommandInput('intSlider', 'Length', 1, 35)
            sliderOne.minimumValue = 20
            sliderOne.isVisible = False

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
        globalComp.modelParameters.item(1).expression = str(globalSize)
        # globalComp.attributes.add('VEX_CAD', 'Name', '2 wide C-Channel')
        # globalComp.attributes.add('VEX_CAD', 'Description', 'Words, words, more words...')
        # globalComp.attributes.add('VEX_CAD', 'Parameters', '1')
        # print('globalComp.attributes.count: ' + str(globalComp.attributes.count))
        # # ui.messageBox(str(globalComp.attributes.count))
        # ui.messageBox(str(globalComp.attributes.groupNames))
        # # ui.messageBox(str(globalComp.attributes.itemsByGroup('VEX_CAD')[0].name))
        # testAttribute = str(globalComp.attributes.itemByName('VEX_CAD', 'parameters').value)
        # # globalComp.modelParameters.itemByName('Model_Param').expression = testAttribute
        # ui.messageBox(testAttribute)

        # # ui.messageBox(str(globalComp.attributes.itemByName('testAttribute')))
        pass

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))