import sys

import sip
from PyQt5 import QtWidgets

from pyMultiCal import trlwidget

app = QtWidgets.QApplication(sys.argv)  # conflicting code requires me to initialize here

form = trlwidget.TRLWidget()
form.show()

sip.setdestroyonexit(False)  # prevent a crash on exit
sys.exit(app.exec_())
