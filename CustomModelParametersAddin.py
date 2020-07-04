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
selectedComp = None
selectedCompAttributes = {}
newAttribute = None

# Global set of event handlers to keep them referenced for the duration of the command
_handlers = []

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

            if cmdInput.id == "selection":
                # changeAttributes(selectionInput.selection(0).entity.component)
                selectedComp = selectionInput.selection(0).entity.component
                global newAttribute
                newAttribute = selectedComp.attributes.add("Test groupName", "Test name", "Test value")
                print('MyCommandInputChangedHandler')
                print('selectedComp: ' + str(selectedComp))
                print('newAttribute: ' + str(newAttribute))
                print('newAttribute.value: ' + str(newAttribute.value))
                print('selectedComp.attributes.count: ' + str(selectedComp.attributes.count))
                print('selectedComp.attributes.groupNames: ' + str(selectedComp.attributes.groupNames))
                print('selectedComp.attributes.itemByName("Test groupName", "Test name"): ' + str(selectedComp.attributes.itemByName("Test groupName", "Test name")))
                print('selectedComp.attributes.itemByName("Test groupName", "Test name").value: ' + str(selectedComp.attributes.itemByName("Test groupName", "Test name").value))

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

            selectionInput = cmd.commandInputs.addSelectionInput("selection", "Select Parametric Part", "Component to select")
            selectionInput.setSelectionLimits(1, 0)
            selectionInput.addSelectionFilter("Occurrences")

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


    except:
        if ui:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))

def stop(context):
    try:
        print('\n\nstop')
        print('selectedComp: ' + str(selectedComp))
        print('selectedComp.attributes.count: ' + str(selectedComp.attributes.count))
        print('selectedComp.attributes.groupNames: ' + str(selectedComp.attributes.groupNames))
        print('newAttribute :' + str(newAttribute))
        print('selectedComp.attributes.itemByName("Test groupName", "Test name"): ' + str(selectedComp.attributes.itemByName("Test groupName", "Test name")))
        # print('newAttribute.value: ' + str(newAttribute.value))
        print('selectedComp.attributes.itemByName("Test groupName", "Test name").value: ' + str(selectedComp.attributes.itemByName("Test groupName", "Test name").value))

    except:
        if ui:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))