import sys
sys.path.append('./lib_vendor')
import rpyc

def import_remote_module(server="127.0.0.1", port=18811, name="hou"):
    connection = rpyc.classic.connect(server, port)
    return connection, connection.modules[name]

connection, hou = import_remote_module()

obj = hou.node("obj")
obj.createNode("geo")