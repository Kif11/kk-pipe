# import threading
# import rpyc
# import rpyc.servers.classic_server
#
#
# args = ["-p", "18811", "--dont-register"]
# options = rpyc.servers.classic_server.parser.parse_args(args)[0]
# options.registrar = None
# options.authenticator = None
# print options
#
#
# rpcServer = rpyc.servers.classic_server.serve_threaded(options)
# newTread = threading.Thread(target=rpcServer, name="myThread")
#
# print newTread.start()

dir(newTread)