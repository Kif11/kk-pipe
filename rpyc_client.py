import sys
sys.path.append('./lib_vendor')
import rpyc

rpyc.classic.connect("MyService", 12345)