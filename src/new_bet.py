import sys, os, inspect
from datetime import datetime
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QWidget, QComboBox, QAction, QPushButton, QShortcut, QHBoxLayout, QLayout, QDateTimeEdit
from PyQt5 import uic
from PyQt5.QtCore import QDateTime, QVariant
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bets import Bets
from decimal import Decimal
from func_aux import str_to_float, str_to_bool

from bbdd import Bbdd
from bookie import Bookie
from libyaml import LibYaml


class NewBet(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/new_bet.ui", self)
		self.mainWindows = mainWindows
		self.mainWindows.setWindowTitle("Nueva Apuesta | Betcon v" + mainWindows.version)
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		self.btnAdd.clicked.connect(self.addCombined)
		self.initData()
		self.cmbRegion.activated.connect(self.setCompetition)
		self.cmbSport.activated.connect(self.setRegion)
		self.cmbResult.activated.connect(self.updateProfit)
		self.cmbMarket.activated.connect(self.combined)
		self.txtQuota.valueChanged.connect(self.updateProfit)
		self.txtBet.valueChanged.connect(self.updateProfit)
		self.chkFree.clicked.connect(self.freeBet)
		self.txtStake.valueChanged.connect(self.updateBet)
		self.txtOne.valueChanged.connect(self.updateBet)

		#self.setPnlVisible(self.pnlDate, False)
		self.combined()


	# self.txtQuota.activated.connect(self.setCompetition)




	def initData(self):
		# dtDate
		sDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		date = QDateTime.fromString(sDate, "yyyy-MM-dd hh:mm:ss")
		self.dtDate.setDateTime(date)

		# cmbSport
		bd = Bbdd()
		data = bd.select("sport", "name")

		self.sportIndexToId = {}
		index = 0
		for i in data:
			id = i[0]
			name = i[1]
			self.cmbSport.addItem(name)
			self.sportIndexToId[index] = id
			index += 1

		# cmbBookie
		data = bd.select("bookie", "name")

		self.bookieIndexToId = {}
		index = 0
		for i in data:
			id = i[0]
			name = i[1]
			self.cmbBookie.addItem(name)
			self.bookieIndexToId[index] = id
			index += 1

		# cmbMarket
		data = bd.select("market", "name")

		self.marketIndexToId = {}
		index = 0
		for i in data:
			id = i[0]
			name = i[1]
			self.cmbMarket.addItem(name)
			self.marketIndexToId[index] = id
			index += 1

		# cmbTipster
		data = bd.select("tipster", "name")

		self.tipsterIndexToId = {}
		index = 0
		for i in data:
			id = i[0]
			name = i[1]
			self.cmbTipster.addItem(name)
			self.tipsterIndexToId[index] = id
			index += 1

		self.players = bd.executeQuery("SELECT player1 as player FROM bet UNION SELECT player2 as player FROM bet ORDER BY player")
		self.players = [row[0] for row in self.players]

		self.txtPlayer1.addItems(self.players)
		self.txtPlayer2.addItems(self.players)
		bd.close()

		# cmbCompetition
		self.setRegion()

		#Combined
		self.contComb = 0
		self.dates = []
		self.sports = []
		self.regions = []
		self.competitions = []
		self.players1 = []
		self.players2 = []
		self.picks = []
		self.results = []
		self.buttons = []

		self.regionIndexToIdCmb = []
		self.competitionIndexToIdCmb = []
		self.calcStake()

	def setCompetition(self):
		self.cmbCompetition.clear()
		bd = Bbdd()

		idRegion = self.regionIndexToId.get(self.cmbRegion.currentIndex())
		idSport = self.sportIndexToId.get(self.cmbSport.currentIndex())

		where = "region=" + str(idRegion) + " AND sport=" + str(idSport)

		data = bd.select("competition", "name", where)

		self.competitionIndexToId = {}
		index = 0
		for i in data:
			id = i[0]
			name = i[1]
			self.cmbCompetition.addItem(name)
			self.competitionIndexToId[index] = id
			index += 1

		if index == 0:
			self.btnAccept.setDisabled(True)
		else:
			self.btnAccept.setDisabled(False)

		bd.close()


	def setRegion(self):
		self.btnAccept.setDisabled(False)
		self.cmbRegion.clear()
		bd = Bbdd()

		idSport = self.sportIndexToId.get(self.cmbSport.currentIndex())

		where = " sport=" + str(idSport)

		data = bd.select("competition", None, where, "region")
		dataRegion = ""

		if len(data) > 0:
			sData = "("
			j= 0
			for i in data:
				if j == len(data)-1:
					sData += str(i[0]) + ")"
				else:
					sData += str(i[0]) + ", "
				j+=1

			where = " id in "+sData
			dataRegion = bd.select("region", "name", where)

			if len(dataRegion) < 1:
				self.btnAccept.setDisabled(True)
				bd.close()
			else:
				self.regionIndexToId = {}
				index = 0
				for i in dataRegion:
					id = i[0]
					name = i[1]
					self.cmbRegion.addItem(name)
					self.regionIndexToId[index] = id
					index += 1
				bd.close()
				self.setCompetition()

		else:
			self.btnAccept.setDisabled(True)
			bd.close()

		if len(data) == 0 or len(dataRegion) == 0:
			self.btnAccept.setDisabled(True)
		else:
			self.btnAccept.setDisabled(False)

	def close(self):
		self.mainWindows.setCentralWidget(Bets(self.mainWindows))

	def cancel(self):
		self.close()

	def accept(self):
		data = []

		bbdd = Bbdd()

		# dtDate
		data.append(self.dtDate.dateTime().toPyDateTime())

		# cmbSport
		idSport = self.sportIndexToId.get(self.cmbSport.currentIndex())
		data.append(idSport)

		# cmbCompetition
		idCompetition = self.competitionIndexToId.get(self.cmbCompetition.currentIndex())
		data.append(idCompetition)

		# cmbRegion
		idRegion = self.regionIndexToId.get(self.cmbRegion.currentIndex())
		data.append(idRegion)

		data.append(self.txtPlayer1.currentText())
		data.append(self.txtPlayer2.currentText())
		data.append(self.txtPick.text())

		# cmbBookie
		idBookie = self.bookieIndexToId.get(self.cmbBookie.currentIndex())
		data.append(idBookie)

		# cmbMarket
		idMarket = self.marketIndexToId.get(self.cmbMarket.currentIndex())
		data.append(idMarket)

		# cmbTipster
		idTipster = self.tipsterIndexToId.get(self.cmbTipster.currentIndex())
		data.append(idTipster)

		data.append(str(str_to_float(self.txtStake.text())))
		data.append(str(str_to_float(self.txtOne.text())))

		# cmbResult
		data.append(self.cmbResult.currentText())

		data.append(str(str_to_float(self.txtProfit.text())))
		data.append(str(str_to_float(self.txtBet.text())))
		data.append(str(str_to_float(self.txtQuota.text())))
		data.append(1 if self.chkFree.isChecked() else 0)

		columns = ["date", "sport", "competition", "region", "player1", "player2", "pick", "bookie", "market",
		           "tipster", "stake", "one", "result", "profit", "bet", "quota", "free"]

		bbdd.insert(columns, data, "bet")

		id_bet = bbdd.max("bet", "id")

		if self.cmbMarket.currentText() == "Combinada":
			columns = ["bet", "date", "sport", "competition", "region", "player1", "player2", "pick", "result"]

			for i in range(0, self.contComb):
				data = []
				data.append(id_bet)
				data.append(self.dates[i].dateTime().toPyDateTime())
				idSport = self.sportIndexToId.get(self.sports[i].currentIndex())
				data.append(idSport)
				idCompetition = self.competitionIndexToIdCmb[i].get(self.competitions[i].currentIndex())
				data.append(idCompetition)
				idRegion = self.regionIndexToIdCmb[i].get(self.regions[i].currentIndex())
				data.append(idRegion)
				data.append(self.players1[i].currentText())
				data.append(self.players2[i].currentText())
				data.append(self.picks[i].text())
				data.append(self.results[i].currentText())
				bbdd.insert(columns, data, "combined")



		bbdd.close()

		QMessageBox.information(self, "Añadida", "Nueva apuesta añadida.")
		self.close()

	

	def setCombinedVisible(self, visible):
		self.btnAdd.setVisible(visible)
		self.lblDate.setVisible(visible)
		self.lblSport.setVisible(visible)
		self.lblRegion.setVisible(visible)
		self.lblCompetition.setVisible(visible)
		self.lblPlayer1.setVisible(visible)
		self.lblPlayer2.setVisible(visible)
		self.lblResult.setVisible(visible)
		self.lblPick.setVisible(visible)
		for i in range(self.contComb):
			self.dates[i].setVisible(visible)
			self.sports[i].setVisible(visible)
			self.competitions[i].setVisible(visible)
			self.regions[i].setVisible(visible)
			self.players1[i].setVisible(visible)
			self.players2[i].setVisible(visible)
			self.picks[i].setVisible(visible)
			self.results[i].setVisible(visible)
			self.buttons[i].setVisible(visible)

	def combined(self):
		if self.cmbMarket.currentText() == "Combinada":
			self.setCombinedVisible(True)
		else:
			self.setCombinedVisible(False)

	def removeRow(self, index):
		# TODO: FIX THIS!!
		obj1 = self.dates.pop(index)
		self.pnlDate.removeWidget(obj1)
		obj1.setVisible(False)
		obj2 = self.sports.pop(index)
		self.pnlSport.removeWidget(obj2)
		obj2.setVisible(False)
		obj3 = self.regions.pop(index)
		self.pnlRegion.removeWidget(obj3)
		obj3.setVisible(False)
		obj4 = self.competitions.pop(index)
		self.pnlCompetition.removeWidget(obj4)
		obj4.setVisible(False)
		obj5 = self.players1.pop(index)
		self.pnlPlayer1.removeWidget(obj5)
		obj5.setVisible(False)
		obj6 = self.players2.pop(index)
		self.pnlPlayer2.removeWidget(obj6)
		obj6.setVisible(False)
		obj7 = self.picks.pop(index)
		self.pnlPick.removeWidget(obj7)
		obj7.setVisible(False)
		obj8 = self.results.pop(index)
		self.pnlResult.removeWidget(obj8)
		obj8.setVisible(False)
		obj9 = self.buttons.pop(index)
		self.pnlButton.removeWidget(obj9)
		obj9.setVisible(False)

		self.contComb -= 1

		for i in range(self.contComb):
			self.pnlButton.removeWidget(self.buttons[i])
			self.buttons[i].disconnect()
			self.buttons[i].clicked.connect(lambda: self.removeRow(i))
			self.pnlButton.addWidget(self.buttons[i])

		if self.contComb == 9:
			self.btnAdd.setEnabled(True)

	def setCompetitionComb(self, index_cmb):
		self.competitions[index_cmb].clear()
		bd = Bbdd()

		idRegion = self.regionIndexToIdCmb[index_cmb].get(self.regions[index_cmb].currentIndex())
		idSport = self.sportIndexToId.get(self.sports[index_cmb].currentIndex())

		where = "region=" + str(idRegion) + " AND sport=" + str(idSport)

		try:
			data = bd.select("competition", "name", where)

			index = 0
			self.competitionIndexToIdCmb[index_cmb] = {}
			for i in data:
				id = i[0]
				name = i[1]
				self.competitions[index_cmb].addItem(name)
				self.competitionIndexToIdCmb[index_cmb][index] = id
				index += 1

			if index == 0:
				self.btnAccept.setDisabled(True)
			else:
				self.btnAccept.setDisabled(False)
		except:
			self.btnAccept.setDisabled(True)

		bd.close()


	def setRegionComb(self, index_cmb):
		self.btnAccept.setDisabled(False)
		self.regions[index_cmb].clear()
		bd = Bbdd()

		idSport = self.sportIndexToId.get(self.sports[index_cmb].currentIndex())

		where = " sport=" + str(idSport)

		data = bd.select("competition", None, where, "region")
		dataRegion = ""

		if len(data) > 0:
			sData = "("
			j= 0
			for i in data:
				if j == len(data)-1:
					sData += str(i[0]) + ")"
				else:
					sData += str(i[0]) + ", "
				j += 1

			where = " id in "+sData
			dataRegion = bd.select("region", "name", where)

			if len(dataRegion) < 1:
				self.btnAccept.setDisabled(True)
				bd.close()
			else:
				self.regionIndexToIdCmb[index_cmb] = {}
				index = 0
				for i in dataRegion:
					id = i[0]
					name = i[1]
					self.regions[index_cmb].addItem(name)
					self.regionIndexToIdCmb[index_cmb][index] = id
					index += 1
				bd.close()
				self.setCompetitionComb(index_cmb)

		else:
			self.btnAccept.setDisabled(True)
			bd.close()

		if len(data) == 0 or len(dataRegion):
			self.btnAccept.setDisabled(True)
		else:
			self.btnAccept.setDisabled(False)

	def calcStake(self):
		self.config = LibYaml()
		if self.config.stake["type"] == 0:
			bd = Bbdd()
			bookies = Bookie.sumAll()
			bonus = Bookie.sumBonus()

			# CC
			cc = bd.select("bank", None, "id=1", "bank")
			cc = cc[0][0]

			# Paypal
			paypal = bd.select("bank", None, "id=2", "bank")
			paypal = paypal[0][0]

			# SKRILL
			skrill = bd.select("bank", None, "id=3", "bank")
			skrill = skrill[0][0]

			total = "{0:.2f}".format(cc + paypal + skrill + bonus + bookies)
			total = float(total) * (self.config.stake["percentage"] * 0.01)
			self.txtOne.setValue(float(total))
		else:
			self.txtOne.setValue(self.config.stake["stake"])


