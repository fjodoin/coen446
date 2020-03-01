"""
Winter2020 - Concordia University
COEN446 - Internet Of Things
MANAGEMENT APPLICATION
"""
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys


class ThermometerApp(QDialog):
    """

    """

    def __init__(self, parent = None):
        temp = 15
        first_user = "VACANT    "
        time_stamp = ""


        super(ThermometerApp, self).__init__(parent)

        self.resize(300, 150)

        self.originalPalette = QApplication.palette()

        # RIGHT BOX
        self.rightGroupBox = QGroupBox("Temperature Setting")
        self.rightGroupBox.setAlignment(Qt.AlignCenter)
        self.firstUser = QLabel()
        self.firstUser.setAlignment(Qt.AlignCenter)
        self.firstUser.setText( first_user+time_stamp)
        temperatureFont = QFont("Helvatica", 8)
        temperatureLabel = QLabel("Select Temperature")
        temperatureLabel.setAlignment(Qt.AlignCenter)
        temperatureLabel.setFont(temperatureFont)
        temperatureCelsius = QLabel("Degree Celsius°")
        temperatureCelsius.setFont(temperatureFont)
        temperatureCelsius.setAlignment(Qt.AlignCenter)
        temperatureLCDNumber = QLCDNumber()
        temperatureLCDNumber.display(temp)
        self.temperatureDial = QDial(self.rightGroupBox)
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
        thermoLayout.addWidget(self.firstUser)
        thermoLayout.addLayout(temperatureTitleLayout)
        thermoLayout.addLayout(temperatureLayout)
        thermoLayout.addStretch(1)
        self.rightGroupBox.setLayout(thermoLayout)

        # MAIN UI
        mainlayout = QGridLayout()
        mainlayout.setRowStretch(1, 1)
        mainlayout.setRowStretch(2, 1)
        mainlayout.setColumnStretch(0, 1)
        mainlayout.setColumnStretch(1, 1)
        self.setLayout(thermoLayout)
        self.setWindowTitle("Thermometer Application")
        self.changeStyle('Fusion')

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
    thermometerApp = ThermometerApp()
    thermometerApp.show()
    sys.exit(app.exec_())
