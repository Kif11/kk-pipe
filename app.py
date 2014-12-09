import os
import sys
import subprocess
import util
from lib_vendor import yaml



class App(util.Util):

    def __init__(self):
        # Read variables from yaml file
        # App launch
        app_launch_file = open('config/app_launch.yml')
        self.app_launch_dictionary = yaml.load(app_launch_file)
        app_launch_file.close()
        # Project
        app_launch_file = open('config/project.yml')
        self.project_dictionary = yaml.load(app_launch_file)
        app_launch_file.close()

        # Find current platforme
        self.platform_name = {"linux2": "linux", "darwin": "mac", "win32": "windows"}[sys.platform]

    def launch(self, app_name=None, projects_directory=None, full_context_path=None):

        # Place where all your projects are
        self.projects_directory = projects_directory.replace("\\", "/")

        # Path for the application executable
        print self.projects_directory
        app_launch_path = self.app_launch_dictionary[app_name]["%s_launch_path" % self.platform_name]

        # Command line arguments
        app_cmd_args = self.app_launch_dictionary[app_name]["%s_args" % self.platform_name]

        # Path to selected context such as project/shot/sq01/sh010
        context_path = full_context_path.replace(self.projects_directory, "")

        # Path to the project such as D:/projects/project_name
        splitPath = context_path.split("/")[1:]
        project_path = self.projects_directory + "/" + splitPath[0]



        if "houdini" in app_name:
            self.run_houdini(app_launch_path, app_cmd_args, project_path, full_context_path)
        elif "maya" in app_name:
            self.run_maya(app_launch_path, app_cmd_args, project_path, full_context_path)

        print "### App.launch feedback ###"
        print "Projects directory: ", projects_directory
        print "Project path", project_path
        print "NAME", app_name
        print "CONTEXT: ", full_context_path
        print "Launch Path: ", app_launch_path


    def run_houdini(self, app_launch_path=None, app_cmd_args=None, project_path=None, full_context_path=None):

        # Test block
        # app_launch_path = "C:/Program Files/Side Effects Software/Houdini 13.0.498/bin/houdini.exe"
        # app_cmd_args = ""
        # project_path = "F:/AAU/ANM_699_03_Particles/snow_ball"
        # full_context_path = "F:/AAU/ANM_699_03_Particles/snow_ball"

        def envjoin(*args):
            concPath = os.path.pathsep.join(args)
            return concPath

        cwd = os.getcwd().replace("\\","/")
        houdini_install_path = "/".join(app_launch_path.split("/")[:-2])
        houdini_pref_dir = cwd + "/user_prefs"
        qlib_otl = cwd + "/lib_vendor/qLib/otls"
        qlib_base = qlib_otl + "/base"
        qlib_exp = qlib_otl + "/experimental"

        # Houdini instaled build such as "C:/Program Files/Side Effects Software/Houdini 13.0.498"
        os.environ["HFS"] = houdini_install_path
        # Houdini standart libraries (shaders etc.)
        # Arnold also looking for this variable
        os.environ["HH"] = envjoin(houdini_install_path, "houdini")
        # SYSTEM PATH
        os.environ["PATH"] = envjoin(houdini_install_path + "/bin", os.environ["PATH"])
        # HOUDINI PATH
        os.environ["HOUDINI_PATH"] = "&"
        # Global otls directories
        os.environ["HOUDINI_OTLSCAN_PATH"] = envjoin(qlib_base, qlib_exp, "@/otls")
        # User preferences folder
        os.environ["HOME"] = houdini_pref_dir
        # Scripts folder
        os.environ["PYTHONPATH"] = os.path.join(cwd, "@/scripts")
        # Set bufeffere_save on for faster save over network
        os.environ["HOUDINI_BUFFEREDSAVE"] = "1"

        # Force to use houdini version of Python
        os.environ["HOUDINI_USE_HFS_PYTHON"] = "1"
        
        # Houdini external help browser
        os.environ["HOUDINI_EXTERNAL_HELP_BROWSER"] = "start chrome"

        # Write data to yaml file that houdini can read it after launch trough 123.py script
        data = {"JOB" : project_path,
                "WORK" : full_context_path}
        with open('config/hou_session.yml', 'w') as yaml_file:
            yaml_file.write( yaml.dump(data, default_flow_style=False))

        launch_cmd = "%s %s" % (app_launch_path, app_cmd_args)
        subprocess.Popen(launch_cmd)

    def run_maya(self, app_launch_path=None, app_cmd_args=None, project_path=None, full_context_path=None):
        cwd = os.getcwd().replace("\\","/")

        maya_pref_dir = cwd + "/" + "user_prefs/maya"
        # User preferences folder
        os.environ["MAYA_APP_DIR"] = maya_pref_dir
        # Maya project directory
        os.environ["MAYA_PROJECT"] = full_context_path
        # Scripts folder
        os.environ["MAYA_PYTHONPATH"] = cwd

        launch_cmd = "%s %s" % (app_launch_path, app_cmd_args)
        subprocess.Popen(launch_cmd)

# Test block
# app = App()
# app.run_houdini()