"""
Winter2020 - Concordia University
COEN446 - Internet Of Things
MANAGEMENT APPLICATION
"""
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import threading
import socket
import json
import datetime
import time


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


# Listen Thread
class ListenThread(threading.Thread):
    def __init__(self, _sock, _temperatureDial, _recentUser):
        threading.Thread.__init__(self)
        self.sock = _sock
        self.temperatureDial = _temperatureDial
        self.recentUser = _recentUser
        print("Listening Thread started")

    def run(self):
        while True:
            # LISTENING FOR INCOMING MESSAGES
            payload_header = int(self.sock.recv(HEADER_LENGTH).decode("utf-8"))
            print("PACKET RECEIVED")
            payload_string = self.sock.recv(payload_header).decode("utf-8")
            payload_dict = json.loads(payload_string)
            time_stamp = str(datetime.datetime.now())[:19]
            self.temperatureDial.setValue(int(payload_dict['temperature']))
            self.recentUser.setText(payload_dict['user'] + " @ " + time_stamp)

# Echo Thread -- Used for testing Listening Thread
# class EchoThread(threading.Thread):
#     def __init__(self, _sock):
#         threading.Thread.__init__(self)
#         self.sock = _sock
#         self.start_temp = "10"
#         print("Echo Thread started")

#     def run(self):
#         while True:
#             # LISTENING FOR INCOMING MESSAGES
#             message = {
#                 "user": "user1",
#                 "temperature": self.start_temp
#             }
#             message = json.dumps(message)
#             encoded_message_header, encoded_message = create_packet(message)
#             self.sock.sendall(encoded_message_header + encoded_message)
#             self.start_temp = int(self.start_temp) + 1
#             time.sleep(2)


class ThermometerApp(QDialog):
    """
    TODO
    """
    def __init__(self, sock, parent = None):
        """
        TODO
        """
        self.sock = sock
        syn_ack(self.sock, "thermometer_app")
        temp = 15
        first_user = "VACANT"
        time_stamp = str(datetime.datetime.now())[:19]
        super(ThermometerApp, self).__init__(parent)
        self.resize(300, 150)
        self.originalPalette = QApplication.palette()

        # CENTER BOX
        self.centerGroupBox = QGroupBox("Temperature Setting")
        self.centerGroupBox.setAlignment(Qt.AlignCenter)
        self.recentUser = QLabel()
        self.recentUser.setAlignment(Qt.AlignCenter)
        self.recentUser.setText( first_user + " @ " + time_stamp)
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
        listening_thread.start()

        # Used for testing Listen Thread
        # echo_thread = EchoThread(self.sock)
        # echo_thread.start()

    def changeStyle(self, styleName):
        """

        :param styleName:
        :return:
        """
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        """

        :return:
        """
        QApplication.setPalette(self.originalPalette)



if __name__ == '__main__':
    app = QApplication(sys.argv)
# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    thermometerApp = ThermometerApp(sock)
    thermometerApp.show()
    sys.exit(app.exec_())
