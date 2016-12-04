import sys
import os

import sip
import visa
from PyQt5 import uic, QtGui, QtWidgets, QtCore
import pyqtgraph as pg
from skrf import Network
import skrf.calibration

from .designer import trl
from . import qt
from .widgets import NetworkPlotWidget


def load_network_file(caption="load network file"):
    fname = qt.getOpenFileName_Global(caption, "touchstone file (*.s2p)")
    if not fname:
        return None

    try:
        ntwk = Network(fname)
    except Exception as e:
        qt.error_popup(e)
        return None

    return ntwk


class NetworkListItem(QtWidgets.QListWidgetItem):
    ntwk = None
    ntwk_calibrated = None


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

        self.ntwk_plot = NetworkPlotWidget()
        self.verticalLayout_plotArea.addWidget(self.ntwk_plot)

        for _list in (self.listWidget_thru, self.listWidget_line,self.listWidget_measurements, self.listWidget_reflect
                      ):  # type: pyMultiCal.widgets
            _list.itemClicked.connect(self.set_active_network)
            _list.item_removed.connect(self.ntwk_plot.clear_plot)
        self.listWidget_thru.item_removed.connect(self.thru_list_item_deleted)

        self.splitter.setStretchFactor(1, 100)
        self.btn_loadThru.clicked.connect(self.load_thru)
        self.btn_loadReflect.clicked.connect(self.load_reflect)
        self.btn_loadLine.clicked.connect(self.load_line)
        self.btn_loadMeasurement.clicked.connect(self.load_measurement)
        self.btn_calibrate.clicked.connect(self.apply_calibration)

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

        self.calibration = skrf.calibration.TRL(measured, n_reflects=n_reflects)

        for i in range(self.listWidget_measurements.count()):
            item = self.listWidget_measurements.item(i)  # type: NetworkListItem
            item.ntwk_calibrated = self.calibration.apply_cal(item.ntwk)

    def set_active_network(self, item):
        """
        :type item: NetworkListItem
        :return:
        """
        self.ntwk_plot.set_networks(item.ntwk, item.ntwk_calibrated)
        self.ntwk_plot.plot.setTitle(item.text())

    def thru_list_item_deleted(self):
        item = self.listWidget_thru.selectedItems()[0]
        if item.text() == self.THRU_ID:
            self.listWidget_thru.thru = None
        elif item.text() == self.SWITCH_TERMS_ID:
            self.listWidget_thru.switch_terms = None

    def load_thru(self):
        thru = load_network_file("load thru file")
        if not thru:
            return

        if self.listWidget_thru.thru is None:
            self.listWidget_thru.thru = NetworkListItem()
            self.listWidget_thru.thru.setText(self.THRU_ID)
            self.listWidget_thru.addItem(self.listWidget_thru.thru)

        self.listWidget_thru.thru.ntwk = thru
        self.set_active_network(self.listWidget_thru.thru)

    def load_switch(self):
        qt.warnMissingFeature()

    def load_from_file(self, list_widget, caption):
        ntwk = load_network_file(caption)  # type: Network
        if not ntwk:
            return

        item = NetworkListItem()
        item.setText(ntwk.name)
        item.ntwk = ntwk
        list_widget.addItem(item)

        self.set_active_network(item)

    def load_reflect(self):
        self.load_from_file(self.listWidget_reflect, "load reflect file")

    def load_line(self):
        self.load_from_file(self.listWidget_line, "load line file")

    def load_measurement(self):
        self.load_from_file(self.listWidget_measurements, "load measurement file")
