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
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from libstats import LibStats
from func_aux import paint_row, key_from_value


class StatsStake(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        uic.loadUi(directory + "/../ui/stats_stake.ui", self)
        self.mainWindows = mainWindows
        self.mainWindows.setWindowTitle("Estadisticas Stake | Betcon v" + mainWindows.version)
        try:
            self.initData()
        except Exception:
            print("Error al intentar cargar los datos.")
            self.setEnabled(False)

        self.cmbYear.activated.connect(self.updateMonths)
        self.cmbMonth.activated.connect(self.updateTree)

    def initData(self):
        self.years, self.months = LibStats.getYears()
        self.cmbYear.addItems(self.years.keys())

        firstKey = next(iter(self.years))
        self.cmbMonth.addItems(self.getMonths(firstKey))

        data = LibStats.getStake()

        items = []
        for i in data:
            item = QTreeWidgetItem(i)
            item = paint_row(item, i[4])
            items.append(item)
        self.treeTotal.addTopLevelItems(items)

        self.updateMonths()

    def updateMonths(self):
        year = self.cmbYear.currentText()
        self.cmbMonth.clear()
        self.cmbMonth.addItems(self.getMonths(year))
        self.updateTree()

    def updateTree(self):
        year = self.cmbYear.currentText()
        sMonth = self.cmbMonth.currentText()
        month = key_from_value(self.months, sMonth)

        data = LibStats.getStake(year, month)
        self.treeMonth.clear()

        items = []
        for i in data:
            item = QTreeWidgetItem(i)
            item = paint_row(item, i[4])
            items.append(item)
        self.treeMonth.addTopLevelItems(items)

    def getMonths(self, year):
        sMonths = []
        for i in self.years[year]:
            sMonths.append(self.months[i])
        return sMonths
