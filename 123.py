import hrpyc
from lib_vendor import yaml
import sys
sys.path.append('F:/python/kk_pipe/lib_vendor')
import rpyc
import rpyc.servers.classic_server

# Run rpc server
server = hrpyc.start_server()
print "RPC Server Running", server

hou_session_file = open('config/hou_session.yml')
hou_session_dictionary = yaml.load(hou_session_file)
hou_session_file.close()

def set_global_var(name, value):
    cmd = 'set -g %s="%s"' % (name, value)
    print cmd
    hou.hscript(str(cmd))

set_global_var("JOB", hou_session_dictionary["JOB"])
set_global_var("WORK", hou_session_dictionary["WORK"])

# Connect ot maya rpc
def import_remote_module(server="127.0.0.1", port=45454, name="maya.cmds"):
    connection = rpyc.classic.connect(server, port)
    return connection, connection.modules[name]

try:
    connection, cmds = import_remote_module()
except:
    pass
    print "Can not connect to Maya rpc server"

