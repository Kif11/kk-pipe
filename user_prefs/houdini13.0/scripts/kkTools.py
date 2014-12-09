import hou 
import shutil
import os
import re


def hello():
    print "Hello from kkTools"

# Create project structure inside your JOB folder
def createProject(projectPath):
	mainDirList = ["geo", "img", "ref", "export", "comp", "asset", "render", "old", "source", "script"]
	for dir in mainDirList:
		if not(os.path.isdir(projectPath + "/" + dir)):
			os.mkdir(projectPath + "/" + dir)
			print "%s has been created." % dir
		else:
			print '"%s" folder is already exist.' % dir
			
# Create new project folder and copy selected files into it                     
def copyToNewProject(newProject, choose=False):

    hipPath = hou.hipFile.name()
    oldProject =  hou.hscript("echo $JOB")[0][:-1]

    def pathForExport():
        allPath = hou.hscript("opextern -rR -g -l /")[0].split("\n")[:-1]
        selectedPath = []
        if choose:
            selectedItem = hou.ui.selectFromList(allPath)
            for item in selectedItem:
                path = allPath[item]
                selectedPath.append(path)
        else:
            selectedPath = allPath
        
        return selectedPath

    def expandSequence(allPath):
        allPathExpanded = []
        for path in allPath:
            match = re.search(r"\[.+\]", path)
            if match:
                frameRange = re.findall("\d+", match.group())
                seqPath = path[:-len(match.group())-2]
                seqDir = os.path.split(seqPath)[0]
                if os.path.isdir(seqDir):
                    filesInDir = os.listdir(seqDir)
                    for file in filesInDir:
                            filePath = seqDir + "/" + file
                            allPathExpanded.append(filePath)
                else: 
                        print seqDir, "- Folder do not exist"
            else:
                    allPathExpanded.append(path)
        return allPathExpanded

    def deleteMissingPaths(allPaths):
        allPathsCleaned = []
        for path in allPaths:
            if os.path.exists(path):
                allPathsCleaned.append(path)
        return allPathsCleaned

    selectedPath = pathForExport()
    allPathExpanded = expandSequence(selectedPath)
    allPath = deleteMissingPaths(allPathExpanded)
    allPath.append(hipPath)

    # Create folders
    for path in allPath:
        if os.path.isfile(path):
            newFilePath = path.replace(oldProject, newProject)
            newPath = os.path.split(newFilePath)[0]
            if len(newPath) > 0:
                if not os.path.isdir(newPath):
                    os.makedirs(newPath)
            if not os.path.isfile(newFilePath):
                shutil.copyfile(path, newFilePath)
                print newFilePath, "- File has been created"
            else:
                print newFilePath, "- File is already exist"
        else:
            print path, "- Do not exist"

    print "DONE!"

# Handle files saving and maintaning versions and forks
def saveFile():
    # Put everything in the loop to have ability to break the execution
    for file in range(0,1):

        hipPath = hou.hipFile.name()
        JOB = hou.expandString("$JOB")
        houdiniScene = JOB + "/scene/houdini"

        # Version up the name 
        # If file exist freeze the main version and only modyfy the fork
        def versionUp(fileExist=False, forkVersion=0, majorVersion=0, minorVersion=0, treshold=10):
        
            forkVersion = int(forkVersion)
            majorVersion = int(majorVersion)
            minorVersion = int(minorVersion)
        
            if fileExist or forkVersion != 0:
                forkVersion += 1
            else:
                if (minorVersion + 1) >= treshold:
                    minorVersion = 0
                    majorVersion += 1
                else:
                    minorVersion += 1
            
            return "f%d_v%d_%d" %(forkVersion, majorVersion, minorVersion)

        # Chech if the file is unsaved prompt the user to enter a name
        if hipPath == 'untitled.hip':

            userFileNameButtons, userFileName = hou.ui.readInput("Enter the file name", buttons=("OK","CANCEL"))

            # Break file creation if canceled
            if userFileNameButtons == 1:
                break

            outFilePath = "%s/%s_%s.hip" %(houdiniScene, userFileName, versionUp())
            
            # Save hip file
            if not os.path.exists(houdiniScene):
                os.makedirs(houdiniScene)

            hou.hipFile.save(outFilePath)
        
        # If file is already been saved extract all versions value and version it up
        else:
            filePath, fileName = os.path.split(hipPath)
            name, ext = os.path.splitext(fileName)
        
            splitName = name.split("_")
            
            # Check if file name is valid
            if len(splitName) == 4:
                userFileName, forkVersion, majorVersion, minorVersion = splitName
                forkVersion = forkVersion.replace("f","")
                majorVersion = majorVersion.replace("v","")
        
                outFilePath = "%s/%s_%s.hip" %(houdiniScene, userFileName, versionUp(False, forkVersion, majorVersion, minorVersion))
                
                # Check if the newer version exist only iterate the fork
                if os.path.isfile(outFilePath):
                    createFork = hou.ui.displayMessage("Newer version of this file is already exist. Create fork?", buttons=("YES","NO"))
                    if createFork == 0:
                        outFilePath = "%s/%s_%s.hip" %(houdiniScene, userFileName, versionUp(True, forkVersion, majorVersion, minorVersion))
                    else:
                        break

                hou.hipFile.save(outFilePath)
        
            else:
                print "The name of you file is node valid"