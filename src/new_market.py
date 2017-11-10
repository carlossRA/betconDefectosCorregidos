import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from markets import Markets

class NewMarket(QWidget):
    def __init__(self, mainWindows):
     #  QWidget.__init__(self)
        uic.loadUi(directory + "/../ui/new_bookie.ui", self)
        self.mainWindows = mainWindows
        self.btnAccept.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.cancel)
        self.mainWindows.setWindowTitle("Nuevo Mercado | Betcon v" + mainWindows.version)
        self.txtName.returnPressed.connect(self.btnAccept.click)

    def close(self):
            self.mainWindows.setCentralWidget(Markets(self.mainWindows))
            #self.mainWindows.aApuesta.setEnabled(True)

    def cancel(self):
        self.close()

    def accept(self):
        data = [self.txtName.text()]
        columns = ["name"]

        bbdd = Bbdd()
        bbdd.insert(columns, data, "market")
        bbdd.close()

        QMessageBox.information(self, "Añadido", "Nuevo mercado añadido.")

        self.close()

