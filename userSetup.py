import maya.cmds as cmds
import maya.utils as util

util.executeDeferred(cmds.polyCube)

print "userSetup.py has been executed"
