import hrpyc
from lib_vendor import yaml

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