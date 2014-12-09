import maya.cmds as cmds
import maya.utils as util
import sys
sys.path.append('./lib_vendor')
import threading
import rpyc
import rpyc.servers.classic_server

# Start Maya rpc server
def start_server(port=45454, use_thread=True, quiet=True):
    # Note that quiet=False only applies when use_thread=False.
    if use_thread:
        thread = threading.Thread(
            target=lambda: start_server(port, use_thread=False))
        thread.start()
        return thread

    args = []
    if quiet:
        args.append("-q")
    args.extend(("-p", str(port), "--dont-register"))

    options, args = rpyc.servers.classic_server.parser.parse_args(args)
    options.registrar = None
    options.authenticator = None
    rpyc.servers.classic_server.serve_threaded(options)

server = start_server()

# Connect to Houdini rpc server
def import_remote_module(server="127.0.0.1", port=18811, name="hou"):
    connection = rpyc.classic.connect(server, port)
    return connection, connection.modules[name]

try:
    connection, hou = import_remote_module()
except:
    print "Can not connect to Houdini rpc server"
    pass



util.executeDeferred(cmds.polyCube)
print "userSetup.py has been executed"
