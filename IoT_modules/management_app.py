"""
Winter2020 - Concordia University
COEN446 - Internet Of Things
MANAGEMENT APPLICATION
"""
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys


class ManagementApp(QDialog):
    """

    """
    def __init__(self, parent=None):
        """

        :param parent:
        """
        super(ManagementApp, self).__init__(parent)

        self.resize(700, 100)

        self.originalPalette = QApplication.palette()

        # LEFT BOX
        self.leftGroupBox = QGroupBox("Users")
        self.userTableWidget = QTableWidget(0, 3)
        layout = QVBoxLayout()
        layout.addWidget(self.userTableWidget)
        layout.addStretch(1)
        self.leftGroupBox.setLayout(layout)

        # RIGHT BOX
        self.rightGroupBox = QGroupBox("New User")
        self.newUserLineEdit = QLineEdit()
        self.newUserLineEdit.setPlaceholderText("Enter Username")
        addUserPushButton = QPushButton("Add User")
        addUserPushButton.setDefault(True)
        addUserPushButton.clicked.connect(self.addNewUser)
        deleteUserPushButton = QPushButton("Delete User")
        deleteUserPushButton.setDefault(True)
        deleteUserPushButton.clicked.connect(self.deleteUser)
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
        layout.addWidget(deleteUserPushButton)
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

        :return:
        """
        if self.newUserLineEdit.text() == "":
            self.newUserLineEdit.setPlaceholderText("Enter Username")
        else:
            self.userTableWidget.insertRow(self.userTableWidget.rowCount())
            newUserName = QTableWidgetItem(self.newUserLineEdit.text())
            newUserTemp = QTableWidgetItem(str(self.temperatureDial.value()))
            newUserStatus = QTableWidgetItem("Connected")
            self.userTableWidget.setItem(self.userTableWidget.rowCount() - 1, 0, newUserName)
            self.userTableWidget.setItem(self.userTableWidget.rowCount() - 1, 1, newUserTemp)
            self.userTableWidget.setItem(self.userTableWidget.rowCount() - 1, 2, newUserStatus)
            self.newUserLineEdit.setText("")

    def deleteUser(self):
        """

        :return:
        """
        if self.userTableWidget.rowCount() > 0:
            self.userTableWidget.removeRow(self.userTableWidget.row(self.userTableWidget.selectedItems()[0]))

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
    import sys

    app = QApplication(sys.argv)
    managementApp = ManagementApp()
    managementApp.show()
    sys.exit(app.exec_())
