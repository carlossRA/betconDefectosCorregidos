import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")

from bookies import Bookies
from bookie import Bookie

class NewBookie(QWidget):
    def __init__(self, mainWindows):
      # QWidget.__init__(self)
        uic.loadUi(directory + "/../ui/new_bookie.ui", self)
        self.mainWindows = mainWindows
        self.btnAccept.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.cancel)
        self.mainWindows.setWindowTitle("Nueva Casa | Betcon v" + mainWindows.version)
        self.txtName.returnPressed.connect(self.btnAccept.click)

    def close(self):
            self.mainWindows.setCentralWidget(Bookies(self.mainWindows))

    def cancel(self):
        self.close()

    def accept(self):

        bookie = Bookie()
        bookie.setAll(self.txtName.text())
        err = bookie.insert()

        if err == 0:
            QMessageBox.information(self, "Añadida", "Nueva casa añadida.")
        else:
            QMessageBox.critical(self, "Error", str(err))

        self.close()

