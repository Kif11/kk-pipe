# import sys
# sys.path.append("./lib_vendor")
# import wmi
#
# print dir(wmi)



# import _winreg
#
# # key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0, _winreg.KEY_READ)
#
# key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall", 0, _winreg.KEY_READ)
#
# print _winreg.DisableReflectionKey(key)
#
# print _winreg.QueryReflectionKey(key)

import win32com.client
strComputer = "."
objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
colItems = objSWbemServices.ExecQuery("Select * from Win32_Product")
for objItem in colItems:
    print "Caption: ", objItem.Caption
    print "Description: ", objItem.Description
    print "Identifying Number: ", objItem.IdentifyingNumber
    print "Install Date: ", objItem.InstallDate
    print "Install Date 2: ", objItem.InstallDate2
    print "Install Location: ", objItem.InstallLocation
    print "Install State: ", objItem.InstallState
    print "Name: ", objItem.Name
    print "Package Cache: ", objItem.PackageCache
    print "SKU Number: ", objItem.SKUNumber
    print "Vendor: ", objItem.Vendor
    print "Version: ", objItem.Version

# for i in range(0,221):
#     try:
#         print _winreg.EnumKey(key, i)
#     except:
#         pass

# HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\LinuxLive USB Creator



# for i in range(0,221):
#     try:
#         keyName = _winreg.EnumKey(key, i)
#         newKey = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\" + keyName
#         subKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, newKey, 0, _winreg.KEY_READ)
#         print _winreg.QueryValueEx(subKey, "DisplayName")
#     except:
#         pass
# for i in xrange(0, _winreg.QueryInfoKey(key)[1]-1):
#     print _winreg.EnumValue(key, i)

# print _winreg.QueryInfoKey(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")