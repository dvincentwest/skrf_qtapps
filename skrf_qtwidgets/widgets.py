from collections import OrderedDict
import os.path
import re
from math import sqrt

from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
import skrf
from qtpy import QtWidgets, QtCore
from skrf import Network, four_oneports_2_twoport

from skrf_qtwidgets import qt
from . import qt

lime_green = "#00FF00"
cyan = "#00FFFF"
magenta = "FF00FF"
yellow = "#FFFF00"
trace_colors_list = [yellow, cyan, magenta, lime_green]


def trace_color_cycle(n=1000):
    """
    :type n: int
    :return:
    """
    count = 0
    colors = [yellow, cyan, magenta, lime_green]
    num = len(colors)
    while count < n:
        yield colors[count % num]
        count += 1


def save_multiple_networks(ntwk_list):
    dirname = qt.getDirName_Global("select directory to save network files")
    if not dirname:
        return

    remember = False
    overwrite = False
    for ntwk in ntwk_list:
        if isinstance(ntwk, skrf.Network):
            fname = os.path.join(dirname, ntwk.name) + ".s{:d}p".format(ntwk.s.shape[1])
            if os.path.isfile(fname):
                if not remember:
                    msg = "The file:\n" + fname + "\nalready exists.\n\nDo you want to overwrite the file?"
                    dialog = OverwriteFilesQuery(title="File Already Exists", msg=msg)
                    dialog.exec_()
                    if dialog.choice == "yes":
                        overwrite = True
                    elif dialog.choice == "yes to all":
                        overwrite = True
                        remember = True
                    elif dialog.choice == "no":
                        overwrite = False
                    elif dialog.choice == "cancel":
                        return
                    else:
                        raise ValueError("did not recognize dialog choice")

                if not overwrite:
                    filter = "Touchstone file (*.s{:d}p)".format(ntwk.s.shape[1])
                    fname = qt.getSaveFileName_Global("save network file", filter)

            ntwk.write_touchstone(fname)


@QtCore.Slot(object, str)
def save_NetworkListItem(ntwk_list_item, save_which):
    """
    :type ntwk_list_item: NetworkListItem
    :param save_which: str
    :return:
    """

    if save_which.lower() not in ("raw", "cal", "both"):
        raise ValueError("Must set save option to 'raw', 'cal', or 'both'")

    ntwk = ntwk_list_item.ntwk
    ntwk_c = ntwk_list_item.ntwk_calibrated

    if type(ntwk) in (list, tuple):
        save_multiple_networks(ntwk)
        return
    elif not isinstance(ntwk, skrf.Network):
        raise TypeError("ntwk must be a Network object to save")

    extension = ".s{:d}p".format(ntwk.s.shape[1])
    file_filter = "touchstone format (*{:s})".format(extension)
    filename = os.path.join(qt.cfg.last_path, ntwk.name + extension)

    if save_which.lower() == "both":
        if isinstance(ntwk, skrf.Network) and isinstance(ntwk_c, skrf.Network):
            filename = qt.getSaveFileName_Global("Save Raw Network File", filter=file_filter, start_path=filename)
            if not filename:
                return
            base, ext = os.path.splitext(filename)
            filename_cal = base + "-cal" + ext
            filename_cal = qt.getSaveFileName_Global("Save Calibrated Network File",
                                                 filter=file_filter,
                                                 start_path=filename_cal)
            if not filename_cal:
                return
            ntwk.write_touchstone(filename)
            ntwk_c.write_touchstone(filename_cal)
            return
        else:
            save_which = "raw"

    if save_which.lower() == "cal":
        if ntwk_list_item.ntwk_calibrated is None:
            Warning("ntwk_calibrated is None, saving raw instead")
            save_which = "raw"
        else:
            ntwk = ntwk_list_item.ntwk_calibrated
            filename = os.path.join(qt.cfg.last_path, ntwk.name + extension)

    caption = "Save Network File" if save_which.lower() == "raw" else "Save Calibrated Network File"
    filename = qt.getSaveFileName_Global(caption, filter=file_filter, start_path=filename)
    ntwk.write_touchstone(filename)


