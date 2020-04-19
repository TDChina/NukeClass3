import nuke

def autoCrop():
 # keep original node information...we'll need this
 original_nodes = nuke.selectedNodes()

 # deselect everything
 all_nodes = nuke.allNodes()
 for i in all_nodes:
   i.knob("selected").setValue(False)

 for i in original_nodes:
   i.knob("selected").setValue(True)
   autocropper = nuke.createNode("CurveTool", "operation 0 ROI {0 0 input.width input.height} Layer rgba name Processing selected true", False)

   # let's get the node info for the curvewriter (we'll need this too)
   # execute the curvewriter thru all the frames
   root = nuke.root()
   nuke.executeMultiple([autocropper,], ([int(root.knob("first_frame").value()), int(root.knob("last_frame").value()), 1],))

   # deselect everything
   all_nodes = nuke.allNodes()
   for j in all_nodes:
     j.knob("selected").setValue(False)

   # select the curvewriter
   autocropper.knob("selected").setValue(True)

   # add crop node
   cropnode = nuke.createNode("Crop", "label AutoCrop", False)

   # put the new data from the autocrop into the new crop
   #nuke.knob(cropnode.name()+".box", nuke.knob(autocropper.name()+".autocropdata"));
   cropbox = cropnode.knob("box");
   autocropbox = autocropper.knob("autocropdata");
   cropbox.copyAnimations(autocropbox.animations())

   # turn on the animated flag
   cropnode.knob("indicators").setValue(1)
   cropnode.knob("icon").setValue("warning.xpm")

   # deselect everything
   all_nodes = nuke.allNodes()
   for j in all_nodes:
     j.knob("selected").setValue(False)

   # select the curvewriter and delete it
   autocropper.knob("selected").setValue(True)

   # delete the autocropper to make it all clean
   nuke.delete( autocropper )

   # deselect everything
   all_nodes = nuke.allNodes()
   for j in all_nodes:
     j.knob("selected").setValue(False)

   # select the new crop
   cropnode.knob("selected").setValue(True)

   # place it in a nice spot
   nuke.autoplace(cropnode)

   # De-Select it
   cropnode.knob("selected").setValue(False)
