import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from markets import Markets

class EditMarket(QWidget):
    def __init__(self, mainWindows, id):
      #  QWidget.__init__(self)
        uic.loadUi(directory + "/../ui/new_bookie.ui", self)
        self.mainWindows = mainWindows
        self.btnAccept.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.cancel)
        self.mainWindows.setWindowTitle("Modificar Mercado | Betcon v" + mainWindows.version)
        self.txtName.returnPressed.connect(self.btnAccept.click)

        self.id = id
        self.initData()

    def initData(self):
        bd = Bbdd()

        name = bd.getValue(self.id, "market")
        self.txtName.setText(name)

        bd.close()

    def close(self):
            self.mainWindows.setCentralWidget(Markets(self.mainWindows))

    def cancel(self):
        self.close()

    def accept(self):
        data = [self.txtName.text()]
        columns = ["name"]

        bbdd = Bbdd()
        bbdd.update(columns, data, "market", "id="+self.id)
        bbdd.close()

        QMessageBox.information(self, "Actualizado", "Mercado actualizado.")

        self.close()

