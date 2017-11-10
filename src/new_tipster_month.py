import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from tipsters_month import TipstersMonth
from func_aux import str_to_float

class NewTipsterMonth(QWidget):
	def __init__(self, mainWindows):
	#	QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/new_tipster_month.ui", self)
		self.mainWindows = mainWindows
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		self.mainWindows.setWindowTitle("Nuevo Pago Tipster | Betcon v" + mainWindows.version)

		self.initData()

	def initData(self):
		bd = Bbdd()
		data = bd.select("tipster", "name")

		self.tipsterIndexToId = {}
		index = 0
		for i in data:
			id = i[0]
			name = i[1]
			self.cmbTipster.addItem(name)
			self.tipsterIndexToId[index] = id
			index += 1

		bd.close()

	def close(self):
			self.mainWindows.setCentralWidget(TipstersMonth(self.mainWindows))
			#self.mainWindows.aApuesta.setEnabled(True)

	def cancel(self):
		self.close()

	def accept(self):
		idTipster = self.tipsterIndexToId.get(self.cmbTipster.currentIndex())
		print(idTipster)
		money = str(str_to_float(self.txtMoney.text()))
		data = [self.cmbMonth.currentIndex(), self.txtYear.text(), idTipster, money]
		columns = ["month", "year", "tipster", "money"]

		bbdd = Bbdd()
		bbdd.insert(columns, data, "tipster_month")
		bbdd.close()

		QMessageBox.information(self, "Añadido", "Nuevo pago de tipster añadido.")

		self.close()

