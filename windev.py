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


class DbLogin():
	def __init__(self):
		try:
			global connection
			connection = pymysql.connect(host= 'localhost',
                                         user='root',
                                         password= 'blackdog',
                                         db= 'Grocery_Tech',
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
			global cursor
			cursor = connection.cursor()
			self.loginwindow = Assigments('deliverer')
			self.loginwindow.show()

		except Exception as e:
			print(f"Couldn't log in to MySQL server on ")
			print(e)
			sys.exit()

class Assigments(QWidget):
	def __init__(self, username):
		super(Assigments, self).__init__()
		self.username = username
		self.setWindowTitle('Assigments')

		self.query  = "select fname, lname from user;"
		self.tabledata = tablemaker(self.query)
		column_headers = self.tabledata[0]
		rows = self.tabledata[1]

		self.table = QTableWidget(len(rows), len(rows[0]), self)
		self.table.horizontalHeader().setStretchLastSection(True)
		self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.table.verticalHeader().setStretchLastSection(True)
		self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

		self.back = QPushButton('Back')
		self.previous = QPushButton('Previous')
		self.next = QPushButton('Next')
		self.view_assn_details = QPushButton('View Assigment Details')

		self.back.clicked.connect(self.accept_back)
		self.previous.clicked.connect(self.accept_prev)
		self.next.clicked.connect(self.accept_next)
		self.view_assn_details.clicked.connect(self.accept_view_assn_details)

		button_group_box = QGroupBox()
		hbox_layout = QHBoxLayout()

		hbox_layout.addWidget(self.back)
		hbox_layout.addWidget(self.previous)
		hbox_layout.addWidget(self.next)
		hbox_layout.addWidget(self.view_assn_details)

		button_group_box.setLayout(hbox_layout)

		self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

		self.table.clicked.connect(self.rowclicked)

		self.table.setHorizontalHeaderLabels(column_headers)
		for i, row in enumerate(rows):
		    for j, field in enumerate(row):
		        item = QTableWidgetItem(field)
		        self.table.setItem(i, j, item)

		vbox_layout = QVBoxLayout()
		vbox_layout.addWidget(self.table)
		vbox_layout.addWidget(button_group_box)

		self.view_assn_details.setEnabled(False)
		self.setLayout(vbox_layout)
		self.setGeometry(740,200,500,200)

	def rowclicked(self):
		self.view_assn_details.setEnabled(True)

	def accept_back(self):
		self.buyer_func = BuyerFunctionality(self.username)
		self.buyer_func.show()
		self.close()

	def accept_prev(self):
		print('PREVIOUS')

	def accept_next(self):
		print("NEXT")

	def accept_view_assn_details(self):
		indexes = self.table.selectionModel().selectedRows()
		for index in indexes:
			# assignment_id = [self.table.item(index.row(),i).text() for i in range(self.table.columnCount())][SOMETHING]
			pass
		assignment_id = 123

		self.assignment_details = AssignmentDetails(self.username, assignment_id)
		self.assignment_details.show()
		self.close()

class AssignmentDetails(QWidget):
	def __init__(self, username, assignment_id):
		super(AssignmentDetails, self).__init__()
		self.setWindowTitle('Assignment Details')
		self.setWindowIcon(QIcon('groceries.png'))
		self.username = username
		self.assignment_id = assignment_id

		assignment_query = "SQL QUERY"

		self.order_placed_field = QLineEdit('12:33')
		self.delivery_time_field = QLineEdit('ASAP')
		self.status_field = QComboBox()
		self.status_field.addItems(['Pending', 'En Route', 'Delivered'])
		self.buyer_address_field = QLineEdit('Poop')
		self.store_name_field = QLineEdit('Publix')

		self.order_placed_field.setEnabled(False)
		self.delivery_time_field.setEnabled(False)
		self.buyer_address_field.setEnabled(False)
		self.store_name_field.setEnabled(False)

		group_box1 = QGroupBox()
		layout1 = QFormLayout()
		layout1.addRow(QLabel('Order Placed: '), self.order_placed_field)
		layout1.addRow(QLabel('Delivery Time: '),self.delivery_time_field)
		layout1.addRow(QLabel('Status: '), self.status_field)
		layout1.addRow(QLabel('Buyer Address: '), self.buyer_address_field)
		layout1.addRow(QLabel('Store Name: '),self.store_name_field)

		group_box1.setLayout(layout1)


		items_query = "SQL QUERY" 

		#list of dicts for each item {item_name : name, quantity: #}
		items = [{'item_name': 'Apple', 'quantity': 5}, {'item_name': 'Pear', 'quantity': 69}]

		items = [{'item_name': 13, 'quantity': 0}, {'item_name': 12, 'quantity': 1}, {'item_name': 11, 'quantity': 2}, {'item_name': 10, 'quantity': 3}, {'item_name': 9, 'quantity': 4}, {'item_name': 8, 'quantity': 5}, {'item_name': 7, 'quantity': 6}, {'item_name': 6, 'quantity': 7}, {'item_name': 5, 'quantity': 8}, {'item_name': 4, 'quantity': 9}, {'item_name': 3, 'quantity': 10}, {'item_name': 2, 'quantity': 11}, {'item_name': 1, 'quantity': 12}, {'item_name': 0, 'quantity': 13}]

		group_box2 = QGroupBox()
		layout2 = QFormLayout()
		layout2.addRow(QLabel('Item Name'), QLabel('Quantity'))

		for item in items:		
			self.item_line = QLineEdit(str(item['item_name']))
			self.quantity_line = QLineEdit(str(item['quantity']))

			self.item_line.setEnabled(False)
			self.quantity_line.setEnabled(False)

			layout2.addRow(self.item_line, self.quantity_line)


		group_box2.setLayout(layout2)


		hbox_layout = QHBoxLayout()
		hbox_layout.addWidget(group_box1)
		hbox_layout.addWidget(group_box2)

		self.setLayout(hbox_layout)
		



def tablemaker(query):
	cursor = connection.cursor()
	cursor.execute(query)
	rows = []
	first_row = cursor.fetchone()

	if first_row == None:
		return ([],[['No Items Found.']])
	else:
		column_headers = [str(k) for k in first_row]
		rows.append([str(v).strip() for v in first_row.values()])
		for row in cursor:
			rows.append([str(v).strip() for v in row.values()])
		return (column_headers, rows)




if __name__ == '__main__':
	app = QApplication(sys.argv)

	login = DbLogin()

	sys.exit(app.exec_())