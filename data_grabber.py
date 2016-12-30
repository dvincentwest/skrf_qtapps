import sys

import sip
from qtpy import QtWidgets, QtCore

from skrf_qtwidgets import qt, widgets
# qt.reconcile_with_matplotlib()  # needed for skrf versions that intialize matplotlib by default


class DataGrabber(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(DataGrabber, self).__init__(parent)

        # --- Setup UI --- #
        self.resize(825, 575)
        self.setWindowTitle("Scikit-RF Data Grabber")
        self.verticalLayout_main = QtWidgets.QVBoxLayout(self)

        self.vna_controller = widgets.VnaController()
        self.verticalLayout_main.addWidget(self.vna_controller)

        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal, self)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        size_policy.setVerticalStretch(1)
        self.splitter.setSizePolicy(size_policy)

        self.measurements_widget = QtWidgets.QWidget(self.splitter)
        self.measurements_widget_layout = QtWidgets.QVBoxLayout(self.measurements_widget)
        self.measurements_widget_layout.setContentsMargins(0, 0, 0, 0)

        self.btn_measureMeasurement = QtWidgets.QPushButton("Measure", self.measurements_widget)
        self.btn_loadMeasurement = QtWidgets.QPushButton("Load", self.measurements_widget)
        self.hlay_measurementButtons = QtWidgets.QHBoxLayout()
        self.hlay_measurementButtons.addWidget(self.btn_loadMeasurement)
        self.hlay_measurementButtons.addWidget(self.btn_measureMeasurement)
        self.measurements_widget_layout.addLayout(self.hlay_measurementButtons)

        self.listWidget_measurements = widgets.NetworkListWidget(self.measurements_widget)
        self.measurements_widget_layout.addWidget(self.listWidget_measurements)

        self.btn_saveSelectedMeasurements = QtWidgets.QPushButton("Save Selected")
        self.btn_saveAllMeasurements = QtWidgets.QPushButton("Save All")
        self.hlay_saveMeasurementButtons = QtWidgets.QHBoxLayout()
        self.hlay_saveMeasurementButtons.addWidget(self.btn_saveSelectedMeasurements)
        self.hlay_saveMeasurementButtons.addWidget(self.btn_saveAllMeasurements)
        self.measurements_widget_layout.addLayout(self.hlay_saveMeasurementButtons)

        self.ntwk_plot = widgets.NetworkPlotWidget(self.splitter)
        self.ntwk_plot.horizontalLayout.removeWidget(self.ntwk_plot.checkBox_useCorrected)

        self.verticalLayout_main.addWidget(self.splitter)
        self.splitter.setStretchFactor(1, 100)  # important that this goes at the end
        # --- END SETUP UI --- #

        self.listWidget_measurements.get_save_which_mode = lambda: "raw"
        self.listWidget_measurements.ntwk_plot = self.ntwk_plot
        self.listWidget_measurements.get_analyzer = self.vna_controller.get_analyzer

        self.btn_loadMeasurement.released.connect(self.listWidget_measurements.load_from_file)
        self.btn_measureMeasurement.clicked.connect(self.listWidget_measurements.measure_ntwk)
        self.btn_saveSelectedMeasurements.clicked.connect(self.listWidget_measurements.save_single_item)
        self.btn_saveAllMeasurements.clicked.connect(self.listWidget_measurements.save_all_measurements)

app = QtWidgets.QApplication(sys.argv)

form = DataGrabber()
qt.set_popup_exceptions()
form.show()

sip.setdestroyonexit(False)  # prevent a crash on exit
sys.exit(app.exec_())
