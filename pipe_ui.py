from PySide.QtCore import *
from PySide.QtGui import *
import sys
import os
import shutil
import app

class PipeUI(QWidget):
    '''
    This class contains the UI elements and the functions
    directly associated with the UI
    '''

    def __init__(self):
        '''
        Initialize the UI elements, set their defaults and connect them.
        '''
        QWidget.__init__(self)

        # Initialize the layouts
        self.qvBoxLayout = QVBoxLayout()
        self.topQhBoxLayout = QHBoxLayout()
        self.qhBoxLayout = QHBoxLayout()

        # Configure file system abstract model
        minimize_to_tray_button = QPushButton()
        create_project_button = QPushButton()
        create_project_button.setIcon(QIcon("./icon/new_project.png"))
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir().currentPath())
        self.model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)

        # Configure autocompletion for project text line
        completer = QCompleter(self)
        completer.setModel(self.model)
        completer.setCompletionMode(completer.InlineCompletion)

        # Configure tree view widget
        self.treeView = QTreeView()
        self.treeView.setModel(self.model)

        # Create a menu for QTree
        qtree_menu = QMenu()
        qtree_menu.addAction("Delete")
        #### ????????#####

        # Other ui elements
        self.projectEditLineLabel = QLabel("Projects Folder:")
        self.projectsDirLine = QLineEdit()
        self.contextLabel = QLabel("Context:")

        # Default project directory
        self.projectsDirLine.setText(app.App().project_dictionary["default_projects_directory"])

        # Assign completer to project edit text line
        self.projectsDirLine.setCompleter(completer)

        # Set directory to display
        self.treeView.setRootIndex(self.model.index(self.projectsDirLine.text()))

        # Configure tree view look
        self.treeView.resizeColumnToContents(0)
        self.treeView.header().hide()
        self.treeView.hideColumn(1)
        self.treeView.hideColumn(2)
        self.treeView.hideColumn(3)

        # Add widgets to layout
        self.qvBoxLayout.addWidget(self.projectEditLineLabel)
        self.topQhBoxLayout.addWidget(self.projectsDirLine)
        self.topQhBoxLayout.addWidget(create_project_button)

        # Set layout of main window
        self.setStyleSheet("QWidget {color: rgb(240,240,240); background-color: rgb(24,24,24)}"
                            "QLabel {color: rgb(240,240,240); background-color: rgb(24,24,24)}"
                            "QPushButton {background-color: rgb(24,24,24)}"
                            "QLineEdit {color: rgb(240,240,240); background-color: rgb(24,24,24)}"
                            "QTreeView {color: rgb(240,240,240); background-color: rgb(24,24,24)}")

        self.create_app_launch_buttons()
        self.qvBoxLayout.addLayout(self.topQhBoxLayout)

        self.qvBoxLayout.addWidget(self.contextLabel)
        self.qvBoxLayout.addWidget(self.treeView)

        self.qvBoxLayout.addLayout(self.qhBoxLayout)



        self.setLayout(self.qvBoxLayout)
        self.qvBoxLayout.addWidget(minimize_to_tray_button)
        self.setWindowTitle("Pipe")
        self.resize(300, 800)
        self.setFocus()

        # Events
        self.projectsDirLine.textChanged.connect(self.update_model_path)
        minimize_to_tray_button.clicked.connect(self.minimize_to_tray)
        create_project_button.clicked.connect(self.create_project)

    def create_project(self):
        projects_directory = self.projectsDirLine.text()
        cwd = os.getcwd().replace("\\", "/")
        schema_project = cwd + "/config/schema"
        project_name_dialog = QInputDialog.getText(self, "Project Name", "Enter new project name", QLineEdit.Normal)
        name, state = project_name_dialog
        if state:
            new_project = shutil.copytree(schema_project, projects_directory + "/" + name)

    def restore_app(self):
        ''' Show the Application if Minimized '''
        self.show()

    def testAction(self):
        ''' Testing A new menu action'''
        print 'Testing Actions'

    def close_app(self):
        ''' Close the Application '''
        self.close()

    @Slot(QSystemTrayIcon.ActivationReason)
    def tray_double_click(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            if self.isHidden():
                self.show()

            else:
                self.hide()

    def create_tray_icon(self):
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction('Restore', self.restore_app)
        self.tray_icon_menu.addSeparator()
        self.tray_icon_menu.addAction('TestAction', self.testAction)
        self.tray_icon_menu.addAction('TestAction2', self.testAction)
        self.tray_icon_menu.addSeparator()
        self.tray_icon_menu.addAction('Close', self.close_app)

        self.tray_icon = QSystemTrayIcon(QIcon("./icon/hidrant.png"))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()
        self.tray_icon.showMessage ('Running', 'Running in the background.')
        self.tray_icon.activated.connect(self.tray_double_click)

    def minimize_to_tray(self):
        self.hide()
        self.create_tray_icon()


    def create_app_launch_buttons(self):
        run_houdini_button = QPushButton()
        run_maya_button = QPushButton()

        # Configure icons for launch buttons
        icon_size = QSize(40, 40)
        # Houdini
        houdini_icon = QIcon("icon/houdini.png")
        run_houdini_button.setIcon(houdini_icon)
        run_houdini_button.setIconSize(icon_size)
        # Maya
        maya_icon = QIcon("icon/maya.png")
        run_maya_button.setIcon(maya_icon)
        run_maya_button.setIconSize(icon_size)

        ##########################

        # Construct the list of maya version defined in app_launch.yml
        maya_versions_list = []
        for key in app.App().app_launch_dictionary.keys():
            if "maya" in key:
                maya_versions_list.append(key)

        # If only one version of maya specified in app_launch.yml do not create the menu
        if len(maya_versions_list) > 1:
            # Create button menu instance
            button_menu = QMenu(self)
            button_menu.setStyleSheet("QMenu {margin: 2px; position: absolute;}")

            # Fill menu with actions
            # Because we have to pass an object as a signal we can't pass costume variables
            # We need to wrap our object to another function by using lambda
            for maya_version in maya_versions_list:
                maya_version_action = button_menu.addAction(maya_version)
                maya_version_action.triggered.connect(
                    lambda maya_version=maya_version: self.run_maya_event(maya_version))
            # Assign the menu to the button
            run_maya_button.setMenu(button_menu)
        else:
            self.runMayaButton.clicked.connect(
                lambda: self.run_maya_event(maya_versions_list[0]))

        ##############################

        houdini_versions_list = []
        for key in app.App().app_launch_dictionary.keys():
            if "houdini" in key:
                houdini_versions_list.append(key)

        # If only one version of houdini specified in app_launch.yml do not create the menu
        if len(houdini_versions_list) > 1:
             # Create button menu instance
            button_menu = QMenu(self)
            # Fill menu with actions
            # Because we have to pass an object as a signal we can't pass costume variables
            # We need to wrap our object to another function by using lambda
            for houdini_version in houdini_versions_list:
                houdini_version_action = button_menu.addAction(houdini_version)
                houdini_version_action.triggered.connect(
                    lambda houdini_version=houdini_version: self.run_houdini_event(houdini_version))
            # Assign the menu to the button
            run_houdini_button.setMenu(button_menu)
        else:
            run_houdini_button.clicked.connect(
                lambda: self.run_houdini_event(houdini_versions_list[0]))

        # Assign buttons to layout
        self.qhBoxLayout.addWidget(run_houdini_button)
        self.qhBoxLayout.addWidget(run_maya_button)

    def update_model_path(self):
        self.model.reset()
        # Set directory to display
        self.treeView.setRootIndex(self.model.index(self.projectsDirLine.text()))

    def get_item_path(self):
        selected_item_index = self.treeView.selectedIndexes()
        if len(selected_item_index) > 0:
            item_path = self.model.filePath(selected_item_index[0])
            return item_path
        else:
            QMessageBox.information(self, "Info", "Select your context first")
            raise Exception("Missing context")

        # return selected_item_index and self.model.filePath(selected_item_index[0]) or -1

    def run_houdini_event(self, app_name):
        full_context_path = self.get_item_path()
        projects_directory = self.projectsDirLine.text()
        app.App().launch(app_name, projects_directory, full_context_path)

    def run_maya_event(self, app_name):
        full_context_path = self.get_item_path()
        projects_directory = self.projectsDirLine.text()
        app.App().launch(app_name, projects_directory, full_context_path)

application = QApplication(sys.argv)
dialog = PipeUI()
dialog.show()
application.exec_()

# Edit test comment