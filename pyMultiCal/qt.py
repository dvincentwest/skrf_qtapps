from __future__ import print_function

import os
import sys
import traceback

from qtpy import QtCore, QtWidgets

from . import cfg


def _excepthook(type, value, tback):
    """overrides the default exception hook so that errors will print the error to the command line
    rather than just exiting with code 1 and no other explanation"""
    # log the exception here

    # then call the default handler
    error = "\n".join(traceback.format_exception(type, value, tback))
    QtWidgets.QMessageBox.warning(None, "Python Exception", error, QtWidgets.QMessageBox.Ok)
    # sys.__excepthook__(type, value, tback)
sys.excepthook = _excepthook


def instantiate_app(sys_argv=[]):
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys_argv)
    return app


class TextWarning(QtWidgets.QDialog):
    def __init__(self, text, parent=None):
        super(TextWarning, self).__init__(parent)
        self.setWindowTitle("Warning")
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.verticalLayout.addWidget(self.textBrowser)

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        if type(text) in (list, tuple):
            text = "\n".join(text)
        self.textBrowser.setText(text)


def error_popup(error):
    if not type(error) is str:
        etype, value, tb = sys.exc_info()
        error = "\n".join(traceback.format_exception(etype, value, tb))
    QtWidgets.QMessageBox.warning(None, "Python Exception", error, QtWidgets.QMessageBox.Ok)


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
    cfg.last_path = dirname
    return dirname


if __name__ == "main":
    # run some tests
    pass
