import re

from PyQt5 import QtWidgets, QtCore
from skrf import Network
import skrf.calibration
from skrf.network import four_oneports_2_twoport

from .designer import trl
from . import qt
from . import widgets
from .widgets import NetworkPlotWidget, NetworkListItem, NetworkListWidget
from .analyzers import analyzers


def load_network_file(caption="load network file", filter="touchstone file (*.s2p)"):
    fname = qt.getOpenFileName_Global(caption, filter)
    if not fname:
        return None

    try:
        ntwk = Network(fname)
    except Exception as e:
        qt.error_popup(e)
        return None

    return ntwk


class SwitchTermsDialog(QtWidgets.QDialog):
    def __init__(self, analyzer=None, parent=None):
        super(SwitchTermsDialog, self).__init__(parent)

        self.setWindowTitle("Measure Switch Terms")

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        
        self.btn_measureSwitch = QtWidgets.QPushButton("Measure Switch Terms")
        self.label_measureSwitch = QtWidgets.QLabel("Not Measured")
        self.btn_loadForwardSwitch = QtWidgets.QPushButton("Load Forward Switch Terms")
        self.label_loadForwardSwitch = QtWidgets.QLabel("Not Measured")
        self.btn_loadReverseSwitch = QtWidgets.QPushButton("Load Reverse Switch Terms")
        self.label_loadReverseSwitch = QtWidgets.QLabel("Not Measured")
        
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.addWidget(self.btn_measureSwitch, 0, 0)
        self.gridLayout.addWidget(self.label_measureSwitch, 0, 1)
        self.gridLayout.addWidget(self.btn_loadForwardSwitch, 1, 0)
        self.gridLayout.addWidget(self.label_loadForwardSwitch, 1, 1)
        self.gridLayout.addWidget(self.btn_loadReverseSwitch, 2, 0)
        self.gridLayout.addWidget(self.label_loadReverseSwitch, 2, 1)

        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.analyzer = analyzer
        if self.analyzer is None:
            self.btn_measureSwitch.setEnabled(False)
        self.forward = None
        self.reverse = None
        self._ready = False
        self.current_item = None

        self.btn_measureSwitch.clicked.connect(self.measure_switch)
        self.btn_loadForwardSwitch.clicked.connect(self.load_forward_switch)
        self.btn_loadReverseSwitch.clicked.connect(self.load_reverse_switch)

        self.ok = self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)  # type: QtWidgets.QPushButton
        self.ok.setEnabled(False)

    def measure_switch(self):
        self.forward, self.reverse = self.analyzer.measure_switch_terms()
        self.evaluate()

    def load_forward_switch(self):
        self.forward = load_network_file("Load Forward Switch Terms", "Touchstone 1-port (*.s1p)")
        if type(self.forward) is not Network:
            self.forward = None
            
        self.evaluate()

    def load_reverse_switch(self):
        self.reverse = load_network_file("Load Reverse Switch Terms", "Touchstone 1-port (*.s1p)")
        if type(self.reverse) is not Network:
            self.reverse = None
            
        self.evaluate()

    @property
    def ready(self): return self._ready

    @ready.setter
    def ready(self, val):
        if val is True:
            self._ready = True
            self.ok.setEnabled(True)
        else:
            self._ready = False
            self.ok.setEnabled(False)

    def evaluate(self):
        if type(self.forward) is Network:
            self.label_loadForwardSwitch.setText("forward - measured")
        else:
            self.label_loadForwardSwitch.setText("forward - not measured")

        if type(self.reverse) is Network:
            self.label_loadReverseSwitch.setText("reverse - measured")
        else:
            self.label_loadReverseSwitch.setText("reverse - not measured")

        if type(self.forward) is Network and type(self.reverse) is Network:
            self.label_measureSwitch.setText("measured")
            self.ready = True


