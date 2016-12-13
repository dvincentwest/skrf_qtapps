import sys

import sip
from qtpy import QtWidgets

from skrf_qtwidgets import trlwidget, qt

app = QtWidgets.QApplication(sys.argv)

form = trlwidget.TRLWidget()
qt.set_popup_exceptions()
form.show()

sip.setdestroyonexit(False)  # prevent a crash on exit
sys.exit(app.exec_())
