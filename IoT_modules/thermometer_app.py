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

    def __init__(self, parent=None):

        super(ThermometerApp, self).__init__(parent)

        self.resize(150, 150)

        self.originalPalette = QApplication.palette()






        # MAIN UI
        mainlayout = QGridLayout()
        mainlayout.addWidget(self.GroupBox, 1, 1)
        mainlayout.setRowStretch(1, 1)
        mainlayout.setRowStretch(2, 1)
        mainlayout.setColumnStretch(0, 1)
        mainlayout.setColumnStretch(1, 1)
        self.setLayout(mainlayout)
        self.setWindowTitle("Thermometer Application")
        self.changeStyle('Fusion')



