from __future__ import print_function
import sys
import os

skrf_qtapps_path = os.path.dirname(os.path.abspath(__file__ + "/.."))
sys.path.insert(0, skrf_qtapps_path)


if len(sys.argv) > 1:
    if sys.argv[1].lower() in ("pyqt4", "pyqt"):
        from PyQt4 import QtCore
    elif sys.argv[1].lower() == "pyside":
        from PySide import QtCore
    else:
        from PyQt5 import QtCore
else:
    from PyQt5 import QtCore

import sip
from qtpy import QtWidgets
from skrf_qtwidgets import qt

app = QtWidgets.QApplication(sys.argv)


def get_filename():
    filename = QtWidgets.QFileDialog.getOpenFileName()
    # filenames = QtWidgets.QFileDialog.getOpenFileNameAndFilter()
    # filename = qt.getOpenFileName_Global("Open File", "*")
    print(filename)
    # print(filenames)
    return filename


# def get_filenames():
#     # filename = QtWidgets.QFileDialog.getOpenFileName()
#     filenames = qt.getOpenFileName_Global("Open File", "*")
#     print(filename)
#     return filename


form = QtWidgets.QWidget()
btn_openFile = QtWidgets.QPushButton("Open File", form)
btn_openFile.clicked.connect(get_filename)
btn_saveFile = QtWidgets.QPushButton("Save File", form)
btn_saveFile.clicked.connect(get_filename)
btn_openFiles = QtWidgets.QPushButton("Open Files", form)
btn_openFiles.clicked.connect(get_filename)
btn_saveFiles = QtWidgets.QPushButton("Save Files", form)
btn_saveFiles.clicked.connect(get_filename)
form.show()

# app.exec_()
sip.setdestroyonexit(False)  # prevent a crash on exit
sys.exit(app.exec_())
