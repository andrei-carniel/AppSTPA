import Constant
from Constant import LINK_HLC_CONTROLLER

elements = {}
saf_elements = {}
DOOR_POSITION = "Door_Position"
DOOR_STATE = "Door_State"
TRAIN_MOTION = "Train_Motion"
TRAIN_POSITION = "Train_Position"
TRAIN_EMERGENCY = "Emergency"

# clean and init with default values
def init_default_elements_dictionary():
    elements.clear()

    # Control structure and safety initialize
    elements[Constant.ACTUATOR] = Constant.ACTUATOR
    elements[Constant.ALGORITHM] = Constant.ALGORITHM
    elements[Constant.CONTROL_ACTION_ACTUATOR] = [Constant.CONTROL_ACTION_ACTUATOR]
    elements[Constant.CONTROL_ACTION_CP] = [Constant.CONTROL_ACTION_CP]
    elements[Constant.CONTROL_ACTION_HLC_CONTROLLER] = [Constant.CONTROL_ACTION_HLC_CONTROLLER]
    elements[Constant.CONTROL_ACTION_HLC_CP] = [Constant.CONTROL_ACTION_HLC_CP]
    elements[Constant.CONTROLLED_PROCESS] = Constant.CONTROLLED_PROCESS
    elements[Constant.CONTROLLER] = Constant.CONTROLLER
    elements[Constant.EXTERNAL_INFORMATION] = [Constant.EXTERNAL_INFORMATION]
    elements[Constant.ENVIRONMENTAL_DISTURBANCES] = [Constant.ENVIRONMENTAL_DISTURBANCES]
    elements[Constant.FEEDBACK_OF_CONTROLLER] = [Constant.FEEDBACK_OF_CONTROLLER]
    elements[Constant.FEEDBACK_OF_CP] = [Constant.FEEDBACK_OF_CP]
    elements[Constant.HIGH_LEVEL_CONTROLLER] = Constant.HIGH_LEVEL_CONTROLLER
    elements[Constant.INPUT] = [Constant.INPUT]
    elements[Constant.LINK_ACTUATOR_CP] = Constant.LINK_ACTUATOR_CP
    elements[Constant.LINK_CONTROLLER_ACTUATOR] = Constant.LINK_CONTROLLER_ACTUATOR
    elements[Constant.LINK_CONTROLLER_CP] = Constant.LINK_CONTROLLER_CP
    elements[Constant.LINK_CONTROLLER_HLC] = Constant.LINK_CONTROLLER_HLC
    elements[Constant.LINK_CP_SENSOR] = Constant.LINK_CP_SENSOR
    elements[Constant.LINK_HLC_CP] = Constant.LINK_HLC_CP
    elements[Constant.LINK_HLC_CONTROLLER] = Constant.LINK_HLC_CONTROLLER
    elements[Constant.LINK_SENSOR_CONTROLLER] = Constant.LINK_SENSOR_CONTROLLER
    elements[Constant.LINK_SENSOR_HLC] = Constant.LINK_SENSOR_HLC
    elements[Constant.OUTPUT] = [Constant.OUTPUT]
    elements[Constant.PROCESS_MODEL] = Constant.PROCESS_MODEL
    elements[Constant.SENSOR] = Constant.SENSOR
    elements[Constant.UCA_TYPE] = ["not provided", "provided", "provided too early", "provided too long", "provided out of order", "stopped too soon", "applied to long"]





