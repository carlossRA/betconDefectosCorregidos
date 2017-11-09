## Cabecera X-Frame-Options para mejorar la seguridad
Header always append X-Frame-Options SAMEORIGIN
 
# Tell the browser to attempt the HTTPS version first
Header add Strict-Transport-Security "max-age=157680000"
 
## Cabecera X-XSS-Protection para evitar ataques XSS en IE y Chrome
Header set X-XSS-Protection "1; mode=block"
 
## Cabecera X-Content-Type-Options para evitar que se carguen hojas de estilo o scripts maliciosos
Header set X-Content-Type-Options "nosniff"
 
# Disable server signature
Header set ServerSignature "Off"
Header set ServerTokens "Prod"
import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget, QTreeWidgetItem
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")

from bbdd import Bbdd


class Tipsters(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        uic.loadUi(directory + "/../ui/tipsters.ui", self)
        self.mainWindows = mainWindows
        mainWindows.diconnectActions()
        mainWindows.aNew.triggered.connect(mainWindows.newTipster)
        self.mainWindows.setWindowTitle("Tipsters | Betcon v" + mainWindows.version)
        self.treeMain.header().hideSection(1)
        self.initTree()

        self.treeMain.itemSelectionChanged.connect(self.changeItem)
        self.mainWindows.aEdit.triggered.connect(self.editItem)
        self.mainWindows.aRemove.triggered.connect(self.deleteItem)
        self.itemSelected = -1

    def initTree(self):
        bd = Bbdd()
        money = {}

        data = bd.select("conjunta")

        for i in data:
            data2 = bd.select("conjunta_tipster", None, "conjunta=" + str(i[0]))
            if len(data2) > 1:
                money_tipster = i[4]/len(data2)
                for j in data2:
                    try:
                        money[j[1]] += money_tipster
                    except:
                        money[j[1]] = money_tipster


        data = bd.select("tipster", "name")

        index = 0
        items = []
        for i in data:
            index += 1
            id = i[0]
            name = i[1]
            cost = bd.sum("tipster_month", "money", "tipster=" + str(id))
            if id in money.keys():
                cost += money[id]
            cost = "{0:.2f}".format(cost)
            profit = bd.sum("bet", "profit", "tipster=" + str(id))
            profit = "{0:.2f}".format(profit)
            item = QTreeWidgetItem([str(index), str(id), name, cost, profit])
            items.append(item)


        self.treeMain.addTopLevelItems(items)

        bd.close()

    def changeItem(self):
        self.itemSelected = self.treeMain.currentItem().text(1)
        self.mainWindows.enableActions()

    def editItem(self):
        self.mainWindows.editTipster(self.itemSelected)

    def deleteItem(self):
        resultado = QMessageBox.question(self, "Eliminar", "¿Estas seguro que desas eliminar este tipster y todas las apuestas asociadas?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resultado == QMessageBox.Yes:
            bd = Bbdd()
            bd.delete("tipster", self.itemSelected)
            bd.deleteWhere("bet", "tipster=" + str(self.itemSelected))
            self.mainWindows.setCentralWidget(Tipsters(self.mainWindows))
            self.mainWindows.enableTools()

