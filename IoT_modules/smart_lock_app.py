"""
Winter2020 - Concordia University
COEN446 - Internet Of Things
SMART LOCK APPLICATION
"""
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import threading
import socket
import json


HEADER_LENGTH = 10
HOST, PORT = "localhost", 9999


def create_packet(payload):
    encoded_payload = payload.encode("utf-8")
    encoded_payload_header = f"{len(encoded_payload):<{HEADER_LENGTH}}".encode("utf-8")
    return encoded_payload_header, encoded_payload

def syn_ack(sock, device_name):
    payload_dict = {
        "device": device_name,
        "action": "SYN_ACK"
    }
    encoded_payload_header, encoded_payload = create_packet(json.dumps(payload_dict))
    sock.sendall(encoded_payload_header + encoded_payload)
    print("Syn ack sent")


class SmartLockApp(QDialog):
    """
    TODO
    """
    def __init__(self, sock, parent=None):
        """
        TODO
        :param parent:
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
        TODO
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
                "user": user
            }
            encoded_payload_header, encoded_payload = create_packet(json.dumps(payload_dict))
            self.sock.sendall(encoded_payload_header + encoded_payload)
        else:
            self.userLineEdit.setText("")

    def userLeaving(self):
        """
        TODO
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
                "user": user
            }
            encoded_payload_header, encoded_payload = create_packet(json.dumps(payload_dict))
            self.sock.sendall(encoded_payload_header + encoded_payload)
        else:
            self.userLineEdit.setText("")

    def changeStyle(self, styleName):
        """
        # TODO
        :param styleName:
        :return:
        """
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        """
        # TODO
        :return:
        """
        QApplication.setPalette(self.originalPalette)


if __name__ == '__main__':
    app = QApplication(sys.argv)
# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    smartLockApp = SmartLockApp(sock)
    smartLockApp.show()
    sys.exit(app.exec_())

