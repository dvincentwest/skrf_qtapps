# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sparameters_plot.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(520, 478)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBox_useCorrected = QtWidgets.QCheckBox(Form)
        self.checkBox_useCorrected.setObjectName("checkBox_useCorrected")
        self.horizontalLayout.addWidget(self.checkBox_useCorrected)
        self.comboBox_unitsSelector = QtWidgets.QComboBox(Form)
        self.comboBox_unitsSelector.setObjectName("comboBox_unitsSelector")
        self.horizontalLayout.addWidget(self.comboBox_unitsSelector)
        self.comboBox_traceSelector = QtWidgets.QComboBox(Form)
        self.comboBox_traceSelector.setObjectName("comboBox_traceSelector")
        self.horizontalLayout.addWidget(self.comboBox_traceSelector)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.ntwkPlot = NetworkPlot(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ntwkPlot.sizePolicy().hasHeightForWidth())
        self.ntwkPlot.setSizePolicy(sizePolicy)
        self.ntwkPlot.setObjectName("ntwkPlot")
        self.verticalLayout.addWidget(self.ntwkPlot)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.checkBox_useCorrected.setText(_translate("Form", "Plot Corrected"))

from skrf_qtapps.widgets import NetworkPlot
