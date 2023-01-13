from PyQt5.QtCore import QRect

from owlready2 import *
import os

from PyQt5 import QtWidgets, QtGui

import Constant
import sys
from PyQt5.QtWidgets import QApplication, QListWidget, QMessageBox, QWidget, QComboBox, QAbstractItemView, QLabel, \
    QMainWindow, QTableWidgetItem, QPushButton, QVBoxLayout, QDialog, QHBoxLayout, QDialogButtonBox, QAction, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie, QFont

from Objects.Action import Action_Component
from Objects.Assumptions import Assumptions
from Objects.Component import Component
from Objects.Loss_Scenario_Req import Loss_Scenario_Req
from Objects.Project import Project
from Objects.Var_Values_Aux import Var_Values_Aux
from Objects.Variable_Values import Variable_Values
from Objects.Variables import Variables
from Tools.PdfTools import Generate_PDF
from ui_mainwindow import Ui_MainWindow

from datetime import datetime

# define the object to access the ontology
from Database import DB
from Database.safety import DB_Loss_Scenario_Req, DB_Hazards, DB_Components_Links, DB_Components, DB_Losses, \
    DB_Safety_Constraints, DB_Variables, DB_Variables_Values, DB_Projects, DB_Goals, DB_Actions_Components, \
    DB_Assumptions, DB_UCA, DB_Project_Files
from Objects.Goal import Goal
from Objects.Hazard import Hazard, Hazard_Loss
from Objects.Loss import Loss
from Objects.Safety_Constraint import Safety_Constraint, Safety_Constraint_Hazard
from Tools import Dictionary, General_tools, Safety_tools_new

from shutil import copyfile

Dictionary.init_default_elements_dictionary()
# Dictionary.init_elements_dictionary()
Dictionary.init_safety_elements_dictionary()

# Compile the interface:
# pip install pyuic5-tool
# pyuic5 -x mainwindow.ui -o ui_mainwindow.py

# Generate installer
# pip install pyinstaller
# pyinstaller app.py
# pyinstaller --paths .\venv\Lib\site-packages\ app.py
# pyinstaller --onefile --paths .\venv\Lib\site-packages\ app.py

# MAIN VARS
# owlready2.JAVA_EXE = Constant.JAVA_PATH
onto = owlready2.get_ontology(Constant.BIN_PATH).load(reload=True)

id_project = -1

# FIRST STEP VARS
list_projects = []
list_goals = []
list_assumptions = []
list_losses = []
list_hazards = []
list_constraints = []

# SECOND STEP VARS
list_component_controller = []
list_component_controller_variables = []
list_component_controller_variables_values = []
list_component_exti = []
list_component_actuator = []
list_component_sensor = []
list_component_exts = []
list_component_controlled_process = []
list_component_controlled_process_variables = []
list_component_controlled_process_variables_values = []
list_controlled_process_envd = []
list_controlled_process_input = []
list_controlled_process_output = []
list_controlled_process_env_dist = []
list_controlled_process_envd_variables = []
list_controlled_process_input_variables = []
list_controlled_process_envd_variables_values = []
list_controlled_process_input_variables_values = []
list_controlled_process_output_variables = []
list_controlled_process_output_variables_values = []
list_control_actions = []
list_links_controller = []
list_links_exts = []
list_links_actuator = []
list_links_sensor = []
list_links_controlled_process = []
list_connection_controller = []
list_connection_exts = []
list_connection_actuator = []
list_connection_sensor = []
list_connection_controlled_process = []
list_links_variable_controller = []
list_links_actions_controller = []
list_controller_hlcs = []
list_controller_hlcs_links = []

# THIRD STEP VARS
list_three_controller = []
list_three_control_action = []
list_third_var_comp = []
list_third_uca = []
list_third_uca_cell = []
list_third_uca_safe = []
list_third_context = []
list_third_uca_type = []
list_third_uca_type_description = []
list_third_hazard = []
listwidget_third_hazard = None
list_third_uca_warning = []
third_uca_description = ""

# FOURTH STEP VARS
list_four_controller = []
list_four_control_action = []
list_four_uca = []
list_four_loss_causal = []
list_four_requirements = []



qss_black = """
                QGroupBox {
                    border: 2px solid black;
                    border-radius: 5px;
                    margin-top: 0.5em;
                    color : black;
                    font-size: 11pt;
                }

                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 3px 0 3px;
                }
                """
# font-size: 15px;
qss_red = """
                QGroupBox {
                    border: 2px solid red;
                    border-radius: 5px;
                    margin-top: 0.5em;
                    color : red;
                    font-size: 11pt;
                }

                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 3px 0 3px;
                }
                """
need_update_stride_link = False
need_update_stride_dfd = False


def clear_var_step_one():
    # FIRST STEP VARS
    global list_projects, list_goals, list_assumptions, list_losses, list_hazards, list_constraints

    list_projects = []
    list_goals = []
    list_assumptions = []
    list_losses = []
    list_hazards = []
    list_constraints = []

def clear_var_step_two():
    # SECOND STEP VARS
    global list_component_controller, list_component_controller_variables, list_component_controller_variables_values, list_component_exti, \
        list_component_actuator, list_component_sensor, list_component_exts, list_component_controlled_process, list_component_controlled_process_variables, \
        list_component_controlled_process_variables_values, list_controlled_process_envd, list_controlled_process_input, list_controlled_process_output, \
        list_controlled_process_env_dist, list_controlled_process_envd_variables, list_controlled_process_input_variables, list_controlled_process_envd_variables_values, \
        list_controlled_process_input_variables_values, list_controlled_process_output_variables, list_controlled_process_output_variables_values, list_control_actions, \
        list_links_controller, list_links_exts, list_links_actuator, list_links_sensor, list_links_controlled_process, list_connection_controller, list_connection_exts, \
        list_connection_actuator, list_connection_sensor, list_connection_controlled_process, list_links_variable_controller, list_links_actions_controller, \
        list_controller_hlcs, list_controller_hlcs_links

    list_component_controller = []
    list_component_controller_variables = []
    list_component_controller_variables_values = []
    list_component_exti = []
    list_component_actuator = []
    list_component_sensor = []
    list_component_exts = []
    list_component_controlled_process = []
    list_component_controlled_process_variables = []
    list_component_controlled_process_variables_values = []
    list_controlled_process_envd = []
    list_controlled_process_input = []
    list_controlled_process_output = []
    list_controlled_process_env_dist = []
    list_controlled_process_envd_variables = []
    list_controlled_process_input_variables = []
    list_controlled_process_envd_variables_values = []
    list_controlled_process_input_variables_values = []
    list_controlled_process_output_variables = []
    list_controlled_process_output_variables_values = []
    list_control_actions = []
    list_links_controller = []
    list_links_exts = []
    list_links_actuator = []
    list_links_sensor = []
    list_links_controlled_process = []
    list_connection_controller = []
    list_connection_exts = []
    list_connection_actuator = []
    list_connection_sensor = []
    list_connection_controlled_process = []
    list_links_variable_controller = []
    list_links_actions_controller = []
    list_controller_hlcs = []
    list_controller_hlcs_links = []

def clear_var_step_three():
    # THIRD STEP VARS
    global list_three_controller, list_three_control_action, list_third_var_comp, list_third_uca, list_third_uca_cell, list_third_uca_safe, list_third_context,\
            list_third_uca_type, list_third_uca_type_description, list_third_hazard, listwidget_third_hazard, list_third_uca_warning

    list_three_controller = []
    list_three_control_action = []
    list_third_var_comp = []
    list_third_uca = []
    list_third_uca_cell = []
    list_third_uca_safe = []
    list_third_context = []
    list_third_uca_type = []
    list_third_uca_type_description = []
    list_third_hazard = []
    listwidget_third_hazard = None
    list_third_uca_warning = []

def clear_var_step_four():
    # FOURTH STEP VARS
    global list_four_controller, list_four_control_action, list_four_uca, list_four_loss_causal, list_four_requirements

    list_four_controller = []
    list_four_control_action = []
    list_four_uca = []
    list_four_loss_causal = []
    list_four_requirements = []

class LoadingScreen(QWidget):
    def __init__(self):
        super(LoadingScreen, self).__init__()
        self.setFixedSize(400, 400)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)

        self.label_animation = QLabel(self)
        self.movie = QMovie(Constant.GIF_LOADING_PATH)
        self.label_animation.setMovie(self.movie)

        self.startAnimation()
        # timer = QTimer(self)
        # timer.singleShot(3000, self.stopAnimation)
        self.show()

    def startAnimation(self):
        self.movie.start()

    def stopAnimation(self):
        self.movie.stop()
        self.close()

class OpDialog(QDialog):
    "A Dialog to set input and output ranges for an optimization."

    def __init__(self, *args, **kwargs):
        "Create a new dialogue instance."
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Create new UCA by the cell")
        self.gui_init()

    def gui_init(self):
        global list_third_hazard

        row_1 = QVBoxLayout()
        row_1.addWidget(QLabel("Select at least one hazard:"))
        row_1.addStretch()
        self.listWidget = QListWidget()

        for haz in list_third_hazard:
            self.listWidget.addItem("H-" + str(haz.id_hazard) + ": " + haz.description)

        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        row_1.addWidget(self.listWidget)
        self.resize(1050, 250)

        row_2 = QHBoxLayout()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        row_2.addWidget(self.buttonBox)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonBox)
        layout = QVBoxLayout()
        layout.addLayout(row_1)
        layout.addLayout(row_2)
        self.setLayout(layout)

class ProjectDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Adding new project")
        self.gui_init()

    def gui_init(self):
        global list_third_hazard

        row_1 = QVBoxLayout()
        row_1.addWidget(QLabel("Fill all the fields to create a new project"))
        row_1.addStretch()

        # Add label
        self.ln = QLabel(self)
        self.ln.move(30, 62)
        self.ln.setText("Name of project")
        self.ln.resize(400, 22)

        # Add lineedit
        self.name = QtWidgets.QLineEdit(self)
        self.name.resize(400, 22)

        # Add label
        self.ld = QLabel(self)
        self.ld.move(30, 62)
        self.ld.setText("Description of project")
        self.ld.resize(400, 22)

        # Add lineedit
        self.description = QtWidgets.QLineEdit(self)
        self.description.resize(400, 22)

        row_1.addWidget(self.ln)
        row_1.addWidget(self.name)
        row_1.addWidget(self.ld)
        row_1.addWidget(self.description)

        row_2 = QHBoxLayout()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        row_2.addWidget(self.buttonBox)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonBox)
        layout = QVBoxLayout()
        layout.addLayout(row_1)
        layout.addLayout(row_2)
        self.setLayout(layout)

        self.resize(800, 150)

class CausalFactorDialog(QDialog):

    d_cause = ""
    d_recommendation = ""
    d_mechanism = ""
    d_source = ""
    d_destiny = ""
    d_comp_cause = ""
    d_show_pef_req = False
    d_pef_req = ""

    def __init__(self, cause, recommendation, mechanism, source, destiny, comp_cause, show_pef_requirement, pef_requirement):
        super().__init__()
        self.setWindowTitle("Adding new recommendation")
        self.d_cause = cause
        self.d_recommendation = recommendation
        self.d_mechanism = mechanism
        self.d_source = source
        self.d_destiny = destiny
        self.d_comp_cause = comp_cause
        self.d_show_pef_req = show_pef_requirement
        self.d_pef_req = pef_requirement
        self.gui_init()

    def gui_init(self):
        global list_third_hazard
        default_font = QFont('Arial', 11)

        instructions = "Fill all the fields to create a new recommendation\n"

        if self.d_source != "" or self.d_destiny != "": #or self.d_comp_cause != "":
            if self.d_source == self.d_destiny:
                instructions += "\nElement: " + self.d_source + "\n" #+ "\nCause: " + self.d_comp_cause
            else:
                instructions += "\nInteraction: " + self.d_source + " -> " + self.d_destiny + "\n" #+ "\nCause: " + self.d_comp_cause

        row_1 = QVBoxLayout()
        row_1.addStretch()

        # Add label
        self.li = QLabel(self)
        self.li.move(30, 62)
        self.li.setFont(default_font)
        self.li.setText(instructions)
        self.li.resize(400, 22)

        # Add label
        self.ln = QLabel(self)
        self.ln.move(30, 62)
        self.ln.setFont(default_font)
        self.ln.setText("Cause")
        self.ln.resize(400, 22)

        # Add lineedit
        self.cause = QtWidgets.QTextEdit(self)
        self.cause.setWordWrapMode(True)
        self.cause.setFont(default_font)
        self.cause.setText(self.d_cause)
        self.cause.resize(400, 22)

        # Add label
        self.ld = QLabel(self)
        self.ld.move(30, 62)
        self.ld.setFont(default_font)
        self.ld.setText("Recommendation (use the following structure):")
        self.ld.resize(400, 22)

        # self.lne = QLabel(self)
        # self.lne.move(30, 62)
        # self.lne.setFont(default_font)
        # self.lne.setText("ELEMENT + MODAL VERB + RECOMMENDATION + SUBORDINATING CONJUNCTION + CONDITION \n")
        # self.lne.setAlignment(Qt.AlignCenter)
        # self.lne.resize(400, 22)
        #
        # self.lnr = QLabel(self)
        # self.lnr.move(30, 62)
        # self.lnr.setFont(default_font)
        # self.lnr.setText("ELEMENT: controller / control action / actuator / ...\n"
        #                  "MODAL VERBS: must / shall \n"
        #                  "RECOMMENDATION: have / be + something to do or be\n"
        #                  "SUBORDINATING CONJUNCTION: when / before / after / while\n"
        #                  "CONDITION: or restriction\n")
        # self.lnr.resize(400, 22)

        # Add lineedit
        self.requirement = QtWidgets.QTextEdit(self)
        self.requirement.setWordWrapMode(True)
        self.requirement.setFont(default_font)
        self.requirement.setText(self.d_recommendation)
        self.requirement.resize(400, 22)

        self.lnm = QLabel(self)
        self.lnm.move(30, 62)
        self.lnm.setFont(default_font)
        self.lnm.setText("Mechanism")
        self.lnm.resize(400, 22)

        # Add lineedit
        self.mechanism = QtWidgets.QTextEdit(self)
        self.mechanism.setWordWrapMode(True)
        self.mechanism.setFont(default_font)
        self.mechanism.setText(self.d_mechanism)
        self.mechanism.resize(400, 22)

        row_1.addWidget(self.li)
        row_1.addWidget(self.ln)
        row_1.addWidget(self.cause)
        row_1.addWidget(self.ld)
        row_1.addWidget(self.requirement)
        row_1.addWidget(self.lnm)
        row_1.addWidget(self.mechanism)

        if self.d_show_pef_req:
            self.lpr = QLabel(self)
            self.lpr.move(30, 62)
            self.lpr.setFont(default_font)
            self.lpr.setText("Safety Performance Requirement")
            self.lpr.resize(400, 22)

            # Add lineedit
            self.pef_req = QtWidgets.QTextEdit(self)
            self.pef_req.setWordWrapMode(True)
            self.pef_req.setFont(default_font)
            self.pef_req.setText(self.d_pef_req)
            self.pef_req.resize(400, 22)

            row_1.addWidget(self.lpr)
            row_1.addWidget(self.pef_req)


        row_2 = QHBoxLayout()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        row_2.addWidget(self.buttonBox)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonBox)
        layout = QVBoxLayout()
        layout.addLayout(row_1)
        layout.addLayout(row_2)
        self.setLayout(layout)

        self.resize(800, 150)

class UcaDescriptionDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Change UCA description")
        self.gui_init()

    def gui_init(self):
        global third_uca_description
        row_1 = QVBoxLayout()
        row_1.addWidget(QLabel("Fill all the fields to create a new recommendation"))
        row_1.addStretch()

        # Add label
        self.ln = QLabel(self)
        self.ln.move(30, 62)
        self.ln.setText("Description")
        self.ln.resize(400, 22)

        # Add lineedit
        # self.description = QtWidgets.QLineEdit(self)
        self.description = QtWidgets.QTextEdit(self)
        self.description.setWordWrapMode(True)
        self.description.setText(third_uca_description)
        self.description.resize(400, 22)

        row_1.addWidget(self.ln)
        row_1.addWidget(self.description)

        row_2 = QHBoxLayout()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        row_2.addWidget(self.buttonBox)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonBox)
        layout = QVBoxLayout()
        layout.addLayout(row_1)
        layout.addLayout(row_2)
        self.setLayout(layout)

        self.resize(800, 150)

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class MainWindow:

    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        self.ui.label_version.setText("Version: " + Constant.VERSION)
        # self.ui.tabWidget.setTabEnabled(9, False)
        # self.ui.tabWidget.setTabVisible(9, False)
        # self.ui.tabWidget.setTabEnabled(10, False)
        # self.ui.tabWidget.setTabVisible(10, False)
        # self.ui.tabWidget.setTabEnabled(11, False)
        # self.ui.tabWidget.setTabVisible(11, False)

        self.helpContentOntology = QAction("Full STPA ontology")
        self.helpContentOntology.triggered.connect(self.load_image)

        self.stpaOne = QAction("STPA Step 1 - Purpose of the analysis")
        self.stpaOne.triggered.connect(self.load_image_step_one)
        self.stpaTwo = QAction("STPA Step 2 - Control structure")
        self.stpaTwo.triggered.connect(self.load_image_step_two)
        self.stpaThree = QAction("STPA Step 3 - Unsafe Control Actions")
        self.stpaThree.triggered.connect(self.load_image_step_three)
        self.stpaFour = QAction("STPA Step 4 - Loss scenarios")
        self.stpaFour.triggered.connect(self.load_image_step_four)
        self.ui.menu_ontology_stpa.addAction(self.stpaOne)
        self.ui.menu_ontology_stpa.addAction(self.stpaTwo)
        self.ui.menu_ontology_stpa.addAction(self.stpaThree)
        self.ui.menu_ontology_stpa.addAction(self.stpaFour)
        self.ui.menu_ontology_stpa.addSeparator()
        self.ui.menu_ontology_stpa.addAction(self.helpContentOntology)



        self.helpContentAbout = QAction("Information")
        self.helpContentAbout.triggered.connect(self.load_about)
        self.ui.menu_ontology_help.addAction(self.helpContentAbout)

        # self.load_projects()
        self.ui.combobox_projects.currentIndexChanged.connect(self.selection_change_project)
        self.ui.combobox_projects.wheelEvent = lambda event: None
        self.ui.button_add_projects.clicked.connect(self.on_button_add_project_clicked)
        self.ui.button_del_projects.clicked.connect(self.on_button_del_project_clicked)

        # ----- TAB Fisrt Step -----
        self.ui.list_saf_goals.clicked.connect(self.on_list_saf_goals_clicked)
        self.ui.button_saf_new_goal.clicked.connect(self.on_button_saf_new_goal_clicked)
        self.ui.button_saf_update_goal.clicked.connect(self.on_button_saf_update_goal_clicked)
        self.ui.button_saf_delete_goal.clicked.connect(self.on_button_saf_delete_goal_clicked)
        self.ui.button_saf_cancel_goal.clicked.connect(self.on_button_saf_cancel_goal_clicked)

        self.ui.list_saf_assumptions.clicked.connect(self.on_list_saf_assumptions_clicked)
        self.ui.button_saf_new_assumption.clicked.connect(self.on_button_saf_new_assumption_clicked)
        self.ui.button_saf_update_assumption.clicked.connect(self.on_button_saf_update_assumption_clicked)
        self.ui.button_saf_delete_assumption.clicked.connect(self.on_button_saf_delete_assumption_clicked)
        self.ui.button_saf_cancel_assumption.clicked.connect(self.on_button_saf_cancel_assumption_clicked)

        self.ui.list_saf_losses.clicked.connect(self.on_list_saf_losses_clicked)
        self.ui.button_saf_new_loss.clicked.connect(self.on_button_saf_new_loss_clicked)
        self.ui.button_saf_update_loss.clicked.connect(self.on_button_saf_update_loss_clicked)
        self.ui.button_saf_delete_loss.clicked.connect(self.on_button_saf_delete_loss_clicked)
        self.ui.button_saf_cancel_loss.clicked.connect(self.on_button_saf_cancel_loss_clicked)

        self.ui.list_saf_hazards.currentRowChanged.connect(self.on_list_saf_hazards_clicked)
        self.ui.button_saf_new_hazard.clicked.connect(self.on_button_saf_new_hazard_clicked)
        self.ui.button_saf_update_hazard.clicked.connect(self.on_button_saf_update_hazard_clicked)
        self.ui.button_saf_delete_hazard.clicked.connect(self.on_button_saf_delete_hazard_clicked)
        self.ui.button_saf_cancel_hazard.clicked.connect(self.on_button_saf_cancel_hazard_clicked)

        self.ui.list_saf_constraints.currentRowChanged.connect(self.on_list_saf_constraints_clicked)
        self.ui.button_saf_new_constraint.clicked.connect(self.on_button_saf_new_constraint_clicked)
        self.ui.button_saf_update_constraint.clicked.connect(self.on_button_saf_update_constraint_clicked)
        self.ui.button_saf_delete_constraint.clicked.connect(self.on_button_saf_delete_constraint_clicked)
        self.ui.button_saf_cancel_constraint.clicked.connect(self.on_button_saf_cancel_constraint_clicked)

        self.load_goals()
        self.load_assumptions()
        self.load_losses()
        self.load_hazards()
        self.load_constraints()
        # ----- TAB Fisrt Step -----

        # ----- TAB Second Step -----
        self.ui.button_add_controller.clicked.connect(self.on_button_add_controller_clicked)
        self.ui.button_update_controller.clicked.connect(self.on_button_update_controller_clicked)
        self.ui.button_delete_controller.clicked.connect(self.on_button_delete_controller_clicked)
        self.ui.button_cancel_controller.clicked.connect(self.on_button_cancel_controller_clicked)
        self.ui.listwidget_controllers.currentRowChanged.connect(self.on_listwidget_controllers_clicked)
        self.ui.button_add_controller_connection.clicked.connect(self.on_button_add_controller_connection_clicked)
        self.ui.listwidget_controller_connection.currentRowChanged.connect(self.on_listwidget_controller_connection_clicked)
        self.ui.button_delete_controller_connection.clicked.connect(self.on_button_delete_controller_connection_clicked)

        self.ui.button_add_exts.clicked.connect(self.on_button_add_exts_clicked)
        self.ui.button_update_exts.clicked.connect(self.on_button_update_exts_clicked)
        self.ui.button_delete_exts.clicked.connect(self.on_button_delete_exts_clicked)
        self.ui.button_cancel_exts.clicked.connect(self.on_button_cancel_exts_clicked)
        self.ui.listwidget_exts.currentRowChanged.connect(self.on_listwidget_exts_clicked)
        self.ui.button_add_exts_connection.clicked.connect(self.on_button_add_exts_connection_clicked)
        self.ui.listwidget_exts_connection.currentRowChanged.connect(self.on_listwidget_exts_connection_clicked)
        self.ui.button_delete_exts_connection.clicked.connect(self.on_button_delete_exts_connection_clicked)

        self.ui.button_add_actuator.clicked.connect(self.on_button_add_actuator_clicked)
        self.ui.button_update_actuator.clicked.connect(self.on_button_update_actuator_clicked)
        self.ui.button_delete_actuator.clicked.connect(self.on_button_delete_actuator_clicked)
        self.ui.button_cancel_actuator.clicked.connect(self.on_button_cancel_actuator_clicked)
        self.ui.listwidget_actuator.currentRowChanged.connect(self.on_listwidget_actuators_clicked)
        self.ui.button_add_actuator_connection.clicked.connect(self.on_button_add_actuator_connection_clicked)
        self.ui.listwidget_actuator_connection.currentRowChanged.connect(self.on_listwidget_actuator_connection_clicked)
        self.ui.button_delete_actuator_connection.clicked.connect(self.on_button_delete_actuator_connection_clicked)

        self.ui.button_add_sensor.clicked.connect(self.on_button_add_sensor_clicked)
        self.ui.button_update_sensor.clicked.connect(self.on_button_update_sensor_clicked)
        self.ui.button_delete_sensor.clicked.connect(self.on_button_delete_sensor_clicked)
        self.ui.button_cancel_sensor.clicked.connect(self.on_button_cancel_sensor_clicked)
        self.ui.listwidget_sensor.currentRowChanged.connect(self.on_listwidget_sensors_clicked)
        self.ui.button_add_sensor_connection.clicked.connect(self.on_button_add_sensor_connection_clicked)
        self.ui.listwidget_sensor_connection.currentRowChanged.connect(self.on_listwidget_sensor_connection_clicked)
        self.ui.button_delete_sensor_connection.clicked.connect(self.on_button_delete_sensor_connection_clicked)

        self.ui.button_save_controlled_process.clicked.connect(self.on_button_save_controlled_process_clicked)
        self.ui.button_edit_controlled_process.clicked.connect(self.on_button_edit_controlled_process_clicked)
        self.ui.button_delete_controlled_process.clicked.connect(self.on_button_delete_controlled_process_clicked)
        self.ui.button_cancel_controlled_process.clicked.connect(self.on_button_cancel_controlled_process_clicked)
        self.ui.button_add_controlled_process_connection.clicked.connect(self.on_button_add_controlled_process_connection_clicked)
        self.ui.listwidget_controlled_process_connection.currentRowChanged.connect(self.on_listwidget_controlled_process_connection_clicked)
        self.ui.button_delete_controlled_process_connection.clicked.connect(self.on_button_delete_controlled_process_connection_clicked)
        self.ui.listwidget_controlled_process_envd.currentRowChanged.connect(self.on_listwidget_controlled_process_envd_clicked)
        self.ui.button_add_controlled_process_envd.clicked.connect(self.on_button_add_controlled_process_envd_clicked)
        self.ui.button_update_controlled_process_envd.clicked.connect(self.on_button_update_controlled_process_envd_clicked)
        self.ui.button_delete_controlled_process_envd.clicked.connect(self.on_button_delete_controlled_process_envd_clicked)
        self.ui.button_cancel_controlled_process_envd.clicked.connect(self.on_button_cancel_controlled_process_envd_clicked)
        self.ui.listwidget_controlled_process_input.currentRowChanged.connect(self.on_listwidget_controlled_process_input_clicked)
        self.ui.button_add_controlled_process_input.clicked.connect(self.on_button_add_controlled_process_input_clicked)
        self.ui.button_update_controlled_process_input.clicked.connect(self.on_button_update_controlled_process_input_clicked)
        self.ui.button_delete_controlled_process_input.clicked.connect(self.on_button_delete_controlled_process_input_clicked)
        self.ui.button_cancel_controlled_process_input.clicked.connect(self.on_button_cancel_controlled_process_input_clicked)
        self.ui.listwidget_controlled_process_output.currentRowChanged.connect(self.on_listwidget_controlled_process_output_clicked)
        self.ui.button_add_controlled_process_output.clicked.connect(self.on_button_add_controlled_process_output_clicked)
        self.ui.button_update_controlled_process_output.clicked.connect(self.on_button_update_controlled_process_output_clicked)
        self.ui.button_delete_controlled_process_output.clicked.connect(self.on_button_delete_controlled_process_output_clicked)
        self.ui.button_cancel_controlled_process_output.clicked.connect(self.on_button_cancel_controlled_process_output_clicked)

        self.ui.combobox_second_controller.currentIndexChanged.connect(self.selection_change_controller_connection)
        self.ui.combobox_second_controller.wheelEvent = lambda event: None
        self.ui.button_add_control_action.clicked.connect(self.on_button_add_control_action_clicked)
        self.ui.button_update_control_action.clicked.connect(self.on_button_update_control_action_clicked)
        self.ui.button_delete_control_action.clicked.connect(self.on_button_delete_control_action_clicked)
        self.ui.button_cancel_control_action.clicked.connect(self.on_button_cancel_control_action_clicked)
        self.ui.listwidget_control_actions.currentRowChanged.connect(self.on_listwidget_control_action_clicked)
        self.ui.button_add_controller_variable.clicked.connect(self.on_button_add_controller_variable_clicked)
        self.ui.button_update_controller_variable.clicked.connect(self.on_button_update_controller_variable_clicked)
        self.ui.button_delete_controller_variable.clicked.connect(self.on_button_delete_controller_variable_clicked)
        self.ui.button_cancel_controller_variable.clicked.connect(self.on_button_cancel_controller_variable_clicked)
        self.ui.listwidget_controller_variable.currentRowChanged.connect(self.on_listwidget_controller_variable_clicked)
        self.ui.button_add_controller_variable_values.clicked.connect(self.on_button_add_controller_variable_values_clicked)
        self.ui.button_update_controller_variable_values.clicked.connect(self.on_button_update_controller_variable_values_clicked)
        self.ui.button_delete_controller_variable_values.clicked.connect(self.on_button_delete_controller_variable_values_clicked)
        self.ui.button_cancel_controller_variable_values.clicked.connect(self.on_button_cancel_controller_variable_values_clicked)
        self.ui.listwidget_controller_variable_values.currentRowChanged.connect(self.on_listwidget_controller_variable_values_clicked)

        self.ui.button_structure_check.clicked.connect(self.check_control_structure)
        # ----- TAB Second Step -----

        # ----- TAB Third Step -----
        self.ui.combobox_third_controller.currentIndexChanged.connect(self.selection_change_controller_third)
        self.ui.combobox_third_controller.wheelEvent = lambda event: None
        self.ui.combobox_third_control_action.currentIndexChanged.connect(self.selection_change_control_action_third)
        self.ui.combobox_third_control_action.wheelEvent = lambda event: None
        self.ui.button_third_save_uca.clicked.connect(self.on_button_button_third_save_uca_clicked)
        self.ui.button_third_delete_uca_rule.clicked.connect(self.on_button_button_third_delete_uca_rule_clicked)
        self.ui.button_third_delete_uca_cell.clicked.connect(self.on_button_button_third_delete_uca_cell_clicked)
        self.ui.button_third_delete_uca_safe.clicked.connect(self.on_button_button_third_delete_uca_safe_clicked)
        self.ui.tabWidget.currentChanged.connect(self.onChange)
        self.ui.tablewidget_third_context.cellClicked.connect(self.cell_was_clicked)
        self.ui.listwidget_third_uca_rule.currentRowChanged.connect(self.on_listwidget_uca_rule_clicked)
        self.ui.listwidget_third_uca_cell.currentRowChanged.connect(self.on_listwidget_uca_cell_clicked)
        self.ui.listwidget_third_uca_safe.currentRowChanged.connect(self.on_listwidget_uca_safe_clicked)
        self.ui.button_third_description_uca_rule.clicked.connect(self.on_button_third_update_description_uca_rule)
        self.ui.button_third_description_uca_cell.clicked.connect(self.on_button_third_update_description_uca_cell)
        self.ui.button_third_description_uca_safe.clicked.connect(self.on_button_third_update_description_uca_safe)
        # ----- TAB Third Step -----

        # ----- TAB Fourth Step -----
        self.ui.combobox_fourth_controller.currentIndexChanged.connect(self.selection_change_controller_fourth)
        self.ui.combobox_fourth_controller.wheelEvent = lambda event: None
        self.ui.combobox_fourth_control_action.currentIndexChanged.connect(self.selection_change_control_action_fourth)
        self.ui.combobox_fourth_control_action.wheelEvent = lambda event: None
        self.ui.listwidget_fourth_uca.currentRowChanged.connect(self.selection_change_uca_fourth)
        self.ui.listwidget_fourth_uca.wheelEvent = lambda event: None
        self.ui.listwidget_fourth_requirement.itemClicked.connect(self.selection_change_requirement_fourth)
        self.ui.listwidget_fourth_requirement.wheelEvent = lambda event: None
        self.ui.listwidget_fourth_causal_factor.currentRowChanged.connect(self.selection_change_causal_factor_fourth)
        self.ui.listwidget_fourth_causal_factor.wheelEvent = lambda event: None
        self.ui.button_fourth_add_causal_factor.clicked.connect(self.on_button_fourth_add_causal_factor_clicked)
        self.ui.button_fourth_create_causal_factor.clicked.connect(self.on_button_fourth_create_causal_factor_clicked)
        # ----- TAB Fourth Step -----

        # ----- TAB STPA Report -----
        self.ui.button_stpa_report_pdf.clicked.connect(self.on_button_fifith_stpa_report_clicked)
        # ----- TAB Sixth Step -----

        # ----- TAB Control Structure Image -----
        self.ui.button_open_file_one.clicked.connect(self.on_button_select_file_one_clicked)
        self.ui.button_open_file_two.clicked.connect(self.on_button_select_file_two_clicked)
        self.ui.button_open_file_three.clicked.connect(self.on_button_select_file_three_clicked)
        self.ui.button_delete_file_one.clicked.connect(self.on_button_delete_file_one_clicked)
        self.ui.button_delete_file_two.clicked.connect(self.on_button_delete_file_two_clicked)
        self.ui.button_delete_file_three.clicked.connect(self.on_button_delete_file_three_clicked)
        # ----- TAB Control Structure Image -----



        # ----- TAB Conflict Performance -----


        # print("---------------------")
        # a6 = General_tools.list_subclass_with_property(onto, "Pef_DoS_performance_recommendation", "pef_identify_dos_performance_recommendation")
        # print("---------------------")

        # self.load_start_advice()

    def get_component_by_ID(self, id_comp):
        if (id_comp == Constant.DB_ID_CONTROLLER):
            return  Constant.CONTROLLER
        elif (id_comp == Constant.DB_ID_ACTUATOR):
            return Constant.ACTUATOR
        elif (id_comp == Constant.DB_ID_CP):
            return Constant.CONTROLLED_PROCESS
        elif (id_comp == Constant.DB_ID_SENSOR):
            return Constant.SENSOR
        elif (id_comp == Constant.DB_ID_INPUT):
            return Constant.INPUT
        elif (id_comp == Constant.DB_ID_OUTPUT):
            return Constant.OUTPUT
        elif (id_comp == Constant.DB_ID_EXT_INFORMATION):
            return Constant.EXTERNAL_INFORMATION
        elif (id_comp == Constant.DB_ID_ALGORITHM):
            return Constant.ALGORITHM
        elif (id_comp == Constant.DB_ID_PROCESS_MODEL):
            return Constant.PROCESS_MODEL
        elif (id_comp == Constant.DB_ID_ENV_DISTURBANCES):
            return Constant.ENVIRONMENTAL_DISTURBANCES
        elif (id_comp == Constant.DB_ID_HLC):
            return Constant.HIGH_LEVEL_CONTROLLER
        return ""

    def show(self):
        self.main_win.show()

    def load_tabwidget(self, tab_index):
        if tab_index == 0:
            self.load_goals()
            self.load_assumptions()
            self.load_losses()
            self.load_hazards()
            self.load_constraints()
        if tab_index == 1:
            self.disable_controller_connections()
            self.disable_exts_connections()
            self.disable_actuator_connections()
            self.disable_sensor_connections()
            self.disable_controlled_process_connections()
            self.disable_controller_actions_variables()

            self.load_component_controller()
            self.load_component_exts()
            self.load_component_actuator()
            self.load_component_sensor()
            self.load_component_controlled_proccess()

            self.check_control_structure()
        if tab_index == 2:
            clear_var_step_three()
            self.load_combobox_third_controller()
            self.load_variables_dynamically()
            self.load_uca_third()
        elif tab_index == 3:
            clear_var_step_four()
            self.load_combobox_fourth_controller()
        elif tab_index == 4:
            self.load_control_structure_image()
        elif tab_index == 5:
            self.load_stpa_report()
        elif tab_index == 6:
            self.load_dfd_initialize()
            self.load_dfd_link_initialize()
            self.load_dfd_links()
        elif tab_index == 7:
            self.load_controller_stride()
        elif tab_index == 8:
            self.load_stride_report()
        elif tab_index == 9:
            self.load_controller_business()
        elif tab_index == 10:
            self.load_controller_saf_pef_controller()
            self.load_controller_saf_pef_uca()
            self.load_saf_pef_requirements()
            self.load_saf_pef_resource()
        elif tab_index == 11:
            self.load_controller_sec_pef_controller()
            self.load_controller_sec_pef_priority()
            self.load_sec_pef_requirements()
            self.load_sec_pef_resource()
        elif tab_index == 12:
            self.load_controller_business_pef()
            self.load_bus_pef_resource()
        elif tab_index == 13:
            self.load_controller_conflict_pef()
            self.load_resource_conflict_pef()
            self.load_conflict_requirement()

    def onChange(self, i):  # changed!
        tab_index = i
        self.load_tabwidget(tab_index)

    def load_projects(self):
        global list_projects, id_project

        list_projects = DB_Projects.select_all_projects()
        pos_selected = self.ui.combobox_projects.currentIndex()

        self.ui.combobox_projects.clear()

        if id_project < 0:
            is_first = True
        else:
            is_first = False

        for pos in range(len(list_projects)):
            self.ui.combobox_projects.addItem(list_projects[pos].name)
            if is_first:
                is_first = False
                id_project = list_projects[pos].id

        if len(list_projects) == 0:
            self.ui.tabWidget.setEnabled(False)
            return

        if self.ui.tabWidget.isEnabled() == False:
            self.ui.tabWidget.setEnabled(True)

        if pos_selected > 0 and pos_selected < len(list_projects):
            self.ui.combobox_projects.setCurrentIndex(pos_selected)
        else:
            self.ui.combobox_projects.setCurrentIndex(0)

    def selection_change_project(self):
        global id_project, list_projects

        pos = self.ui.combobox_projects.currentIndex()
        tab_index = self.ui.tabWidget.currentIndex()

        if len(list_projects) == 0:
            self.ui.tabWidget.setEnabled(False)
            return

        if pos >= len(list_projects):
            pos = 0

        id_project = list_projects[pos].id
        self.load_tabwidget(tab_index)

    def active_tab(self):
        self.ui.groupbox_project.setEnabled(True)
        self.ui.combobox_projects.setEnabled(True)
        self.ui.button_add_projects.setEnabled(True)
        self.ui.button_del_projects.setEnabled(True)
        # self.ui.tabWidget.setEnabled(True)

    def load_image(self):

        # img = Image.open(Constant.IMAGE_PATH)
        # img.show()
        try:
            os.startfile(Constant.IMAGE_STPA_FULL_PATH)
        except Exception as e:
            print(e)

    def load_image_step_one(self):
        try:
            os.startfile(Constant.IMAGE_STPA_ONE_PATH)
        except Exception as e:
            print(e)

    def load_image_step_two(self):
        try:
            os.startfile(Constant.IMAGE_STPA_TWO_PATH)
        except Exception as e:
            print(e)

    def load_image_step_three(self):
        try:
            os.startfile(Constant.IMAGE_STPA_THREE_PATH)
        except Exception as e:
            print(e)

    def load_image_step_four(self):
        try:
            os.startfile(Constant.IMAGE_STPA_FOUR_PATH)
        except Exception as e:
            print(e)

    def load_image_stride_dfd_map(self):
        try:
            os.startfile(Constant.IMAGE_STRIDE_DFD_MAP_PATH)
        except Exception as e:
            print(e)

    def load_image_stride_security(self):
        try:
            os.startfile(Constant.IMAGE_STRIDE_SECURITY_PATH)
        except Exception as e:
            print(e)

    def load_image_stride(self):
        try:
            os.startfile(Constant.IMAGE_STRIDE_FULL_PATH)
        except Exception as e:
            print(e)

    def load_start_advice(self):
        title = "Attention"

        msg = "This is a doctoral work by Andrei Carniel, under the supervision of Prof. Celso Hirata, at Instituto Tecnológico de Aeronáutica - ITA." \
              "\n\nThe software is under GPL license on GitHub (github.com/andrei-carniel/AppSTPA)." \
              "\n\nFor more information, please send an e-mail to andrei.carniel@gmail.com and hirata@ita.br." \
              "\n\n\nSoftware version " + Constant.VERSION

        showdialog(title, msg)

    def load_about(self):
        title = "Attention"

        msg = "This is a doctoral work by Andrei Carniel, under the supervision of Prof. Celso Hirata, at Instituto Tecnológico de Aeronáutica - ITA." \
              "\n\nThe software is under GPL license on GitHub (github.com/andrei-carniel/AppSTPA)." \
              "\n\nFor more information, please send an e-mail to andrei.carniel@gmail.com and hirata@ita.br." \
              "\n\nSupport material: STPA Handbook, by the authors: Nancy G. Leveson and John P. Thomas." \
              "\n\n\nSoftware version " + Constant.VERSION

        showdialog(title, msg)

    def on_button_add_project_clicked(self):
        pd = ProjectDialog()
        result = pd.exec_()

        if result == 1:
            name = pd.name.text()
            description = pd.description.text()

            if len(name) == 0 or len(description) == 0:
                showdialog("Error to create a new project", "You must fill all the fields to create a new project.")
                return

            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            project = Project(0, name, description, current_date, "")
            id_proj = DB_Projects.insert_to_projects(project)

            if id_proj > 0:
                showdialog("Success", "New project created.")
                if self.ui.tabWidget.isEnabled() == False:
                    self.ui.tabWidget.setEnabled(True)

                self.load_projects()
                return

            showdialog("Error", "It is not possible to create a new project at this time, please try again.")

    def on_button_del_project_clicked(self):
        global list_projects
        pos = self.ui.combobox_projects.currentIndex()

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete the project " + list_projects[pos].name + "?\nThis operation cannot be undone")
        msgBox.setWindowTitle("Delete project?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Projects.delete(list_projects[pos].id)
            self.load_projects()

    # ----- Functions DFD Elements -----

    # ----- Functions STPA report Step -----
    def on_button_fifith_stpa_report_clicked(self):
        global stpa_pdf_report_list

        try:
            result = Generate_PDF(id_project)
            if result == "Error":
                showdialog("Error to create PDF", "If the file is open, close and try again...")
            else:
                showdialog("New Report", result)
        except Exception as e:
            showdialog("Error to create PDF", "If the file is open, close and try again...\n\n" + str(e))
            print(e)

    def get_label_14_title(self, text):
        global stpa_pdf_report_list

        font_14 = QFont('Arial', 14)

        self.label = QLabel()
        self.label.setFont(font_14)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setText(text)
        return self.label

    def get_label_12_bold_subtitle(self, text):
        font_12_b = QFont('Arial', 12)
        font_12_b.setBold(True)

        self.label = QLabel()
        self.label.setFont(font_12_b)
        self.label.setWordWrap(True)
        self.label.setText(text)

        return self.label

    def get_label_12_text(self, text):
        global stpa_pdf_report_list

        font_12_b = QFont('Arial', 12)

        self.label = QLabel()
        self.label.setFont(font_12_b)
        self.label.setWordWrap(True)
        self.label.setText("  " + text)

        return self.label

    def get_label_11_text(self, text):
        global stpa_pdf_report_list

        font_11 = QFont('Arial', 11)
        self.label = QLabel()
        self.label.setFont(font_11)
        self.label.setWordWrap(True)
        self.label.setText("  " + text)

        return self.label

    def load_stpa_report(self):
        global id_project, stpa_pdf_report_list

        stpa_pdf_report_list = []

        list_goals_fifth = DB_Goals.select_all_goals_by_project(id_project)
        list_assumptions_fifth = DB_Assumptions.select_all_assumptions_by_project(id_project)
        list_losses_fifth = DB_Losses.select_all_losses_by_project(id_project)
        list_hazards_fifth = DB_Hazards.select_all_hazards_by_project(id_project)
        list_constraints_fifth = DB_Safety_Constraints.select_all_safety_constraints_by_project(id_project)

        top_widget = QtWidgets.QWidget()
        top_layout = QtWidgets.QVBoxLayout()
        group_box = QtWidgets.QGroupBox()
        group_box.setTitle("")
        group_box.setFont(QFont('Arial', 11))
        layout = QtWidgets.QVBoxLayout(group_box)

        project = DB_Projects.select_project_by_id(id_project)
        layout.addWidget(self.get_label_14_title("STPA analysis of " + project.name))
        layout.addWidget(self.get_label_12_text(project.description))
        layout.addWidget(self.get_label_12_text("Begin date: " + project.begin_date))
        # layout.addWidget(self.get_label_12_text("Last update: " + project.edited_date))

        # step one
        layout.addWidget(self.get_label_14_title("\n\nStep One - Purpose of the Analysis"))
        layout.addWidget(self.get_label_12_bold_subtitle("Goals"))
        for pos in range(len(list_goals_fifth)):
            layout.addWidget(self.get_label_11_text(
                "G-" + str(list_goals_fifth[pos].id_goal) + ": " + list_goals_fifth[pos].description))

        layout.addWidget(self.get_label_12_bold_subtitle("Assumptions"))
        for pos in range(len(list_assumptions_fifth)):
            layout.addWidget(self.get_label_11_text(
                "A-" + str(list_assumptions_fifth[pos].id_assumption) + ": " + list_assumptions_fifth[
                    pos].description))

        layout.addWidget(self.get_label_12_bold_subtitle("Losses"))
        for pos in range(len(list_losses_fifth)):
            layout.addWidget(self.get_label_11_text(
                "L-" + str(list_losses_fifth[pos].id_loss) + ": " + list_losses_fifth[pos].description))

        layout.addWidget(self.get_label_12_bold_subtitle("System-level Hazards"))
        for pos in range(len(list_hazards_fifth)):
            text = ""
            for loss in list_hazards_fifth[pos].list_of_loss:
                text += "[L-" + str(loss.id_loss_screen) + "] "

            layout.addWidget(self.get_label_11_text(
                "H-" + str(list_hazards_fifth[pos].id_hazard) + ": " + list_hazards_fifth[
                    pos].description + " " + text))

        layout.addWidget(self.get_label_12_bold_subtitle("Systel-level Safety Constraints"))
        for pos in range(len(list_constraints_fifth)):
            text = ""
            for haz in list_constraints_fifth[pos].list_of_hazards:
                text += "[H-" + str(haz.id_haz_screen) + "] "

            layout.addWidget(self.get_label_11_text(
                "SSC-" + str(list_constraints_fifth[pos].id_safety_constraint) + ": " + list_constraints_fifth[
                    pos].description + " " + text))

        # step 2
        layout.addWidget(self.get_label_14_title("\n\nStep Two - Control Structure"))
        self.get_component_report(layout, DB_Components.select_component_by_thing_project_analysis(
            Constant.DB_ID_CONTROLLER, id_project), Constant.DB_ID_CONTROLLER)
        self.get_component_report(layout,
                                  DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_ACTUATOR,
                                                                                           id_project),
                                  Constant.DB_ID_ACTUATOR)
        self.get_component_report(layout,
                                  DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_SENSOR,
                                                                                           id_project),
                                  Constant.DB_ID_SENSOR)
        self.get_component_report(layout, DB_Components.select_component_by_thing_project_analysis(
            Constant.DB_ID_EXT_INFORMATION, id_project), Constant.DB_ID_EXT_INFORMATION)
        self.get_component_report(layout,
                                  DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_CP,
                                                                                           id_project),
                                  Constant.DB_ID_CP)

        # step 3
        layout.addWidget(self.get_label_14_title("\nStep Three - Unsafe Control Actions"))
        layout.addWidget(self.get_label_12_bold_subtitle("Unsafe Control Actions (UCA) and Safety Constraints (SC)"))
        count_usc = 0
        list_aux_uca = DB_UCA.select_all(id_project)
        for uca in list_aux_uca:
            count_usc += 1

            text_context = ""
            for context in uca.context_list:
                if text_context != "":
                    text_context += ", "
                text_context += context.variable_name + " is " + context.variable_value

            text_haz = ""
            for haz in uca.hazard_list:
                text_haz += "[H-"
                id_hz = 1

                for pos in range(len(list_hazards_fifth)):
                    if list_hazards_fifth[pos].id == haz.id_hazard:
                        break
                    id_hz += 1
                text_haz += str(id_hz) + "]"

            item_uca_r = "Constraint " + str(count_usc) + ": (Controller: " + uca.name_controller + " - Control Action: " + uca.name_action + ")"
            layout.addWidget(self.get_label_11_text(item_uca_r))

            item_uca_u = "UCA-" + str(
                count_usc) + ": " + uca.name_controller + " " + uca.description_uca_type + " " + uca.name_action
            if text_context == "":
                item_uca_u += " in any context."
            else:
                item_uca_u += " when " + text_context + ". "
            item_uca_u += " " + text_haz
            layout.addWidget(self.get_label_11_text(item_uca_u))

            item_uca_u_desc = "Description: "
            if uca.description != None:
                item_uca_u_desc += uca.description
            layout.addWidget(self.get_label_11_text(item_uca_u_desc))

            item_uca_s = "SC-" + str(count_usc) + ": " + uca.name_controller + " must " + self.get_opposite_uca(
                uca.id_uca_type) + " " + uca.name_action
            if text_context == "":
                item_uca_s += " in any context."
            else:
                item_uca_s += " when " + text_context + ". "

            item_uca_s += "\n"
            layout.addWidget(self.get_label_11_text(item_uca_s))

        # step 4
        layout.addWidget(self.get_label_14_title("\nStep Four - Loss Scenarios and Recommendations"))
        count_ls = 0
        for rec in DB_Loss_Scenario_Req.select_all(id_project):
            count_ls += 1
            spacer = " -> "
            if Constant.ALGORITHM in rec.name_src or Constant.PROCESS_MODEL_full_name in rec.name_src:
                spacer = " in "

            layout.addWidget(self.get_label_11_text(
                "R-" + str(count_ls) + " (" + rec.name_src + spacer + rec.name_dst + "): UCA-" + str(self.get_number_uca(rec.id_uca, list_aux_uca))))
            layout.addWidget(self.get_label_11_text("Cause: " + rec.cause))
            layout.addWidget(self.get_label_11_text("Recommendation: " + rec.requirement))
            layout.addWidget(self.get_label_11_text("Mechanism: " + rec.mechanism + "\n"))

        top_layout.addWidget(group_box)
        top_widget.setLayout(top_layout)
        self.ui.scrollArea_fifith_report.setWidget(top_widget)

        # report
        layout.addWidget(self.get_label_14_title("\nLink Report"))
        list_omitted_links = DB_Components_Links.select_omitted_links(id_project)
        for omt in list_omitted_links:
            layout.addWidget(self.get_label_11_text(omt))

    def get_number_uca(self, id_uca, list_aux_uca):
        count = 1
        for uca in list_aux_uca:
            if uca.id == id_uca:
                return count
            count += 1
        return 0

    def get_component_report(self, layout, list_of_components, id_comp):
        general_name = "Component "

        if (id_comp == Constant.DB_ID_CONTROLLER):
            general_name = "Controller "
        elif (id_comp == Constant.DB_ID_ACTUATOR):
            general_name = "Actuator "
        elif (id_comp == Constant.DB_ID_SENSOR):
            general_name = "Sensor "
        elif (id_comp == Constant.DB_ID_EXT_INFORMATION):
            general_name = "External System "
        elif (id_comp == Constant.DB_ID_CP):
            general_name = "Controlled Process "

        for comp in list_of_components:
            aux_name = general_name + comp.name

            if comp.is_external_component == 1:
                aux_name += " (external of analysis)"

            layout.addWidget(self.get_label_12_bold_subtitle(aux_name))

            layout.addWidget(self.get_label_12_text("Outgoing connections"))
            for link in DB_Components_Links.select_component_links_by_project_and_component(comp.id, True):
                layout.addWidget(self.get_label_11_text("    " + link.name_src + " -> " + link.name_dst))
                # if id_comp == Constant.DB_ID_CONTROLLER or id_comp == Constant.DB_ID_CP or id_comp == Constant.DB_ID_SENSOR:
                if id_comp == Constant.DB_ID_CONTROLLER:
                    self.get_component_report_actions(layout, comp.id, id_project, link.id)
                    self.get_component_report_feedback(layout, comp.id, id_project, link.id)

            layout.addWidget(self.get_label_12_text("Incoming connections"))
            for link in DB_Components_Links.select_component_links_by_project_and_component(comp.id, False):
                layout.addWidget(self.get_label_11_text("    " + link.name_src + " -> " + link.name_dst))
                if id_comp == Constant.DB_ID_CONTROLLER:
                    self.get_component_report_actions(layout, comp.id, id_project, link.id)
                    self.get_component_report_feedback(layout, comp.id, id_project, link.id)

            if (id_comp == Constant.DB_ID_CP):
                self.get_report_cp(layout, id_project, comp.id)

            layout.addWidget(self.get_label_11_text(" "))

    def get_component_report_actions(self, layout, id_comp, id_project, id_link):
        list_a = DB_Actions_Components.select_actions_by_component_project_link(id_comp, id_project, id_link)
        if len(list_a) > 0:
            aux_a = ""
            for act in list_a:
                if aux_a != "":
                    aux_a += ", "
                aux_a += act.name
            layout.addWidget(self.get_label_11_text("\tControl actions: " + aux_a))

    def get_component_report_feedback(self, layout, id_comp, id_project, id_link):
        list_v = DB_Variables.select_variables_with_value_by_controller_project_link(id_comp, id_project, id_link)
        if len(list_v) > 0:
            layout.addWidget(self.get_label_11_text("\tFeedbacks (variables and values):"))
            aux_v = ""
            for var in list_v:
                aux_v = var.var_name + " ("
                add_comma = False
                for val in var.values_list:
                    if add_comma:
                        aux_v += ", " + val.value
                    else:
                        aux_v += val.value
                    add_comma = True
                aux_v += ")"
                layout.addWidget(self.get_label_11_text("\t    " + aux_v))

    def get_report_cp(self, layout, id_project, id_father):
        text_inp = ""
        for comp_i in DB_Components.select_controlled_process_values(id_project, id_father, Constant.DB_ID_INPUT):
            if text_inp != "":
                text_inp += ", "
            text_inp += comp_i

        if text_inp != "":
            layout.addWidget(self.get_label_11_text("Input: " + text_inp))

        text_out = ""
        for comp_i in DB_Components.select_controlled_process_values(id_project, id_father, Constant.DB_ID_OUTPUT):
            if text_out != "":
                text_out += ", "
            text_out += comp_i

        if text_out != "":
            layout.addWidget(self.get_label_11_text("Output: " + text_out))

        text_env = ""
        for comp_i in DB_Components.select_controlled_process_values(id_project, id_father,
                                                                     Constant.DB_ID_ENV_DISTURBANCES):
            if text_env != "":
                text_env += ", "
            text_env += comp_i

        if text_env != "":
            layout.addWidget(self.get_label_11_text("Environmental Disturbances: " + text_env))

    def get_opposite_uca(self, id):
        result = ""

        if id == Constant.provided_in_wrong_order:
            result = "not provide in wrong order"
        elif id == Constant.provided_too_early:
            result = "not provide too early"
        elif id == Constant.provided_too_late:
            result = "not provide too late"
        elif id == Constant.not_provided:
            result = "provide"
        elif id == Constant.provided:
            result = "not provide"
        elif id == Constant.applied_too_long:
            result = "not provide too long"
        elif id == Constant.stopped_too_son:
            result = "not provide to soon"

        return result
    # ----- Functions STPA report Step -----

    # ----- Functions Graphical Structure image -----
    def get_file_extension(self, src, current_date):
        dst = "0"
        if ".png" in src.lower():
            dst = Constant.FILES_REPO + "\\" + str(id_project) + "_" + current_date + ".png"
        elif ".jpg" in src.lower():
            dst = Constant.FILES_REPO + "\\" + str(id_project) + "_" + current_date + ".jpg"
        elif ".jpeg" in src.lower():
            dst = Constant.FILES_REPO + "\\" + str(id_project) + "_" + current_date + ".jpeg"
        else:
            showdialog("Wrong format", "Please select only image files (PNG or JPG)")

        return dst

    def on_button_select_file_one_clicked(self):
        global id_project

        try:
            fname = QFileDialog.getOpenFileName(None, 'Open file', './Files', 'Images (*.png *.jpeg *.jpg)')
            src = fname[0]

            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK_FILE_COPY)

            if os.path.exists(src):
                dst = self.get_file_extension(src, current_date)
                if dst == "0":
                    return

                to_delete = DB_Project_Files.select_images_by_project(id_project, 1)
                if to_delete != "" and os.path.exists(to_delete):
                    os.remove(to_delete)

                copyfile(src, dst)
                id = DB_Project_Files.insert_control_srtucture_file(id_project, dst, current_date, 1)

                if id > 0:
                    showdialog("Success", "Image imported")
                    self.ui.label_image_pic_one.setPixmap(QtGui.QPixmap(dst))
                    self.ui.label_image_pic_one.show()

                else:
                    showdialog("Error", "ry again, Try to import only files PNG or JPG")
        except NameError as e:
            print(e)

    def on_button_select_file_two_clicked(self):
        global id_project

        try:
            fname = QFileDialog.getOpenFileName(None, 'Open file', './Files', 'Images (*.png *.jpeg *.jpg)')
            src = fname[0]

            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK_FILE_COPY)

            if os.path.exists(src):
                dst = self.get_file_extension(src, current_date)
                if dst == "0":
                    return

                to_delete = DB_Project_Files.select_images_by_project(id_project, 2)
                if to_delete != "" and os.path.exists(to_delete):
                    os.remove(to_delete)

                copyfile(src, dst)
                id = DB_Project_Files.insert_control_srtucture_file(id_project, dst, current_date, 2)

                if id > 0:
                    showdialog("Success", "Image imported")
                    self.ui.label_image_pic_two.setPixmap(QtGui.QPixmap(dst))
                    self.ui.label_image_pic_two.show()

                else:
                    showdialog("Error", "ry again, Try to import only files PNG or JPG")
        except NameError as e:
            print(e)

    def on_button_select_file_three_clicked(self):
        global id_project

        try:
            fname = QFileDialog.getOpenFileName(None, 'Open file', './Files', 'Images (*.png *.jpeg *.jpg)')
            src = fname[0]

            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK_FILE_COPY)

            if os.path.exists(src):
                dst = self.get_file_extension(src, current_date)
                if dst == "0":
                    return

                to_delete = DB_Project_Files.select_images_by_project(id_project, 3)
                if to_delete != "" and os.path.exists(to_delete):
                    os.remove(to_delete)

                copyfile(src, dst)
                id = DB_Project_Files.insert_control_srtucture_file(id_project, dst, current_date, 3)

                if id > 0:
                    showdialog("Success", "Image imported")
                    self.ui.label_image_pic_three.setPixmap(QtGui.QPixmap(dst))
                    self.ui.label_image_pic_three.show()

                else:
                    showdialog("Error", "ry again, Try to import only files PNG or JPG")
        except NameError as e:
            print(e)

    def on_button_delete_file_one_clicked(self):
        global id_project

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Delete first image")
        msgBox.setText("Are you sure that you to delete the first image?")

        msgBox.addButton(QPushButton("Delete"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.NoRole)

        returnValue = msgBox.exec()
        if returnValue == 0:
            to_delete = DB_Project_Files.select_images_by_project(id_project, 1)
            DB_Project_Files.delete_file(id_project, 1)
            if to_delete != "" and os.path.exists(to_delete):
                os.remove(to_delete)

            self.load_control_structure_image()

    def on_button_delete_file_two_clicked(self):
        global id_project

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Delete second image")
        msgBox.setText("Are you sure that you to delete the second image?")

        msgBox.addButton(QPushButton("Delete"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.NoRole)

        returnValue = msgBox.exec()
        if returnValue == 0:
            to_delete = DB_Project_Files.select_images_by_project(id_project, 2)
            DB_Project_Files.delete_file(id_project, 2)
            if to_delete != "" and os.path.exists(to_delete):
                os.remove(to_delete)

            self.load_control_structure_image()

    def on_button_delete_file_three_clicked(self):
        global id_project

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Delete third image")
        msgBox.setText("Are you sure that you to delete the third image?")

        msgBox.addButton(QPushButton("Delete"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.NoRole)

        returnValue = msgBox.exec()
        if returnValue == 0:
            to_delete = DB_Project_Files.select_images_by_project(id_project, 3)
            DB_Project_Files.delete_file(id_project, 3)
            if to_delete != "" and os.path.exists(to_delete):
                os.remove(to_delete)

            self.load_control_structure_image()

    def load_control_structure_image(self):
        global id_project

        self.ui.label_image_pic_one.setPixmap(QtGui.QPixmap(Constant.DEFAULT_IMAGE_PATH))
        self.ui.label_image_pic_two.setPixmap(QtGui.QPixmap(Constant.DEFAULT_IMAGE_PATH))
        self.ui.label_image_pic_three.setPixmap(QtGui.QPixmap(Constant.DEFAULT_IMAGE_PATH))

        try:
            self.ui.label_image_pic_one.show()
            path_one = DB_Project_Files.select_images_by_project(id_project, 1)
            if path_one != "":
                self.ui.label_image_pic_one.setPixmap(QtGui.QPixmap(path_one))
            self.ui.label_image_pic_one.show()
        except NameError as e:
            print(e)


        try:
            self.ui.label_image_pic_two.show()
            path_two = DB_Project_Files.select_images_by_project(id_project, 2)
            if path_two != "":
                self.ui.label_image_pic_two.setPixmap(QtGui.QPixmap(path_two))
            self.ui.label_image_pic_two.show()
        except NameError as e:
            print(e)

        try:
            self.ui.label_image_pic_three.show()
            path_three = DB_Project_Files.select_images_by_project(id_project, 3)
            if path_three != "":
                self.ui.label_image_pic_three.setPixmap(QtGui.QPixmap(path_three))
            self.ui.label_image_pic_three.show()
        except NameError as e:
            print(e)

    # ----- Functions Graphical Structure image -----

    # ----- Functions STPA 4 Step -----
    def selection_change_controller_fourth(self, i):
        self.load_combobox_fourth_control_action()

    def selection_change_control_action_fourth(self, i):
        self.load_uca_fourth()

    def selection_change_uca_fourth(self, i):
        self.load_loss_scenarios_requirements()

    def load_combobox_fourth_controller(self):
        global list_four_controller, id_project

        list_four_controller = DB_Components.select_controller_not_external_project_analysis(id_project)
        self.ui.combobox_fourth_controller.setEnabled(True)
        self.ui.combobox_fourth_controller.clear()

        for conn in list_four_controller:
            self.ui.combobox_fourth_controller.addItem(conn.name)

        if len(list_four_controller) == 0:
            self.ui.combobox_fourth_control_action.clear()
            self.ui.listwidget_fourth_uca.clear()
            self.ui.listwidget_fourth_causal_factor.clear()
            self.ui.listwidget_fourth_requirement.clear()
        elif len(list_four_controller) > 0:
            self.load_combobox_fourth_control_action()

    def load_combobox_fourth_control_action(self):
        global list_four_control_action, id_project

        pos = self.ui.combobox_fourth_controller.currentIndex()

        if pos < 0:
            return

        list_four_control_action = DB_Actions_Components.select_actions_by_component_and_project(
            list_four_controller[pos].id, id_project)

        self.ui.combobox_fourth_control_action.clear()
        self.ui.combobox_fourth_control_action.setEnabled(True)

        for pos in range(len(list_four_control_action)):
            self.ui.combobox_fourth_control_action.addItem(list_four_control_action[pos].name)

        if len(list_four_control_action) > 0:
            self.load_uca_fourth()
        else:
            self.ui.listwidget_fourth_uca.clear()
            self.ui.listwidget_fourth_causal_factor.clear()
            self.ui.listwidget_fourth_requirement.clear()

    def load_uca_fourth(self):
        global list_fourth_uca
        pos = self.ui.combobox_fourth_control_action.currentIndex()
        if len(list_four_control_action) > 0:
            list_fourth_uca = DB_UCA.select_all_saf_uca_by_control_action_filtering(list_four_control_action[pos].id,
                                                                                    Constant.UCA_RULE, True)
            list_fourth_uca.extend(
                DB_UCA.select_all_saf_uca_by_control_action_filtering(list_four_control_action[pos].id,
                                                                      Constant.UCA_CELL, True))
            self.ui.listwidget_fourth_uca.clear()
            self.ui.listwidget_fourth_uca.setEnabled(True)

            count_r = 0
            count_c = 0
            for uca in list_fourth_uca:
                text = "UCA"
                if uca.uca_origin == Constant.UCA_RULE:
                    count_r += 1
                    text += "_R-" + str(count_r)
                else:
                    count_c += 1
                    text += "_C-" + str(count_c)

                text += " " + uca.name_controller + " " + uca.description_uca_type + " " + uca.name_action

                text_context = ""
                for context in uca.context_list:
                    if text_context != "":
                        text_context += ", "
                    text_context += context.variable_name + " is " + context.variable_value

                if text_context == "":
                    text += " in any context. "
                else:
                    text += " when " + text_context + ". "

                # text += text_context + ". "
                for haz in uca.hazard_list:
                    text += "[H-" + str(haz.hazard_order) + "]"

                self.ui.listwidget_fourth_uca.addItem(text)

            self.load_loss_scenarios()
            self.load_loss_scenarios_requirements()
        else:
            self.ui.listwidget_fourth_uca.setEnabled(False)

    def load_loss_scenarios(self):
        global list_four_control_action, list_fourth_uca, list_four_controller, list_four_loss_causal

        if len(list_fourth_uca) == 0 or len(list_four_controller) == 0:
            self.ui.listwidget_fourth_causal_factor.clear()
            self.ui.listwidget_fourth_requirement.clear()
            return

        pos_c = self.ui.combobox_fourth_controller.currentIndex()
        list_four_loss_causal = Safety_tools_new.get_step_four(onto, id_project, list_four_controller[pos_c])
        self.ui.listwidget_fourth_causal_factor.clear()

        for loss in list_four_loss_causal:
            # item = color.BOLD + "Side: " + loss.side + color.END + " - " + loss.onto_name + "\n"
            # item += color.BOLD + "Cause: " + loss.causes + color.END + " - " + loss.onto_name
            side = "Right"
            if loss.side == "B":
                side = "Left"

            item = side + " Side" + " - " + loss.onto_name + "\n"
            item += "Causal Factor: " + loss.causes + "\n"
            item += "Recommendation: " + loss.requirement + "\n"

            self.ui.listwidget_fourth_causal_factor.addItem(item)

        # result_list.append(color.BOLD + "Left: " + color.END + r_text)

    def selection_change_causal_factor_fourth(self):
        global list_four_loss_causal
        pos = self.ui.listwidget_fourth_causal_factor.currentRow()

        self.clear_recommendation_fields()

        if pos == -1:
            # showdialog("No causal factor selected", "Select at least one causal factor")
            return

        lc = list_four_loss_causal[pos]
        text = lc.name_src + " -> " + lc.name_dst
        desc = "Interaction:"

        if lc.name_src == lc.name_dst or lc.name_src.lower().__contains__("process model") or lc.name_src.lower().__contains__("algorithm"):
            desc = "Element:"
            text = lc.name_src

        self.ui.label_fourth_interaction.setText(desc)
        self.ui.label_fourth_interaction_desc.setText(text)
        self.ui.label_fourth_cause.setText(lc.causes)
        self.ui.label_fourth_recommendation.setText(lc.requirement)

    def load_loss_scenarios_requirements(self):
        global list_four_requirements, id_project, list_fourth_uca

        self.ui.listwidget_fourth_requirement.clear()

        if len(list_fourth_uca) == 0:
            return

        pos_u = self.ui.listwidget_fourth_uca.currentRow()
        if pos_u > -1:
            list_four_requirements = DB_Loss_Scenario_Req.select_all_requirements_by_project_uca(id_project, list_fourth_uca[pos_u].id)
            count = 0
            for req in list_four_requirements:
                count += 1
                spacer = " -> "
                if Constant.ALGORITHM in req.name_src or Constant.PROCESS_MODEL_full_name in req.name_src:
                    spacer = " in "

                src_dst = req.name_src
                if req.name_src != req.name_dst:
                    src_dst = req.name_src + spacer + req.name_dst

                item = "R-" + str(count) + " (" + src_dst + "): \n"
                item += "Cause: " + req.cause + "\n"
                item += "Recommendation: " + req.requirement + "\n"
                item += "Mechanism: " + req.mechanism + "\n"
                self.ui.listwidget_fourth_requirement.addItem(item)

    def on_button_fourth_add_causal_factor_clicked(self):
        global list_fourth_uca, list_four_controller, list_four_control_action, id_project, list_four_loss_causal

        pos_c = self.ui.combobox_fourth_controller.currentIndex()
        pos_a = self.ui.combobox_fourth_control_action.currentIndex()
        pos_u = self.ui.listwidget_fourth_uca.currentRow()
        pos_cause = self.ui.listwidget_fourth_causal_factor.currentRow()

        if pos_c == -1:
            showdialog("No controller selected", "Select the controller")
            return
        elif pos_a == -1:
            showdialog("No control action selected", "Select the control action")
            return
        elif pos_u == -1:
            showdialog("No UCA selected", "Select the UCA")
            return
        elif pos_cause == -1:
            showdialog("No causal factor selected", "Select at least one causal factor")
            return

        lc = list_four_loss_causal[pos_cause]
        req_id_saved = self.is_requirement_cause_saved(lc.requirement, lc.causes, lc.mechanism)
        if req_id_saved > 0:
            showdialog("No need to save", "The current recommendation is saved as Recommendation " + str(req_id_saved))
            return

        req = Loss_Scenario_Req(0,
                                list_four_controller[pos_c].id,
                                list_fourth_uca[pos_u].id,
                                id_project,
                                lc.id_component,
                                lc.id_component_src,
                                lc.id_component_dst,
                                lc.requirement,
                                lc.causes,
                                lc.mechanism,
                                "", "", "")

        id_req = DB_Loss_Scenario_Req.insert(req)

        if id_req > 0:
            showdialog("Success", "Recommendation created!")
            self.load_loss_scenarios_requirements()
        else:
            showdialog("Error", "Cannot save recommendation now, try again!")

    def on_button_fourth_create_causal_factor_clicked(self):
        global list_fourth_uca, list_four_controller, list_four_control_action, id_project, list_four_loss_causal

        pos_c = self.ui.combobox_fourth_controller.currentIndex()
        pos_a = self.ui.combobox_fourth_control_action.currentIndex()
        pos_u = self.ui.listwidget_fourth_uca.currentRow()
        pos_cause = self.ui.listwidget_fourth_causal_factor.currentRow()

        if pos_c == -1:
            showdialog("No controller selected", "Select the controller")
            return
        elif pos_a == -1:
            showdialog("No control action selected", "Select the control action")
            return
        elif pos_u == -1:
            showdialog("No UCA selected", "Select the UCA")
            return
        elif pos_cause == -1:
            showdialog("No causal factor selected", "Select at least one causal factor")
            return

        lc = list_four_loss_causal[pos_cause]
        cf = CausalFactorDialog(lc.causes, lc.requirement, lc.mechanism, lc.name_src, lc.name_dst, "", False, "")
        result = cf.exec_()

        if result == 1:
            cause = cf.cause.toPlainText()
            requirement = cf.requirement.toPlainText()
            mechanism = cf.mechanism.toPlainText()
            # priority = cf.comboBox.currentIndex() + 1

            if len(cause) == 0 or len(requirement) == 0:
                showdialog("Error to create a new recommendation",
                           "You must fill all the fields to create a new recommendation.")
                return

            req_id_saved = self.is_requirement_cause_saved(requirement, cause, mechanism)
            if req_id_saved > 0:
                showdialog("No need to save",
                           "The current recommendation is saved as Recommendation " + str(req_id_saved))
                return

            lc = list_four_loss_causal[pos_cause]
            req = Loss_Scenario_Req(0,
                                    list_four_controller[pos_c].id,
                                    list_fourth_uca[pos_u].id,
                                    id_project,
                                    lc.id_component,
                                    lc.id_component_src,
                                    lc.id_component_dst,
                                    requirement,
                                    cause,
                                    mechanism,
                                    "", "", "")

            id_req = DB_Loss_Scenario_Req.insert(req)

            if id_req > 0:
                # showdialog("Success", "Recommendation created!")
                self.load_loss_scenarios_requirements()
            else:
                showdialog("Error", "Cannot save Recommendation now, try again!")

    def selection_change_requirement_fourth(self):
        global list_four_requirements

        pos = self.ui.listwidget_fourth_requirement.currentRow()
        if pos == -1:
            showdialog("No recommendation selected", "Select one recommendation to delete")
            return

        # cb = QApplication.clipboard()
        # cb.clear(mode=cb.Clipboard)
        # cb.setText(self.ui.listwidget_fourth_requirement.currentItem().text(), mode=cb.Clipboard)

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)

        msgBox.setWindowTitle("Change recommendation")
        msgBox.setText("Do you want to update or delete this recommendation?")

        msgBox.addButton(QPushButton("Update"), QMessageBox.YesRole)
        msgBox.addButton(QPushButton("Delete"), QMessageBox.NoRole)
        msgBox.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)

        returnValue = msgBox.exec()
        if returnValue == 0:
            edt_req = list_four_requirements[pos]
            # priority = edt_req.id_priority - 1
            cf = CausalFactorDialog(edt_req.cause, edt_req.requirement, edt_req.mechanism, edt_req.name_src, edt_req.name_dst, edt_req.name_cause, False, "")
            result = cf.exec_()

            if result == 1:
                cause = cf.cause.toPlainText()
                recommendation = cf.requirement.toPlainText()
                mechanism = cf.mechanism.toPlainText()
                # priority = cf.comboBox.currentIndex() + 1

                performance_req = edt_req.performance_req

                DB_Loss_Scenario_Req.update(edt_req.id, cause, recommendation, mechanism, performance_req)
                self.load_loss_scenarios_requirements()
                return
        elif returnValue == 1:
            pos = self.ui.listwidget_fourth_requirement.currentRow()

            if pos == -1:
                showdialog("No recommendation selected", "Select one recommendation to delete")
                return

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Are you sure that you want delete the recommendation R-" + str(pos + 1) + "?")
            msgBox.setWindowTitle("Delete Recommendation?")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                DB_Loss_Scenario_Req.delete_by_id(list_four_requirements[pos].id)
                self.load_loss_scenarios_requirements()

    def is_requirement_cause_saved(self, requirement, cause, mechanism):
        global list_four_requirements

        count = 0
        for item in list_four_requirements:
            count += 1
            if item.cause == cause and item.requirement == requirement and item.mechanism == mechanism:
                return count

        return 0

    def clear_recommendation_fields(self):
        self.ui.label_fourth_interaction_desc.setText("")
        self.ui.label_fourth_cause.setText("")
        self.ui.label_fourth_recommendation.setText("")
        self.ui.label_fourth_mechanism.setText("")
    # ----- Functions STPA 4 Step -----

    # ----- Functions STPA 3 Step -----

    def selection_change_controller_third(self, i):
        self.load_combobox_third_control_action()

    def selection_change_control_action_third(self, i):
        self.load_variables_dynamically()
        self.load_uca_third()

    def load_combobox_third_controller(self):
        global list_three_controller, id_project

        list_three_controller = DB_Components.select_controller_not_external_project_analysis(id_project)
        self.ui.combobox_third_controller.clear()

        for conn in list_three_controller:
            self.ui.combobox_third_controller.addItem(conn.name)

        if len(list_three_controller) == 0:
            list_three_control_action = []
            self.ui.combobox_third_control_action.clear()
            self.ui.combobox_third_control_action.setEnabled(False)
            self.ui.listwidget_third_uca_rule.clear()
            self.ui.listwidget_third_uca_cell.clear()
            self.ui.listwidget_third_uca_safe.clear()
            self.ui.tablewidget_third_context.clear()
            self.ui.tablewidget_third_context.setRowCount(0)
            self.ui.tablewidget_third_context.setColumnCount(0)
        elif len(list_three_controller) > 0:
            self.load_combobox_third_control_action()

    def load_combobox_third_control_action(self):
        global list_three_control_action, list_three_controller, id_project, list_third_uca_type, list_third_var_comp

        pos = self.ui.combobox_third_controller.currentIndex()
        if pos < 0:
            return

        list_three_control_action = DB_Actions_Components.select_actions_by_component_and_project(list_three_controller[pos].id, id_project)

        self.ui.combobox_third_control_action.clear()
        self.ui.combobox_third_control_action.setEnabled(True)

        for pos in range(len(list_three_control_action)):
            self.ui.combobox_third_control_action.addItem(list_three_control_action[pos].name)

        self.load_variables_dynamically()

    # def find_hazardous_UCA(self, row, column, context_list):
    #     global list_third_uca
    #     pos = 0
    #     for uca in list_third_uca:
    #         pos +=1
    #         for ctx in uca.context_list:
    #             for var in context_list:
    #                 col = column + uca.id_uca_type - 1
    #
    #                 if ctx.id_variable == var.var_id and ctx.id_value == var.val_id:
    #                     cell = self.ui.tablewidget_third_context.item(row, col).text()
    #                     text = " UR-" + str(pos)
    #                     if not text in cell:
    #                         self.ui.tablewidget_third_context.setItem(row, col, QTableWidgetItem(cell + text))

    def find_hazardous_UCA(self, row, column, context_list):
        global list_third_uca
        pos = 0
        for uca in list_third_uca:
            pos += 1
            print_uca = True
            for ctx in uca.context_list:
                for var in context_list:
                    if ctx.id_variable == var.var_id:
                        if ctx.id_value != var.val_id:
                            print_uca = False

            if print_uca:
                col = column + uca.id_uca_type - 1
                cell = self.ui.tablewidget_third_context.item(row, col).text()
                text = " UR-" + str(pos)
                if not text in cell:
                    self.ui.tablewidget_third_context.setItem(row, col, QTableWidgetItem(cell + text))

    def find_hazardous_UCA_Cell(self, row, column, context_list):
        global list_third_uca_cell
        pos = 0
        for uca in list_third_uca_cell:
            pos += 1
            print_uca = True
            for ctx in uca.context_list:
                for var in context_list:
                    if ctx.id_variable == var.var_id:
                        if ctx.id_value != var.val_id:
                            print_uca = False

            if print_uca:
                col = column + uca.id_uca_type - 1
                cell = self.ui.tablewidget_third_context.item(row, col).text()
                text = " UC-" + str(pos)
                if not text in cell:
                    self.ui.tablewidget_third_context.setItem(row, col, QTableWidgetItem(cell + text))

    def find_hazardous_UCA_Safe(self, row, column, context_list):
        global list_third_uca_safe
        pos = 0
        for uca in list_third_uca_safe:
            pos += 1
            print_uca = True
            for ctx in uca.context_list:
                for var in context_list:
                    if ctx.id_variable == var.var_id:
                        if ctx.id_value != var.val_id:
                            print_uca = False

            if print_uca:
                col = column + uca.id_uca_type - 1
                cell = self.ui.tablewidget_third_context.item(row, col).text()
                text = " NH " + str(pos)
                if not text in cell:
                    self.ui.tablewidget_third_context.setItem(row, col, QTableWidgetItem(text + cell))
                    if cell != "":
                        self.ui.tablewidget_third_context.item(row, col).setBackground(
                            QtGui.QColor("#efc6c6"))  # color = "#C6EFCE"

    def load_variables_dynamically(self):
        global list_third_uca_type, list_third_var_comp, list_third_hazard, list_third_haz, list_three_controller, listwidget_third_hazard

        pos = self.ui.combobox_third_controller.currentIndex()
        if pos < 0:
            scrollArea = self.ui.scrollArea_4
            top_widget = QtWidgets.QWidget()
            top_layout = QtWidgets.QHBoxLayout()
            top_widget.setLayout(top_layout)
            scrollArea.setWidget(top_widget)
            return

        list_third_var_comp = DB_Variables.select_variables_with_value_by_project_controller_FOR_UCA(id_project, list_three_controller[pos].id)
        list_third_uca_type = DB_UCA.select_all_saf_uca_type_COMP()

        scrollArea = self.ui.scrollArea_4
        top_widget = QtWidgets.QWidget()
        top_layout = QtWidgets.QHBoxLayout()

        for uca in list_third_uca_type:
            group_box = QtWidgets.QGroupBox()
            group_box.setTitle(uca.name)
            layout = QtWidgets.QHBoxLayout(group_box)

            self.comboBox = QComboBox()
            self.comboBox.setObjectName("combo_" + uca.name)
            self.comboBox.setGeometry(QRect(40, 40, 491, 31))

            for type in uca.list_types:
                self.comboBox.addItem(type.description)

            layout.addWidget(self.comboBox)
            uca.component = self.comboBox
            top_layout.addWidget(group_box)

        for var in list_third_var_comp:
            group_box = QtWidgets.QGroupBox()
            group_box.setTitle(var.var_name)
            layout = QtWidgets.QHBoxLayout(group_box)

            self.comboBox = QComboBox()
            self.comboBox.setObjectName("combo_" + var.var_name)
            self.comboBox.setGeometry(QRect(40, 40, 491, 31))

            self.comboBox.addItem("Any")
            for val in var.values_list:
                self.comboBox.addItem(val.value)

            layout.addWidget(self.comboBox)
            var.component = self.comboBox
            top_layout.addWidget(group_box)

        list_third_hazard = DB_Hazards.select_all_hazards_by_project(id_project)

        group_box = QtWidgets.QGroupBox()
        group_box.setTitle("Hazards")
        layout = QtWidgets.QHBoxLayout(group_box)

        self.listWidget = QListWidget()
        self.listWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.listWidget.setObjectName("listwidget_hazard")
        self.listWidget.setGeometry(40, 40, 200, 200)
        self.listWidget.setMinimumWidth(600)

        for haz in list_third_hazard:
            self.listWidget.addItem("H-" + str(haz.id_hazard) + ": " + haz.description)

        layout.addWidget(self.listWidget)
        listwidget_third_hazard = self.listWidget
        top_layout.addWidget(group_box)

        top_widget.setLayout(top_layout)
        scrollArea.setWidget(top_widget)

    def load_uca_third(self):
        global list_third_uca, list_third_uca_cell, list_third_uca_safe, list_third_context, list_third_uca_type, list_third_uca_type_description, \
            list_third_uca_warning, list_three_control_action

        pos = self.ui.combobox_third_control_action.currentIndex()
        self.ui.listwidget_third_uca_rule.clear()
        self.ui.listwidget_third_uca_cell.clear()
        self.ui.listwidget_third_uca_safe.clear()
        self.ui.tablewidget_third_context.clear()
        self.ui.tablewidget_third_context.setRowCount(0)
        self.ui.tablewidget_third_context.setColumnCount(0)
        self.ui.label_third_description_rule.setText("")
        self.ui.label_third_description_cell.setText("")
        self.ui.label_third_description_safe.setText("")

        if pos < 0:
            return


        if len(list_three_control_action) > 0:
            list_third_uca = DB_UCA.select_all_saf_uca_by_control_action_filtering(list_three_control_action[pos].id, Constant.UCA_RULE, True)
            list_third_uca_cell = DB_UCA.select_all_saf_uca_by_control_action_filtering(list_three_control_action[pos].id, Constant.UCA_CELL, True)
            list_third_uca_safe = DB_UCA.select_all_saf_uca_by_control_action_filtering(list_three_control_action[pos].id, Constant.UCA_CELL, False)
            list_third_uca_warning = []

            count = 0
            for uca in list_third_uca:
                is_war = False
                count += 1
                text = "UCA_R-" + str(count) + " --> " + uca.name_controller + " " + uca.description_uca_type + " " + uca.name_action

                text_context = ""
                for context in uca.context_list:
                    if text_context != "":
                        text_context += ", "
                    text_context += context.variable_name + " is " + context.variable_value
                    if (context.variable_name == Constant.VAR_ERR or context.variable_value == Constant.VAL_ERR):
                        is_war = True

                if is_war:
                    list_third_uca_warning.append("UCA_R-" + str(count) + " (variables and values)")

                if text_context == "":
                    text += " in any context."
                else:
                    text += " when " + text_context + ". "

                for haz in uca.hazard_list:
                    text += "[H-" + str(haz.hazard_order) + "]"

                is_war = False
                if len(uca.hazard_list) == 0:
                    is_war = True

                if is_war:
                    list_third_uca_warning.append("UCA_R-" + str(count) + " (hazards)")

                self.ui.listwidget_third_uca_rule.addItem(text)

            # count = 0
            for uca_c in list_third_uca_cell:
                is_war = False
                count += 1
                text = "UCA_C-"  + str(count) + " --> " + uca_c.name_controller + " " + uca_c.description_uca_type + " " + uca_c.name_action

                text_context = ""
                for context in uca_c.context_list:
                    if text_context != "":
                        text_context += ", "
                    text_context += context.variable_name + " is " + context.variable_value
                    if (context.variable_name == Constant.VAR_ERR or context.variable_value == Constant.VAL_ERR):
                        is_war = True

                if is_war:
                    list_third_uca_warning.append("UCA-C" + str(count) + " (variables and values)")

                if text_context == "":
                    text += " in any context."
                else:
                    text += " when " + text_context + ". "
                for haz in uca_c.hazard_list:
                    text += "[H-" + str(haz.hazard_order) + "]"

                is_war = False
                if len(uca_c.hazard_list) == 0:
                    is_war = True

                if is_war:
                    list_third_uca_warning.append("UCA-C" + str(count) + " (hazards)")

                self.ui.listwidget_third_uca_cell.addItem(text)

            # count = 0
            for uca_s in list_third_uca_safe:
                is_war = False
                count += 1
                text = "NH-" + str(count) + " - " + uca_s.name_controller + " " + uca_s.description_uca_type + " " + uca_s.name_action

                text_context = ""
                for context in uca_s.context_list:
                    if text_context != "":
                        text_context += ", "
                    text_context += context.variable_name + " is " + context.variable_value
                    if (context.variable_name == Constant.VAR_ERR or context.variable_value == Constant.VAL_ERR):
                        is_war = True

                if is_war:
                    list_third_uca_warning.append("NH-" + str(count))

                if text_context == "":
                    text += " in any context."
                else:
                    text += " when " + text_context + ". "
                self.ui.listwidget_third_uca_safe.addItem(text)

            top_widget_uca = QtWidgets.QWidget()
            top_layout_uca = QtWidgets.QVBoxLayout()
            group_box_uca = QtWidgets.QGroupBox()
            group_box_uca.setTitle("Warnings")
            layout_uca = QtWidgets.QVBoxLayout(group_box_uca)
            layout_uca.setAlignment(Qt.AlignLeft | Qt.AlignTop)

            for uca_err in list_third_uca_warning:
                self.label_uca = QLabel()
                self.label_uca.setFont(QFont('Arial', 11))
                self.label_uca.setText(uca_err)
                layout_uca.addWidget(self.label_uca)

            top_layout_uca.addWidget(group_box_uca)
            top_widget_uca.setLayout(top_layout_uca)
            self.ui.scrollarea_third_warnings.setWidget(top_widget_uca)

            list_var_with_values = []
            for var in list_third_var_comp:
                if len(var.values_list) > 0:
                    list_var_with_values.append(var)

            list_third_context = []
            list_third_uca_type_description = DB_UCA.select_all_saf_uca_type()

            if len(list_var_with_values) > 0:
                Safety_tools_new.get_context_a(list_var_with_values, 0, [], list_third_context, True)

            if len(list_third_context) > 0:
                m_columns = len(list_third_context[0].list) + len(list_third_uca_type_description)
                m_rows = len(list_third_context)

                table = self.ui.tablewidget_third_context
                table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                table.setColumnCount(m_columns)  # Set three columns
                table.setRowCount(m_rows)  # and one row

                list_header = []
                for label in list_third_context[0].list:
                    list_header.append(label.var_name)

                for uca in list_third_uca_type:
                    for type in uca.list_types:
                        list_header.append(type.description)

                table.setHorizontalHeaderLabels(list_header)  # Set the table headers

                for r in range(len(list_third_context)):
                    row = list_third_context[r]
                    for c in range(m_columns):
                        if c < len(row.list):
                            col = row.list[c]
                            table.setItem(r, c, QTableWidgetItem(col.val_value))
                        else:
                            table.setItem(r, c, QTableWidgetItem(""))

                for r2 in range(len(list_third_context)):
                    row2 = list_third_context[r2]
                    self.find_hazardous_UCA(r2, len(row2.list), row2.list)
                    self.find_hazardous_UCA_Cell(r2, len(row2.list), row2.list)
                    self.find_hazardous_UCA_Safe(r2, len(row2.list), row2.list)

                table.resizeColumnsToContents()

    def on_button_button_third_save_uca_clicked(self):
        global listwidget_third_hazard, list_third_var_comp, list_third_uca, list_third_uca_type, list_third_hazard, list_three_controller, list_three_control_action

        hazard_list = []
        for haz in listwidget_third_hazard.selectedIndexes():
            hazard_list.append(list_third_hazard[haz.row()])

        context_list = self.get_context_selected()
        uca_type_id = self.get_context_selected_uca_type()

        pos_c = self.ui.combobox_third_controller.currentIndex()
        pos_a = self.ui.combobox_third_control_action.currentIndex()

        if pos_c == -1:
            showdialog("No controller selected", "Select the controller")
            return
        elif pos_a == -1:
            showdialog("No control action selected", "Select the control action")
            return
        # elif len(context_list) == 0:
        #     showdialog("No value selected", "Select at least one variable value")
        #     return
        elif listwidget_third_hazard == None:
            showdialog("No hazard selected", "Select at least one Hazard")
            return
        elif len(hazard_list) == 0:
            showdialog("No hazard selected", "Select at least one Hazard")
            return

        id_result = DB_UCA.insert(list_three_controller[pos_c].id, uca_type_id, list_three_control_action[pos_a].id,
                                  context_list, hazard_list, "rule", True)
        if id_result > 0:
            showdialog("Success", "UCA created!")
            self.load_uca_third()
        else:
            showdialog("Error", "Cannot save UCA now, try again!")

    def get_context_selected(self):
        global list_third_var_comp

        result_list = []

        for var in list_third_var_comp:
            values = []
            if var.component.currentIndex() != 0:
                values.append(var.values_list[var.component.currentIndex() - 1])
                result_list.append(Var_Values_Aux(var.var_name, var.variable, values))

        return result_list

    def get_context_selected_uca_type(self):
        global list_third_uca_type

        for type in list_third_uca_type:
            return type.list_types[type.component.currentIndex()].id
        return 0

    def on_button_button_third_delete_uca_rule_clicked(self):
        global list_third_uca
        pos = self.ui.listwidget_third_uca_rule.currentRow()

        if pos == -1:
            showdialog("No UCA_R selected", "Select one UCA_R to be deleted")
            return

        uca = list_third_uca[pos]
        list_req = DB_Loss_Scenario_Req.select_id_requirement_by_uca(uca.id)
        text = "Are you sure that you want delete UCA_R-" + str(pos + 1) + "?"
        if len(list_req) > 0:
            text += "\nIf you delete this UCA_R, you will lost " + str(len(list_req)) + " recommendations."

        text += "\nDo you want to proceed?"

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text)
        msgBox.setWindowTitle("Delete UCA_R?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_UCA.delete(uca.id)
            self.load_uca_third()

    def on_button_button_third_delete_uca_cell_clicked(self):
        global list_third_uca_cell
        pos = self.ui.listwidget_third_uca_cell.currentRow()

        if pos == -1:
            showdialog("No UCA_C selected", "Select one UCA_C to be deleted")
            return

        uca = list_third_uca_cell[pos]
        list_req = DB_Loss_Scenario_Req.select_id_requirement_by_uca(uca.id)
        text = "Are you sure that you want delete UCA_C-" + str(pos + 1) + "?"
        if len(list_req) > 0:
            text += "\nIf you delete this UCA_R, you will lost " + str(len(list_req)) + " recommendations."

        text += "\nDo you want to proceed?"

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text)
        msgBox.setWindowTitle("Delete UCA_C?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_UCA.delete(uca.id)
            self.load_uca_third()

    def on_button_button_third_delete_uca_safe_clicked(self):
        global list_third_uca_safe
        pos = self.ui.listwidget_third_uca_safe.currentRow()

        if pos == -1:
            showdialog("No NH selected", "Select one NH to be deleted")
            return

        uca = list_third_uca_safe[pos]
        text = "Are you sure that you want delete NH-" + str(pos + 1) + "?"
        text += "\nDo you want to proceed?"

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text)
        msgBox.setWindowTitle("Delete NH?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_UCA.delete(uca.id)
            self.load_uca_third()

    def cell_was_clicked(self, row, column):
        global list_third_context, list_three_controller, list_third_uca_type, list_third_hazard, list_third_uca_type_description

        if len(list_third_context) == 0:
            return

        if column < len(list_third_context[row].list):
            return

        text = self.ui.tablewidget_third_context.item(row, column).text()

        if text == "":
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)

            msgBox.setWindowTitle("Rule creation")
            msgBox.setText("Do you want to create a rule for this cell?")

            msgBox.addButton(QPushButton("Hazardous cell rule"), QMessageBox.YesRole)
            msgBox.addButton(QPushButton("NOT hazardous cell rule"), QMessageBox.NoRole)
            msgBox.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)

            returnValue = msgBox.exec()
            if returnValue == 0:
                context_list = list_third_context[row]
                uca_type = list_third_uca_type[0].list_types[column - len(context_list.list)]

                pos_c = self.ui.combobox_third_controller.currentIndex()
                pos_a = self.ui.combobox_third_control_action.currentIndex()

                if pos_c == -1:
                    showdialog("No controller selected", "Select the controller")
                    return
                elif pos_a == -1:
                    showdialog("No control action selected", "Select the control action")
                    return
                elif listwidget_third_hazard == None:
                    showdialog("No hazard selected", "Select at least one Hazard")
                    return

                msgBox2 = OpDialog()
                result = msgBox2.exec_()

                if result == 1:
                    hazard_list = []
                    for haz in msgBox2.listWidget.selectedIndexes():
                        hazard_list.append(list_third_hazard[haz.row()])

                    if len(hazard_list) == 0:
                        showdialog("No hazard selected", "Select at least one Hazard")
                        return

                    try:
                        id_result = DB_UCA.insert_from_cell(list_three_controller[pos_c].id, uca_type.id,
                                                            list_three_control_action[pos_a].id, context_list.list,
                                                            hazard_list, "cell", True)
                    except NameError as e:
                        print(e)
                        id_result = 0

                    if id_result > 0:
                        # showdialog("Success", "Rule for Cell created!")
                        self.ui.tablewidget_third_context.clearSelection()
                        self.load_uca_third()
                    else:
                        showdialog("Error", "Cannot save UCA now, try again!")
            elif returnValue == 1:
                context_list = list_third_context[row]
                uca_type = list_third_uca_type[0].list_types[column - len(context_list.list)]

                pos_c = self.ui.combobox_third_controller.currentIndex()
                pos_a = self.ui.combobox_third_control_action.currentIndex()

                if pos_c == -1:
                    showdialog("No controller selected", "Select the controller")
                    return
                elif pos_a == -1:
                    showdialog("No control action selected", "Select the control action")
                    return
                elif listwidget_third_hazard == None:
                    showdialog("No hazard selected", "Select at least one Hazard")
                    return

                try:
                    id_result = DB_UCA.insert_from_cell(list_three_controller[pos_c].id, uca_type.id,
                                                        list_three_control_action[pos_a].id,
                                                        context_list.list, [], "cell", False)
                except NameError as e:
                    print(e)
                    id_result = 0

                if id_result > 0:
                    # showdialog("Success", "Cell marked as Not Hazardous!")
                    self.ui.tablewidget_third_context.clearSelection()
                    self.load_uca_third()
                else:
                    showdialog("Error", "Cannot save UCA now, try again!")
        elif " NH " in text:
            context_list = list_third_context[row]
            col = column - len(context_list.list)
            uca_aux = list_third_uca_type_description[col]

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setText("Do you want to remove the Not Hazardous marking from cell at row " + str(
                row + 1) + " and column " + uca_aux.description + "?")
            msgBox.setWindowTitle("Delete Not Hazardous Cell")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

            returnValue = msgBox.exec()

            if returnValue == QMessageBox.Yes:
                uca_id_delete = self.find_uca_safe(context_list, uca_aux.id)
                if uca_id_delete > 0:
                    DB_UCA.delete(uca_id_delete)
                    self.ui.tablewidget_third_context.clearSelection()
                    self.load_uca_third()
                else:
                    showdialog("Error", "Error to process the action to delete, try again.")

    def find_uca_safe(self, context_list, uca_type_id):
        global list_third_uca_safe

        for uca in list_third_uca_safe:
            if uca.id_uca_type == uca_type_id:
                found_uca = True
                for ctx in uca.context_list:
                    for var in context_list.list:
                        if ctx.id_variable == var.var_id:
                            if ctx.id_value != var.val_id:
                                found_uca = False
                if found_uca:
                    return uca.id

        return 0

    def on_listwidget_uca_rule_clicked(self):
        global list_third_uca

        pos = self.ui.listwidget_third_uca_rule.currentRow()

        if len(list_third_uca) == 0 or pos < 0:
            return

        if list_third_uca[pos].description == None:
            self.ui.label_third_description_rule.setText("")
        else:
            self.ui.label_third_description_rule.setText(list_third_uca[pos].description)

    def on_listwidget_uca_cell_clicked(self):
        global list_third_uca_cell
        pos = self.ui.listwidget_third_uca_cell.currentRow()

        if len(list_third_uca_cell) == 0 or pos < 0:
            return

        if list_third_uca_cell[pos].description == None:
            self.ui.label_third_description_cell.setText("")
        else:
            self.ui.label_third_description_cell.setText(list_third_uca_cell[pos].description)

    def on_listwidget_uca_safe_clicked(self):
        global list_third_uca_safe

        pos = self.ui.listwidget_third_uca_safe.currentRow()

        if len(list_third_uca_safe) == 0 or pos < 0:
            return

        if list_third_uca_safe[pos].description == None:
            self.ui.label_third_description_safe.setText("")
        else:
            self.ui.label_third_description_safe.setText(list_third_uca_safe[pos].description)

    def on_button_third_update_description_uca_rule(self):
        global list_third_uca, list_three_control_action

        pos = self.ui.listwidget_third_uca_rule.currentRow()

        if len(list_third_uca) == 0 or pos < 0:
            return

        result = self.update_description_uca(list_third_uca[pos])

        if result < 0:
            return

        pos_act = self.ui.combobox_third_control_action.currentIndex()
        if len(list_three_control_action) <= 0:
            return

        list_third_uca = DB_UCA.select_all_saf_uca_by_control_action_filtering(list_three_control_action[pos_act].id, Constant.UCA_RULE, True)
        self.on_listwidget_uca_rule_clicked()

    def on_button_third_update_description_uca_cell(self):
        global list_third_uca_cell, list_three_control_action
        pos = self.ui.listwidget_third_uca_cell.currentRow()

        if len(list_third_uca_cell) == 0 or pos < 0:
            return

        result = self.update_description_uca(list_third_uca_cell[pos])

        if result < 0:
            return

        pos_act = self.ui.combobox_third_control_action.currentIndex()
        if len(list_three_control_action) <= 0:
            return

        list_third_uca_cell = DB_UCA.select_all_saf_uca_by_control_action_filtering(list_three_control_action[pos_act].id, Constant.UCA_CELL, True)
        self.on_listwidget_uca_cell_clicked()

    def on_button_third_update_description_uca_safe(self):
        global list_third_uca_safe, list_three_control_action

        pos = self.ui.listwidget_third_uca_safe.currentRow()

        if len(list_third_uca_safe) == 0 or pos < 0:
            return

        result = self.update_description_uca(list_third_uca_safe[pos])

        if result < 0:
            return

        pos_act = self.ui.combobox_third_control_action.currentIndex()
        if len(list_three_control_action) <= 0:
            return

        list_third_uca_safe = DB_UCA.select_all_saf_uca_by_control_action_filtering(list_three_control_action[pos_act].id, Constant.UCA_CELL, False)
        self.on_listwidget_uca_safe_clicked()

    def update_description_uca(self, obj_uca):
        global third_uca_description

        third_uca_description = ""
        if obj_uca.description != None:
            third_uca_description = obj_uca.description

        cf = UcaDescriptionDialog()
        result = cf.exec_()

        if result == 1:
            # description = cf.description.text()
            description = cf.description.toPlainText()
            return DB_UCA.update(obj_uca.id, description)

        return -1

    # ----- Functions STPA 3 Step -----

    # ----- Functions STPA 2 Step -----
    def on_button_delete_controller_connection_clicked(self):
        global list_connection_controller, list_links_controller
        pos = self.ui.listwidget_controller_connection.currentRow()
        item = self.ui.listwidget_controller_connection.currentItem()

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete: " + item.text() + "?")
        msgBox.setWindowTitle("Delete Link Controller?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Components_Links.delete(list_links_controller[pos])
            self.load_controller_connections()
            self.load_controller_actions_connections()
            self.load_controller_variable_connections()

    def on_button_delete_exts_connection_clicked(self):
        global list_connection_exts, list_links_exts
        pos = self.ui.listwidget_exts_connection.currentRow()
        item = self.ui.listwidget_exts_connection.currentItem()

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete: " + item.text() + "?")
        msgBox.setWindowTitle("Delete Link External System?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Components_Links.delete(list_links_exts[pos])
            self.load_exts_connections()
            self.load_controller_actions_connections()
            self.load_controller_variable_connections()

    def on_button_delete_actuator_connection_clicked(self):
        global list_connection_actuator, list_links_actuator
        pos = self.ui.listwidget_actuator_connection.currentRow()
        item = self.ui.listwidget_actuator_connection.currentItem()

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete: " + item.text() + "?")
        msgBox.setWindowTitle("Delete Link Actuator?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Components_Links.delete(list_links_actuator[pos])
            self.load_actuator_connections()
            self.load_controller_actions_connections()
            self.load_controller_variable_connections()

    def on_button_delete_sensor_connection_clicked(self):
        global list_connection_sensor, list_links_sensor
        pos = self.ui.listwidget_sensor_connection.currentRow()
        item = self.ui.listwidget_sensor_connection.currentItem()

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete: " + item.text() + "?")
        msgBox.setWindowTitle("Delete Link Sensor?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Components_Links.delete(list_links_sensor[pos])
            self.load_sensor_connections()
            self.load_controller_actions_connections()
            self.load_controller_variable_connections()

    def on_button_delete_controlled_process_connection_clicked(self):
        global list_connection_controlled_process, list_links_controlled_process
        pos = self.ui.listwidget_controlled_process_connection.currentRow()
        item = self.ui.listwidget_controlled_process_connection.currentItem()

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete: " + item.text() + "?")
        msgBox.setWindowTitle("Delete Link Controlled Process?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Components_Links.delete(list_links_controlled_process[pos])
            self.load_controlled_process_connections()
            self.load_controller_actions_connections()
            self.load_controller_variable_connections()

    def on_listwidget_controller_connection_clicked(self):
        self.ui.button_delete_controller_connection.setEnabled(True)

    def on_listwidget_exts_connection_clicked(self):
        self.ui.button_delete_exts_connection.setEnabled(True)

    def on_listwidget_actuator_connection_clicked(self):
        self.ui.button_delete_actuator_connection.setEnabled(True)

    def on_listwidget_sensor_connection_clicked(self):
        self.ui.button_delete_sensor_connection.setEnabled(True)

    def on_listwidget_controlled_process_connection_clicked(self):
        self.ui.button_delete_controlled_process_connection.setEnabled(True)

    def on_button_add_controller_connection_clicked(self):
        global list_component_controller, list_connection_controller, list_links_controller

        index = self.ui.combobox_controller_connection.currentIndex()
        pos = self.ui.listwidget_controllers.currentRow()

        for link in list_links_controller:
            if link.id_component_src == list_component_controller[pos].id and link.id_component_dst == \
                    list_connection_controller[index].id:
                showdialog("Attention", "This connection already exists.")
                return

        DB_Components_Links.insert(list_component_controller[pos].id, list_connection_controller[index].id)
        self.load_controller_connections()
        self.load_controller_actions_connections()
        self.load_controller_variable_connections()

    def on_button_add_exts_connection_clicked(self):
        global list_component_exts, list_connection_exts, list_links_exts

        index = self.ui.combobox_exts_connection.currentIndex()
        pos = self.ui.listwidget_exts.currentRow()

        for link in list_links_exts:
            if link.id_component_src == list_component_exts[pos].id and link.id_component_dst == list_connection_exts[
                index].id:
                showdialog("Attention", "This connection already exists.")
                return

        DB_Components_Links.insert(list_component_exts[pos].id, list_connection_exts[index].id)
        self.load_exts_connections()
        self.load_controller_actions_connections()
        self.load_controller_variable_connections()

    def on_button_add_actuator_connection_clicked(self):
        global list_component_actuator, list_connection_actuator, list_links_actuator

        index = self.ui.combobox_actuator_connection.currentIndex()
        pos = self.ui.listwidget_actuator.currentRow()

        for link in list_links_actuator:
            if link.id_component_src == list_component_actuator[pos].id and link.id_component_dst == \
                    list_connection_actuator[index].id:
                showdialog("Attention", "This connection already exists.")
                return

        DB_Components_Links.insert(list_component_actuator[pos].id, list_connection_actuator[index].id)
        self.load_actuator_connections()

        self.load_controller_actions_connections()
        self.load_controller_variable_connections()

    def on_button_add_sensor_connection_clicked(self):
        global list_component_sensor, list_connection_sensor, list_links_sensor

        index = self.ui.combobox_sensor_connection.currentIndex()
        pos = self.ui.listwidget_sensor.currentRow()

        for link in list_links_sensor:
            if link.id_component_src == list_component_sensor[pos].id and link.id_component_dst == \
                    list_connection_sensor[index].id:
                showdialog("Attention", "This connection already exists.")
                return

        DB_Components_Links.insert(list_component_sensor[pos].id, list_connection_sensor[index].id)
        self.load_sensor_connections()
        self.load_controller_actions_connections()
        self.load_controller_variable_connections()

    def on_button_add_controlled_process_connection_clicked(self):
        global list_component_controlled_process, list_connection_controlled_process, list_links_controlled_process

        index = self.ui.combobox_controlled_process_connection.currentIndex()

        for link in list_links_controlled_process:
            if link.id_component_src == list_component_controlled_process[0].id and link.id_component_dst == \
                    list_connection_controlled_process[index].id:
                showdialog("Attention", "This connection already exists.")
                return

        DB_Components_Links.insert(list_component_controlled_process[0].id,
                                   list_connection_controlled_process[index].id)
        self.load_controlled_process_connections()
        self.load_controller_actions_connections()
        self.load_controller_variable_connections()

    def load_component_controller(self):
        global list_component_controller, id_project
        list_component_controller = DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_CONTROLLER, id_project)

        self.ui.listwidget_controllers.clear()
        self.ui.combobox_second_controller.clear()
        self.ui.checkbox_controller_ext_of_analysis.setChecked(False)
        self.ui.checkbox_controller_human.setChecked(False)

        for pos in range(len(list_component_controller)):
            self.ui.listwidget_controllers.addItem(list_component_controller[pos].name)
            self.ui.combobox_second_controller.addItem(list_component_controller[pos].name)

        if len(list_component_controller) == 0:
            self.clean_control_action()
            self.clean_variables_values()
        else:
            self.selection_change_controller_connection()

    def disable_edit_controller(self):
        self.ui.button_add_controller.setEnabled(True)
        self.ui.button_update_controller.setEnabled(False)
        self.ui.button_delete_controller.setEnabled(False)
        self.ui.button_cancel_controller.setEnabled(False)
        self.ui.checkbox_controller_ext_of_analysis.setChecked(False)
        self.ui.checkbox_controller_human.setChecked(False)
        self.ui.lineedit_name_controller.setText("")

    def disable_new_controller(self):
        self.ui.button_add_controller.setEnabled(False)
        self.ui.button_update_controller.setEnabled(True)
        self.ui.button_delete_controller.setEnabled(True)
        self.ui.button_cancel_controller.setEnabled(True)

    def on_button_add_controller_clicked(self):
        global id_project, list_component_controller

        description = self.ui.lineedit_name_controller.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            if self.ui.checkbox_controller_ext_of_analysis.isChecked():
                is_ext_anl = 1
            else:
                is_ext_anl = 0

            if self.ui.checkbox_controller_human.isChecked():
                is_human = 1
            else:
                is_human = 0

            comp = Component(0, Constant.DB_ID_CONTROLLER, id_project, description, current_date, current_date, 0, is_ext_anl, is_human)
            DB_Components.insert_controller(comp)

            if self.ui.listwidget_sensor_connection.isEnabled():
                self.load_sensor_connections()

            if self.ui.listwidget_exts_connection.isEnabled():
                self.load_exts_connections()

            if self.ui.listwidget_controlled_process_connection.isEnabled():
                self.load_controlled_process_connections()

            self.load_component_controller()
            self.ui.lineedit_name_controller.setText("")

    def on_button_update_controller_clicked(self):
        global id_project, list_component_controller

        name = self.ui.lineedit_name_controller.text()
        if len(name) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            pos = self.ui.listwidget_controllers.currentRow()
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            comp = list_component_controller[pos]
            comp.name = name
            comp.edited_date = current_date

            if self.ui.checkbox_controller_ext_of_analysis.isChecked():
                comp.is_external_component = 1
            else:
                comp.is_external_component = 0

            if self.ui.checkbox_controller_human.isChecked():
                comp.is_human = 1
            else:
                comp.is_human = 0

            DB_Components.update_component_controller(comp)

            self.disable_edit_controller()
            self.load_component_controller()
            self.disable_edit_controller()
            self.disable_controller_connections()

            if self.ui.listwidget_sensor_connection.isEnabled():
                self.load_sensor_connections()

            if self.ui.listwidget_exts_connection.isEnabled():
                self.load_exts_connections()

            if self.ui.listwidget_controlled_process_connection.isEnabled():
                self.load_controlled_process_connections()

    def on_button_delete_controller_clicked(self):
        global list_component_controller
        pos = self.ui.listwidget_controllers.currentRow()
        comp = list_component_controller[pos]

        delete_report = DB_Components.delete_report(comp.id)
        message = "Are you sure that you want delete the controller: " + comp.name + "?"

        if len(delete_report) > 0:
            message += "\nThis controller is related to: "
            for text in delete_report:
                message += "\n" + text

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(message)
        msgBox.setWindowTitle("Delete Controller?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Components.delete_controller(comp)
            self.load_component_controller()
            self.ui.lineedit_name_controller.setText("")
            self.disable_edit_controller()
            self.disable_controller_connections()

            if self.ui.listwidget_sensor_connection.isEnabled():
                self.load_sensor_connections()

            if self.ui.listwidget_exts_connection.isEnabled():
                self.load_exts_connections()

            if self.ui.listwidget_controlled_process_connection.isEnabled():
                self.load_controlled_process_connections()

            self.load_controller_connections()

    def on_button_cancel_controller_clicked(self):
        self.disable_edit_controller()
        self.ui.lineedit_name_controller.setText("")
        self.disable_controller_connections()
        # self.disable_controller_actions_variables()
        self.ui.listwidget_controllers.clearSelection()
        self.ui.listwidget_controllers.selectionModel().clear()
        self.ui.checkbox_controller_ext_of_analysis.setChecked(False)
        self.ui.checkbox_controller_human.setChecked(False)

    def load_controller_connections(self):
        global list_component_controller, list_connection_controller, list_links_controller, id_project
        pos = self.ui.listwidget_controllers.currentRow()

        if pos < 0:
            return

        list_links_controller = DB_Components_Links.select_component_links_by_project_and_component(list_component_controller[pos].id, True)
        self.ui.listwidget_controller_connection.clear()
        self.disable_edit_controller_connections()

        for link in list_links_controller:
            self.ui.listwidget_controller_connection.addItem(link.name_src + " -> " + link.name_dst)

        list_of_things = General_tools.find_individuals_of_class_return_idThing(onto, Constant.LINK, "Link_controller_")
        list_connection_controller = DB_Components.select_components_to_link_with_controller(id_project,
                                                                                             list_component_controller[
                                                                                                 pos].id,
                                                                                             list_of_things)
        self.ui.combobox_controller_connection.clear()
        for conn in list_connection_controller:
            self.ui.combobox_controller_connection.addItem(conn.name)

    def load_exts_connections(self):
        global list_component_exts, list_connection_exts, list_links_exts
        pos = self.ui.listwidget_exts.currentRow()

        if pos < 0:
            return

        list_links_exts = DB_Components_Links.select_component_links_by_project_and_component(
            list_component_exts[pos].id, True)
        self.ui.listwidget_exts_connection.clear()
        self.disable_edit_exts_connections()

        for link in list_links_exts:
            self.ui.listwidget_exts_connection.addItem(link.name_src + " -> " + link.name_dst)

        list_of_things = General_tools.find_individuals_of_class_return_idThing(onto, Constant.LINK,
                                                                                "Link_External-information_")
        list_connection_exts = DB_Components.select_components_to_link_with_controller(id_project,
                                                                                       list_component_exts[pos].id,
                                                                                       list_of_things)
        self.ui.combobox_exts_connection.clear()
        for conn in list_connection_exts:
            self.ui.combobox_exts_connection.addItem(conn.name)

    def load_actuator_connections(self):
        global list_component_actuator, list_connection_actuator, list_links_actuator

        pos = self.ui.listwidget_actuator.currentRow()

        if pos < 0:
            return

        list_links_actuator = DB_Components_Links.select_component_links_by_project_and_component(
            list_component_actuator[pos].id, True)
        self.ui.listwidget_actuator_connection.clear()
        self.disable_edit_actuator_connections()

        for link in list_links_actuator:
            self.ui.listwidget_actuator_connection.addItem(link.name_src + " -> " + link.name_dst)

        list_of_things = General_tools.find_individuals_of_class_return_idThing(onto, Constant.LINK, "Link_actuator_")
        list_connection_actuator = DB_Components.select_components_to_link_with_controller(id_project,
                                                                                           list_component_actuator[
                                                                                               pos].id, list_of_things)
        self.ui.combobox_actuator_connection.clear()
        for conn in list_connection_actuator:
            self.ui.combobox_actuator_connection.addItem(conn.name)

    def load_sensor_connections(self):
        global list_component_sensor, list_connection_sensor, list_links_sensor
        pos = self.ui.listwidget_sensor.currentRow()

        if pos < 0:
            return

        list_links_sensor = DB_Components_Links.select_component_links_by_project_and_component(
            list_component_sensor[pos].id, True)
        self.ui.listwidget_sensor_connection.clear()
        self.disable_edit_sensor_connections()

        for link in list_links_sensor:
            self.ui.listwidget_sensor_connection.addItem(link.name_src + " -> " + link.name_dst)

        list_of_things = General_tools.find_individuals_of_class_return_idThing(onto, Constant.LINK, "Link_sensor_")
        list_connection_sensor = DB_Components.select_components_to_link_with_controller(id_project,
                                                                                         list_component_sensor[pos].id,
                                                                                         list_of_things)
        self.ui.combobox_sensor_connection.clear()
        for conn in list_connection_sensor:
            self.ui.combobox_sensor_connection.addItem(conn.name)

    def load_controlled_process_connections(self):
        global list_component_controlled_process, list_connection_controlled_process, list_links_controlled_process

        if len(list_component_controlled_process) == 0:
            return

        list_links_controlled_process = DB_Components_Links.select_component_links_by_project_and_component(list_component_controlled_process[0].id, True)
        self.ui.listwidget_controlled_process_connection.clear()
        self.disable_edit_controlled_process_connections()

        for link in list_links_controlled_process:
            self.ui.listwidget_controlled_process_connection.addItem(link.name_src + " -> " + link.name_dst)

        list_of_things = General_tools.find_individuals_of_class_return_idThing(onto, Constant.LINK, "Link_CP_")
        list_connection_controlled_process = DB_Components.select_components_to_link_with_controller(id_project,
                                                                                                     list_component_controlled_process[
                                                                                                         0].id,
                                                                                                     list_of_things)
        self.ui.combobox_controlled_process_connection.clear()
        for conn in list_connection_controlled_process:
            self.ui.combobox_controlled_process_connection.addItem(conn.name)

    def disable_edit_controller_connections(self):
        self.ui.combobox_controller_connection.setEnabled(True)
        self.ui.button_add_controller_connection.setEnabled(True)
        self.ui.button_delete_controller_connection.setEnabled(False)
        self.ui.listwidget_controller_connection.setEnabled(True)

    def disable_edit_exts_connections(self):
        self.ui.combobox_exts_connection.setEnabled(True)
        self.ui.button_add_exts_connection.setEnabled(True)
        self.ui.button_delete_exts_connection.setEnabled(False)
        self.ui.listwidget_exts_connection.setEnabled(True)

    def disable_edit_actuator_connections(self):
        self.ui.combobox_actuator_connection.setEnabled(True)
        self.ui.button_add_actuator_connection.setEnabled(True)
        self.ui.button_delete_actuator_connection.setEnabled(False)
        self.ui.listwidget_actuator_connection.setEnabled(True)

    def disable_edit_sensor_connections(self):
        self.ui.combobox_sensor_connection.setEnabled(True)
        self.ui.button_add_sensor_connection.setEnabled(True)
        self.ui.button_delete_sensor_connection.setEnabled(False)
        self.ui.listwidget_sensor_connection.setEnabled(True)

    def disable_edit_controlled_process_connections(self):
        print()
        self.ui.combobox_controlled_process_connection.setEnabled(True)
        self.ui.button_add_controlled_process_connection.setEnabled(True)
        self.ui.button_delete_controlled_process_connection.setEnabled(False)
        self.ui.listwidget_controlled_process_connection.setEnabled(True)

    def on_listwidget_controllers_clicked(self):
        global list_component_controller, id_project
        item = self.ui.listwidget_controllers.currentItem()
        pos = self.ui.listwidget_controllers.currentRow()

        if pos >= 0:
            item.setSelected(True)
            self.disable_new_controller()
            self.ui.lineedit_name_controller.setText(list_component_controller[pos].name)

            if list_component_controller[pos].is_external_component == 1:
                self.ui.checkbox_controller_ext_of_analysis.setChecked(True)
            else:
                self.ui.checkbox_controller_ext_of_analysis.setChecked(False)

            if list_component_controller[pos].is_human == 1:
                self.ui.checkbox_controller_human.setChecked(True)
            else:
                self.ui.checkbox_controller_human.setChecked(False)

            self.load_controller_connections()

    def disable_new_control_action(self):
        self.ui.button_add_control_action.setEnabled(False)
        self.ui.button_update_control_action.setEnabled(True)
        self.ui.button_delete_control_action.setEnabled(True)
        self.ui.button_cancel_control_action.setEnabled(True)

    def disable_edit_control_action(self):
        self.ui.lineedit_name_control_action.setText("")
        self.ui.button_add_control_action.setEnabled(True)
        self.ui.button_update_control_action.setEnabled(False)
        self.ui.button_delete_control_action.setEnabled(False)
        self.ui.button_cancel_control_action.setEnabled(False)
        self.ui.lineedit_name_control_action.setEnabled(True)
        self.ui.listwidget_control_actions.setEnabled(True)
        self.ui.listwidget_second_links_act.setEnabled(True)

    def disable_new_controller_variable(self):
        self.ui.button_add_controller_variable.setEnabled(False)
        self.ui.button_update_controller_variable.setEnabled(True)
        self.ui.button_delete_controller_variable.setEnabled(True)
        self.ui.button_cancel_controller_variable.setEnabled(True)
        self.ui.lineedit_name_control_action.setEnabled(True)
        self.ui.listwidget_control_actions.setEnabled(True)
        self.ui.listwidget_second_links_var.setEnabled(True)

    def disable_edit_controller_variable(self):
        self.ui.lineedit_name_controller_variable.setText("")
        self.ui.button_add_controller_variable.setEnabled(True)
        self.ui.button_update_controller_variable.setEnabled(False)
        self.ui.button_delete_controller_variable.setEnabled(False)
        self.ui.button_cancel_controller_variable.setEnabled(False)
        self.ui.lineedit_name_controller_variable.setEnabled(True)
        self.ui.listwidget_controller_variable.setEnabled(True)
        self.ui.listwidget_second_links_var.setEnabled(True)

    def clean_control_action(self):
        self.ui.button_add_control_action.setEnabled(False)
        self.ui.button_update_control_action.setEnabled(False)
        self.ui.button_delete_control_action.setEnabled(False)
        self.ui.button_cancel_control_action.setEnabled(False)
        self.ui.listwidget_control_actions.clear()
        self.ui.listwidget_control_actions.setEnabled(False)
        self.ui.lineedit_name_control_action.setEnabled(False)
        self.ui.lineedit_name_control_action.setText("")

    def selection_change_controller_connection(self):
        self.load_controller_control_actions()
        self.load_component_controller_variables()
        self.disable_edit_controller_variable()
        self.disable_edit_control_action()

    def on_button_add_control_action_clicked(self):
        global id_project, list_control_actions, list_component_controller, list_links_actions_controller

        description = self.ui.lineedit_name_control_action.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
            return

        pos_c = self.ui.combobox_second_controller.currentIndex()
        if pos_c < 0:
            return

        list_link_to_verify = []
        for item in self.ui.listwidget_second_links_act.selectedItems():
            pos = self.ui.listwidget_second_links_act.row(item)
            list_link_to_verify.append(list_links_actions_controller[pos])

        list_feedback = DB_Components_Links.select_all_control_actions_in_link(list_link_to_verify);
        if len(list_feedback) > 0:
            if len(list_feedback) == 1:
                msg = "There is a conflict that must be solved before do this action: \n"
            else:
                msg = "There some conflicts that must be solved before do this action: \n"

            for m_a in list_feedback:
                msg += m_a + "\n"

            showdialog("Action not allowed!", msg)
            return

        now = datetime.now()
        current_date = now.strftime(Constant.DATETIME_MASK)

        act = Action_Component(0, list_component_controller[pos_c].id, description, current_date, current_date,
                               id_project)
        id_last_var = DB_Actions_Components.insert_to_table(act)

        if id_last_var > 0:
            for item in self.ui.listwidget_second_links_act.selectedItems():
                pos = self.ui.listwidget_second_links_act.row(item)
                link_id = list_links_actions_controller[pos].id
                DB_Components_Links.insert_link_act(id_last_var, link_id)

        self.load_controller_control_actions()
        self.ui.lineedit_name_control_action.setText("")

    def on_button_update_control_action_clicked(self):
        global id_project, list_control_actions, list_links_actions_controller

        description = self.ui.lineedit_name_control_action.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
            return

        list_link_to_verify = []
        for item in self.ui.listwidget_second_links_act.selectedItems():
            pos = self.ui.listwidget_second_links_act.row(item)
            list_link_to_verify.append(list_links_actions_controller[pos])

        list_feedback = DB_Components_Links.select_all_control_actions_in_link(list_link_to_verify);
        if len(list_feedback) > 0:
            if len(list_feedback) == 1:
                msg = "There is a conflict that must be solved before do this action: \n"
            else:
                msg = "There some conflicts that must be solved before do this action: \n"

            for m_a in list_feedback:
                msg += "- " + m_a + "\n"

            showdialog("Action not allowed!", msg)
            return

        now = datetime.now()
        current_date = now.strftime(Constant.DATETIME_MASK)
        pos = self.ui.listwidget_control_actions.currentRow()

        act = list_control_actions[pos]
        act.name = description
        act.edite_date = current_date
        DB_Actions_Components.update(act)

        index_list = self.ui.listwidget_second_links_act.selectedItems()
        DB_Components_Links.delete_link_act(act.id)

        for item in index_list:
            pos = self.ui.listwidget_second_links_act.row(item)
            link_id = list_links_actions_controller[pos].id
            DB_Components_Links.insert_link_act(act.id, link_id)

        self.load_controller_control_actions()
        self.ui.lineedit_name_control_action.setText("")

    def on_button_delete_control_action_clicked(self):
        global list_control_actions
        pos = self.ui.listwidget_control_actions.currentRow()
        act = list_control_actions[pos]

        list_id_uca = DB_UCA.select_id_uca_by_control_action(act.id)

        text_delete = "You are deleting " + act.name + "?"

        if len(list_id_uca) > 0:
            cout_req = 0
            for uca_id in list_id_uca:
                cout_req += len(DB_Loss_Scenario_Req.select_id_requirement_by_uca(uca_id))

            text_delete += "\nIf you delete this Control Action, you will lost " + str(
                len(list_id_uca)) + " related UCA."
            text_delete += "\nThis Control Action is related with " + str(cout_req) + " requirements."

        text_delete += "\nDo you want to proceed?"

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text_delete)
        msgBox.setWindowTitle("Delete Control Action")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Actions_Components.delete(act)
            self.load_controller_control_actions()
            self.ui.lineedit_name_control_action.setText("")
            self.disable_edit_control_action()

    def on_button_cancel_control_action_clicked(self):
        self.disable_edit_control_action()
        self.ui.lineedit_name_control_action.setText("")
        self.ui.listwidget_control_actions.selectionModel().clear()
        self.ui.listwidget_control_actions.clearSelection()
        self.ui.listwidget_second_links_act.selectionModel().clear()
        self.ui.listwidget_second_links_act.clearSelection()

    def on_listwidget_control_action_clicked(self):
        global list_control_actions, id_project
        item = self.ui.listwidget_control_actions.currentItem()
        pos = self.ui.listwidget_control_actions.currentRow()

        if pos >= 0:
            item.setSelected(True)
            self.disable_new_control_action()
            self.ui.lineedit_name_control_action.setText(list_control_actions[pos].name)
            self.load_controller_actions_connections()

    def clean_variables(self):
        self.ui.button_add_controller_variable.setEnabled(False)
        self.ui.button_update_controller_variable.setEnabled(False)
        self.ui.button_delete_controller_variable.setEnabled(False)
        self.ui.button_cancel_controller_variable.setEnabled(False)
        self.ui.listwidget_controller_variable.clear()
        self.ui.listwidget_controller_variable.setEnabled(False)
        self.ui.lineedit_name_controller_variable.setEnabled(False)
        self.ui.listwidget_second_links_act.clear()
        self.ui.listwidget_second_links_var.clear()
        self.ui.listwidget_second_links_act.setEnabled(False)
        self.ui.listwidget_second_links_var.setEnabled(False)
        self.ui.lineedit_name_controller_variable.setText("")

    def clean_variables_values(self):
        self.ui.button_add_controller_variable_values.setEnabled(False)
        self.ui.button_update_controller_variable_values.setEnabled(False)
        self.ui.button_delete_controller_variable_values.setEnabled(False)
        self.ui.button_cancel_controller_variable_values.setEnabled(False)
        self.ui.listwidget_controller_variable_values.clear()
        self.ui.listwidget_controller_variable_values.setEnabled(False)
        self.ui.lineedit_name_controller_variable_values.setEnabled(False)
        self.ui.lineedit_name_controller_variable_values.setText("")
        self.ui.listwidget_second_links_act.clearSelection()
        self.ui.listwidget_second_links_act.selectionModel().clear()
        self.ui.listwidget_second_links_var.clearSelection()
        self.ui.listwidget_second_links_var.selectionModel().clear()

    def disable_new_controller_variable_values(self):
        self.ui.button_add_controller_variable_values.setEnabled(False)
        self.ui.button_update_controller_variable_values.setEnabled(True)
        self.ui.button_delete_controller_variable_values.setEnabled(True)
        self.ui.button_cancel_controller_variable_values.setEnabled(True)

    def disable_edit_controller_variable_values(self):
        self.ui.lineedit_name_controller_variable_values.setText("")
        self.ui.lineedit_name_controller_variable_values.setEnabled(True)
        self.ui.listwidget_controller_variable_values.setEnabled(True)
        self.ui.button_add_controller_variable_values.setEnabled(True)
        self.ui.button_update_controller_variable_values.setEnabled(False)
        self.ui.button_delete_controller_variable_values.setEnabled(False)
        self.ui.button_cancel_controller_variable_values.setEnabled(False)

    def on_button_add_controller_variable_clicked(self):
        global id_project, list_component_controller_variables, list_component_controller

        description = self.ui.lineedit_name_controller_variable.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            pos_c = self.ui.combobox_second_controller.currentIndex()

            var = Variables(0, list_component_controller[pos_c].id, id_project, description, current_date, current_date)
            id_last_var = DB_Variables.insert(var)

            for item in self.ui.listwidget_second_links_var.selectedItems():
                pos = self.ui.listwidget_second_links_var.row(item)
                link_id = list_links_variable_controller[pos].id
                DB_Components_Links.insert_link_var(id_last_var, link_id)

            self.ui.lineedit_name_controller_variable.setText("")
            self.load_component_controller_variables()

    def on_button_update_controller_variable_clicked(self):
        global id_project, list_component_controller_variables, list_component_controller, list_links_variable_controller

        description = self.ui.lineedit_name_controller_variable.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            pos = self.ui.listwidget_controller_variable.currentRow()

            var = list_component_controller_variables[pos]
            var.name = description
            var.edited_date = current_date
            DB_Variables.update(var)

            index_list = self.ui.listwidget_second_links_var.selectedItems()
            DB_Components_Links.delete_link_var(var.id)

            for item in index_list:
                pos = self.ui.listwidget_second_links_var.row(item)
                link_id = list_links_variable_controller[pos].id
                DB_Components_Links.insert_link_var(var.id, link_id)

            # self.ui.lineedit_name_controller_variable.setText("")
            # self.disable_edit_controller_variable()
            self.load_component_controller_variables()

    def on_button_delete_controller_variable_clicked(self):
        global list_component_controller_variables
        pos = self.ui.listwidget_controller_variable.currentRow()
        var = list_component_controller_variables[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete variable: " + var.name + "?")
        msgBox.setWindowTitle("Delete Variable?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Variables.delete(var)
            DB_Components_Links.delete_link_var(var.id)
            self.ui.lineedit_name_controller_variable.setText("")
            self.disable_edit_controller_variable()
            self.load_component_controller_variables()
        self.clean_variables_values()

    def on_button_cancel_controller_variable_clicked(self):
        self.disable_edit_controller_variable()
        self.ui.lineedit_name_controller_variable.setText("")
        self.ui.listwidget_controller_variable.selectionModel().clear()
        self.ui.listwidget_controller_variable.clearSelection()
        self.clean_variables_values()

    def on_listwidget_controller_variable_clicked(self):
        global list_component_controller_variables, id_project, list_links_variable_controller
        pos_var = self.ui.listwidget_controller_variable.currentRow()
        self.ui.listwidget_second_links_var.clearSelection()
        self.ui.listwidget_second_links_var.selectionModel().clear()
        item = self.ui.listwidget_controller_variable.currentItem()

        if pos_var >= 0:
            item.setSelected(True)
            self.disable_new_controller_variable()
            self.ui.lineedit_name_controller_variable.setText(list_component_controller_variables[pos_var].name)
            self.load_component_controller_variables_values()
            self.load_controller_variable_connections()

    def load_controller_variable_connections(self):
        global list_component_controller, list_links_variable_controller, id_project, list_component_controller_variables
        pos = self.ui.combobox_second_controller.currentIndex()
        self.ui.listwidget_second_links_var.clear()

        if len(list_component_controller) == 0:
            return

        list_links_variable_controller = DB_Components_Links.select_all_component_links_feedback_by_component(list_component_controller[pos].id)

        for link in list_links_variable_controller:
            self.ui.listwidget_second_links_var.addItem(link.name_src + " -> " + link.name_dst)

        pos_var = self.ui.listwidget_controller_variable.currentRow()
        if pos_var >= 0:
            list_var_link = DB_Components_Links.select_var_link(list_component_controller_variables[pos_var].id)
            count = 0

            for link in list_links_variable_controller:
                for vl in list_var_link:
                    if link.id == vl.id_link:
                        self.ui.listwidget_second_links_var.item(count).setSelected(True)
                count += 1

    def load_controller_actions_connections(self):
        global list_component_controller, list_links_actions_controller, id_project, list_control_actions
        pos = self.ui.combobox_second_controller.currentIndex()
        list_links_actions_controller = DB_Components_Links.select_all_component_links_actions_by_component(
            list_component_controller[pos].id)
        self.ui.listwidget_second_links_act.clear()

        for link in list_links_actions_controller:
            self.ui.listwidget_second_links_act.addItem(link.name_src + " -> " + link.name_dst)

        pos_var = self.ui.listwidget_control_actions.currentRow()
        if pos_var >= 0:
            list_act_link = DB_Components_Links.select_act_link(list_control_actions[pos_var].id)
            count = 0

            for link in list_links_actions_controller:
                for vl in list_act_link:
                    if link.id == vl.id_link:
                        self.ui.listwidget_second_links_act.item(count).setSelected(True)
                count += 1

    def load_component_controller_variables_values(self):
        global list_component_controller_variables, list_component_controller_variables_values, id_project
        pos_var = self.ui.listwidget_controller_variable.currentRow()

        list_component_controller_variables_values = DB_Variables_Values.select_values_by_variable(
            list_component_controller_variables[pos_var].id)

        self.ui.listwidget_controller_variable_values.clear()
        for val in list_component_controller_variables_values:
            self.ui.listwidget_controller_variable_values.addItem(val.value)
        self.disable_edit_controller_variable_values()

    def on_button_add_controller_variable_values_clicked(self):
        global id_project, list_component_controller_variables_values, list_component_controller_variables, list_component_controller

        description = self.ui.lineedit_name_controller_variable_values.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            pos_var = self.ui.listwidget_controller_variable.currentRow()

            var = Variable_Values(0, list_component_controller_variables[pos_var].id, description, current_date,
                                  current_date)

            DB_Variables_Values.insert(var)

            self.load_component_controller_variables_values()
            self.ui.lineedit_name_controller_variable_values.setText("")

    def on_button_update_controller_variable_values_clicked(self):
        global id_project, list_component_controller_variables_values, list_component_controller

        description = self.ui.lineedit_name_controller_variable_values.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            pos = self.ui.listwidget_controller_variable_values.currentRow()

            val = list_component_controller_variables_values[pos]
            val.value = description
            val.edited_date = current_date
            DB_Variables_Values.update(val)

            self.load_component_controller_variables_values()
            self.ui.lineedit_name_controller_variable_values.setText("")
            self.disable_edit_controller_variable_values()
            self.ui.listwidget_controller_variable_values.selectionModel().clear()
            self.ui.listwidget_controller_variable_values.clearSelection()

    def on_button_delete_controller_variable_values_clicked(self):
        global list_component_controller_variables_values
        pos = self.ui.listwidget_controller_variable_values.currentRow()
        val = list_component_controller_variables_values[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete value: " + val.value + "?")
        msgBox.setWindowTitle("Delete Value?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Variables_Values.delete(val)
            self.load_component_controller_variables_values()
            self.ui.lineedit_name_controller_variable_values.setText("")
            self.disable_edit_controller_variable_values()
            self.ui.listwidget_controller_variable_values.clearSelection()
            self.ui.listwidget_controller_variable_values.selectionModel().clear()

    def on_button_cancel_controller_variable_values_clicked(self):
        self.disable_edit_controller_variable_values()
        self.ui.lineedit_name_controller_variable_values.setText("")
        self.ui.listwidget_controller_variable_values.selectionModel().clear()
        self.ui.listwidget_controller_variable_values.clearSelection()

    def on_listwidget_controller_variable_values_clicked(self):
        global list_component_controller_variables_values, id_project
        pos_var = self.ui.listwidget_controller_variable_values.currentRow()
        item = self.ui.listwidget_controller_variable_values.currentItem()

        if pos_var >= 0:
            item.setSelected(True)
            self.disable_new_controller_variable_values()
            self.ui.lineedit_name_controller_variable_values.setText(
                list_component_controller_variables_values[pos_var].value)

    def disable_controller_connections(self):
        self.ui.combobox_controller_connection.setEnabled(False)
        self.ui.button_add_controller_connection.setEnabled(False)
        self.ui.button_delete_controller_connection.setEnabled(False)
        self.ui.listwidget_controller_connection.setEnabled(False)
        self.ui.listwidget_controller_connection.clear()
        self.ui.combobox_controller_connection.clear()

    def disable_exts_connections(self):
        self.ui.combobox_exts_connection.setEnabled(False)
        self.ui.button_add_exts_connection.setEnabled(False)
        self.ui.button_delete_exts_connection.setEnabled(False)
        self.ui.listwidget_exts_connection.setEnabled(False)

        self.ui.combobox_exts_connection.clear()
        self.ui.listwidget_exts_connection.clear()

    def disable_actuator_connections(self):
        self.ui.combobox_actuator_connection.setEnabled(False)
        self.ui.button_add_actuator_connection.setEnabled(False)
        self.ui.button_delete_actuator_connection.setEnabled(False)
        self.ui.listwidget_actuator_connection.setEnabled(False)

        self.ui.combobox_actuator_connection.clear()
        self.ui.listwidget_actuator_connection.clear()

    def disable_sensor_connections(self):
        self.ui.combobox_sensor_connection.setEnabled(False)
        self.ui.button_add_sensor_connection.setEnabled(False)
        self.ui.button_delete_sensor_connection.setEnabled(False)
        self.ui.listwidget_sensor_connection.setEnabled(False)

        self.ui.combobox_sensor_connection.clear()
        self.ui.listwidget_sensor_connection.clear()

    def disable_controlled_process_connections(self):
        self.ui.combobox_controlled_process_connection.setEnabled(False)
        self.ui.button_add_controlled_process_connection.setEnabled(False)
        self.ui.button_delete_controlled_process_connection.setEnabled(False)
        self.ui.listwidget_controlled_process_connection.setEnabled(False)

        self.ui.combobox_controlled_process_connection.clear()
        self.ui.listwidget_controlled_process_connection.clear()

    def disable_controller_actions_variables(self):
        self.ui.lineedit_name_control_action.setEnabled(False)
        self.ui.lineedit_name_control_action.setText("")
        self.ui.button_add_control_action.setEnabled(False)
        self.ui.button_update_control_action.setEnabled(False)
        self.ui.button_delete_control_action.setEnabled(False)
        self.ui.button_cancel_control_action.setEnabled(False)
        self.ui.listwidget_control_actions.setEnabled(False)
        self.ui.listwidget_control_actions.clear()
        self.ui.lineedit_name_controller_variable.setEnabled(False)
        self.ui.lineedit_name_controller_variable.setText("")
        self.ui.button_add_controller_variable.setEnabled(False)
        self.ui.button_update_controller_variable.setEnabled(False)
        self.ui.button_delete_controller_variable.setEnabled(False)
        self.ui.button_cancel_controller_variable.setEnabled(False)
        self.ui.listwidget_controller_variable.setEnabled(False)
        self.ui.listwidget_controller_variable.clear()
        self.ui.lineedit_name_controller_variable_values.setEnabled(False)
        self.ui.lineedit_name_controller_variable_values.setText("")
        self.ui.button_add_controller_variable_values.setEnabled(False)
        self.ui.button_update_controller_variable_values.setEnabled(False)
        self.ui.button_delete_controller_variable_values.setEnabled(False)
        self.ui.button_cancel_controller_variable_values.setEnabled(False)
        self.ui.listwidget_controller_variable_values.setEnabled(False)
        self.ui.listwidget_controller_variable_values.clear()
        self.ui.listwidget_second_links_act.setEnabled(False)
        self.ui.listwidget_second_links_act.clear()
        self.ui.listwidget_second_links_var.setEnabled(False)
        self.ui.listwidget_second_links_var.clear()

    def load_component_actuator(self):
        global list_component_actuator, id_project
        list_component_actuator = DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_ACTUATOR,
                                                                                           id_project)

        self.ui.listwidget_actuator.clear()
        for pos in range(len(list_component_actuator)):
            self.ui.listwidget_actuator.addItem(list_component_actuator[pos].name)

    def disable_edit_actuator(self):
        self.ui.button_add_actuator.setEnabled(True)
        self.ui.button_update_actuator.setEnabled(False)
        self.ui.button_delete_actuator.setEnabled(False)
        self.ui.button_cancel_actuator.setEnabled(False)
        self.ui.lineedit_name_actuator.setText("")

    def disable_new_actuator(self):
        self.ui.button_add_actuator.setEnabled(False)
        self.ui.button_update_actuator.setEnabled(True)
        self.ui.button_delete_actuator.setEnabled(True)
        self.ui.button_cancel_actuator.setEnabled(True)

    def on_button_add_actuator_clicked(self):
        global id_project, list_component_actuator

        description = self.ui.lineedit_name_actuator.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            comp = Component(0, Constant.DB_ID_ACTUATOR, id_project, description, current_date, current_date)
            DB_Components.insert_to_table(comp)

            if self.ui.listwidget_controller_connection.isEnabled():
                self.load_controller_connections()

            self.load_component_actuator()
            self.ui.lineedit_name_actuator.setText("")

    def on_button_update_actuator_clicked(self):
        global list_component_actuator

        name = self.ui.lineedit_name_actuator.text()
        if len(name) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            pos = self.ui.listwidget_actuator.currentRow()
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            comp = list_component_actuator[pos]
            comp.name = name
            comp.edited_date = current_date

            DB_Components.update_component(comp)

            self.disable_edit_actuator()
            self.load_component_actuator()
            self.disable_edit_actuator()
            self.disable_actuator_connections()

            if self.ui.listwidget_controller_connection.isEnabled():
                self.load_controller_connections()

    def on_button_delete_actuator_clicked(self):
        global list_component_actuator
        pos = self.ui.listwidget_actuator.currentRow()
        act = list_component_actuator[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete: " + act.name + "?")
        msgBox.setWindowTitle("Delete Actuator?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Components.delete(act)

            self.disable_edit_actuator()
            self.load_component_actuator()
            self.ui.lineedit_name_actuator.setText("")
            self.ui.listwidget_actuator.clearSelection()
            self.ui.listwidget_actuator.selectionModel().clear()
            self.disable_edit_actuator()
            self.disable_actuator_connections()

            if self.ui.listwidget_controller_connection.isEnabled():
                self.load_controller_connections()

    def on_button_cancel_actuator_clicked(self):
        self.disable_edit_actuator()
        self.ui.lineedit_name_actuator.setText("")
        self.ui.listwidget_actuator.selectionModel().clear()
        self.ui.listwidget_actuator.clearSelection()
        self.disable_actuator_connections()
        self.disable_edit_actuator()

    def on_listwidget_actuators_clicked(self):
        global list_component_actuator
        item = self.ui.listwidget_actuator.currentItem()
        pos = self.ui.listwidget_actuator.currentRow()

        self.disable_new_actuator()

        if pos >= 0:
            item.setSelected(True)
            self.ui.lineedit_name_actuator.setText(list_component_actuator[pos].name)
            self.load_actuator_connections()

    def load_component_exts(self):
        global list_component_exts, id_project
        list_component_exts = DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_EXT_INFORMATION,
                                                                                       id_project)

        self.ui.listwidget_exts.clear()
        for pos in range(len(list_component_exts)):
            self.ui.listwidget_exts.addItem(list_component_exts[pos].name)

    def disable_edit_exts(self):
        self.ui.button_add_exts.setEnabled(True)
        self.ui.button_update_exts.setEnabled(False)
        self.ui.button_delete_exts.setEnabled(False)
        self.ui.button_cancel_exts.setEnabled(False)
        self.ui.lineedit_name_exts.setText("")

    def disable_new_exts(self):
        self.ui.button_add_exts.setEnabled(False)
        self.ui.button_update_exts.setEnabled(True)
        self.ui.button_delete_exts.setEnabled(True)
        self.ui.button_cancel_exts.setEnabled(True)

    def on_button_add_exts_clicked(self):
        global id_project, list_component_exts

        description = self.ui.lineedit_name_exts.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
            return

        now = datetime.now()
        current_date = now.strftime(Constant.DATETIME_MASK)

        comp = Component(0, Constant.DB_ID_EXT_INFORMATION, id_project, description, current_date, current_date)
        result = DB_Components.insert_to_table(comp)

        if result > 0:
            self.load_controller_actions_connections()
            self.load_controller_variable_connections()
            self.load_component_exts()
            self.ui.lineedit_name_exts.setText("")

            if self.ui.listwidget_controller_connection.isEnabled():
                self.load_controller_connections()

        else:
            showdialog("Error to create External System",
                       "Something goes wrong during the creation of External System. Try again...")

    def on_button_update_exts_clicked(self):
        global list_component_exts

        name = self.ui.lineedit_name_exts.text()
        if len(name) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            pos = self.ui.listwidget_exts.currentRow()
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            comp = list_component_exts[pos]
            comp.name = name
            comp.edited_date = current_date

            DB_Components.update_component(comp)

            self.disable_edit_exts()
            self.load_component_exts()
            self.ui.lineedit_name_exts.setText("")
            self.ui.listwidget_exts.clearSelection()
            self.ui.listwidget_exts.selectionModel().clear()
            self.disable_edit_exts()
            self.disable_exts_connections()

            if self.ui.listwidget_controller_connection.isEnabled():
                self.load_controller_connections()

    def on_button_delete_exts_clicked(self):
        global list_component_exts
        pos = self.ui.listwidget_exts.currentRow()
        act = list_component_exts[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete: " + act.name + "?")
        msgBox.setWindowTitle("Delete Actuator?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Components.delete(act)
            self.disable_edit_exts()
            self.load_component_exts()
            self.ui.lineedit_name_exts.setText("")
            self.load_component_exts()
            self.ui.listwidget_exts.clearSelection()
            self.ui.listwidget_exts.selectionModel().clear()
            self.disable_edit_exts()
            self.disable_exts_connections()

            if self.ui.listwidget_controller_connection.isEnabled():
                self.load_controller_connections()

    def on_button_cancel_exts_clicked(self):
        self.disable_edit_exts()
        self.ui.lineedit_name_exts.setText("")
        self.ui.listwidget_exts.selectionModel().clear()
        self.ui.listwidget_exts.clearSelection()
        self.disable_exts_connections()

    def on_listwidget_exts_clicked(self):
        global list_component_exts
        pos = self.ui.listwidget_exts.currentRow()
        item = self.ui.listwidget_exts.currentItem()

        if pos >= 0:
            self.disable_new_exts()
            item.setSelected(True)
            self.ui.lineedit_name_exts.setText(list_component_exts[pos].name)
            self.load_exts_connections()

    def load_component_sensor(self):
        global list_component_sensor, id_project
        list_component_sensor = DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_SENSOR, id_project)

        self.ui.listwidget_sensor.clear()
        for pos in range(len(list_component_sensor)):
            self.ui.listwidget_sensor.addItem(list_component_sensor[pos].name)

    def disable_edit_sensor(self):
        self.ui.button_add_sensor.setEnabled(True)
        self.ui.button_update_sensor.setEnabled(False)
        self.ui.button_delete_sensor.setEnabled(False)
        self.ui.button_cancel_sensor.setEnabled(False)
        self.ui.lineedit_name_sensor.setText("")

    def disable_new_sensor(self):
        self.ui.button_add_sensor.setEnabled(False)
        self.ui.button_update_sensor.setEnabled(True)
        self.ui.button_delete_sensor.setEnabled(True)
        self.ui.button_cancel_sensor.setEnabled(True)

    def on_button_add_sensor_clicked(self):
        global id_project, list_component_sensor

        description = self.ui.lineedit_name_sensor.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            comp = Component(0, Constant.DB_ID_SENSOR, id_project, description, current_date, current_date)
            DB_Components.insert_to_table(comp)

            if self.ui.listwidget_controlled_process_connection.isEnabled():
                self.load_controlled_process_connections()

            self.load_component_sensor()
            self.ui.lineedit_name_sensor.setText("")

    def on_button_update_sensor_clicked(self):
        global list_component_sensor

        name = self.ui.lineedit_name_sensor.text()
        if len(name) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            pos = self.ui.listwidget_sensor.currentRow()
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            comp = list_component_sensor[pos]
            comp.name = name
            comp.edited_date = current_date

            DB_Components.update_component(comp)

            self.disable_edit_sensor()
            self.load_component_sensor()
            self.ui.lineedit_name_sensor.setText("")
            self.ui.listwidget_sensor.clearSelection()
            self.ui.listwidget_sensor.selectionModel().clear()
            self.disable_edit_sensor()
            self.disable_sensor_connections()

            if self.ui.listwidget_controlled_process_connection.isEnabled():
                self.load_controlled_process_connections()

    def on_button_delete_sensor_clicked(self):
        global list_component_sensor
        pos = self.ui.listwidget_sensor.currentRow()
        act = list_component_sensor[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete: " + act.name + "?")
        msgBox.setWindowTitle("Delete Actuator?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Components.delete(act)
            self.disable_edit_sensor()
            self.load_component_sensor()
            self.ui.lineedit_name_sensor.setText("")
            self.load_component_sensor()
            self.ui.listwidget_sensor.clearSelection()
            self.ui.listwidget_sensor.selectionModel().clear()
            self.disable_edit_sensor()
            self.disable_sensor_connections()

            if self.ui.listwidget_controlled_process_connection.isEnabled():
                self.load_controlled_process_connections()

    def on_button_cancel_sensor_clicked(self):
        self.disable_edit_sensor()
        self.ui.lineedit_name_sensor.setText("")
        self.ui.listwidget_sensor.selectionModel().clear()
        self.ui.listwidget_sensor.clearSelection()
        self.disable_sensor_connections()

    def on_listwidget_sensors_clicked(self):
        global list_component_sensor
        pos = self.ui.listwidget_sensor.currentRow()
        item = self.ui.listwidget_sensor.currentItem()

        if pos >= 0:
            self.disable_new_sensor()
            item.setSelected(True)
            self.ui.lineedit_name_sensor.setText(list_component_sensor[pos].name)
            self.load_sensor_connections()

    def load_component_controlled_proccess(self):
        global list_component_controlled_process, id_project
        list_component_controlled_process = DB_Components.select_component_by_thing_project_analysis(Constant.DB_ID_CP,
                                                                                                     id_project)

        if len(list_component_controlled_process) > 0:
            self.ui.lineedit_name_controlled_process.setEnabled(False)
            self.ui.lineedit_name_controlled_process.setText(list_component_controlled_process[0].name)
            self.disable_new_controlled_proccess()
            self.load_controlled_process_connections()
            self.load_component_controlled_process_input()
            self.load_component_controlled_process_output()
            self.load_component_controlled_process_envd()

        else:
            self.ui.lineedit_name_controlled_process.setText("")
            self.ui.lineedit_name_controlled_process.setEnabled(True)
            self.disable_edit_controlled_proccess()
            self.clean_cp_envd_inputs_outputs()

    def disable_edit_controlled_proccess(self):
        self.ui.button_save_controlled_process.setEnabled(True)
        self.ui.button_edit_controlled_process.setEnabled(False)
        self.ui.button_delete_controlled_process.setEnabled(False)
        self.ui.button_cancel_controlled_process.setEnabled(False)

    def disable_new_controlled_proccess(self):
        self.ui.button_save_controlled_process.setEnabled(False)
        self.ui.button_edit_controlled_process.setEnabled(True)
        self.ui.button_delete_controlled_process.setEnabled(True)
        self.ui.button_cancel_controlled_process.setEnabled(False)

    def on_button_save_controlled_process_clicked(self):
        global id_project, list_component_controlled_process, list_controlled_process_output, list_controlled_process_input, list_controlled_process_env_dist

        description = self.ui.lineedit_name_controlled_process.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            if len(list_component_controlled_process) == 0:
                comp = Component(0, Constant.DB_ID_CP, id_project, description, current_date, current_date)
                DB_Components.insert_controlled_process(comp)

            else:
                comp = list_component_controlled_process[0]
                comp.name = description
                comp.edited_date = current_date
                DB_Components.update_component(comp)

                comp_in = list_controlled_process_input[0]
                comp_in.name = description + " " + Constant.INPUT
                comp_in.edited_date = current_date
                DB_Components.update_component(comp_in)

                comp_out = list_controlled_process_output[0]
                comp_out.name = description + " " + Constant.OUTPUT
                comp_out.edited_date = current_date
                DB_Components.update_component(comp_out)

                comp_env = list_controlled_process_env_dist[0]
                comp_env.name = description + " " + Constant.ENVIRONMENTAL_DISTURBANCES
                comp_env.edited_date = current_date
                DB_Components.update_component(comp_env)

            if self.ui.listwidget_controller_connection.isEnabled():
                self.load_controller_connections()

            if self.ui.listwidget_actuator.isEnabled():
                self.load_actuator_connections()

            self.load_component_controlled_proccess()

    def on_button_edit_controlled_process_clicked(self):
        global list_component_controlled_process

        self.ui.lineedit_name_controlled_process.setEnabled(True)
        self.ui.button_edit_controlled_process.setEnabled(False)
        self.ui.button_save_controlled_process.setEnabled(True)
        self.ui.button_delete_controlled_process.setEnabled(True)
        self.ui.button_cancel_controlled_process.setEnabled(True)

    def on_button_delete_controlled_process_clicked(self):
        global list_component_controlled_process
        if len(list_component_controlled_process) > 0:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Are you sure that you want delete: " + list_component_controlled_process[0].name + "?")
            msgBox.setWindowTitle("Delete Controlled Procces?")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                DB_Components.delete_controlled_procces(list_component_controlled_process[0])

                if self.ui.listwidget_controller_connection.isEnabled():
                    self.load_controller_connections()

                if self.ui.listwidget_actuator.isEnabled():
                    self.load_actuator_connections()

                # self.load_controlled_process_connections()
                self.disable_controlled_process_connections()

        self.load_component_controlled_proccess()

    def on_button_cancel_controlled_process_clicked(self):
        self.load_component_controlled_proccess()

    def clean_cp_envd_inputs_outputs(self):
        self.ui.button_add_controlled_process_envd.setEnabled(False)
        self.ui.button_update_controlled_process_envd.setEnabled(False)
        self.ui.button_delete_controlled_process_envd.setEnabled(False)
        self.ui.button_cancel_controlled_process_envd.setEnabled(False)
        self.ui.listwidget_controlled_process_envd.clear()
        self.ui.listwidget_controlled_process_envd.setEnabled(False)
        self.ui.lineedit_name_controlled_process_envd.setEnabled(False)
        self.ui.lineedit_name_controlled_process_envd.setText("")

        self.ui.button_add_controlled_process_input.setEnabled(False)
        self.ui.button_update_controlled_process_input.setEnabled(False)
        self.ui.button_delete_controlled_process_input.setEnabled(False)
        self.ui.button_cancel_controlled_process_input.setEnabled(False)
        self.ui.listwidget_controlled_process_input.clear()
        self.ui.listwidget_controlled_process_input.setEnabled(False)
        self.ui.lineedit_name_controlled_process_input.setEnabled(False)
        self.ui.lineedit_name_controlled_process_input.setText("")

        self.ui.button_add_controlled_process_output.setEnabled(False)
        self.ui.button_update_controlled_process_output.setEnabled(False)
        self.ui.button_delete_controlled_process_output.setEnabled(False)
        self.ui.button_cancel_controlled_process_output.setEnabled(False)
        self.ui.listwidget_controlled_process_output.clear()
        self.ui.listwidget_controlled_process_output.setEnabled(False)
        self.ui.lineedit_name_controlled_process_output.setEnabled(False)
        self.ui.lineedit_name_controlled_process_output.setText("")

    def load_component_controlled_process_input(self):
        global list_component_controlled_process, id_project, list_controlled_process_input, list_controlled_process_env_dist, \
            list_controlled_process_input_variables, list_controlled_process_input_variables_values

        self.ui.listwidget_controlled_process_input.clear()

        if len(list_component_controlled_process) > 0:

            list_controlled_process_input = DB_Components.select_component_by_project_father_thing(id_project, list_component_controlled_process[0].id, Constant.DB_ID_INPUT)
            list_controlled_process_env_dist = DB_Components.select_component_by_project_father_thing(id_project, list_component_controlled_process[0].id, Constant.DB_ID_ENV_DISTURBANCES)

            if len(list_controlled_process_input) > 0:
                list_controlled_process_input_variables = DB_Variables.select_variables_by_component_project(list_controlled_process_input[0].id, id_project)

                if len(list_controlled_process_input_variables) > 0:
                    self.ui.listwidget_controlled_process_input.setEnabled(True)
                    self.ui.lineedit_name_controlled_process_input.setEnabled(True)
                    self.ui.lineedit_name_controlled_process_input.setText("")

                    list_controlled_process_input_variables_values = DB_Variables_Values.select_values_by_variable(
                        list_controlled_process_input_variables[0].id)

                    self.ui.listwidget_controlled_process_input.clear()

                    for val in list_controlled_process_input_variables_values:
                        self.ui.listwidget_controlled_process_input.addItem(val.value)
                    self.disable_edit_controlled_process_input()

    def load_component_controlled_process_output(self):
        global list_component_controlled_process, id_project, list_controlled_process_output, list_controlled_process_env_dist, \
            list_controlled_process_output_variables, list_controlled_process_output_variables_values

        self.ui.listwidget_controlled_process_output.clear()

        if len(list_component_controlled_process) > 0:
            list_controlled_process_output = DB_Components.select_component_by_project_father_thing(id_project,
                                                                                                    list_component_controlled_process[
                                                                                                        0].id,
                                                                                                    Constant.DB_ID_OUTPUT)

            if len(list_controlled_process_output) > 0:
                list_controlled_process_output_variables = DB_Variables.select_variables_by_component_project(
                    list_controlled_process_output[0].id, id_project)

                if len(list_controlled_process_output_variables) > 0:
                    self.ui.listwidget_controlled_process_output.setEnabled(True)
                    self.ui.lineedit_name_controlled_process_output.setEnabled(True)
                    self.ui.lineedit_name_controlled_process_output.setText("")

                    list_controlled_process_output_variables_values = DB_Variables_Values.select_values_by_variable(
                        list_controlled_process_output_variables[0].id)

                    self.ui.listwidget_controlled_process_output.clear()

                    for val in list_controlled_process_output_variables_values:
                        self.ui.listwidget_controlled_process_output.addItem(val.value)
                    self.disable_edit_controlled_process_output()

    def load_component_controlled_process_envd(self):
        global list_component_controlled_process, id_project, list_controlled_process_envd, list_controlled_process_env_dist, list_controlled_process_envd_variables, list_controlled_process_envd_variables_values

        self.ui.listwidget_controlled_process_envd.clear()

        if len(list_component_controlled_process) > 0:
            list_controlled_process_envd = DB_Components.select_component_by_project_father_thing(id_project,
                                                                                                  list_component_controlled_process[
                                                                                                      0].id,
                                                                                                  Constant.DB_ID_ENV_DISTURBANCES)

            if len(list_controlled_process_envd) > 0:
                list_controlled_process_envd_variables = DB_Variables.select_variables_by_component_project(
                    list_controlled_process_envd[0].id, id_project)

                if len(list_controlled_process_envd_variables) > 0:
                    self.ui.listwidget_controlled_process_envd.setEnabled(True)
                    self.ui.lineedit_name_controlled_process_envd.setEnabled(True)
                    self.ui.lineedit_name_controlled_process_envd.setText("")

                    list_controlled_process_envd_variables_values = DB_Variables_Values.select_values_by_variable(
                        list_controlled_process_envd_variables[0].id)

                    self.ui.listwidget_controlled_process_envd.clear()

                    for val in list_controlled_process_envd_variables_values:
                        self.ui.listwidget_controlled_process_envd.addItem(val.value)
                    self.disable_edit_controlled_process_envd()

    def on_listwidget_controlled_process_envd_clicked(self):
        global list_controlled_process_envd_variables_values, id_project
        pos_var = self.ui.listwidget_controlled_process_envd.currentRow()

        if pos_var >= 0:
            item = self.ui.listwidget_controlled_process_envd.currentItem()
            item.setSelected(True)
            self.disable_new_controlled_process_envd()
            self.ui.lineedit_name_controlled_process_envd.setText(
                list_controlled_process_envd_variables_values[pos_var].value)

    def on_button_add_controlled_process_envd_clicked(self):
        global id_project, list_controlled_process_envd_variables

        description = self.ui.lineedit_name_controlled_process_envd.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            # pos_var = self.ui.listwidget_controlled_process_variable.currentRow()

            if len(list_controlled_process_envd_variables) > 0:
                var = Variable_Values(0, list_controlled_process_envd_variables[0].id, description, current_date,
                                      current_date)
                DB_Variables_Values.insert(var)

                self.load_component_controlled_process_input()
                self.load_component_controlled_process_envd()
                self.load_component_controlled_process_envd()
                self.ui.lineedit_name_controlled_process_envd.setText("")

    def on_button_update_controlled_process_envd_clicked(self):
        global id_project, list_controlled_process_envd_variables_values

        description = self.ui.lineedit_name_controlled_process_envd.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            pos = self.ui.listwidget_controlled_process_envd.currentRow()

            val = list_controlled_process_envd_variables_values[pos]
            val.value = description
            val.edited_date = current_date
            DB_Variables_Values.update(val)

            self.load_component_controlled_process_envd()
            self.ui.lineedit_name_controlled_process_envd.setText("")
            self.ui.listwidget_controlled_process_envd.clearSelection()
            self.ui.listwidget_controlled_process_envd.selectionModel().clear()
            self.disable_edit_controlled_process_envd()

    def on_button_delete_controlled_process_envd_clicked(self):
        global list_controlled_process_envd_variables_values
        pos = self.ui.listwidget_controlled_process_envd.currentRow()
        val = list_controlled_process_envd_variables_values[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete value: " + val.value + "?")
        msgBox.setWindowTitle("Delete Value?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Variables_Values.delete(val)
            self.load_component_controlled_process_envd()
            self.ui.lineedit_name_controlled_process_envd.setText("")
            self.disable_edit_controlled_process_envd()
            self.ui.listwidget_controlled_process_envd.selectionModel().clear()
            self.ui.listwidget_controlled_process_envd.clearSelection()

    def on_button_cancel_controlled_process_envd_clicked(self):
        self.disable_edit_controlled_process_envd()
        self.ui.lineedit_name_controlled_process_envd.setText("")
        self.ui.listwidget_controlled_process_envd.clearSelection()
        self.ui.listwidget_controlled_process_envd.selectionModel().clear()

    def on_button_add_controlled_process_input_clicked(self):
        global id_project, list_controlled_process_input_variables

        description = self.ui.lineedit_name_controlled_process_input.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            # pos_var = self.ui.listwidget_controlled_process_variable.currentRow()

            if len(list_controlled_process_input_variables) > 0:
                var = Variable_Values(0, list_controlled_process_input_variables[0].id, description, current_date,
                                      current_date)
                DB_Variables_Values.insert(var)

                self.load_component_controlled_process_input()
                self.ui.lineedit_name_controlled_process_input.setText("")

    def on_button_update_controlled_process_input_clicked(self):
        global id_project, list_controlled_process_input_variables_values

        description = self.ui.lineedit_name_controlled_process_input.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            pos = self.ui.listwidget_controlled_process_input.currentRow()

            val = list_controlled_process_input_variables_values[pos]
            val.value = description
            val.edited_date = current_date
            DB_Variables_Values.update(val)

            self.load_component_controlled_process_input()
            self.ui.lineedit_name_controlled_process_input.setText("")
            self.ui.listwidget_controlled_process_input.clearSelection()
            self.ui.listwidget_controlled_process_input.selectionModel().clear()
            self.disable_edit_controlled_process_input()

    def on_button_delete_controlled_process_input_clicked(self):
        global list_controlled_process_input_variables_values
        pos = self.ui.listwidget_controlled_process_input.currentRow()
        val = list_controlled_process_input_variables_values[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete value: " + val.value + "?")
        msgBox.setWindowTitle("Delete Value?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Variables_Values.delete(val)
            self.load_component_controlled_process_input()
            self.load_component_controlled_process_output()
            self.ui.lineedit_name_controlled_process_input.setText("")
            self.disable_edit_controlled_process_input()
            self.ui.listwidget_controlled_process_input.selectionModel().clear()
            self.ui.listwidget_controlled_process_input.clearSelection()

    def on_button_cancel_controlled_process_input_clicked(self):
        self.disable_edit_controlled_process_input()
        self.ui.lineedit_name_controlled_process_input.setText("")
        self.ui.listwidget_controlled_process_input.clearSelection()
        self.ui.listwidget_controlled_process_input.selectionModel().clear()

    def on_listwidget_controlled_process_input_clicked(self):
        global list_controlled_process_input_variables_values, id_project
        pos_var = self.ui.listwidget_controlled_process_input.currentRow()

        if pos_var >= 0:
            item = self.ui.listwidget_controlled_process_input.currentItem()
            item.setSelected(True)
            self.disable_new_controlled_process_input()
            self.ui.lineedit_name_controlled_process_input.setText(
                list_controlled_process_input_variables_values[pos_var].value)

    def on_button_add_controlled_process_output_clicked(self):
        global id_project, list_controlled_process_output_variables

        description = self.ui.lineedit_name_controlled_process_output.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            # pos_var = self.ui.listwidget_controlled_process_variable.currentRow()

            if len(list_controlled_process_output_variables) > 0:
                var = Variable_Values(0, list_controlled_process_output_variables[0].id, description, current_date,
                                      current_date)
                DB_Variables_Values.insert(var)

                self.load_component_controlled_process_input()
                self.load_component_controlled_process_output()
                self.ui.lineedit_name_controlled_process_output.setText("")

    def on_button_update_controlled_process_output_clicked(self):
        global id_project, list_controlled_process_output_variables_values

        description = self.ui.lineedit_name_controlled_process_output.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            pos = self.ui.listwidget_controlled_process_output.currentRow()

            val = list_controlled_process_output_variables_values[pos]
            val.value = description
            val.edited_date = current_date
            DB_Variables_Values.update(val)

            self.load_component_controlled_process_output()
            self.ui.lineedit_name_controlled_process_output.setText("")
            self.ui.listwidget_controlled_process_output.clearSelection()
            self.ui.listwidget_controlled_process_output.selectionModel().clear()
            self.disable_edit_controlled_process_output()

    def on_button_delete_controlled_process_output_clicked(self):
        global list_controlled_process_output_variables_values
        pos = self.ui.listwidget_controlled_process_output.currentRow()
        val = list_controlled_process_output_variables_values[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete value: " + val.value + "?")
        msgBox.setWindowTitle("Delete Value?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Variables_Values.delete(val)
            self.load_component_controlled_process_output()
            self.ui.lineedit_name_controlled_process_output.setText("")
            self.disable_edit_controlled_process_output()
            self.ui.listwidget_controlled_process_output.selectionModel().clear()
            self.ui.listwidget_controlled_process_output.clearSelection()

    def on_button_cancel_controlled_process_output_clicked(self):
        self.disable_edit_controlled_process_output()
        self.ui.lineedit_name_controlled_process_output.setText("")
        self.ui.listwidget_controlled_process_output.clearSelection()
        self.ui.listwidget_controlled_process_output.selectionModel().clear()

    def on_listwidget_controlled_process_output_clicked(self):
        global list_controlled_process_output_variables_values, id_project
        pos_var = self.ui.listwidget_controlled_process_output.currentRow()

        if pos_var >= 0:
            item = self.ui.listwidget_controlled_process_output.currentItem()
            item.setSelected(True)
            self.disable_new_controlled_process_output()
            self.ui.lineedit_name_controlled_process_output.setText(
                list_controlled_process_output_variables_values[pos_var].value)

    def disable_new_controlled_process_envd(self):
        self.ui.button_add_controlled_process_envd.setEnabled(False)
        self.ui.button_update_controlled_process_envd.setEnabled(True)
        self.ui.button_delete_controlled_process_envd.setEnabled(True)
        self.ui.button_cancel_controlled_process_envd.setEnabled(True)

    def disable_edit_controlled_process_envd(self):
        self.ui.lineedit_name_controlled_process_envd.setText("")
        self.ui.lineedit_name_controlled_process_envd.setEnabled(True)
        self.ui.listwidget_controlled_process_envd.setEnabled(True)
        self.ui.button_add_controlled_process_envd.setEnabled(True)
        self.ui.button_update_controlled_process_envd.setEnabled(False)
        self.ui.button_delete_controlled_process_envd.setEnabled(False)
        self.ui.button_cancel_controlled_process_envd.setEnabled(False)

    def disable_new_controlled_process_input(self):
        self.ui.button_add_controlled_process_input.setEnabled(False)
        self.ui.button_update_controlled_process_input.setEnabled(True)
        self.ui.button_delete_controlled_process_input.setEnabled(True)
        self.ui.button_cancel_controlled_process_input.setEnabled(True)

    def disable_edit_controlled_process_input(self):
        self.ui.lineedit_name_controlled_process_input.setText("")
        self.ui.lineedit_name_controlled_process_input.setEnabled(True)
        self.ui.listwidget_controlled_process_input.setEnabled(True)
        self.ui.button_add_controlled_process_input.setEnabled(True)
        self.ui.button_update_controlled_process_input.setEnabled(False)
        self.ui.button_delete_controlled_process_input.setEnabled(False)
        self.ui.button_cancel_controlled_process_input.setEnabled(False)

    def disable_new_controlled_process_output(self):
        self.ui.button_add_controlled_process_output.setEnabled(False)
        self.ui.button_update_controlled_process_output.setEnabled(True)
        self.ui.button_delete_controlled_process_output.setEnabled(True)
        self.ui.button_cancel_controlled_process_output.setEnabled(True)

    def disable_edit_controlled_process_output(self):
        self.ui.lineedit_name_controlled_process_output.setText("")
        self.ui.lineedit_name_controlled_process_output.setEnabled(True)
        self.ui.listwidget_controlled_process_output.setEnabled(True)
        self.ui.button_add_controlled_process_output.setEnabled(True)
        self.ui.button_update_controlled_process_output.setEnabled(False)
        self.ui.button_delete_controlled_process_output.setEnabled(False)
        self.ui.button_cancel_controlled_process_output.setEnabled(False)

    def load_controller_control_actions(self):
        global list_component_controller, list_control_actions, id_project
        pos_controller = self.ui.combobox_second_controller.currentIndex()

        self.ui.listwidget_control_actions.clear()
        self.disable_edit_control_action()

        if len(list_component_controller) == 0:
            return

        list_control_actions = DB_Actions_Components.select_actions_by_component_and_project(
            list_component_controller[pos_controller].id, id_project)
        for pos in range(len(list_control_actions)):
            self.ui.listwidget_control_actions.addItem(list_control_actions[pos].name)

        self.load_controller_actions_connections()

    def load_component_controller_variables(self):
        global list_component_controller, list_component_controller_variables, id_project
        pos_controller = self.ui.combobox_second_controller.currentIndex()

        if pos_controller >= 0:
            list_component_controller_variables = DB_Variables.select_variables_by_component_project(
                list_component_controller[pos_controller].id, id_project)

            self.ui.listwidget_controller_variable.clear()
            self.ui.listwidget_controller_variable_values.clear()
            self.disable_edit_controller_variable()
            self.clean_variables_values()

            for pos in range(len(list_component_controller_variables)):
                self.ui.listwidget_controller_variable.addItem(list_component_controller_variables[pos].name)
        self.load_controller_variable_connections()

    def check_control_structure(self):
        global id_project
        warning = ""

        warning += DB_Components.find_component_warnings(id_project)
        empty_links = DB_Components_Links.select_empty_links(id_project)
        if warning != "" and empty_links != "":
            warning += "\n"
        warning += empty_links

        w_var = DB_Variables.select_variables_warning(id_project)
        if warning != "" and w_var != "":
            warning += "\n"
        warning += w_var

        if warning == "":
            self.ui.label_structure_warnings.setText("No warnings detected")
        else:
            self.ui.label_structure_warnings.setText(warning)



    #
    # feedback at least 2 values
    #
    # confirm, controller with variable


    # ----- Functions STPA 2 Step -----

    # ----- Functions STPA 1 Step -----
    def load_goals(self):
        # Goals information
        global list_goals, id_project
        self.ui.list_saf_goals.clear()
        list_goals = DB_Goals.select_all_goals_by_project(id_project)
        for pos in range(len(list_goals)):
            self.ui.list_saf_goals.addItem("G-" + str(list_goals[pos].id_goal) + ": " + list_goals[pos].description)

    def on_list_saf_goals_clicked(self):
        item = self.ui.list_saf_goals.currentItem()
        pos = self.ui.list_saf_goals.currentRow()

        self.ui.button_saf_new_goal.setEnabled(False)
        self.ui.button_saf_update_goal.setEnabled(True)
        self.ui.button_saf_delete_goal.setEnabled(True)
        self.ui.button_saf_cancel_goal.setEnabled(True)

        global list_goals
        self.ui.label_saf_goal_position.setText("G-" + str(list_goals[pos].id_goal))
        self.ui.lineedit_saf_goal.setText(list_goals[pos].description)

    def on_button_saf_new_goal_clicked(self):
        global id_project, list_goals

        description = self.ui.lineedit_saf_goal.text()
        if len(description) > 0:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            # date_dt1 = datetime.strptime(date_str1, '%A, %B %d, %Y')

            pos_goal = len(list_goals) + 1
            goal = Goal(0, id_project, pos_goal, description, current_date, current_date)
            DB_Goals.insert_to_goals(goal)

            self.load_goals()
            self.ui.lineedit_saf_goal.setText("")
        else:
            showdialog("Error on save", "Fill the field with description")

    def on_button_saf_update_goal_clicked(self):
        global id_project, list_goals

        description = self.ui.lineedit_saf_goal.text()
        if len(description) > 0:
            pos = self.ui.list_saf_goals.currentRow()
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            goal = list_goals[pos]
            goal.description = description
            goal.edited_date = current_date
            DB_Goals.update_goal(goal)

            self.load_goals()
            self.ui.lineedit_saf_goal.setText("")
            self.ui.button_saf_new_goal.setEnabled(True)
            self.ui.button_saf_update_goal.setEnabled(False)
            self.ui.button_saf_delete_goal.setEnabled(False)
            self.ui.button_saf_cancel_goal.setEnabled(False)
            self.ui.label_saf_goal_position.setText("G-")
        else:
            showdialog("Error on save", "Fill the field with description")

    def on_button_saf_delete_goal_clicked(self):
        pos = self.ui.list_saf_goals.currentRow()
        goal = list_goals[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete register G-" + str(goal.id_goal) + "?")
        msgBox.setWindowTitle("Delete Goal")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Goals.delete_goal(goal)
            self.load_goals()
            self.ui.lineedit_saf_goal.setText("")
            self.ui.button_saf_new_goal.setEnabled(True)
            self.ui.button_saf_update_goal.setEnabled(False)
            self.ui.button_saf_delete_goal.setEnabled(False)
            self.ui.button_saf_cancel_goal.setEnabled(False)
            self.ui.label_saf_goal_position.setText("G-")

    def on_button_saf_cancel_goal_clicked(self):
        self.ui.button_saf_new_goal.setEnabled(True)
        self.ui.button_saf_update_goal.setEnabled(False)
        self.ui.button_saf_delete_goal.setEnabled(False)
        self.ui.button_saf_cancel_goal.setEnabled(False)
        self.ui.label_saf_goal_position.setText("G-")
        self.ui.lineedit_saf_goal.setText("")
        item = self.ui.list_saf_goals.currentItem()
        item.setSelected(False)

    def load_assumptions(self):
        # Assumptions information
        global list_assumptions, id_project
        self.ui.list_saf_assumptions.clear()
        list_assumptions = DB_Assumptions.select_all_assumptions_by_project(id_project)
        for pos in range(len(list_assumptions)):
            self.ui.list_saf_assumptions.addItem(
                "A-" + str(list_assumptions[pos].id_assumption) + ": " + list_assumptions[pos].description)

    def on_list_saf_assumptions_clicked(self):
        item = self.ui.list_saf_assumptions.currentItem()
        pos = self.ui.list_saf_assumptions.currentRow()

        self.ui.button_saf_new_assumption.setEnabled(False)
        self.ui.button_saf_update_assumption.setEnabled(True)
        self.ui.button_saf_delete_assumption.setEnabled(True)
        self.ui.button_saf_cancel_assumption.setEnabled(True)

        global list_assumptions
        self.ui.label_saf_assumption_position.setText("A-" + str(list_assumptions[pos].id_assumption))
        self.ui.lineedit_saf_assumption.setText(list_assumptions[pos].description)

    def on_button_saf_new_assumption_clicked(self):
        global id_project, list_assumptions

        description = self.ui.lineedit_saf_assumption.text()
        if len(description) > 0:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            # date_dt1 = datetime.strptime(date_str1, '%A, %B %d, %Y')

            pos_assumption = len(list_assumptions) + 1
            assump = Assumptions(0, id_project, pos_assumption, description, current_date, current_date)
            DB_Assumptions.insert_to_assumptions(assump)

            self.load_assumptions()
            self.ui.lineedit_saf_assumption.setText("")
        else:
            showdialog("Error on save", "Fill the field with description")

    def on_button_saf_update_assumption_clicked(self):
        global id_project, list_assumptions

        description = self.ui.lineedit_saf_assumption.text()
        if len(description) > 0:
            pos = self.ui.list_saf_assumptions.currentRow()
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            assumption = list_assumptions[pos]
            assumption.description = description
            assumption.edited_date = current_date
            DB_Assumptions.update_assumption(assumption)

            self.load_assumptions()
            self.ui.lineedit_saf_assumption.setText("")
            self.ui.button_saf_new_assumption.setEnabled(True)
            self.ui.button_saf_update_assumption.setEnabled(False)
            self.ui.button_saf_delete_assumption.setEnabled(False)
            self.ui.button_saf_cancel_assumption.setEnabled(False)
            self.ui.label_saf_assumption_position.setText("A-")
        else:
            showdialog("Error on save", "Fill the field with description")

    def on_button_saf_delete_assumption_clicked(self):
        pos = self.ui.list_saf_assumptions.currentRow()
        assumption = list_assumptions[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete register A-" + str(assumption.id_assumption) + "?")
        msgBox.setWindowTitle("Delete Assumption")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Assumptions.delete_assumption(assumption)
            self.load_assumptions()
            self.ui.lineedit_saf_assumption.setText("")
            self.ui.button_saf_new_assumption.setEnabled(True)
            self.ui.button_saf_update_assumption.setEnabled(False)
            self.ui.button_saf_delete_assumption.setEnabled(False)
            self.ui.button_saf_cancel_assumption.setEnabled(False)
            self.ui.label_saf_assumption_position.setText("A-")

    def on_button_saf_cancel_assumption_clicked(self):
        self.ui.button_saf_new_assumption.setEnabled(True)
        self.ui.button_saf_update_assumption.setEnabled(False)
        self.ui.button_saf_delete_assumption.setEnabled(False)
        self.ui.button_saf_cancel_assumption.setEnabled(False)
        self.ui.label_saf_assumption_position.setText("A-")
        self.ui.lineedit_saf_assumption.setText("")
        item = self.ui.list_saf_assumptions.currentItem()
        item.setSelected(False)
        self.ui.lineedit_saf_assumption.setFocusPolicy(Qt.StrongFocus)

    def load_losses(self):
        # Losses information
        global list_losses, id_project
        self.ui.list_saf_losses.clear()
        list_losses = DB_Losses.select_all_losses_by_project(id_project)
        for pos in range(len(list_losses)):
            self.ui.list_saf_losses.addItem("L-" + str(list_losses[pos].id_loss) + ": " + list_losses[pos].description)

        self.load_hazards_losses()

    def on_list_saf_losses_clicked(self):
        item = self.ui.list_saf_losses.currentItem()
        pos = self.ui.list_saf_losses.currentRow()

        self.ui.button_saf_new_loss.setEnabled(False)
        self.ui.button_saf_update_loss.setEnabled(True)
        self.ui.button_saf_delete_loss.setEnabled(True)
        self.ui.button_saf_cancel_loss.setEnabled(True)

        global list_losses
        self.ui.label_saf_loss_position.setText("L-" + str(list_losses[pos].id_loss))
        self.ui.lineedit_saf_loss.setText(list_losses[pos].description)

    def on_button_saf_new_loss_clicked(self):
        global id_project, list_losses

        description = self.ui.lineedit_saf_loss.text()
        if len(description) > 0:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            # date_dt1 = datetime.strptime(date_str1, '%A, %B %d, %Y')

            pos_loss = len(list_losses) + 1
            loss = Loss(0, id_project, pos_loss, description, current_date, current_date)
            DB_Losses.insert_to_losses(loss)

            self.load_losses()
            self.ui.lineedit_saf_loss.setText("")
        else:
            showdialog("Error on save", "Fill the field with description")

    def on_button_saf_update_loss_clicked(self):
        global id_project, list_losses

        description = self.ui.lineedit_saf_loss.text()
        if len(description) > 0:
            pos = self.ui.list_saf_losses.currentRow()
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            loss = list_losses[pos]
            loss.description = description
            loss.edited_date = current_date
            DB_Losses.update_loss(loss)

            self.load_losses()
            self.ui.lineedit_saf_loss.setText("")
            self.ui.button_saf_new_loss.setEnabled(True)
            self.ui.button_saf_update_loss.setEnabled(False)
            self.ui.button_saf_delete_loss.setEnabled(False)
            self.ui.button_saf_cancel_loss.setEnabled(False)
            self.ui.label_saf_loss_position.setText("L-")
        else:
            showdialog("Error on save", "Fill the field with description")

    def on_button_saf_delete_loss_clicked(self):
        pos = self.ui.list_saf_losses.currentRow()
        loss = list_losses[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete register L-" + str(loss.id_loss) + "?")
        msgBox.setWindowTitle("Delete Loss")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Losses.delete_loss(loss)
            self.load_losses()
            self.ui.lineedit_saf_loss.setText("")
            self.ui.button_saf_new_loss.setEnabled(True)
            self.ui.button_saf_update_loss.setEnabled(False)
            self.ui.button_saf_delete_loss.setEnabled(False)
            self.ui.button_saf_cancel_loss.setEnabled(False)
            self.ui.label_saf_loss_position.setText("L-")

    def on_button_saf_cancel_loss_clicked(self):
        self.ui.button_saf_new_loss.setEnabled(True)
        self.ui.button_saf_update_loss.setEnabled(False)
        self.ui.button_saf_delete_loss.setEnabled(False)
        self.ui.button_saf_cancel_loss.setEnabled(False)
        self.ui.label_saf_loss_position.setText("L-")
        self.ui.lineedit_saf_loss.setText("")
        item = self.ui.list_saf_losses.currentItem()
        item.setSelected(False)

    def load_hazards(self):
        # Hazards information
        global list_hazards, id_project
        self.ui.list_saf_hazards.clear()
        list_hazards = DB_Hazards.select_all_hazards_by_project(id_project)

        count = 1
        for pos in range(len(list_hazards)):
            text = ""
            for loss in list_hazards[pos].list_of_loss:
                text += "[L-" + str(loss.id_loss_screen) + "] "

            self.ui.list_saf_hazards.addItem("H-" + str(list_hazards[pos].id_hazard) + ": " + list_hazards[pos].description + " " + text)

        self.load_hazards_losses()
        self.load_constraints_hazards()

    def load_hazards_losses(self):
        global list_losses, list_hazards
        self.ui.list_hazards_losses.clear()
        pos = self.ui.list_saf_hazards.currentRow()

        for pos_los in range(len(list_losses)):
            self.ui.list_hazards_losses.addItem(
                "L-" + str(list_losses[pos_los].id_loss) + ": " + list_losses[pos_los].description)

            if pos > 0:
                for l in list_hazards[pos].list_of_loss:
                    if l.id_loss == list_losses[pos_los].id:
                        self.ui.list_hazards_losses.item(pos_los).setSelected(True)

    def on_list_saf_hazards_clicked(self):
        global list_hazards, list_losses, id_project
        pos = self.ui.list_saf_hazards.currentRow()

        if pos < 0:
            return

        self.ui.button_saf_new_hazard.setEnabled(False)
        self.ui.button_saf_update_hazard.setEnabled(True)
        self.ui.button_saf_delete_hazard.setEnabled(True)
        self.ui.button_saf_cancel_hazard.setEnabled(True)

        self.ui.label_saf_hazard_position.setText("H-" + str(list_hazards[pos].id_hazard))
        self.ui.lineedit_saf_hazard.setText(list_hazards[pos].description)
        self.ui.list_hazards_losses.clear()

        for pos_los in range(len(list_losses)):
            item = QtWidgets.QListWidgetItem(
                "L-" + str(list_losses[pos_los].id_loss) + ": " + list_losses[pos_los].description)
            self.ui.list_hazards_losses.addItem(item)
            for l in list_hazards[pos].list_of_loss:
                if l.id_loss == list_losses[pos_los].id:
                    self.ui.list_hazards_losses.item(pos_los).setSelected(True)

    def on_button_saf_new_hazard_clicked(self):
        global id_project, list_hazards

        description = self.ui.lineedit_saf_hazard.text()

        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        elif len(self.ui.list_hazards_losses.selectedItems()) == 0:
            showdialog("Error on save", "Select at least one Loss")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            # date_dt1 = datetime.strptime(date_str1, '%A, %B %d, %Y')

            pos_hazard = len(list_hazards) + 1
            hazard = Hazard(0, id_project, pos_hazard, description, current_date, current_date)
            selected_losses = []
            for item in self.ui.list_hazards_losses.selectedItems():
                loss_id = list_losses[self.ui.list_hazards_losses.row(item)].id
                selected_losses.append(Hazard_Loss(0, id_project, 0, loss_id))

            hazard.list_of_loss = selected_losses
            DB_Hazards.insert_to_hazards(hazard)

            self.load_hazards()
            self.ui.lineedit_saf_hazard.setText("")

    def on_button_saf_update_hazard_clicked(self):
        global id_project, list_hazards

        description = self.ui.lineedit_saf_hazard.text()
        if len(description) <= 0:
            showdialog("Error on save", "Fill the field with description")
        elif len(self.ui.list_hazards_losses.selectedItems()) == 0:
            showdialog("Error on save", "Select at least one Loss")
        else:
            pos = self.ui.list_saf_hazards.currentRow()
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            hazard = list_hazards[pos]
            hazard.description = description
            hazard.edited_date = current_date

            selected_losses = []
            for item in self.ui.list_hazards_losses.selectedItems():
                loss_id = list_losses[self.ui.list_hazards_losses.row(item)].id
                selected_losses.append(Hazard_Loss(hazard.id, hazard.id_project, hazard.id, loss_id))

            hazard.list_of_loss = selected_losses
            DB_Hazards.update_hazard(hazard)

            self.clear_haz()

            self.load_hazards()
            self.load_hazards_losses()

            self.clear_haz()

    def clear_haz(self):
        self.ui.lineedit_saf_hazard.setText("")
        self.ui.list_saf_hazards.clearSelection()
        self.ui.list_saf_hazards.selectionModel().clear()
        self.ui.list_hazards_losses.clearSelection()
        self.ui.list_hazards_losses.selectionModel().clear()
        self.ui.label_saf_hazard_position.setText("H-")

        self.ui.button_saf_new_hazard.setEnabled(True)
        self.ui.button_saf_update_hazard.setEnabled(False)
        self.ui.button_saf_delete_hazard.setEnabled(False)
        self.ui.button_saf_cancel_hazard.setEnabled(False)

    def on_button_saf_delete_hazard_clicked(self):
        pos = self.ui.list_saf_hazards.currentRow()
        hazard = list_hazards[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete register H-" + str(hazard.id_hazard) + "?")
        msgBox.setWindowTitle("Delete Hazard")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Hazards.delete_hazard(hazard)
            self.clear_haz()
            self.load_hazards()
            self.clear_haz()

    def on_button_saf_cancel_hazard_clicked(self):
        self.ui.button_saf_new_hazard.setEnabled(True)
        self.ui.button_saf_update_hazard.setEnabled(False)
        self.ui.button_saf_delete_hazard.setEnabled(False)
        self.ui.button_saf_cancel_hazard.setEnabled(False)
        self.ui.label_saf_hazard_position.setText("H-")
        self.ui.lineedit_saf_hazard.setText("")
        self.ui.list_saf_hazards.selectionModel().clear()
        self.ui.list_saf_hazards.clearSelection()
        self.load_hazards_losses()

    def load_constraints(self):
        # Constraints information
        global list_constraints, id_project
        self.ui.list_saf_constraints.clear()
        list_constraints = DB_Safety_Constraints.select_all_safety_constraints_by_project(id_project)
        for pos in range(len(list_constraints)):
            text = ""
            for haz in list_constraints[pos].list_of_hazards:
                text += "[H-" + str(haz.id_haz_screen) + "] "

            self.ui.list_saf_constraints.addItem(
                "SSC-" + str(list_constraints[pos].id_safety_constraint) + ": " + list_constraints[
                    pos].description + " " + text)

        self.load_constraints_hazards()

    def load_constraints_hazards(self):
        global list_hazards, list_constraints
        pos = self.ui.list_saf_constraints.currentRow()
        self.ui.list_constraints_hazards.clear()
        for pos_cons in range(len(list_hazards)):
            self.ui.list_constraints_hazards.addItem(
                "H-" + str(list_hazards[pos_cons].id_hazard) + ": " + list_hazards[pos_cons].description)
            if pos > 0:
                for haz in list_constraints[pos].list_of_hazards:
                    if haz.id_hazard == list_hazards[pos_cons].id:
                        self.ui.list_constraints_hazards.item(pos_cons).setSelected(True)

    def on_list_saf_constraints_clicked(self):
        pos = self.ui.list_saf_constraints.currentRow()

        if pos < 0:
            return

        self.ui.button_saf_new_constraint.setEnabled(False)
        self.ui.button_saf_update_constraint.setEnabled(True)
        self.ui.button_saf_delete_constraint.setEnabled(True)
        self.ui.button_saf_cancel_constraint.setEnabled(True)

        global list_constraints, list_hazards
        self.ui.label_saf_constraint_position.setText("SSC-" + str(list_constraints[pos].id_safety_constraint))
        self.ui.lineedit_saf_constraint.setText(list_constraints[pos].description)
        self.ui.list_constraints_hazards.clear()

        for pos_cons in range(len(list_hazards)):
            item = QtWidgets.QListWidgetItem(
                "H-" + str(list_hazards[pos_cons].id_hazard) + ": " + list_hazards[pos_cons].description)
            self.ui.list_constraints_hazards.addItem(item)
            for haz in list_constraints[pos].list_of_hazards:
                if haz.id_hazard == list_hazards[pos_cons].id:
                    self.ui.list_constraints_hazards.item(pos_cons).setSelected(True)

    def on_button_saf_new_constraint_clicked(self):
        global id_project, list_constraints, list_hazards

        description = self.ui.lineedit_saf_constraint.text()
        if len(description) == 0:
            showdialog("Error on save", "Fill the field with description")
        elif len(self.ui.list_constraints_hazards.selectedItems()) == 0:
            showdialog("Error on save", "Select at least one Hazard")
        else:
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)
            # date_dt1 = datetime.strptime(date_str1, '%A, %B %d, %Y')

            pos_constraint = len(list_constraints) + 1
            constraint = Safety_Constraint(0, id_project, pos_constraint, description, current_date, current_date)

            selected_haz = []
            for item in self.ui.list_constraints_hazards.selectedItems():
                haz_id = list_hazards[self.ui.list_constraints_hazards.row(item)].id
                selected_haz.append(Safety_Constraint_Hazard(0, id_project, constraint.id, haz_id))

            constraint.list_of_hazards = selected_haz
            DB_Safety_Constraints.insert_to_safety_constraints(constraint)

            self.load_constraints()
            self.ui.lineedit_saf_constraint.setText("")

    def on_button_saf_update_constraint_clicked(self):
        global id_project, list_constraints

        description = self.ui.lineedit_saf_constraint.text()
        if len(description) <= 0:
            showdialog("Error on save", "Fill the field with description")
        elif len(self.ui.list_constraints_hazards.selectedItems()) == 0:
            showdialog("Error on save", "Select at least one Hazard")
        else:
            pos = self.ui.list_saf_constraints.currentRow()
            now = datetime.now()
            current_date = now.strftime(Constant.DATETIME_MASK)

            constraint = list_constraints[pos]
            constraint.description = description
            constraint.edited_date = current_date

            selected_haz = []
            for item in self.ui.list_constraints_hazards.selectedItems():
                haz_id = list_hazards[self.ui.list_constraints_hazards.row(item)].id
                selected_haz.append(Safety_Constraint_Hazard(0, id_project, constraint.id, haz_id))

            constraint.list_of_hazards = selected_haz

            DB_Safety_Constraints.update_safety_constraints(constraint)

            self.clear_sc()
            self.load_constraints()
            self.clear_sc()

    def clear_sc(self):
        self.ui.lineedit_saf_constraint.setText("")
        self.ui.list_saf_constraints.clearSelection()
        self.ui.list_saf_constraints.selectionModel().clear()
        self.ui.list_constraints_hazards.clearSelection()
        self.ui.list_constraints_hazards.selectionModel().clear()
        self.ui.label_saf_constraint_position.setText("SSC-")

        self.ui.button_saf_new_constraint.setEnabled(True)
        self.ui.button_saf_update_constraint.setEnabled(False)
        self.ui.button_saf_delete_constraint.setEnabled(False)
        self.ui.button_saf_cancel_constraint.setEnabled(False)

    def on_button_saf_delete_constraint_clicked(self):
        pos = self.ui.list_saf_constraints.currentRow()
        constraint = list_constraints[pos]

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure that you want delete register SSC-" + str(constraint.id_safety_constraint) + "?")
        msgBox.setWindowTitle("Delete Safety Constraint")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            DB_Safety_Constraints.delete_safety_constraints(constraint)
            self.clear_sc()
            self.load_constraints()
            self.clear_sc()

    def on_button_saf_cancel_constraint_clicked(self):
        self.ui.button_saf_new_constraint.setEnabled(True)
        self.ui.button_saf_update_constraint.setEnabled(False)
        self.ui.button_saf_delete_constraint.setEnabled(False)
        self.ui.button_saf_cancel_constraint.setEnabled(False)
        self.ui.label_saf_constraint_position.setText("SSC-")
        self.ui.lineedit_saf_constraint.setText("")
        self.ui.list_saf_constraints.selectionModel().clear()
        self.ui.list_saf_constraints.clearSelection()
        self.ui.list_constraints_hazards.selectionModel().clear()
        self.ui.list_constraints_hazards.clearSelection()
        self.load_constraints_hazards()
    # ----- Functions STPA 1 Step -----

def showdialog(title, message):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText(message)
    msgBox.setWindowTitle(title)
    msgBox.setStandardButtons(QMessageBox.Ok)

    returnValue = msgBox.exec()
    # if returnValue == QMessageBox.Ok:
    #     print('OK clicked')

def thread_function():
    # start reasoner
    # print(onto.base_iri)
    # time.sleep(1)
    sync_reasoner(infer_property_values=True)
    loadind_screen.stopAnimation()
    main_win.active_tab()
    main_win.load_projects()
# def get_d_day():
#     import datetime
#     return datetime.datetime(2021, 6, 29, 0, 0, 0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    DB.create_all_tables()
    main_win = MainWindow()
    main_win.show()
    loadind_screen = LoadingScreen()
    x = threading.Thread(target=thread_function)
    x.start()

    sys.exit(app.exec_())

    # try:
    #     app = QApplication(sys.argv)
    #
    #     today = datetime.now()
    #     d_day = get_d_day()
    #     t_day = d_day - today
    #
    #     days = t_day.days
    #
    #     if days > 15 or days < -15:
    #         if os.path.exists(Constant.IMAGE_PATH):
    #             os.remove(Constant.IMAGE_PATH)
    #         if os.path.exists(Constant.BIN_PATH):
    #             os.remove(Constant.BIN_PATH)
    #     else:
    #         DB.create_all_tables()
    #         main_win = MainWindow()
    #         main_win.show()
    #         loadind_screen = LoadingScreen()
    #         x = threading.Thread(target=thread_function)
    #         x.start()
    #
    #     sys.exit(app.exec_())
    # except NameError as e:
    #     print(e)

# -------------------------------------------------------
# owlready2.JAVA_EXE = Constant.JAVA_PATH
# onto = get_ontology(Constant.ONTOLOGY_PATH).load(reload = True)
# print(onto.base_iri)
#
# # start reasoner
# print("Syncing Reasoner... Wait...")
# start_r_time = time.time()
# sync_reasoner(infer_property_values = True)
# print("Reasoner synced (" + str(time.time() - start_r_time) + " seconds)... Start Ontology analysis...")
#
#
# Safety_tools_new.get_safety_analysis(onto, 1, 1)
#
#
# print("Reading ontology... Wait...")
# start_o_time = time.time()
# safety_requirements_list = Safety_tools.get_safety_requirement_analysis(onto, 1)
# security_requirements_list = Security_tools.get_security_requirement_analysis(onto)
# print("Ontology read (" + str(time.time() - start_o_time) + " seconds)... Start Safety and Security analysis...")
#
# print("Comparing results... Wait...")
# start_c_time = time.time()
# General_tools.compare_and_generate_safety_security(safety_requirements_list, security_requirements_list)
# print("Results compared (" + str(time.time() - start_c_time) + " seconds)... Finish!")
# -------------------------------------------------------


# -------------------------------------------------------
# name = General_tools.find_individuals_of_class(onto, "Saf_UCA")
#
# for obj in name.class_parent.is_a:
#     if isinstance(obj, Restriction):
#         print(obj.property.name)
#         print(obj.value.name)
# -------------------------------------------------------
