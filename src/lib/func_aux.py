from locale import *
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt

def updateProfit(self):
		result = self.cmbResult.currentIndex()
		quota = self.txtQuota.value()
		bet = self.txtBet.value()

		if self.chkFree.isChecked():
			profit = {
				0: lambda quota: 0,  # Pendiente
				1: lambda quota: quota - 1,  # Acertada
				2: lambda quota: 0,  # Fallada
				3: lambda quota: 0,  # Nula
				4: lambda quota: (quota - 1) * 0.5,  # Medio Acertada
				5: lambda quota: 0,  # Medio Fallada
				6: lambda quota: 0  # Retirada
			}[result](float(quota))
		else:
			profit = {
				0: lambda quota: -1,  # Pendiente
				1: lambda quota: quota - 1,  # Acertada
				2: lambda quota: -1,  # Fallada
				3: lambda quota: 0,  # Nula
				4: lambda quota: (quota - 1) * 0.5,  # Medio Acertada
				5: lambda quota: (quota - 1) * -0.5,  # Medio Fallada
				6: lambda quota: 0  # Retirada
			}[result](float(quota))

		profit *= bet

		self.txtProfit.setValue(profit)
		
def freeBet(self):
		self.updateProfit()

	def updateBet(self):
		if self.txtStake.text() != "0,00" and self.txtOne.text() != "0,00":
			bet = str_to_float(self.txtStake.text()) * str_to_float(self.txtOne.text())
			self.txtBet.setValue(bet)

	def addCombined(self):
		self.dates.append(QDateTimeEdit())
		sDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		date = QDateTime.fromString(sDate, "yyyy-MM-dd hh:mm:ss")
		self.dates[self.contComb].setDateTime(date)
		self.dates[self.contComb].setMaximumSize(120, 50)
		self.pnlDate.addWidget(self.dates[self.contComb])

		self.sports.append(QComboBox())
		self.sports[self.contComb].setModel(self.cmbSport.model())
		self.regionIndexToIdCmb.append({})
		cont = self.contComb
		self.sports[self.contComb].activated.connect(lambda: self.setRegionComb(cont))
		self.pnlSport.addWidget(self.sports[self.contComb])

		self.regions.append(QComboBox())
		self.competitionIndexToIdCmb.append({})
		self.regions[self.contComb].activated.connect(lambda: self.setCompetitionComb(cont))
		self.pnlRegion.addWidget(self.regions[self.contComb])

		self.competitions.append(QComboBox())
		self.pnlCompetition.addWidget(self.competitions[self.contComb])
		self.players1.append(QComboBox())
		self.players1[self.contComb].setEditable(True)
		self.players1[self.contComb].addItems(self.players)
		self.players1[self.contComb].setMaximumSize(200, 50)
		self.pnlPlayer1.addWidget(self.players1[self.contComb])
		self.players2.append(QComboBox())
		self.players2[self.contComb].setEditable(True)
		self.players2[self.contComb].addItems(self.players)
		self.players2[self.contComb].setMaximumSize(200, 50)
		self.pnlPlayer2.addWidget(self.players2[self.contComb])
		self.picks.append(QLineEdit())
		self.picks[self.contComb].setMaximumSize(200, 50)
		self.pnlPick.addWidget(self.picks[self.contComb])
		self.results.append(QComboBox())
		self.results[self.contComb].addItems(["Pendiente", "Acertada", "Fallada", "Nula", "Medio Acertada", "Medio Fallada", "Retirada"])
		self.pnlResult.addWidget(self.results[self.contComb])
		self.buttons.append(QPushButton())
		self.buttons[self.contComb].setText("X")
		self.buttons[self.contComb].setStyleSheet("color:red; font-weight: bold;")
		self.buttons[self.contComb].setMaximumSize(50, 50)
		self.buttons[self.contComb].clicked.connect(lambda: self.removeRow(cont))
		self.pnlButton.addWidget(self.buttons[self.contComb])

		self.contComb += 1
		if self.contComb == 10:
			self.btnAdd.setEnabled(False)
def str_to_float(sValue):
	setlocale(LC_NUMERIC, '')
	value = atof(sValue)
	return value


def paint_row(item, profit, result=None):
	profit = str_to_float(profit)
	if result == "Pendiente":
		for j in range(18):
			item.setBackground(j, QBrush(Qt.yellow))
	else:
		if profit < 0:
			for j in range(18):
				item.setBackground(j, QBrush(Qt.red))
		elif profit > 0:
			for j in range(18):
				item.setBackground(j, QBrush(Qt.green))
		else:
			for j in range(18):
				item.setBackground(j, QBrush(Qt.cyan))

	return item


def key_from_value(dic, value):
	key = list(dic.keys())[list(dic.values()).index(value)]
	return key

def str_to_bool(s):
	if s == 'True':
		return True
	else:
		return False

def numberToMonth(index):
	month = {
		1: "Enero",
		2: "Febrero",
		3: "Marzo",
		4: "Abril",
		5: "Mayo",
		6: "Junio",
		7: "Julio",
		8: "Agosto",
		9: "Septiembre",
		10: "Octubre",
		11: "Noviembre",
		12: "Diciembre"
	}[index]

	return month



