import re

from qtpy import QtWidgets, QtCore
import skrf

from . import qt
from . import widgets


class TRLWidget(QtWidgets.QWidget):
    THRU_ID = "thru"
    SWITCH_TERMS_ID = "switch terms"

    def __init__(self, parent=None):
        super(TRLWidget, self).__init__(parent)

        # --- Setup UI --- #
        self.resize(825, 575)
        self.verticalLayout_main = QtWidgets.QVBoxLayout(self)

        self.vna_controller = widgets.VnaController()
        self.vna_controller.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_main.addWidget(self.vna_controller)

        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal, self)

        self.tabWidget = QtWidgets.QTabWidget(self.splitter)
        self.tab_calStandards = QtWidgets.QWidget()
        self.tab_calStandards_layout = QtWidgets.QVBoxLayout(self.tab_calStandards)
        self.tab_calStandards_layout.setContentsMargins(6, 6, 6, 6)

        self.label_thru = QtWidgets.QLabel("Thru", self.tab_calStandards)
        self.btn_measureThru = QtWidgets.QPushButton("Measure", self.tab_calStandards)
        self.btn_loadThru = QtWidgets.QPushButton("Load", self.tab_calStandards)
        self.hlay_thru = QtWidgets.QHBoxLayout()
        self.hlay_thru.addWidget(self.label_thru)
        self.hlay_thru.addWidget(self.btn_measureThru)
        self.hlay_thru.addWidget(self.btn_loadThru)
        self.tab_calStandards_layout.addLayout(self.hlay_thru)

        self.label_switchTerms = QtWidgets.QLabel("Switch Terms", self.tab_calStandards)
        self.btn_measureSwitchTerms = QtWidgets.QPushButton("Measure", self.tab_calStandards)
        self.btn_loadSwitchTerms = QtWidgets.QPushButton("Load", self.tab_calStandards)
        self.hlay_switchTerms = QtWidgets.QHBoxLayout()
        self.hlay_switchTerms.addWidget(self.label_switchTerms)
        self.hlay_switchTerms.addWidget(self.btn_measureSwitchTerms)
        self.hlay_switchTerms.addWidget(self.btn_loadSwitchTerms)
        self.tab_calStandards_layout.addLayout(self.hlay_switchTerms)

        self.listWidget_thru = widgets.NetworkListWidget(self.tab_calStandards)
        self.tab_calStandards_layout.addWidget(self.listWidget_thru)

        self.label_reflect = QtWidgets.QLabel("Reflect", self.tab_calStandards)
        self.btn_measureReflect = QtWidgets.QPushButton("Measure", self.tab_calStandards)
        self.btn_loadReflect = QtWidgets.QPushButton("Load", self.tab_calStandards)
        self.hlay_reflect = QtWidgets.QHBoxLayout()
        self.hlay_reflect.addWidget(self.label_reflect)
        self.hlay_reflect.addWidget(self.btn_measureReflect)
        self.hlay_reflect.addWidget(self.btn_loadReflect)
        self.tab_calStandards_layout.addLayout(self.hlay_reflect)

        self.listWidget_reflect = widgets.NetworkListWidget(self.tab_calStandards)
        self.tab_calStandards_layout.addWidget(self.listWidget_reflect)

        self.label_line = QtWidgets.QLabel("Line", self.tab_calStandards)
        self.btn_measureLine = QtWidgets.QPushButton("Measure", self.tab_calStandards)
        self.btn_loadLine = QtWidgets.QPushButton("Load", self.tab_calStandards)
        self.hlay_line = QtWidgets.QHBoxLayout()
        self.hlay_line.addWidget(self.label_line)
        self.hlay_line.addWidget(self.btn_measureLine)
        self.hlay_line.addWidget(self.btn_loadLine)
        self.tab_calStandards_layout.addLayout(self.hlay_line)

        self.listWidget_line = widgets.NetworkListWidget(self.tab_calStandards)
        self.tab_calStandards_layout.addWidget(self.listWidget_line)

        self.btn_saveCalibration = QtWidgets.QPushButton("Save Cal", self.tab_calStandards)
        self.btn_loadCalibration = QtWidgets.QPushButton("Load Cal", self.tab_calStandards)
        self.hlay_saveCal = QtWidgets.QHBoxLayout()
        self.hlay_saveCal.addWidget(self.btn_saveCalibration)
        self.hlay_saveCal.addWidget(self.btn_loadCalibration)
        self.tab_calStandards_layout.addLayout(self.hlay_saveCal)

        self.tabWidget.addTab(self.tab_calStandards, "Cal Standards")

        self.tab_measurements = QtWidgets.QWidget()
        self.tab_measurements_layout = QtWidgets.QVBoxLayout(self.tab_measurements)
        self.tab_measurements_layout.setContentsMargins(6, 6, 6, 6)

        self.btn_measureMeasurement = QtWidgets.QPushButton("Measure", self.tab_measurements)
        self.btn_loadMeasurement = QtWidgets.QPushButton("Load", self.tab_measurements)
        self.btn_calibrate = QtWidgets.QPushButton("Calibrate", self.tab_measurements)
        self.hlay_measurementButtons = QtWidgets.QHBoxLayout()
        self.hlay_measurementButtons.addWidget(self.btn_loadMeasurement)
        self.hlay_measurementButtons.addWidget(self.btn_measureMeasurement)
        self.hlay_measurementButtons.addWidget(self.btn_calibrate)
        self.tab_measurements_layout.addLayout(self.hlay_measurementButtons)

        self.listWidget_measurements = widgets.NetworkListWidget(self.tab_measurements)
        self.tab_measurements_layout.addWidget(self.listWidget_measurements)

        self.groupBox_saveOptions = QtWidgets.QGroupBox("Save Options", self.tab_measurements)

        self.vlay_saveOptions = QtWidgets.QVBoxLayout(self.groupBox_saveOptions)
        
        self.radio_saveRaw = QtWidgets.QRadioButton("Save Raw", self.groupBox_saveOptions)
        self.radio_saveCal = QtWidgets.QRadioButton("Save Cal", self.groupBox_saveOptions)
        self.radio_saveBoth = QtWidgets.QRadioButton("Save Both", self.groupBox_saveOptions)
        self.radio_saveBoth.setChecked(True)
        self.hlay_saveOptionsRadio = QtWidgets.QHBoxLayout()
        self.hlay_saveOptionsRadio.addWidget(self.radio_saveRaw)
        self.hlay_saveOptionsRadio.addWidget(self.radio_saveCal)
        self.hlay_saveOptionsRadio.addWidget(self.radio_saveBoth)
        self.vlay_saveOptions.addLayout(self.hlay_saveOptionsRadio)
        
        self.btn_saveSelectedMeasurements = QtWidgets.QPushButton("Save Selected", self.groupBox_saveOptions)
        self.btn_saveAllMeasurements = QtWidgets.QPushButton("Save All", self.groupBox_saveOptions)
        self.hlay_saveMeasurementButtons = QtWidgets.QHBoxLayout()
        self.hlay_saveMeasurementButtons.addWidget(self.btn_saveSelectedMeasurements)
        self.hlay_saveMeasurementButtons.addWidget(self.btn_saveAllMeasurements)
        self.vlay_saveOptions.addLayout(self.hlay_saveMeasurementButtons)

        self.tab_measurements_layout.addWidget(self.groupBox_saveOptions)
        self.tabWidget.addTab(self.tab_measurements, "Measurements")

        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.verticalLayout_plotArea = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.splitter.setContentsMargins(0, 0, 0, 0)
        self.layoutWidget.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_plotArea.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_main.addWidget(self.splitter)

        self.tabWidget.setCurrentIndex(0)
        # --- END SETUP UI --- #

        self.setWindowTitle("Multiline TRL Calibration")

        self.listWidget_thru.thru = None
        self.listWidget_thru.switch_terms = None
        self.listWidget_reflect.reflects = []
        self.listWidget_line.lines = []
        self.calibration = None
        self.currentItem = None

        self.ntwk_plot = widgets.NetworkPlotWidget()
        self.ntwk_plot.verticalLayout.setContentsMargins(0, 0, 0, 0)
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

    def save_all_measurements(self):
        save_which = self.get_save_which_mode()
        ntwk_list = []

        for i in range(self.listWidget_measurements.count()):
            item = self.listWidget_measurements.item(i)
            if save_which != "cal" and isinstance(item.ntwk, skrf.Network):
                ntwk_list.append(item.ntwk)
            if save_which != "raw" and isinstance(item.ntwk_calibrated, skrf.Network):
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
        with self.vna_controller.get_analyzer() as nwa:
            thru = nwa.measure_twoport_ntwk()
            thru.name = "thru"
        self.load_thru(thru)

    def measure_reflect(self):
        with self.vna_controller.get_analyzer() as nwa:
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
        with self.vna_controller.get_analyzer() as nwa:
            line = nwa.measure_twoport_ntwk()
            line.name = self.get_unique_name("line", self.listWidget_line)
        self.load_network(line, self.listWidget_line)

    def measure_measurement(self):
        with self.vna_controller.get_analyzer() as nwa:
            meas = nwa.measure_twoport_ntwk()
            meas.name = self.get_unique_name("meas", self.listWidget_measurements)
        self.load_network(meas, self.listWidget_measurements)

    def measure_switch_terms(self):
        with self.vna_controller.get_analyzer() as nwa:
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
        ntwk = widgets.load_network_file(caption)  # type: skrf.Network
        if not ntwk:
            return
        self.load_network(ntwk, list_widget)

    def load_thru(self, thru=None):
        if type(thru) is not skrf.Network:
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
