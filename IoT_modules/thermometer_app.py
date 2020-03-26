"""
Winter2020 - Concordia University
COEN446 - Internet Of Things
THERMOMETER APPLICATION
"""
import sys, threading, socket, json, datetime
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

############################################ VARIABLE DECLARATION ############################################
HEADER_LENGTH = 10
HOST, PORT = "localhost", 9999

user_database = {}
connected_users = {}
###################################### END OF VARIABLE DECLARATION ###########################################


def create_packet(payload):
    """
    Format outgoing messages to a standard TCP packet with HEADER_LENGTH + payload
    :param payload: string
    :return encoded_payload_header, encoded_payload: bytes, bytes
    """
    encoded_payload = payload.encode("utf-8")
    encoded_payload_header = f"{len(encoded_payload):<{HEADER_LENGTH}}".encode("utf-8")
    return encoded_payload_header, encoded_payload


###################################### VARIOUS THERMOMETER APP FUNCTIONS #####################################
def syn_ack(sock, device_name):
    """
    Function used during connection establishment; communicates device info to broker
    :param sock: TCP socket
    :param device_name: string
    """
    payload_dict = {
                "device": device_name,
                "action": "SYN_ACK",
                "topics_of_interest": ["DOOR_STATUS", "USER_MANAGEMENT"]
            }
    encoded_payload_header, encoded_payload = create_packet(json.dumps(payload_dict))
    sock.sendall(encoded_payload_header + encoded_payload)
################################ END OF VARIOUS THERMOMETER APP FUNCTIONS ####################################


############################################ LISTENING THREAD ################################################
class ListenThread(threading.Thread):
    """
    Listening Thread is used to capture topics published by the Broker which the Thermometer App is subscribed 
    to
    """
    def __init__(self, _sock, _temperatureDial, _recentUser):
        threading.Thread.__init__(self)
        self.sock = _sock
        self.temperatureDial = _temperatureDial
        self.recentUser = _recentUser
        self.time_stamp = ""
        print("Listening Thread started")

    def run(self):
        """
        Thread listens to incoming messages services the message immediately
        """
        while True:
            # LISTENING FOR INCOMING MESSAGES
            payload_header = int(self.sock.recv(HEADER_LENGTH).decode("utf-8"))
            payload_string = self.sock.recv(payload_header).decode("utf-8")
            payload_dict = json.loads(payload_string)
            self.time_stamp = str(datetime.datetime.now())[:19]

            if payload_dict['notification'] == "ADD_NEW_USER":
                user_database.update({payload_dict['user_info'][0]: payload_dict['user_info'][1]})
            elif payload_dict['notification'] == "DELETE_USER" and payload_dict['user_info'][0] in user_database:
                user_database.pop(payload_dict['user_info'][0])
            elif payload_dict['notification'] == "ENTERING" and payload_dict['user_info'][0] in user_database:
                # TODO check if already connected
                connected_users.update({payload_dict['user_info'][0]: self.time_stamp})
                self.set_temp(str(list(connected_users.keys())[0]), user_database[str(list(connected_users.keys())[0])])
            elif payload_dict['notification'] == "LEAVING" and payload_dict['user_info'][0] in connected_users:
                connected_users.pop(payload_dict['user_info'][0])
                if len(connected_users) > 0:
                    self.set_temp(str(list(connected_users.keys())[0]), user_database[str(list(connected_users.keys())[0])])
                else:
                    self.set_temp("VACANT", "15")

    def set_temp(self, user_name, user_temp):
        """
        Function used to set the temperature depending on who (or who is not) in the house
        :param user_name: string
        "param user_temp: string"
        :return:
        """
        if user_name != "VACANT":
            print(user_name, user_temp, connected_users[user_name])
            self.temperatureDial.setValue(int(user_temp))
            self.recentUser.setText(user_name + " @ " + connected_users[user_name])
        elif user_name == "VACANT":
            print("VACANT", "15", self.time_stamp)
            self.temperatureDial.setValue(15)
            self.recentUser.setText(user_name + " @ " + self.time_stamp)
