import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5 import uic, QtGui

Ui_Dialog, QDialog = uic.loadUiType('ui/dialog.ui')


class Dialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setFixedSize(372, 106)

        self.setWindowIcon(QtGui.QIcon('imgs/YoumuAava.ico'))

        # Привязка кнопок
        self.randomizeWC.clicked.connect(self.randomizeWC_clicked)
        self.randomizeWC.clicked.connect(self.accept)

    def randomizeWC_clicked(self):
        self.close()