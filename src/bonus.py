import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget, QTreeWidgetItem
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from func_aux import str_to_bool


class Bonus(QWidget):
	def __init__(self, mainWindows):
		#QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/bonus.ui", self)
		self.mainWindows = mainWindows
		mainWindows.diconnectActions()
		mainWindows.aNew.triggered.connect(mainWindows.newBonus)
		self.mainWindows.setWindowTitle("Bonos | Betcon v" + mainWindows.version)
		self.treeMain.header().hideSection(1)
		self.initTree()

		self.treeMain.itemSelectionChanged.connect(self.changeItem)
		self.mainWindows.aEdit.triggered.connect(self.editItem)
		self.mainWindows.aRemove.triggered.connect(self.deleteItem)
		self.itemSelected = -1

	def initTree(self):
		bd = Bbdd()
		data = bd.select("bonus", "date")

		items = []
		for i in data:
			id = i[0]
			date = i[1]
			bookie = bd.getValue(i[2], "bookie")
			money = i[3]
			free = "Sí" if str_to_bool(i[4]) else "No"
			item = QTreeWidgetItem([str(date), str(id), str(bookie), str(money), str(free)])
			items.append(item)

		self.treeMain.addTopLevelItems(items)

		bd.close()

	def changeItem(self):
		self.itemSelected = self.treeMain.currentItem().text(1)
		self.mainWindows.enableActions()

	def editItem(self):
		self.mainWindows.editBonus(self.itemSelected)

	def deleteItem(self):
		resultado = QMessageBox.question(self, "Eliminar", "¿Estas seguro que desas eliminarlo?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if resultado == QMessageBox.Yes:
			bd = Bbdd()
			bd.delete("bonus", self.itemSelected)
			self.mainWindows.setCentralWidget(Bonus(self.mainWindows))
			self.mainWindows.enableTools()

