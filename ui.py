# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/bill/Documents/PythonStuff/DriveIt/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(511, 314)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(0, -1, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 4, 4, 1, 1)
        self.label_threads = QtWidgets.QLabel(self.centralwidget)
        self.label_threads.setObjectName("label_threads")
        self.gridLayout.addWidget(self.label_threads, 2, 0, 1, 1)
        self.spinBox_fetch_limit = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_fetch_limit.setKeyboardTracking(False)
        self.spinBox_fetch_limit.setProperty("value", 1)
        self.spinBox_fetch_limit.setObjectName("spinBox_fetch_limit")
        self.gridLayout.addWidget(self.spinBox_fetch_limit, 1, 1, 1, 1)
        self.label_chapters = QtWidgets.QLabel(self.centralwidget)
        self.label_chapters.setObjectName("label_chapters")
        self.gridLayout.addWidget(self.label_chapters, 1, 2, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 5, 0, 1, 5)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 1, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 5)
        self.spinBox_threads = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_threads.setKeyboardTracking(True)
        self.spinBox_threads.setMinimum(1)
        self.spinBox_threads.setMaximum(16)
        self.spinBox_threads.setObjectName("spinBox_threads")
        self.gridLayout.addWidget(self.spinBox_threads, 2, 4, 1, 1)
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(16)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.gridLayout.addWidget(self.horizontalSlider, 2, 1, 1, 3)
        self.label_save = QtWidgets.QLabel(self.centralwidget)
        self.label_save.setObjectName("label_save")
        self.gridLayout.addWidget(self.label_save, 3, 0, 1, 1)
        self.lineEdit_save_location = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_save_location.setObjectName("lineEdit_save_location")
        self.gridLayout.addWidget(self.lineEdit_save_location, 3, 1, 1, 3)
        self.pushButton_browse_file = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_browse_file.setObjectName("pushButton_browse_file")
        self.gridLayout.addWidget(self.pushButton_browse_file, 3, 4, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.horizontalSlider.valueChanged['int'].connect(self.spinBox_threads.setValue)
        self.spinBox_threads.valueChanged['int'].connect(self.horizontalSlider.setValue)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DriveIt"))
        self.pushButton.setText(_translate("MainWindow", "Fetch!"))
        self.label_threads.setText(_translate("MainWindow", "Threads:"))
        self.label_chapters.setText(_translate("MainWindow", "chapters"))
        self.checkBox.setText(_translate("MainWindow", "Only fetch latest"))
        self.label_save.setText(_translate("MainWindow", "Save to:"))
        self.pushButton_browse_file.setText(_translate("MainWindow", "Browse"))

