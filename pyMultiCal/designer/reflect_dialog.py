# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reflect_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ReflectDialog(object):
    def setupUi(self, ReflectDialog):
        ReflectDialog.setObjectName("ReflectDialog")
        ReflectDialog.resize(471, 153)
        self.verticalLayout = QtWidgets.QVBoxLayout(ReflectDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_port2 = QtWidgets.QLabel(ReflectDialog)
        self.label_port2.setObjectName("label_port2")
        self.gridLayout.addWidget(self.label_port2, 1, 2, 1, 1)
        self.btn_loadPort1 = QtWidgets.QPushButton(ReflectDialog)
        self.btn_loadPort1.setObjectName("btn_loadPort1")
        self.gridLayout.addWidget(self.btn_loadPort1, 0, 1, 1, 1)
        self.btn_loadPort2 = QtWidgets.QPushButton(ReflectDialog)
        self.btn_loadPort2.setObjectName("btn_loadPort2")
        self.gridLayout.addWidget(self.btn_loadPort2, 1, 1, 1, 1)
        self.label_port1 = QtWidgets.QLabel(ReflectDialog)
        self.label_port1.setObjectName("label_port1")
        self.gridLayout.addWidget(self.label_port1, 0, 2, 1, 1)
        self.btn_measurePort2 = QtWidgets.QPushButton(ReflectDialog)
        self.btn_measurePort2.setObjectName("btn_measurePort2")
        self.gridLayout.addWidget(self.btn_measurePort2, 1, 0, 1, 1)
        self.btn_measurePort1 = QtWidgets.QPushButton(ReflectDialog)
        self.btn_measurePort1.setObjectName("btn_measurePort1")
        self.gridLayout.addWidget(self.btn_measurePort1, 0, 0, 1, 1)
        self.btn_measureBoth = QtWidgets.QPushButton(ReflectDialog)
        self.btn_measureBoth.setObjectName("btn_measureBoth")
        self.gridLayout.addWidget(self.btn_measureBoth, 2, 0, 1, 1)
        self.btn_loadBoth = QtWidgets.QPushButton(ReflectDialog)
        self.btn_loadBoth.setObjectName("btn_loadBoth")
        self.gridLayout.addWidget(self.btn_loadBoth, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(ReflectDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ReflectDialog)
        self.buttonBox.accepted.connect(ReflectDialog.accept)
        self.buttonBox.rejected.connect(ReflectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReflectDialog)

    def retranslateUi(self, ReflectDialog):
        _translate = QtCore.QCoreApplication.translate
        ReflectDialog.setWindowTitle(_translate("ReflectDialog", "Dialog"))
        self.label_port2.setText(_translate("ReflectDialog", "port2 - not ready"))
        self.btn_loadPort1.setText(_translate("ReflectDialog", "Load Port 1 (.s1p)"))
        self.btn_loadPort2.setText(_translate("ReflectDialog", "Load Port (.s1p)"))
        self.label_port1.setText(_translate("ReflectDialog", "port1 - not ready"))
        self.btn_measurePort2.setText(_translate("ReflectDialog", "Measure Port2"))
        self.btn_measurePort1.setText(_translate("ReflectDialog", "Measure Port1"))
        self.btn_measureBoth.setText(_translate("ReflectDialog", "Measure Both"))
        self.btn_loadBoth.setText(_translate("ReflectDialog", "Load Both (.s2p)"))

