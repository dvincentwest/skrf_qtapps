from collections import OrderedDict
import os.path
import re

from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
import skrf

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
    while count < n:
        yield trace_colors_list[count % n]
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


@QtCore.pyqtSlot(object, str)
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

    item_removed = QtCore.pyqtSignal()
    save_single_requested = QtCore.pyqtSignal(object, str)

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
        self._ntwk_list = None

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
        if ntwk_list is None:
            self._ntwk_list = ntwk_list
        elif type(ntwk_list) in (list, tuple):
            for ntwk in ntwk_list:
                if not isinstance(ntwk, skrf.Network):
                    raise TypeError("all items in list must be network objects")
            self._ntwk_list = ntwk_list
            self.plot_ntwk_list()
        else:
            raise TypeError("must provide a list of Network Objects")

    def set_networks(self, ntwk, ntwk_corrected=None):
        if ntwk is None or isinstance(ntwk, skrf.Network):
            self._ntwk = ntwk
            if ntwk is None:
                self._ntwk_corrected = None
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
            if self.ntwk_list is None:
                return
            else:
                self.plot_ntwk_list()

        colors = trace_color_cycle(ntwk.s.shape[1] ** 2)

        for i in range(ntwk.s.shape[2]):
            for j in range(ntwk.s.shape[1]):
                c = colors.__next__()
                label = "S{:d}{:d}".format(j + 1, i + 1)

                s_units = self.comboBox_unitsSelector.currentText()

                s = getattr(ntwk, self.S_VALS[s_units])[:, j, i]
                self.plot.plot(ntwk.f, s, pen=pg.mkPen(c), name=label)
                self.plot.setLabel("left", s_units)
        self.plot.setTitle(ntwk.name)

    def plot_ntwk_list(self):
        self.reset_plot()

        if self.ntwk_list is None:
            return

        colors = trace_color_cycle()

        for ntwk in self.ntwk_list:
            for i in range(ntwk.s.shape[2]):
                for j in range(ntwk.s.shape[1]):
                    c = colors.__next__()

                    label = ntwk.name
                    if ntwk.s.shape[1] > 1:
                        label += " - S{:d}{:d}".format(j + 1, i + 1)

                    s_units = self.comboBox_unitsSelector.currentText()

                    s = getattr(ntwk, self.S_VALS[s_units])[:, j, i]
                    self.plot.plot(ntwk.f, s, pen=pg.mkPen(c), name=label)
                    self.plot.setLabel("left", s_units)
