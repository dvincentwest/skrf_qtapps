import re

import skrf.calibration
from qtpy import QtWidgets, QtCore
from skrf import Network

from . import qt
from .analyzers import analyzers
from . import widgets
from .widgets import NetworkListWidget


class Ui_TRL(object):
    def setupUi(self, TRL):
        TRL.resize(850, 500)
        self.tab_calStandards_layout_2 = QtWidgets.QVBoxLayout(TRL)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.addLayout(self.horizontalLayout_9)
        self.checkBox_TriggerNew = QtWidgets.QCheckBox(TRL)
        self.horizontalLayout_10.addWidget(self.checkBox_TriggerNew)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.label_6 = QtWidgets.QLabel(TRL)
        self.horizontalLayout_8.addWidget(self.label_6)
        self.comboBox_analyzer = QtWidgets.QComboBox(TRL)
        self.comboBox_analyzer.addItem("")
        self.horizontalLayout_8.addWidget(self.comboBox_analyzer)
        self.horizontalLayout_10.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.label_7 = QtWidgets.QLabel(TRL)
        self.horizontalLayout_7.addWidget(self.label_7)
        self.lineEdit_visaString = QtWidgets.QLineEdit(TRL)
        self.horizontalLayout_7.addWidget(self.lineEdit_visaString)
        self.horizontalLayout_10.addLayout(self.horizontalLayout_7)
        self.tab_calStandards_layout_2.addLayout(self.horizontalLayout_10)
        self.splitter = QtWidgets.QSplitter(TRL)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.tabWidget = QtWidgets.QTabWidget(self.splitter)
        self.tab_calStandards = QtWidgets.QWidget()
        self.tab_calStandards_layout = QtWidgets.QVBoxLayout(self.tab_calStandards)
        self.tab_calStandards_layout.setContentsMargins(8, 8, 8, 8)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(self.tab_calStandards)
        self.horizontalLayout.addWidget(self.label)
        self.btn_measureThru = QtWidgets.QPushButton(self.tab_calStandards)
        self.horizontalLayout.addWidget(self.btn_measureThru)
        self.btn_loadThru = QtWidgets.QPushButton(self.tab_calStandards)
        self.horizontalLayout.addWidget(self.btn_loadThru)
        self.tab_calStandards_layout.addLayout(self.horizontalLayout)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.label_5 = QtWidgets.QLabel(self.tab_calStandards)
        self.horizontalLayout_6.addWidget(self.label_5)
        self.btn_measureSwitchTerms = QtWidgets.QPushButton(self.tab_calStandards)
        self.horizontalLayout_6.addWidget(self.btn_measureSwitchTerms)
        self.btn_loadSwitchTerms = QtWidgets.QPushButton(self.tab_calStandards)
        self.horizontalLayout_6.addWidget(self.btn_loadSwitchTerms)
        self.tab_calStandards_layout.addLayout(self.horizontalLayout_6)
        self.listWidget_thru = NetworkListWidget(self.tab_calStandards)
        self.tab_calStandards_layout.addWidget(self.listWidget_thru)
        self.tab_calStandards_2 = QtWidgets.QHBoxLayout()
        self.label_2 = QtWidgets.QLabel(self.tab_calStandards)
        self.tab_calStandards_2.addWidget(self.label_2)
        self.btn_measureReflect = QtWidgets.QPushButton(self.tab_calStandards)
        self.tab_calStandards_2.addWidget(self.btn_measureReflect)
        self.btn_loadReflect = QtWidgets.QPushButton(self.tab_calStandards)
        self.tab_calStandards_2.addWidget(self.btn_loadReflect)
        self.tab_calStandards_layout.addLayout(self.tab_calStandards_2)
        self.listWidget_reflect = NetworkListWidget(self.tab_calStandards)
        self.tab_calStandards_layout.addWidget(self.listWidget_reflect)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.label_3 = QtWidgets.QLabel(self.tab_calStandards)
        self.horizontalLayout_3.addWidget(self.label_3)
        self.btn_measureLine = QtWidgets.QPushButton(self.tab_calStandards)
        self.horizontalLayout_3.addWidget(self.btn_measureLine)
        self.btn_loadLine = QtWidgets.QPushButton(self.tab_calStandards)
        self.horizontalLayout_3.addWidget(self.btn_loadLine)
        self.tab_calStandards_layout.addLayout(self.horizontalLayout_3)
        self.listWidget_line = NetworkListWidget(self.tab_calStandards)
        self.tab_calStandards_layout.addWidget(self.listWidget_line)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.btn_saveCalibration = QtWidgets.QPushButton(self.tab_calStandards)
        self.horizontalLayout_11.addWidget(self.btn_saveCalibration)
        self.btn_loadCalibration = QtWidgets.QPushButton(self.tab_calStandards)
        self.horizontalLayout_11.addWidget(self.btn_loadCalibration)
        self.tab_calStandards_layout.addLayout(self.horizontalLayout_11)
        self.tabWidget.addTab(self.tab_calStandards, "")
        self.tab_measurements = QtWidgets.QWidget()
        self.tab_measurements_layout = QtWidgets.QVBoxLayout(self.tab_measurements)
        self.tab_measurements_layout.setContentsMargins(8, 8, 8, 8)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.btn_measureMeasurement = QtWidgets.QPushButton(self.tab_measurements)
        self.horizontalLayout_5.addWidget(self.btn_measureMeasurement)
        self.btn_loadMeasurement = QtWidgets.QPushButton(self.tab_measurements)
        self.horizontalLayout_5.addWidget(self.btn_loadMeasurement)
        self.btn_calibrate = QtWidgets.QPushButton(self.tab_measurements)
        self.horizontalLayout_5.addWidget(self.btn_calibrate)
        self.tab_measurements_layout.addLayout(self.horizontalLayout_5)
        self.listWidget_measurements = NetworkListWidget(self.tab_measurements)
        self.tab_measurements_layout.addWidget(self.listWidget_measurements)
        self.groupBox = QtWidgets.QGroupBox(self.tab_measurements)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.radio_saveRaw = QtWidgets.QRadioButton(self.groupBox)
        self.horizontalLayout_2.addWidget(self.radio_saveRaw)
        self.radio_saveCal = QtWidgets.QRadioButton(self.groupBox)
        self.horizontalLayout_2.addWidget(self.radio_saveCal)
        self.radio_saveBoth = QtWidgets.QRadioButton(self.groupBox)
        self.radio_saveBoth.setChecked(True)
        self.horizontalLayout_2.addWidget(self.radio_saveBoth)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.btn_saveSelectedMeasurements = QtWidgets.QPushButton(self.groupBox)
        self.horizontalLayout_4.addWidget(self.btn_saveSelectedMeasurements)
        self.btn_saveAllMeasurements = QtWidgets.QPushButton(self.groupBox)
        self.horizontalLayout_4.addWidget(self.btn_saveAllMeasurements)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.tab_measurements_layout.addWidget(self.groupBox)
        self.tabWidget.addTab(self.tab_measurements, "")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.verticalLayout_plotArea = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_plotArea.setContentsMargins(0, 0, 0, 0)
        self.tab_calStandards_layout_2.addWidget(self.splitter)

        self.retranslateUi(TRL)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TRL)

    def retranslateUi(self, TRL):
        _translate = QtCore.QCoreApplication.translate
        TRL.setWindowTitle(_translate("TRL", "Multiline TRL Calibration"))
        self.checkBox_TriggerNew.setText(_translate("TRL", "Trigger New"))
        self.label_6.setText(_translate("TRL", "Network Analyzer"))
        self.comboBox_analyzer.setItemText(0, _translate("TRL", "none"))
        self.label_7.setText(_translate("TRL", "Visa String"))
        self.label.setText(_translate("TRL", "Thru"))
        self.btn_measureThru.setText(_translate("TRL", "Measure"))
        self.btn_loadThru.setText(_translate("TRL", "Load"))
        self.label_5.setText(_translate("TRL", "Switch Terms"))
        self.btn_measureSwitchTerms.setText(_translate("TRL", "Measure"))
        self.btn_loadSwitchTerms.setText(_translate("TRL", "Load"))
        self.label_2.setText(_translate("TRL", "Reflect"))
        self.btn_measureReflect.setText(_translate("TRL", "Measure"))
        self.btn_loadReflect.setText(_translate("TRL", "Load"))
        self.label_3.setText(_translate("TRL", "Line"))
        self.btn_measureLine.setText(_translate("TRL", "Measure"))
        self.btn_loadLine.setText(_translate("TRL", "Load"))
        self.btn_saveCalibration.setText(_translate("TRL", "Save Cal"))
        self.btn_loadCalibration.setText(_translate("TRL", "Load Cal"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_calStandards), _translate("TRL", "Cal Standards"))
        self.btn_measureMeasurement.setText(_translate("TRL", "Measure"))
        self.btn_loadMeasurement.setText(_translate("TRL", "Load"))
        self.btn_calibrate.setText(_translate("TRL", "Calibrate"))
        self.groupBox.setTitle(_translate("TRL", "Save Options"))
        self.radio_saveRaw.setText(_translate("TRL", "Save Raw"))
        self.radio_saveCal.setText(_translate("TRL", "Save Cal"))
        self.radio_saveBoth.setText(_translate("TRL", "Save Both"))
        self.btn_saveSelectedMeasurements.setText(_translate("TRL", "Save Selected"))
        self.btn_saveAllMeasurements.setText(_translate("TRL", "Save All"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_measurements), _translate("TRL", "Measurements"))