class OverwriteFilesQuery(QtWidgets.QDialog):
    def __init__(self, title="", msg="", parent=None):
        super(OverwriteFilesQuery, self).__init__(parent)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.verticalLayout.addWidget(self.textBrowser)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes|QtWidgets.QDialogButtonBox.YesToAll)

        self.choice = None

        self.yes = self.buttonBox.button(QtWidgets.QDialogButtonBox.Yes)
        self.yesToAll = self.buttonBox.button(QtWidgets.QDialogButtonBox.YesToAll)
        self.no = self.buttonBox.button(QtWidgets.QDialogButtonBox.No)
        self.cancel = self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel)
        self.yes.clicked.connect(self.set_yes)
        self.yesToAll.clicked.connect(self.set_yesToAll)
        self.no.clicked.connect(self.set_no)
        self.cancel.clicked.connect(self.set_cancel)

        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.setWindowTitle(title)
        self.textBrowser.setText(msg)

    def set_yes(self):
        self.choice = "yes"

    def set_yesToAll(self):
        self.choice = "yes to all"

    def set_no(self):
        self.choice = "no"

    def set_cancel(self):
        self.choice = "cancel"


class NetworkListItem(QtWidgets.QListWidgetItem):

    def __init__(self, parent=None):
        super(NetworkListItem, self).__init__(parent)
        self.ntwk = None
        self.ntwk_calibrated = None

    def update_ntwk_names(self):
        if isinstance(self.ntwk, skrf.Network):
            self.ntwk.name = self.text()
        if isinstance(self.ntwk_calibrated, skrf.Network):
            self.ntwk_calibrated.name = self.text() + "-cal"


class NetworkListWidget(QtWidgets.QListWidget):

    item_removed = QtCore.Signal()
    item_updated = QtCore.Signal(object)
    save_single_requested = QtCore.Signal(object, str)

    def __init__(self, parent=None):
        super(NetworkListWidget, self).__init__(parent)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.customContextMenuRequested.connect(self.listItemRightClicked)
        self.save_single_requested.connect(save_NetworkListItem)
        self.itemDelegate().commitData.connect(self.item_text_updated)

    def get_unique_name(self, name, exclude_item=-1):
        '''
        :type name: str
        :type exclude_item: int
        :return:
        '''
        names = []
        for i in range(self.count()):
            if i == exclude_item:
                continue

            item = self.item(i)
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

    def item_text_updated(self):
        item = self.currentItem()  # type: NetworkListItem
        item.setText(self.get_unique_name(item.text(), self.row(item)))
        item.update_ntwk_names()
        self.item_updated.emit(item)

    def listItemRightClicked(self, position):
        menu = QtWidgets.QMenu()

        if len(self.selectedItems()) == 1:
            save = QtWidgets.QAction("Save Item", self)
            menu.addAction(save)
            save.triggered.connect(self.save_single_item)

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

    def get_save_which_mode(self):
        """
        because the item will potentially have a raw and calibrated network attached we need
        to determine if we want to save
        "raw", "cal", or "both"
        the default will be to save both, and this method must be replaced by the parent infrastructure
        for a different result

        :return: int
        """
        return "both"

    def save_single_item(self):
        items = self.selectedItems()
        if len(items) > 0:
            item = items[0]
            self.save_single_requested.emit(item, self.get_save_which_mode())