class ReflectDialog(QtWidgets.QDialog):
    def __init__(self, analyzer=None, parent=None):
        super(ReflectDialog, self).__init__(parent)

        self.setWindowTitle("Measure Reflect Standards")

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.gridLayout = QtWidgets.QGridLayout()
        self.label_port2 = QtWidgets.QLabel(self)
        self.gridLayout.addWidget(self.label_port2, 1, 2, 1, 1)
        self.btn_loadPort1 = QtWidgets.QPushButton(self)
        self.gridLayout.addWidget(self.btn_loadPort1, 0, 1, 1, 1)
        self.btn_loadPort2 = QtWidgets.QPushButton(self)
        self.gridLayout.addWidget(self.btn_loadPort2, 1, 1, 1, 1)
        self.label_port1 = QtWidgets.QLabel(self)
        self.gridLayout.addWidget(self.label_port1, 0, 2, 1, 1)
        self.btn_measurePort2 = QtWidgets.QPushButton(self)
        self.gridLayout.addWidget(self.btn_measurePort2, 1, 0, 1, 1)
        self.btn_measurePort1 = QtWidgets.QPushButton(self)
        self.gridLayout.addWidget(self.btn_measurePort1, 0, 0, 1, 1)
        self.btn_measureBoth = QtWidgets.QPushButton(self)
        self.gridLayout.addWidget(self.btn_measureBoth, 2, 0, 1, 1)
        self.btn_loadBoth = QtWidgets.QPushButton(self)
        self.gridLayout.addWidget(self.btn_loadBoth, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.label_port2.setText("port2 - not ready")
        self.btn_loadPort1.setText("Load Port 1 (.s1p)")
        self.btn_loadPort2.setText("Load Port (.s1p)")
        self.label_port1.setText("port1 - not ready")
        self.btn_measurePort2.setText("Measure Port2")
        self.btn_measurePort1.setText("Measure Port1")
        self.btn_measureBoth.setText("Measure Both")
        self.btn_loadBoth.setText("Load Both (.s2p)")

        self._ready = False
        self.analyzer = analyzer

        if self.analyzer is None:
            for btn in (self.btn_measureBoth, self.btn_measurePort1, self.btn_measurePort2):
                btn.setEnabled(False)

        self.reflect_2port = None
        self.s11 = None
        self.s22 = None

        self.ok = self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)  # type: QtWidgets.QPushButton
        self.ok.setEnabled(False)

        self.btn_measureBoth.clicked.connect(self.measure_both)
        self.btn_measurePort1.clicked.connect(self.measure_s11)
        self.btn_measurePort2.clicked.connect(self.measure_s22)

        self.btn_loadBoth.clicked.connect(self.load_both)
        self.btn_loadPort1.clicked.connect(self.load_s11)
        self.btn_loadPort2.clicked.connect(self.load_s22)

    def measure_s11(self):
        self.s11 = self.analyzer.get_oneport(port=1)
        self.evaluate()

    def measure_s22(self):
        self.s22 = self.analyzer.get_oneport(port=2)
        self.evaluate()

    def measure_both(self):
        self.reflect_2port = self.analyzer.get_twoport()
        self.evaluate()

    def load_s11(self):
        self.s11 = load_network_file("load port 1 reflect", "1-port touchstone (*.s1p)")
        self.evaluate()

    def load_s22(self):
        self.s22 = load_network_file("load port 2 reflect", "1-port touchstone (*.s1p)")
        self.evaluate()

    def load_both(self):
        self.reflect_2port = load_network_file("load reflect cal standard")
        self.evaluate()

    @property
    def ready(self): return self._ready

    @ready.setter
    def ready(self, val):
        if val is True:
            self._ready = True
            self.ok.setEnabled(True)
        else:
            self._ready = False
            self.ok.setEnabled(False)

    def evaluate(self):
        if type(self.reflect_2port) is Network:
            self.ready = True
            self.label_port1.setText("port1 - measured")
            self.label_port2.setText("port2 - measured")
        else:
            if type(self.s11) is Network and type(self.s22) is Network:
                self.reflect_2port = four_oneports_2_twoport(self.s11, self.s11, self.s22, self.s22)
                self.reflect_2port.s[:, 0, 1] = 1
                self.reflect_2port.s[:, 1, 0] = 1
                self.ready = True
                self.label_port1.setText("port1 - measured")
                self.label_port2.setText("port2 - measured")
            else:
                self.ready = False
                if type(self.s11) is Network:
                    self.label_port1.setText("port1 - measured")
                else:
                    self.label_port1.setText("port1 - not measured")
                if type(self.s22) is Network:
                    self.label_port2.setText("port2 - measured")
                else:
                    self.label_port2.setText("port2 - not measured")


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

        self.ntwk_plot = NetworkPlotWidget()
        self.verticalLayout_plotArea.addWidget(self.ntwk_plot)

        for _list in (self.listWidget_thru, self.listWidget_line,
                      self.listWidget_measurements, self.listWidget_reflect
                      ):  # type: NetworkListWidget
            _list.itemClicked.connect(self.set_active_network)
            _list.item_removed.connect(self.ntwk_plot.clear_plot)
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
            dialog = ReflectDialog(nwa)
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
            dialog = SwitchTermsDialog(nwa)
            try:
                accepted = dialog.exec_()
                if accepted:
                    switch_terms = (dialog.forward, dialog.reverse)
                    self.load_switch(switch_terms)
            finally:
                dialog.close()

    def load_network(self, ntwk, list_widget):
        item = NetworkListItem()
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        item.setText(ntwk.name)
        item.ntwk = ntwk
        list_widget.addItem(item)
        list_widget.setCurrentItem(item)
        list_widget.item_text_updated()

        self.set_active_network(item)

    def load_from_file(self, list_widget, caption):
        ntwk = load_network_file(caption)  # type: Network
        if not ntwk:
            return
        self.load_network(ntwk, list_widget)

    def load_thru(self, thru=None):
        if type(thru) is not Network:
            thru = load_network_file("load thru file")

        if not thru:
            return

        if self.listWidget_thru.thru is None:
            self.listWidget_thru.thru = NetworkListItem()
            self.listWidget_thru.thru.setText(self.THRU_ID)
            self.listWidget_thru.addItem(self.listWidget_thru.thru)

        self.listWidget_thru.thru.ntwk = thru
        self.set_active_network(self.listWidget_thru.thru)

    def load_switch(self, switch_terms):

        if self.listWidget_thru.switch_terms is None:
            self.listWidget_thru.switch_terms = NetworkListItem()
            self.listWidget_thru.switch_terms.setText(self.SWITCH_TERMS_ID)
            self.listWidget_thru.addItem(self.listWidget_thru.switch_terms)

        self.listWidget_thru.switch_terms.ntwk = switch_terms
        self.set_active_network(self.listWidget_thru.switch_terms)

    def load_reflect(self):
        # self.load_from_file(self.listWidget_reflect, "load reflect file")
        # self.measure_reflect()
        dialog = ReflectDialog()
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
        dialog = SwitchTermsDialog()
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
