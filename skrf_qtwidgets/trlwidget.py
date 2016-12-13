import re

import skrf.calibration
from qtpy import QtWidgets, QtCore
from skrf import Network

from . import qt
from .analyzers import analyzers
from .designer import trl
from . import widgets


class TRLWidget(QtWidgets.QWidget, trl.Ui_TRL):
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