# clean and init names of elements
def init_elements_dictionary():
    elements.clear()

    elements[Constant.ACTUATOR] = "Train Door Actuator"
    elements[Constant.ALGORITHM] = "Train Door Algorithm"
    elements[Constant.CONTROL_ACTION_ACTUATOR] = ["Open Door", "Stop Opening Door", "Close Door", "Stop Closing Door"]
    elements[Constant.CONTROL_ACTION_CP] = []
    elements[Constant.CONTROL_ACTION_HLC_CONTROLLER] = []
    elements[Constant.CONTROL_ACTION_HLC_CP] = []
    elements[Constant.CONTROLLED_PROCESS] = "Physical Door"
    elements[Constant.CONTROLLER] = "Train Door Controller"
    elements[Constant.EXTERNAL_INFORMATION] = ["Train_Motion", "Train_Position", "Emergency"]
    elements[Constant.ENVIRONMENTAL_DISTURBANCES] = ["Environmental disturbances"]
    elements[Constant.FEEDBACK_OF_CONTROLLER] = ["teste to DELETE"]
    elements[Constant.FEEDBACK_OF_CP] = ["Door_Position", "Door_State"]
    elements[Constant.HIGH_LEVEL_CONTROLLER] = ""
    elements[Constant.INPUT] = ["Passengers entering", "Passengers exiting"]
    elements[Constant.LINK_ACTUATOR_CP] = "Link_actuator_CP"
    elements[Constant.LINK_CONTROLLER_ACTUATOR] = "Link_controller_actuator"
    elements[Constant.LINK_CONTROLLER_CP] = "Link_controller_CP"
    elements[Constant.LINK_CONTROLLER_HLC] = "Link_controller_HLC"
    elements[Constant.LINK_CP_SENSOR] = "Link_CP_sensor"
    elements[Constant.LINK_HLC_CP] = "Link_HLC_CP"
    elements[Constant.LINK_HLC_CONTROLLER] = "Link_HLC_controller"
    elements[Constant.LINK_SENSOR_CONTROLLER] = "Link_sensor_controller"
    elements[Constant.LINK_SENSOR_HLC] = "Link_sensor_HLC"
    elements[Constant.OUTPUT] = ["Passengers in of the train", "Passengers out of the train"]
    elements[Constant.PROCESS_MODEL] = "Train Process Model"
    elements[Constant.SENSOR] = "Door Sensors"
    elements[Constant.UCA_TYPE] = ["provided", "not provided", "provided too early", "provided too long", "provided out of order", "stopped too soon", "applied to long"]



    # Security initialize
    elements[Constant.SEC_SECURITY_REQUIREMENT] = [Constant.SEC_SECURITY_REQUIREMENT]

    elements[Constant.SEC_SPOOFING] = ["ARP spoofing", "IP spoofing", "DNS spoofing", "DNS Compromise", "IP redirection"]
    elements[Constant.SEC_TAMPERING] = ["Modifies links or redirects", "Modifies your code", "Modifies data they’ve supplied to your API", "Enhances spoofing attacks"]
    elements[Constant.SEC_REPUDIATION] = ["Claims to have not clicked", "Claims to have not received", "Claims to have been a fraud victim", "Uses someone else’s account"]
    elements[Constant.SEC_INFORMATION_DISCLOSURE] = ["Gets data from logs or temp files", "Reads data on the network", "Sees interesting information in filenames", "Finds files protected by obscurity"]
    elements[Constant.SEC_DENIAL_OF_SERVICE] = ["Absorbs CPU", "Consumes network resources", "Makes enough requests to slow down the system", "Absorbs memory (RAM or disk)"]
    elements[Constant.SEC_ELEVATION_OF_PRIVILEGE] = ["Send inputs that the code doesn’t handle properly", "Gains access to read or write memory inappropriately", "Modifies bits on disk to do things other than what the authorized user intends"]

    elements[Constant.SEC_SPOOFING_CONTROL] = ["IPSec", "DNSSEC", "SSH host keys", "HTTP Digest or Basic authentication"]
    elements[Constant.SEC_TAMPERING_CONTROL] = ["ACLs or permissions", "Digital signatures", "SSL", "SSH"]
    elements[Constant.SEC_REPUDIATION_CONTROL] = ["Logging", "Log analysis tools", "Security log storage", "Digital signatures"]
    elements[Constant.SEC_INFORMATION_DISCLOSURE_CONTROL] = ["ACLs/permissions", "Encryption", "Mix networks", "Steganography"]
    elements[Constant.SEC_DENIAL_OF_SERVICE_CONTROL] = ["Filters", "Quotas (rate limitin, thresholding, throttling", "High-availability design", "Extra bandwidth"]
    elements[Constant.SEC_ELEVATION_OF_PRIVILEGE_CONTROL] = ["ACLs", "Group or role membership", "Role based access control", "Unix sudo"]


# clean and init names of Safety elements
def init_safety_elements_dictionary():
    saf_elements.clear()
    
    saf_elements[DOOR_POSITION] = ["Fully_Open", "Fully_Closed", "Partially Open"]
    saf_elements[DOOR_STATE] = ["Person_in_doorway", "Person_not_in_doorway"]
    saf_elements[TRAIN_POSITION] = ["Aligned_with_platform", "Not_aligned_with_platform"]
    saf_elements[TRAIN_MOTION] = ["Stopped", "Train_is_moving"]
    saf_elements[TRAIN_EMERGENCY] = ["No_emergency", "Evacuation_required"]


def get_list(name):
    try:
        aux_list = elements[name]
        if not isinstance(aux_list, list):
            aux_list = []
    except:
        aux_list = []

    return aux_list
