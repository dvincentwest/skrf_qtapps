import sys

import sip
from qtpy import QtWidgets

from skrf_qtwidgets import qt
# qt.reconcile_with_matplotlib()  # needed for skrf which initializes matplotlib by default

from skrf_qtwidgets import widgets

app = QtWidgets.QApplication(sys.argv)

form = widgets.VnaController()
qt.set_popup_exceptions()
form.show()

sip.setdestroyonexit(False)  # prevent a crash on exit
sys.exit(app.exec_())
