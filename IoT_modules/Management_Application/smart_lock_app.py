"""
Winter2020 - Concordia University
COEN446 - Internet Of Things
SMART LOCK APPLICATION
"""
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys


class SmartLockApp(QDialog):
    """

    """

    def __init__(self, parent=None):
        """

        :param parent:
        """
        super(SmartLockApp, self).__init__(parent)

        self.resize(700, 500)

        self.originalPallette = QApplication.palette()

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



    def userEntering(self):
        """
        TODO
        :return:
        """
        print("ENTERING")

    def userLeaving(self):
        """
        TODO
        :return:
        """
        print("LEAVING")
