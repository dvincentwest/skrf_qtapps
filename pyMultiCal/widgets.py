from collections import OrderedDict
from PyQt5 import QtCore, QtWidgets

import pyqtgraph as pg
import skrf

lime_green = "#00FF00"
cyan = "#00FFFF"
magenta = "FF00FF"
yellow = "#FFFF00"
trace_colors_list = [yellow, cyan, lime_green, magenta]


def trace_color_cycle(n):
    count = 0
    while count < n:
        yield trace_colors_list[count % n]
        count += 1


class ListWidget(QtWidgets.QListWidget):

    item_removed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(ListWidget, self).__init__(parent)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.customContextMenuRequested.connect(self.listItemRightClicked)
        # self.

    def listItemRightClicked(self, position):
        menu = QtWidgets.QMenu()

        if len(self.selectedItems()) == 1:
            remove = QtWidgets.QAction("Remove Item", self)
            menu.addAction(remove)
            remove.triggered.connect(self.remove_item)

        menu.exec_(self.mapToGlobal(position))  # QtWidgets.QAction

    def remove_item(self):
        items = self.selectedItems()
        if len(items) > 0:
            item = items[0]
            self.item_removed.emit()
            self.takeItem(self.row(item))


class NetworkPlotWidget(QtWidgets.QWidget):

    S_VALS = OrderedDict((
        ("decibels", "s_db"),
        ("magnitude", "s_mag"),
        ("phase (deg)", "s_deg"),
        ("phase unwrapped (deg)", "s_deg_unwrap"),
        ("phase (rad)", "s_rad"),
        ("real", "s_re"),
        ("imaginary", "s_im"),
    ))
    S_UNITS = S_VALS.keys()

    def __init__(self, parent=None):
        super(NetworkPlotWidget, self).__init__(parent)

        self.checkBox_useCorrected = QtWidgets.QCheckBox(self)
        self.checkBox_useCorrected.setText("Plot Corrected")
        self.checkBox_useCorrected.clicked.connect(self.plot_ntwk)

        self.comboBox_unitsSelector = QtWidgets.QComboBox(self)
        self.comboBox_unitsSelector.addItems(self.S_UNITS)
        self.comboBox_unitsSelector.currentIndexChanged.connect(self.plot_ntwk)

        self.comboBox_traceSelector = QtWidgets.QComboBox(self)
        self.set_trace_items()

        self.plot_layout = pg.GraphicsLayoutWidget(self)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.addWidget(self.checkBox_useCorrected)
        self.horizontalLayout.addWidget(self.comboBox_unitsSelector)
        self.horizontalLayout.addWidget(self.comboBox_traceSelector)

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.plot_layout)
        
        self.plot = self.plot_layout.addPlot()  # type: pg.PlotItem

        self._ntwk = None
        self._ntwk_corrected = None

        self.plot.addLegend()
        self.plot.showGrid(True, True)
        self.plot.setLabel("bottom", "frequency", units="Hz")

    @property
    def ntwk(self): return self._ntwk

    @ntwk.setter
    def ntwk(self, ntwk):
        if ntwk is None or isinstance(ntwk, skrf.Network):
            self._ntwk = ntwk
            self.plot_ntwk()
        else:
            print("must set to skrf.Network or None")
            return

    @property
    def ntwk_corrected(self): return self._ntwk_corrected

    @ntwk_corrected.setter
    def ntwk_corrected(self, ntwk):
        if ntwk is None or isinstance(ntwk, skrf.Network):
            self._ntwk_corrected = ntwk
            self.plot_ntwk()
        else:
            print("must set to skrf.Network or None")
            return

    def set_networks(self, ntwk, ntwk_corrected=None):
        if ntwk is None or isinstance(ntwk, skrf.Network):
            self._ntwk = ntwk
            if ntwk is None:
                self._ntwk_corrected = None
                return
        else:
            print("ntwk must be None or skrf.Network object")

        if ntwk_corrected is None or isinstance(ntwk_corrected, skrf.Network):
            self._ntwk_corrected = ntwk_corrected
        else:
            print("corrected network must be None or skrf.Network object")

        self.plot_ntwk()

    def reset_plot(self):
        self.plot.clear()
        legend = self.plot.legend
        if legend is not None:
            legend.scene().removeItem(legend)
        self.plot.addLegend()

    def clear_plot(self):
        self._ntwk = None
        self._ntwk_corrected = None
        self.reset_plot()

    def set_trace_items(self):
        self.comboBox_traceSelector.clear()
        self.comboBox_traceSelector.addItem("all")

    def plot_ntwk(self):
        self.reset_plot()

        if self.checkBox_useCorrected.isChecked() and self._ntwk_corrected is not None:
            ntwk = self._ntwk_corrected
        else:
            ntwk = self._ntwk

        if ntwk is None:
            return

        colors = trace_color_cycle(ntwk.s.shape[1] ** 2)

        for i in range(ntwk.s.shape[2]):
            for j in range(ntwk.s.shape[1]):
                c = colors.__next__()
                label = "S{:d}{:d}".format(j + 1, i + 1)

                s_units = self.comboBox_unitsSelector.currentText()

                s = getattr(ntwk, self.S_VALS[s_units])[:, j, i]
                self.plot.plot(ntwk.f, s, pen=pg.mkPen(c), name=label)
                self.plot.setLabel("left", s_units)
