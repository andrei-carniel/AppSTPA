# Ontology complete path
# BIN_PATH = "PyQt5\\Qt5\\bin\\libOSA-5.bin"
BIN_PATH = "Ontologies\\safety.owl"
ANALYSIS_PATH = ".\\analysis\\"


IMAGE_STPA_FULL_PATH = ".\Ontologies\safety_ontology.png"


IMAGE_STPA_ONE_PATH = ".\Ontologies\step_one_stpa.png"
IMAGE_STPA_TWO_PATH = ".\Ontologies\step_two_stpa.png"
IMAGE_STPA_THREE_PATH = ".\Ontologies\step_three_stpa.png"
IMAGE_STPA_FOUR_PATH = ".\Ontologies\step_four_stpa.png"
FILES_REPO = "Files"
DB_FILE = "Database/Ontology_DB.db"  # Database path
GIF_LOADING_PATH = "Images/Loading_Gear_400px.gif"
DEFAULT_IMAGE_PATH = "Images/image.png"
PATH_REPORT = "Reports\\"
VERSION = "1.0.0"

# Java complete path
#JAVA_PATH = "C:\\Program Files\\Java\\jre1.8.0_281\\bin\\java.exe"

# RESERVED words
SAFETY = "SAFETY"
SECURITY = "SECURITY"
PRIVACY = "PRIVACY"
RELIABILITY = "RELIABILITY"
PERFORMANCE = "PERFORMANCE"

provided_in_wrong_order = 1
provided_too_early = 2
provided_too_late = 3
not_provided = 4
provided = 5
applied_too_long = 6
stopped_too_son = 7

# Database data
DB_ID_CONTROLLER = 1
DB_ID_ACTUATOR = 2
DB_ID_CP = 3
DB_ID_SENSOR = 4
DB_ID_INPUT = 5
DB_ID_OUTPUT = 6
DB_ID_EXT_INFORMATION = 7
DB_ID_ALGORITHM = 8
DB_ID_PROCESS_MODEL = 9
DB_ID_ENV_DISTURBANCES = 10
DB_ID_HLC = 11

# Database UCA Type
DB_ID_UT_PWO = 1
DB_ID_UT_PTE = 2
DB_ID_UT_PTL = 3
DB_ID_UT_NP = 4
DB_ID_UT_P = 5
DB_ID_UT_ATL = 6
DB_ID_UT_STS = 7

# Database Control Action
DB_ID_ACT_CACA = 1
DB_ID_ACT_CACCP = 2
DB_ID_ACT_FCP = 3
DB_ID_ACT_CAHC = 4
DB_ID_ACT_CAHCP = 5
DB_ID_ACT_FCH = 6


# Control structure analysis variables
ACTUATOR = "Actuator"
ALGORITHM = "Algorithm"
CONTEXT = "Context"
CONTROL_ACTION = "Control_action"
CONTROL_ACTION_ACTUATOR = "Control_action_actuator"
CONTROL_ACTION_CP = "Control_action_CP"
CONTROL_ACTION_HLC_CONTROLLER = "Control_action_HLC_controller"
CONTROL_ACTION_HLC_CP = "Control_action_HLC_CP"
CONTROLLED_PROCESS = "CP"
CONTROLLED_PROCESS_full_name = "Controlled_process_CP"
CONTROLLER = "Controller"
CONTROLLER_CONSTANTS = "Controller_constraints"
EXTERNAL_INFORMATION = "External-information"
EXTERNAL_INFORMATION_SENT = "External-information-sent"
EXTERNAL_INFORMATION_RECEIVED = "External-information-received"
ENVIRONMENTAL_DISTURBANCES = "Environmental_disturbances"
FEEDBACK_OF_CONTROLLER = "Feedback_of_controller"
FEEDBACK_OF_CP = "Feedback_of_CP"
HIGH_LEVEL_CONTROLLER = "HLC"
INPUT = "Input"
LINK = "Link"
LINK_ACTUATOR_CP = "Link_actuator_CP"
LINK_CONTROLLER_ACTUATOR = "Link_controller_actuator"
LINK_CONTROLLER_CP = "Link_controller_CP"
LINK_CONTROLLER_EXT_INF = "Link_controller_external-information"
LINK_CONTROLLER_HLC = "Link_controller_HLC"
LINK_CP_CONTROLLER = "Link_CP_controller"
LINK_CP_HLC = "Link_CP_HLC"
LINK_CP_SENSOR = "Link_CP_sensor"
LINK_EXT_INF_CONTROLLER = "Link_external-information_controller"
LINK_HLC_CONTROLLER = "Link_HLC_controller"
LINK_HLC_CP = "Link_HLC_CP"
LINK_SENSOR_CONTROLLER = "Link_sensor_controller"
LINK_SENSOR_HLC = "Link_sensor_HLC"
OUTPUT = "Output"
PROCESS_MODEL = "Process_model"
PROCESS_MODEL_full_name = "Process Model"
SENSOR = "Sensor"
VARIABLES = "Variables"
VALUES = "Values"


# Safety analysis variables
CAUSAL_FACTOR = "Causal_factor"
CAUSAL_FACTOR_A = "Causal_factor_A"
CAUSAL_FACTOR_B = "Causal_factor_B"
LOSS_MISHAP = "Loss_mishap"
LOSS_SCENARIO = "Loss_scenario"
LOSS_SCENARIO_A = "Loss_scenario_A"
LOSS_SCENARIO_B = "Loss_scenario_B"
SAFETY_REQUIREMENT = "Safety_recommendation"
TIME = "Saf_Time"
UCA = "UCA"
UCA_TYPE = "UCA_type"
UCA_RULE = "rule"
UCA_CELL = "cell"
CONTEXT = "Context"
HAZARDS = "Hazard"

DB_ID_EXTERNAL_ENTITY = 1
DB_ID_DATA_FLOW = 2
DB_ID_DATA_STORE = 3
DB_ID_PROCESS = 4


MUST = " must "
MUST_HAVE = " must have "
SHALL = " shall "
SHALL_HAVE = " shall have "
WHEN = " when "
BEFORE = " before "
AFTER = " after "
WHILE = " while "
FOR = " for "


VAR_ERR = "VAR_ERR"
VAL_ERR = "VAL_ERR"

DATETIME_MASK = "%d/%m/%Y %H:%M:%S"
DATETIME_MASK_FILE = "%d-%m-%Y_%H-%M-%S"
DATETIME_MASK_FILE_COPY = "%Y_%m_%d_%H_%M_%S"