class NetworkPlotWidget(QtWidgets.QWidget):

    S_VALS = OrderedDict((
        ("decibels", "s_db"),
        ("magnitude", "s_mag"),
        ("phase (deg)", "s_deg"),
        ("phase unwrapped (deg)", "s_deg_unwrap"),
        ("phase (rad)", "s_rad"),
        ("phase unwrapped (rad)", "s_rad_unwrap"),
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
        self.comboBox_traceSelector.setCurrentIndex(0)
        self.comboBox_traceSelector.currentIndexChanged.connect(self.plot_ntwk)

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
        self._ntwk_list = None

        self.plot.addLegend()
        self.plot.showGrid(True, True)
        self.plot.setLabel("bottom", "frequency", units="Hz")

    @property
    def ntwk(self): return self._ntwk

    @ntwk.setter
    def ntwk(self, ntwk):
        if ntwk is None or isinstance(ntwk, skrf.Network):
            self.set_trace_items(ntwk)
            self._ntwk = ntwk
            self.plot_ntwk()
        elif type(ntwk) in (list, tuple):
            self.ntwk_list = ntwk
        else:
            raise TypeError("must set to skrf.Network or None")

    @property
    def ntwk_corrected(self): return self._ntwk_corrected

    @ntwk_corrected.setter
    def ntwk_corrected(self, ntwk):
        if ntwk is None or isinstance(ntwk, skrf.Network):
            self._ntwk_corrected = ntwk
            self.plot_ntwk()
        else:
            raise TypeError("must set to skrf.Network or None")

    @property
    def ntwk_list(self): return self._ntwk_list

    @ntwk_list.setter
    def ntwk_list(self, ntwk_list):
        self.set_trace_items(ntwk_list)
        if ntwk_list is None:
            self._ntwk_list = ntwk_list
        elif type(ntwk_list) in (list, tuple):
            for ntwk in ntwk_list:
                if not isinstance(ntwk, skrf.Network):
                    raise TypeError("all items in list must be network objects")
            self._ntwk = self._ntwk_corrected = None
            self._ntwk_list = ntwk_list
            self.plot_ntwk_list()
        else:
            raise TypeError("must provide a list of Network Objects")

    def set_networks(self, ntwk, ntwk_corrected=None):
        if ntwk is None or isinstance(ntwk, skrf.Network):
            self._ntwk = ntwk
            self.set_trace_items(self._ntwk)
            if ntwk is None:
                self._ntwk_corrected = None
                self.set_trace_items(self._ntwk)
                return
        else:
            raise TypeError("must set to skrf.Network or None")

        if ntwk_corrected is None or isinstance(ntwk_corrected, skrf.Network):
            self._ntwk_corrected = ntwk_corrected
        else:
            raise TypeError("must set to skrf.Network or None")

        self.plot_ntwk()

    def reset_plot(self):
        self.plot.clear()
        self.plot.setTitle(None)
        legend = self.plot.legend
        if legend is not None:
            legend.scene().removeItem(legend)
        self.plot.addLegend()

    def clear_plot(self):
        self._ntwk = None
        self._ntwk_corrected = None
        self._ntwk_list = None
        self.reset_plot()

    def set_trace_items(self, ntwk=None):
        self.comboBox_traceSelector.blockSignals(True)
        current_index = self.comboBox_traceSelector.currentIndex()
        nports = 0

        if isinstance(ntwk, Network):
            nports = ntwk.nports
        elif type(ntwk) in (list, tuple):
            for n in ntwk:
                if n.nports > nports:
                    nports = n.nports

        self.comboBox_traceSelector.clear()
        self.comboBox_traceSelector.addItem("all")

        for n in range(nports):
            for m in range(nports):
                self.comboBox_traceSelector.addItem("S{:d}{:d}".format(m + 1, n + 1))

        if current_index <= self.comboBox_traceSelector.count():
            self.comboBox_traceSelector.setCurrentIndex(current_index)
        else:
            self.comboBox_traceSelector.setCurrentIndex(0)
        self.comboBox_traceSelector.blockSignals(False)

    def plot_ntwk(self):
        self.reset_plot()

        if self.checkBox_useCorrected.isChecked() and self._ntwk_corrected is not None:
            ntwk = self._ntwk_corrected
        else:
            ntwk = self._ntwk

        if ntwk is None:
            if self.ntwk_list is not None:
                self.plot_ntwk_list()
            return

        colors = trace_color_cycle(ntwk.s.shape[1] ** 2)

        trace = self.comboBox_traceSelector.currentIndex()
        mn = _n = _m = 0
        if trace > 0:
            mn = trace - 1
            nports = int(sqrt(self.comboBox_traceSelector.count() - 1))
            _m = mn % nports
            _n = int((mn - mn % nports) / nports)

        for n in range(ntwk.s.shape[2]):
            for m in range(ntwk.s.shape[1]):
                c = next(colors)

                if trace > 0:
                    if not n == _n or not m == _m:
                        continue

                label = "S{:d}{:d}".format(m + 1, n + 1)

                s_units = self.comboBox_unitsSelector.currentText()

                s = getattr(ntwk, self.S_VALS[s_units])[:, m, n]
                self.plot.plot(ntwk.f, s, pen=pg.mkPen(c), name=label)
                self.plot.setLabel("left", s_units)
        self.plot.setTitle(ntwk.name)

    def plot_ntwk_list(self):
        self.reset_plot()

        if self.ntwk_list is None:
            return

        colors = trace_color_cycle()

        trace = self.comboBox_traceSelector.currentIndex()
        mn = _n = _m = 0
        if trace > 0:
            mn = trace - 1
            nports = int(sqrt(self.comboBox_traceSelector.count() - 1))
            _m = mn % nports
            _n = int((mn - mn % nports) / nports)

        for ntwk in self.ntwk_list:
            for n in range(ntwk.s.shape[2]):
                for m in range(ntwk.s.shape[1]):
                    c = next(colors)

                    if trace > 0:
                        if not n == _n or not m == _m:
                            continue

                    label = ntwk.name
                    if ntwk.s.shape[1] > 1:
                        label += " - S{:d}{:d}".format(m + 1, n + 1)

                    s_units = self.comboBox_unitsSelector.currentText()

                    s = getattr(ntwk, self.S_VALS[s_units])[:, m, n]
                    self.plot.plot(ntwk.f, s, pen=pg.mkPen(c), name=label)
                    self.plot.setLabel("left", s_units)


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
                self.reflect_2port.s[:, 0, 1] = 0
                self.reflect_2port.s[:, 1, 0] = 0
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