class TRLWidget(QtWidgets.QWidget, Ui_TRL):
    THRU_ID = "thru"
    SWITCH_TERMS_ID = "switch terms"

    def __init__(self, parent=None):
        super(TRLWidget, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle("Multiline TRL Calibration")

        self.listWidget_thru.thru = None
        self.listWidget_thru.switch_terms = None
        self.listWidget_reflect.reflects = []
        self.listWidget_line.lines = []
        self.calibration = None
        self.currentItem = None

        self.ntwk_plot = widgets.NetworkPlotWidget()
        self.verticalLayout_plotArea.addWidget(self.ntwk_plot)

        for _list in (self.listWidget_thru, self.listWidget_line,
                      self.listWidget_measurements, self.listWidget_reflect
                      ):  # type: widgets.NetworkListWidget
            _list.itemClicked.connect(self.set_active_network)
            _list.item_removed.connect(self.ntwk_plot.clear_plot)
            _list.item_updated.connect(self.set_active_network)
            _list.get_save_which_mode = lambda: "raw"
        self.listWidget_thru.item_removed.connect(self.thru_list_item_deleted)
        self.listWidget_measurements.get_save_which_mode = self.get_save_which_mode

        self.splitter.setStretchFactor(1, 100)
        self.btn_loadThru.clicked.connect(self.load_thru)
        self.btn_loadReflect.clicked.connect(self.load_reflect)
        self.btn_loadLine.clicked.connect(self.load_line)
        self.btn_loadSwitchTerms.clicked.connect(self.load_switch_terms)
        self.btn_loadMeasurement.clicked.connect(self.load_measurement)
        self.btn_measureThru.clicked.connect(self.measure_thru)
        self.btn_measureReflect.clicked.connect(self.measure_reflect)
        self.btn_measureLine.clicked.connect(self.measure_line)
        self.btn_measureSwitchTerms.clicked.connect(self.measure_switch_terms)
        self.btn_measureMeasurement.clicked.connect(self.measure_measurement)
        self.btn_calibrate.clicked.connect(self.apply_calibration)
        self.btn_saveCalibration.clicked.connect(self.save_calibration)
        self.btn_loadCalibration.clicked.connect(self.load_calibration)

        self.btn_saveSelectedMeasurements.clicked.connect(self.listWidget_measurements.save_single_item)
        self.btn_saveAllMeasurements.clicked.connect(self.save_all_measurements)

        self.comboBox_analyzer.currentIndexChanged.connect(self.set_visa_address)
        for key, val in analyzers.items():
            self.comboBox_analyzer.addItem(key)
        self.comboBox_analyzer.removeItem(0)
        self.comboBox_analyzer.setCurrentIndex(0)

    def save_all_measurements(self):
        save_which = self.get_save_which_mode()
        ntwk_list = []

        for i in range(self.listWidget_measurements.count()):
            item = self.listWidget_measurements.item(i)
            if save_which != "cal" and isinstance(item.ntwk, Network):
                ntwk_list.append(item.ntwk)
            if save_which != "raw" and isinstance(item.ntwk_calibrated, Network):
                ntwk_list.append(item.ntwk_calibrated)

        widgets.save_multiple_networks(ntwk_list)

    def save_calibration(self):
        qt.warnMissingFeature()

    def load_calibration(self):
        qt.warnMissingFeature()

    def get_save_which_mode(self):
        if self.radio_saveRaw.isChecked():
            return "raw"
        elif self.radio_saveCal.isChecked():
            return "cal"
        else:
            return "both"

    @staticmethod
    def get_unique_name(name, list_widget):
        '''
        :type name: str
        :type list_widget: QtWidgets.QListWidget
        :return:
        '''
        names = []
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            names.append(item.text())

        if name in names:
            if re.match("_\d\d", name[-3:]):
                name_base = name[:-3]
                suffix = int(name[-2:])
            else:
                name_base = name
                suffix = 1

            for num in range(suffix, 100, 1):
                name = "{:s}_{:02d}".format(name_base, num)
                if name not in names:
                    break
        return name

    def set_visa_address(self):
        self.lineEdit_visaString.setText(
            analyzers[self.comboBox_analyzer.currentText()].DEFAULT_VISA_ADDRESS
        )

    def get_analyzer(self):
        return analyzers[self.comboBox_analyzer.currentText()](self.lineEdit_visaString.text())

    def set_active_network(self, item):
        """
        :type item: NetworkListItem
        :return:
        """
        self.currentItem = item
        if item is None:
            return

        if type(item.ntwk) in (list, tuple):
            self.ntwk_plot.ntwk_list = item.ntwk
        else:
            self.ntwk_plot.set_networks(item.ntwk, item.ntwk_calibrated)

    def thru_list_item_deleted(self):
        item = self.listWidget_thru.selectedItems()[0]
        if item.text() == self.THRU_ID:
            self.listWidget_thru.thru = None
        elif item.text() == self.SWITCH_TERMS_ID:
            self.listWidget_thru.switch_terms = None

    def measure_thru(self):
        with self.get_analyzer() as nwa:
            thru = nwa.measure_twoport_ntwk()
            thru.name = "thru"
        self.load_thru(thru)

    def measure_reflect(self):
        with self.get_analyzer() as nwa:
            dialog = widgets.ReflectDialog(nwa)
            try:
                accepted = dialog.exec_()
                if accepted:
                    if not dialog.reflect_2port.name:
                        dialog.reflect_2port.name = self.get_unique_name("reflect", self.listWidget_reflect)
                    self.load_network(dialog.reflect_2port, self.listWidget_reflect)
            finally:
                dialog.close()

    def measure_line(self):
        with self.get_analyzer() as nwa:
            line = nwa.measure_twoport_ntwk()
            line.name = self.get_unique_name("line", self.listWidget_line)
        self.load_network(line, self.listWidget_line)

    def measure_measurement(self):
        with self.get_analyzer() as nwa:
            meas = nwa.measure_twoport_ntwk()
            meas.name = self.get_unique_name("meas", self.listWidget_measurements)
        self.load_network(meas, self.listWidget_measurements)

    def measure_switch_terms(self):
        with self.get_analyzer() as nwa:
            dialog = widgets.SwitchTermsDialog(nwa)
            try:
                accepted = dialog.exec_()
                if accepted:
                    switch_terms = (dialog.forward, dialog.reverse)
                    self.load_switch(switch_terms)
            finally:
                dialog.close()

    def load_network(self, ntwk, list_widget):
        item = widgets.NetworkListItem()
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        item.setText(ntwk.name)
        item.ntwk = ntwk
        list_widget.addItem(item)
        list_widget.setCurrentItem(item)
        list_widget.item_text_updated()

        self.set_active_network(item)

    def load_from_file(self, list_widget, caption):
        ntwk = widgets.load_network_file(caption)  # type: Network
        if not ntwk:
            return
        self.load_network(ntwk, list_widget)

    def load_thru(self, thru=None):
        if type(thru) is not Network:
            thru = widgets.load_network_file("load thru file")

        if not thru:
            return

        if self.listWidget_thru.thru is None:
            self.listWidget_thru.thru = widgets.NetworkListItem()
            self.listWidget_thru.thru.setText(self.THRU_ID)
            self.listWidget_thru.addItem(self.listWidget_thru.thru)

        self.listWidget_thru.thru.ntwk = thru
        self.set_active_network(self.listWidget_thru.thru)

    def load_switch(self, switch_terms):

        if self.listWidget_thru.switch_terms is None:
            self.listWidget_thru.switch_terms = widgets.NetworkListItem()
            self.listWidget_thru.switch_terms.setText(self.SWITCH_TERMS_ID)
            self.listWidget_thru.addItem(self.listWidget_thru.switch_terms)

        self.listWidget_thru.switch_terms.ntwk = switch_terms
        self.set_active_network(self.listWidget_thru.switch_terms)

    def load_reflect(self):
        # self.load_from_file(self.listWidget_reflect, "load reflect file")
        # self.measure_reflect()
        dialog = widgets.ReflectDialog()
        try:
            accepted = dialog.exec_()
            if accepted:
                if not dialog.reflect_2port.name:
                    dialog.reflect_2port.name = self.get_unique_name("reflect", self.listWidget_reflect)
                self.load_network(dialog.reflect_2port, self.listWidget_reflect)
        finally:
            dialog.close()

    def load_line(self):
        self.load_from_file(self.listWidget_line, "load line file")

    def load_measurement(self):
        self.load_from_file(self.listWidget_measurements, "load measurement file")

    def load_switch_terms(self):
        dialog = widgets.SwitchTermsDialog()
        try:
            accepted = dialog.exec_()
            if accepted:
                switch_terms = (dialog.forward, dialog.reverse)
                self.load_switch(switch_terms)
        finally:
            dialog.close()

    def apply_calibration(self):
        measured = []

        error_messages = []

        if self.listWidget_thru.thru is not None:
            measured.append(self.listWidget_thru.thru.ntwk)
        else:
            error_messages.append("missing a thru calibration standard")

        n_reflects = self.listWidget_reflect.count()
        if n_reflects > 0:
            for i in range(n_reflects):
                measured.append(self.listWidget_reflect.item(i).ntwk)
        else:
            error_messages.append("missing reflect standards")

        n_lines = self.listWidget_line.count()
        if n_lines > 0:
            for i in range(n_lines):
                measured.append(self.listWidget_line.item(i).ntwk)

        if len(error_messages) > 0:
            qt.error_popup("\n\n".join(error_messages))
            return

        if self.listWidget_thru.switch_terms is not None:
            switch_terms = self.listWidget_thru.switch_terms.ntwk
        else:
            switch_terms = None

        try:
            self.calibration = skrf.calibration.TRL(measured, n_reflects=n_reflects, switch_terms=switch_terms)
            for i in range(self.listWidget_measurements.count()):
                item = self.listWidget_measurements.item(i)  # type: NetworkListItem
                item.ntwk_calibrated = self.calibration.apply_cal(item.ntwk)
                item.ntwk_calibrated.name = item.ntwk.name + "-cal"
        except Exception as e:
            qt.error_popup(e)

        self.set_active_network(self.currentItem)
