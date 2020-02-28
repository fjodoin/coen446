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
    TODO
    """

    def __init__(self, parent=None):
        """
        TODO
        :param parent:
        """
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
    smartLockApp = SmartLockApp()
    smartLockApp.show()
    sys.exit(app.exec_())

