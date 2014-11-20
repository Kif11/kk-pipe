import sys
sys.path.append('./lib_vendor')
import threading
import rpyc
import rpyc.servers.classic_server
# from rpyc.utils.server import ThreadedServer

# "./lib_vendor/rpyc/servers/classic_server.py"

# import rpyc
#
# from rpyc.utils.server import ThreadedServer # or ForkingServer
#
# class MyService(rpyc.Service):
#     #
#     # ... you service's implementation
#     #
#     pass
#
#
# server = ThreadedServer(MyService, port = 12345)
# server.start()

def start_server(port=18811, use_thread=True, quiet=True):
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

# start_server()