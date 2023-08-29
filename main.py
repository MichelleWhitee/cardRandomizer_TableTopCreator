import random
import math
import os
import sys
import subprocess

from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QMenuBar
from dialog import Dialog
from PyQt5.QtCore import QLocale, QTranslator, QCoreApplication


filePath = "CSV_files"
outputPath = "output_CSV"

directories = [filePath, outputPath]
cf = 0

for dir in directories:
    if os.path.isdir(dir):
        pass
    else:
        os.mkdir(dir)


fileList = os.listdir(filePath)

if len(fileList) == 0:
    pass
else:
    cf = math.ceil(100 / len(fileList))

def CSV_shuffle(filePath):
    with open(filePath, 'r') as CSV_file:
        lines = [line for line in CSV_file.readlines() if not line.isspace()]

    header = lines[0]
    data = lines[1:]
    data[-1] = data[-1] + '\n'

    random.shuffle(data)

    filePath = filePath.split('/')
    filePath[1] = filePath[1].replace('.csv', '-randomized.csv')
    with open(outputPath + '/' + filePath[1], 'w') as outputFile:
        outputFile.write(header)
        outputFile.writelines(data[:-1])
        outputFile.write(data[-1].strip())

def partition(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]


def CSV_shuffleWithCut(filePath, val):

    with open(filePath, 'r') as CSV_file:
        lines = [line for line in CSV_file.readlines() if not line.isspace()]

    header = lines[0]
    data = lines[1:]
    data[-1] = data[-1] + '\n'

    random.shuffle(data)

    partitions = partition(data, int(val))

    part = 1
    for chunk in partitions:
        fileName = filePath.split('/')
        fileName[1] = fileName[1].replace('.csv', '-part-' + str(part) + '.csv')
        with open(outputPath + '/' + fileName[1], 'w') as outputFile:
            outputFile.write(header)
            outputFile.writelines(chunk[:-1])
            outputFile.write(chunk[-1].strip())

        part += 1




Ui_MainWindow, QMainWindow = uic.loadUiType("ui/mainWindow.ui")

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setFixedSize(492, 302)

        #Привязка кнопок
        self.randomize.clicked.connect(self.randomize_clicked)
        self.randomizeWithCut.clicked.connect(self.randomizeWithCut_clicked)
        self.update.clicked.connect(self.update_clicked)

        self.sourceFiles.clicked.connect(self.sourceFiles_clicked)
        self.outputFiles.clicked.connect(self.outputFiles_clicked)

        self.update.setIcon(QtGui.QIcon("imgs/update.png"))
        self.sourceFiles.setIcon(QtGui.QIcon("imgs/open.png"))
        self.outputFiles.setIcon(QtGui.QIcon("imgs/output.png"))

        #Темы
        self.MacOS.triggered.connect(self.MacOS_triggered)
        self.ElegantDark.triggered.connect(self.ElegantDark_triggered)
        self.Pink.triggered.connect(self.Pink_triggered)

        #Инициализация прогресс бара
        self.progressBar.setValue(0)
        self.progressBar.setFixedSize(391, 21)

        #Инициализация списка файлов
        for fileName in fileList:
            self.fileListEdit.append(fileName)

        #Диалоговое окно
        self.dialog = Dialog()

        #Локаль
        self.Russian.triggered.connect(self.Russian_triggered)
        self.English.triggered.connect(self.English_triggered)

        self.translator = QTranslator()


    def loadLanguage(self, language):
        self.translator.load(f"locale/{language}.qm")
        QApplication.instance().installTranslator(self.translator)

        self.retranslateUI()

    def retranslateUI(self):
        self.randomize.setText(self.tr("Перемешать"))
        self.randomizeWithCut.setText(self.tr("Перемешать \n с разбиением на части"))
        self.menu.setTitle(self.tr("Выбор темы"))

    def English_triggered(self):
        self.loadLanguage("mainWindow_en")

    def Russian_triggered(self):
        QApplication.instance().removeTranslator(self.translator)
        self.retranslateUI()

    def update_clicked(self):
        global fileList
        global cf

        fileList = os.listdir(filePath)
        if len(fileList) == 0:
            pass
        else:
            cf = math.ceil(100 / len(fileList))

        self.fileListEdit.clear()
        for fileName in fileList:
            self.fileListEdit.append(fileName)


    def sourceFiles_clicked(self):
        try:
            subprocess.Popen(["explorer", filePath])
        except Exception as e:
            print("Ошибка при открытии папки исходников")

    def outputFiles_clicked(self):
        try:
            subprocess.Popen(["explorer", outputPath])
        except Exception as e:
            print("Ошибка при открытии папки вывода")


    def randomize_clicked(self):
        if len(fileList) == 0:
            self.fileListEdit.setPlainText('Папка "CSV_files" пуста')
        else:
            for fileName in fileList:
                if fileName.endswith('.csv') and os.path.isfile(filePath + '/' + fileName):
                    CSV_shuffle(filePath + '/' + fileName)
                else:
                    pass

                self.update_progress()

            self.progressBar.setValue(0)

            messageBox = QMessageBox(self)
            messageBox.setWindowTitle("Успех")
            messageBox.setIcon(QMessageBox.Information)
            messageBox.setText("Выполнено !")
            messageBox.setDefaultButton(QMessageBox.Ok)
            messageBox.exec_()


    def randomizeWithCut_clicked(self):
        result = self.dialog.exec_()
        if result == QDialog.Accepted:
            val = self.dialog.cutValue.text()
            if len(fileList) == 0:
                self.fileListEdit.setPlainText('Папка "CSV_files" пуста')
            else:
                for fileName in fileList:
                    if fileName.endswith('.csv') and os.path.isfile(filePath + '/' + fileName):
                        CSV_shuffleWithCut(filePath + '/' + fileName, val)
                    else:
                        pass

                    self.update_progress()

                self.progressBar.setValue(0)

                messageBox = QMessageBox(self)
                messageBox.setWindowTitle("Успех")
                messageBox.setIcon(QMessageBox.Information)
                messageBox.setText("Выполнено !")
                messageBox.setDefaultButton(QMessageBox.Ok)
                messageBox.exec_()


    def update_progress(self):
        currentValue = self.progressBar.value()
        if currentValue < 100:
            self.progressBar.setValue(currentValue + cf)

    def MacOS_triggered(self):
        file = QtCore.QFile("themes/MacOS.qss")
        file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        style = file.readAll().data().decode('utf-8')
        self.setStyleSheet(style)
        self.dialog.setStyleSheet(style)

    def ElegantDark_triggered(self):
        file = QtCore.QFile("themes/ElegantDark.qss")
        file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        style = file.readAll().data().decode('utf-8')
        self.setStyleSheet(style)
        self.dialog.setStyleSheet(style)


    def Pink_triggered(self):
        file = QtCore.QFile("themes/Pink.qss")
        file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        style = file.readAll().data().decode('utf-8')
        self.setStyleSheet(style)
        self.dialog.setStyleSheet(style)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowIcon(QtGui.QIcon('imgs/YoumuAava.ico'))
    window.show()
    sys.exit(app.exec())


