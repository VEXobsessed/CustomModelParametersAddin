#Author-Justin K
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import json, os, sys

app = None
ui  = None

# shawn - to access these globals try to declare them at the top and only assign after using the global <name> syntax
# shawn - Since you declare them here no need to specify global it's automatically derived from the context
selectedComp = None
selectedCompAttributes = {}

# Global set of event handlers to keep them referenced for the duration of the command
_handlers = []

# shawn - This is the command that gets run when you push OK
class MyCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            eventArgs = adsk.core.CommandEventArgs.cast(args)

            # Get the values from the command inputs. 
            inputs = eventArgs.command.commandInputs

            selectionInput = inputs.itemById("selection")

            # because you are assigning selectedComp we need to use global selectedComp here
            global selectedComp

            print("Someone clicked okay and a occurence was found")
            # changeAttributes(selectionInput.selection(0).entity.component)
            selectedComp = selectionInput.selection(0).entity.component
            selectedComp.attributes.add("Test groupName", "Test name", "Test value")
            print('MyCommandInputChangedHandler')
            print('selectedComp:\n' + str(selectedComp))
            print('selectedComp.attributes.count:\n' + str(selectedComp.attributes.count))
            print('selectedComp.attributes.groupNames:\n' + str(selectedComp.attributes.groupNames))
            print('selectedComp.attributes.itemByName("Test groupName", "Test name"):\n' + str(selectedComp.attributes.itemByName("Test groupName", "Test name")))
            print('selectedComp.attributes.itemByName("Test groupName", "Test name").value:\n' + str(selectedComp.attributes.itemByName("Test groupName", "Test name").value))

            # Destroy event handler will still be called
        except:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))
 

# Event handler that reacts to any changes the user makes to any of the command inputs.
class MyCommandInputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            print("Something is changing but not set yet.\n")
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

            # NEW ______________________
            # Connect to the execute event.
            onExecute = MyCommandExecuteHandler()
            cmd.execute.add(onExecute)
            _handlers.append(onExecute)
            # __________________________

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
        print('\nstop')

        # shawn - Real fast check to see if the global variable was ever set this instance, if multiple commands are started I would assign in the run method to None.
        if selectedComp:
            # shawn - A little output to show you the result even if you don't have debug open.
            if ui:
                ui.messageBox('{} has {} test attribute , \n \tTest groupName : {}'.format(selectedComp.name, selectedComp.attributes.count, selectedComp.attributes.itemByName("Test groupName", "Test name").value))
            print('selectedComp:\n' + str(selectedComp))
            print('selectedComp.attributes.count:\n' + str(selectedComp.attributes.count))
            print('selectedComp.attributes.groupNames:\n' + str(selectedComp.attributes.groupNames))
            print('selectedComp.attributes.itemByName("Test groupName", "Test name"):\n' + str(selectedComp.attributes.itemByName("Test groupName", "Test name")))
            print('selectedComp.attributes.itemByName("Test groupName", "Test name").value:\n' + str(selectedComp.attributes.itemByName("Test groupName", "Test name").value))

    except:
        if ui:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))
