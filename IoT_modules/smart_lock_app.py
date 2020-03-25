"""
Winter2020 - Concordia University
COEN446 - Internet Of Things
SMART LOCK APPLICATION
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
        "topic_to_publish": "DOOR_STATUS"
    }
    encoded_payload_header, encoded_payload = create_packet(json.dumps(payload_dict))
    sock.sendall(encoded_payload_header + encoded_payload)
################################ END OF VARIOUS MANAGEMENT APP FUNCTIONS #####################################


########################################## SMART LOCK APP GUI ################################################
class SmartLockApp(QDialog):
    """
    PyQt5 GUI class; contains GUI and functions pertaining to smart lock app
    """
    def __init__(self, sock, parent=None):
        """
        Generate GUI upon initialization
        :parak sock: TCP socket
        :param parent: None
        """
        self.sock = sock
        syn_ack(self.sock, "smart_lock")

        super(SmartLockApp, self).__init__(parent)
        self.resize(700, 100)
        self.originalPalette = QApplication.palette()

        # LEFT BOX
        self.leftGroupBox = QGroupBox("User")
        self.userLineEdit = QLineEdit()
        self.userLineEdit.setPlaceholderText("Enter Username")
        enteringPushButton = QPushButton("Entering")
        enteringPushButton.setDefault(True)
        enteringPushButton.clicked.connect(self.userEntering)
        leavingPushButton = QPushButton("Leaving")
        leavingPushButton.setDefault(True)
        leavingPushButton.clicked.connect(self.userLeaving)
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.userLineEdit)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(enteringPushButton)
        buttonLayout.addWidget(leavingPushButton)
        leftLayout.addLayout(buttonLayout)
        leftLayout.addStretch(1)
        self.leftGroupBox.setLayout(leftLayout)

        # RIGHT BOX
        self.rightGroupBox = QGroupBox()
        self.messageTextEdit = QTextEdit()
        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.messageTextEdit)
        rightLayout.addStretch(1)
        self.rightGroupBox.setLayout(rightLayout)


        # MAIN UI
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.leftGroupBox, 1, 0)
        mainLayout.addWidget(self.rightGroupBox, 1, 1)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)
        self.setWindowTitle("Smart Lock Application")
        self.changeStyle('Fusion')

    def userEntering(self):
        """
        Communicates that a user is ENTERING to the broker via topic publishing
        :return:
        """
        user = self.userLineEdit.text()
        if len(user) > 0:
            messageFont = QFont("Helvatica", 16)
            message = "Welcome " + user
            self.messageTextEdit.setText(message)
            self.messageTextEdit.setFont(messageFont)
            self.userLineEdit.setText("")
            payload_dict = {
                "device": "smart_lock",
                "action": "ENTERING",
                "user_info": [user]
            }
            encoded_payload_header, encoded_payload = create_packet(json.dumps(payload_dict))
            self.sock.sendall(encoded_payload_header + encoded_payload)
        else:
            self.userLineEdit.setText("")

    def userLeaving(self):
        """
        Communicates that a user IS LEAVING to the broker via topic publishing
        :return:
        """
        user = self.userLineEdit.text()
        if len(user) > 0:
            messageFont = QFont("Helvatica", 16)
            message = "Goodbye " + user
            self.messageTextEdit.setText(message)
            self.messageTextEdit.setFont(messageFont)
            self.userLineEdit.setText("")
            payload_dict = {
                "device": "smart_lock",
                "action": "LEAVING",
                "user_info": [user]
            }
            encoded_payload_header, encoded_payload = create_packet(json.dumps(payload_dict))
            self.sock.sendall(encoded_payload_header + encoded_payload)
        else:
            self.userLineEdit.setText("")

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
###################################### END OF SMART LOCK APP GUI #############################################


###################################################### MAIN ##################################################
if __name__ == '__main__':
    app = QApplication(sys.argv)
# Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        smartLockApp = SmartLockApp(sock)
        smartLockApp.show()
        sys.exit(app.exec_())
################################################## END OF MAIN ################################################
