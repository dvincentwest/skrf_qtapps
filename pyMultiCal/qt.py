from __future__ import print_function

import os
import sys
import traceback

from PyQt5 import QtCore, QtWidgets

from . import cfg


def custom_excepthook(type, value, tback):
    """overrides the default exception hook so that PyQt5 will print the error to the command line
    rather than just exiting with code 1 and no other explanation"""
    # log the exception here

    # then call the default handler
    sys.__excepthook__(type, value, tback)


def instantiate_app(sys_argv=[]):
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys_argv)
    return app


class TextWarning(QtWidgets.QDialog):
    def __init__(self, text, parent=None):
        self.setObjectName("Dialog")
        self.setWindowTitle("Warning")
        self.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(TextWarning)

        if type(text) in (list, tuple):
            text = "\n".join(text)
        self.textBrowser.setText(text)


def error_popup(error):
    if type(error) is str:
        warning = TextWarning(error)
    else:
        etype, value, tb = sys.exc_info()
        warning = TextWarning(traceback.format_exception(etype, value, tb))

    warning.exec_()


def warnMissingFeature():
    msg = "Coming soon..."
    QtWidgets.QMessageBox.warning(None, "Feature Missing", msg, QtWidgets.QMessageBox.Ok)


def getOpenFileName_Global(caption, filter, start_path=None, **kwargs):
    if start_path is None:
        start_path = cfg.last_path
    fname = str(QtWidgets.QFileDialog.getOpenFileName(None, caption, start_path, filter, **kwargs)[0])
    if fname in ("", None):
        return ""
    cfg.last_path = os.path.dirname(fname)
    return fname


def getOpenFileNames_Global(caption, filter, start_path=None, **kwargs):
    if start_path is None:
        start_path = cfg.last_path
    fnames = QtWidgets.QFileDialog.getOpenFileNames(None, caption, start_path, filter, **kwargs)[0]
    fnames = [str(fname) for fname in fnames]
    if fnames in ("", None, []):
        return []
    cfg.last_path = os.path.dirname(fnames[0])
    return fnames


def getSaveFileName_Global(caption, filter, start_path=None, **kwargs):
    if start_path is None:
        start_path = cfg.last_path
    fname = str(QtWidgets.QFileDialog.getSaveFileName(None, caption, start_path, filter, **kwargs)[0])
    if fname in ("", None):
        return ""
    cfg.last_path = os.path.dirname(fname)
    return fname


def getDirName_Global(caption=None, start_path=None, **kwargs):
    if start_path is None:
        start_path = cfg.last_path
    dirname = str(QtWidgets.QFileDialog.getExistingDirectory(None, caption, start_path, **kwargs))
    if dirname in ("", None):
        return ""
    cfg.last_path = os.path.dirname(dirname)
    return dirname
