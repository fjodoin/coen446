"""
Winter2020 - Concordia University
COEN446 - Internet Of Things
MANAGEMENT APPLICATION
"""
import sys, threading, socket, json
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


############################################ VARIABLE DECLARATION ############################################
HEADER_LENGTH = 10
HOST, PORT = "localhost", 9999
###################################### END OF VARIABLE DECLARATION ###########################################


###################################### VARIOUS MANAGEMENT APP FUNCTIONS ######################################
def create_packet(payload):
    """
    Format outgoing messages to a standard TCP packet with HEADER_LENGTH + payload
    :param payload: string
    :return encoded_payload_header, encoded_payload: bytes, bytes
    """
    encoded_payload = payload.encode("utf-8")
    encoded_payload_header = f"{len(encoded_payload):<{HEADER_LENGTH}}".encode("utf-8")
    return encoded_payload_header, encoded_payload


def syn_ack(sock, device_name):
	"""
	Function used during connection establishment; communicates device info to broker
	:param sock: TCP socket
	:param device_name: string
	"""
	payload_dict = {
	    "device": device_name,
	    "action": "SYN_ACK",
	    "topic_to_publish": "USER_MANAGEMENT"
	}
	encoded_payload_header, encoded_payload = create_packet(json.dumps(payload_dict))
	sock.sendall(encoded_payload_header + encoded_payload)
################################ END OF VARIOUS MANAGEMENT APP FUNCTIONS #####################################


########################################## MANAGEMENT APP GUI ################################################
class ManagementApp(QDialog):
    """
	PyQt5 GUI class; contains GUI and functions pertaining to management app
    """
    def __init__(self, sock, parent=None):
        """
		Generate GUI upon initialization
		:parak sock: TCP socket
        :param parent: None
        """
        self.sock = sock
        syn_ack(self.sock, "management_app")

        super(ManagementApp, self).__init__(parent)
        self.resize(500, 100)
        self.originalPalette = QApplication.palette()

        # LEFT BOX
        self.leftGroupBox = QGroupBox("Users")
        self.userTableWidget = QTableWidget(0, 2)
        deleteUserPushButton = QPushButton("Delete User")
        deleteUserPushButton.setDefault(True)
        deleteUserPushButton.clicked.connect(self.deleteUser)
        layout = QVBoxLayout()
        layout.addWidget(self.userTableWidget)
        layout.addWidget(deleteUserPushButton)
        layout.addStretch(1)
        self.leftGroupBox.setLayout(layout)

        # RIGHT BOX
        self.rightGroupBox = QGroupBox("New User")
        self.newUserLineEdit = QLineEdit()
        self.newUserLineEdit.setPlaceholderText("Enter Username")
        addUserPushButton = QPushButton("Add User")
        addUserPushButton.setDefault(True)
        addUserPushButton.clicked.connect(self.addNewUser)
        temperatureFont = QFont("Helvatica", 8)
        temperatureLabel = QLabel("Select Temperature")
        temperatureLabel.setFont(temperatureFont)
        temperatureCelsius = QLabel("Degree Celsius°")
        temperatureCelsius.setFont(temperatureFont)
        temperatureLCDNumber = QLCDNumber()
        temperatureLCDNumber.display(20)
        self.temperatureDial = QDial(self.rightGroupBox)
        self.temperatureDial.setMinimum(0)
        self.temperatureDial.setMaximum(30)
        self.temperatureDial.setValue(20)
        self.temperatureDial.setNotchesVisible(True)
        self.temperatureDial.valueChanged.connect(temperatureLCDNumber.display)
        layout = QVBoxLayout()
        temperatureTitleLayout = QHBoxLayout()
        temperatureTitleLayout.addWidget(temperatureLabel)
        temperatureTitleLayout.addWidget(temperatureCelsius)
        temperatureLayout = QHBoxLayout()
        temperatureLayout.addWidget(self.temperatureDial)
        temperatureLayout.addWidget(temperatureLCDNumber)
        layout.addWidget(self.newUserLineEdit)
        layout.addLayout(temperatureTitleLayout)
        layout.addLayout(temperatureLayout)
        layout.addWidget(addUserPushButton)
        layout.addStretch(1)
        self.rightGroupBox.setLayout(layout)

        # MAIN UI
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.leftGroupBox, 1, 0)
        mainLayout.addWidget(self.rightGroupBox, 1, 1)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)
        self.setWindowTitle("Management Application")
        self.changeStyle('Fusion')

    def addNewUser(self):
        """
		Adding new user to the Management App; communicates username and preferred temperature to the broker via topic publishing
        :return:
        """
        user = self.newUserLineEdit.text()
        if len(user) > 0:
            self.userTableWidget.insertRow(self.userTableWidget.rowCount())
            newUserName = QTableWidgetItem(self.newUserLineEdit.text())
            newUserTemp = QTableWidgetItem(str(self.temperatureDial.value()))
            self.userTableWidget.setItem(self.userTableWidget.rowCount() - 1, 0, newUserName)
            self.userTableWidget.setItem(self.userTableWidget.rowCount() - 1, 1, newUserTemp)
            payload_dict = {
                "device": "management_app",
                "action": "ADD_NEW_USER",
                "user_info": [self.newUserLineEdit.text(), str(self.temperatureDial.value())]
            }
            encoded_payload_header, encoded_payload = create_packet(json.dumps(payload_dict))
            self.sock.sendall(encoded_payload_header + encoded_payload)
            self.newUserLineEdit.setText("")
        else:
            self.newUserLineEdit.setText("")

    def deleteUser(self):
        """
		Remove existing user from the Management App; communicates username to the broker via topic publishing
        :return:
        """
        if (self.userTableWidget.rowCount() > 0) and (len(self.userTableWidget.selectedItems()) > 0):
            deleted_user_row = self.userTableWidget.selectedItems()[0]
            deleted_user = self.userTableWidget.item(deleted_user_row.row(), 0).data(0)
            self.userTableWidget.removeRow(self.userTableWidget.row(self.userTableWidget.selectedItems()[0]))
            payload_dict = {
                "device": "management_app",
                "action": "DELETE_USER",
                "user_info": [deleted_user]
            }
            encoded_payload_header, encoded_payload = create_packet(json.dumps(payload_dict))
            self.sock.sendall(encoded_payload_header + encoded_payload)

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
###################################### END OF MANAGEMENT APP GUI #############################################


###################################################### MAIN ##################################################
if __name__ == '__main__':
	app = QApplication(sys.argv)
	# Create a socket (SOCK_STREAM means a TCP socket)
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
	    # Connect to server and send data
	    sock.connect((HOST, PORT))
	    managementApp = ManagementApp(sock)
	    managementApp.show()
	    sys.exit(app.exec_())
################################################## END OF MAIN ################################################