######################################## END OF LISTENING THREAD #############################################


############################################ THERMOMETER GUI #################################################
class ThermometerApp(QDialog):
    """
    PyQt5 GUI class; contains GUI and functions pertaining to management app
    """
    def __init__(self, sock, parent = None):
        """
        Generate GUI upon initialization
        :parak sock: TCP socket
        :param parent: None
        """
        self.sock = sock
        syn_ack(self.sock, "thermometer_app")
        temp = 15
        first_user = "VACANT"
        self.time_stamp = str(datetime.datetime.now())[:19]
        super(ThermometerApp, self).__init__(parent)
        self.resize(300, 150)
        self.originalPalette = QApplication.palette()

        # CENTER BOX
        self.centerGroupBox = QGroupBox("Temperature Setting")
        self.centerGroupBox.setAlignment(Qt.AlignCenter)
        self.recentUser = QLabel()
        self.recentUser.setAlignment(Qt.AlignCenter)
        self.recentUser.setText( first_user + " @ " + self.time_stamp)
        temperatureFont = QFont("Helvatica", 8)
        temperatureLabel = QLabel("Select Temperature")
        temperatureLabel.setAlignment(Qt.AlignCenter)
        temperatureLabel.setFont(temperatureFont)
        temperatureCelsius = QLabel("Degree Celsius°")
        temperatureCelsius.setFont(temperatureFont)
        temperatureCelsius.setAlignment(Qt.AlignCenter)
        temperatureLCDNumber = QLCDNumber()
        temperatureLCDNumber.display(temp)
        self.temperatureDial = QDial(self.centerGroupBox)
        self.temperatureDial.setDisabled(1)
        self.temperatureDial.setMinimum(0)
        self.temperatureDial.setMaximum(30)
        self.temperatureDial.setValue(temp)
        self.temperatureDial.setNotchesVisible(True)
        self.temperatureDial.valueChanged.connect(temperatureLCDNumber.display)
        thermoLayout = QVBoxLayout()
        temperatureTitleLayout = QHBoxLayout()
        temperatureTitleLayout.addWidget(temperatureLabel)
        temperatureTitleLayout.addWidget(temperatureCelsius)
        temperatureLayout = QHBoxLayout()
        temperatureLayout.addWidget(self.temperatureDial)
        temperatureLayout.addWidget(temperatureLCDNumber)
        thermoLayout.addWidget(self.recentUser)
        thermoLayout.addLayout(temperatureTitleLayout)
        thermoLayout.addLayout(temperatureLayout)
        thermoLayout.addStretch(1)
        self.centerGroupBox.setLayout(thermoLayout)

        # MAIN UI
        mainlayout = QGridLayout()
        mainlayout.setRowStretch(1, 1)
        mainlayout.setRowStretch(2, 1)
        mainlayout.setColumnStretch(0, 1)
        mainlayout.setColumnStretch(1, 1)
        self.setLayout(thermoLayout)
        self.setWindowTitle("Thermometer Application")
        self.changeStyle('Fusion')

        listening_thread = ListenThread(self.sock, self.temperatureDial, self.recentUser)
        listening_thread.daemon = True
        listening_thread.start()

    def changeStyle(self, styleName):
        """
        Used for GUI design; called during initialization
        :param styleName: string
        :return:
        """
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        """
        Used for GUI design; called from changeStyle
        :return:
        """
        QApplication.setPalette(self.originalPalette)
######################################## END OF THERMOMETER GUI ##############################################


###################################################### MAIN ##################################################
if __name__ == '__main__':
    app = QApplication(sys.argv)
# Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        thermometerApp = ThermometerApp(sock)
        thermometerApp.show()
        sys.exit(app.exec_())
################################################## END OF MAIN ################################################
