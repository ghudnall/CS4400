#!/usr/bin/env python3

import pymysql
import sys
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
# from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication
from PyQt5.QtGui import QIcon
import re

class BuyerFunctionality(QWidget):
	def __init__(self):
		super(BuyerFunctionality,self).__init__()
		self.setWindowIcon(QIcon('groceries.png'))
		self.setWindowTitle('Buyer Functionality')

		
		self.first_name_field = QLineEdit()
		self.username_field = QLineEdit()
		self.password_field = QLineEdit()
		self.email_field = QLineEdit()
		self.address_field = QLineEdit()
		self.city_field = QLineEdit()

		self.last_name_field = QLineEdit()
		self.phone_field = QLineEdit()
		self.confirm_pass_field = QLineEdit()
		self.state_field = QComboBox()
		self.zip_field = QLineEdit()

		print('big ol titties')

		self.state_field.addItems(["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
								  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
								  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
								  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
								  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
								  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
								  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
								  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"])


		field_label_dict = {'First Name: ': self.first_name_field, 'Last Name: ': self.last_name_field, 'Username: ': self.username_field,
							'Phone: ': self.phone_field, 'Password: ': self.password_field, 'Confirm Password: ': self.confirm_pass_field,
							'Email: ': self.email_field, 'State: ': self.state_field, 'Address: ': self.address_field, 'Zip Code: ': self.zip_field,
							'City: ': self.city_field}

		names = ['First Name: ', 'Last Name: ', 'Username: ', 'Phone: ', 'Password: ', 'Confirm Password: ', 'Email: ', 'State: ', 'Address: ', 'Zip Code: ', 'City: ']

		field_dict = {}
		grid = QGridLayout()
		group_box = QGroupBox()
		vbox_layout = QVBoxLayout()

		for i, name in enumerate(names):
			field_dict[name] = QLabel(name)
			row, col = divmod(i,4)
			if col%2 == 1:
				grid.addWidget(field_dict[name], row, col)
			else:
				grid.addWidget(field_label_dict[name], row, col+1)

		group_box.setLayout(grid)
		vbox_layout.addWidget(group_box)

		self.setGeometry(740,200,500,100)
		self.setLayout(vbox_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = BuyerFunctionality()
    main.show
    sys.exit(app.exec_())