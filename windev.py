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
global user_min_len
user_min_len = 1

global pass_min_len
pass_min_len = 1

class LoginMessage(QWidget):
    def __init__(self, error_code):
        super(LoginMessage, self).__init__()
        self.setWindowIcon(QIcon('groceries.png'))
        self.error_code = error_code
        self.setWindowTitle('Login Message')
        self.layout = QVBoxLayout()

        error_message_dict = {'wrong_password':'Wrong password. Please try again.', 'wrong_user':'The username you have entered does not match any accounts.',
        					  'user_length': 'Username must be between 3 and 18 characters.', 'pass_length': 'Password must be between 6 and 18 characters',
        					  'first_name_length': 'First name must be greater than 2 characters', 'last_name_length': 'Last name must be greater than 2 characters',
        					  'existing_user': 'Username already exists. Please choose a different username.', 'invalid_user' : 'Please enter a valid username.', 
        					  'invalid_pass' : 'Please enter a valid password.', 'pass_mismatch': 'Passwords don\'t match.', 'pass_changed': 'Password changed.',
        					  'invalid_email': 'Please enter a valid email address.', 'zip_code': 'Please enter a valid zip code.', 'phone': 'Please enter a valid phone number.',
        					  'confirmation_code' : 'Incorrect confirmation code.'}

        self.messagelabel = QLabel(error_message_dict[error_code])
        self.layout.addWidget(self.messagelabel)

        self.ok = QPushButton('OK')
        self.ok.clicked.connect(self.close)
        self.layout.addWidget(self.ok)

        self.setGeometry(600,375,300,100)
        self.setLayout(self.layout) #displays login error screen. incorrect pass/user, etc


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
			self.loginwindow = NewManager()
			self.loginwindow.show()

		except Exception as e:
			print(f"Couldn't log in to MySQL server on ")
			print(e)
			sys.exit()

class NewManager(QWidget):
	def __init__(self):
		super(NewManager,self).__init__()
		self.setWindowIcon(QIcon('groceries.png'))
		self.setWindowTitle('Register Manager')

		self.first_name_field = QLineEdit()
		self.last_name_field = QLineEdit()
		self.username_field = QLineEdit()
		self.confirmation_code_field = QLineEdit()
		self.password_field = QLineEdit()
		self.confirm_pass_field = QLineEdit()
		self.email_field = QLineEdit()
		self.phone_field = QLineEdit()

	
		store_query = "select store_name, house_number, street, address_id from grocery_store natural join addresses;"
		cursor.execute(store_query)
		store_address_dicts = cursor.fetchall()
		self.store_address_list = ['{} - {} {}'.format(store['store_name'], store['house_number'], store['street']) for store in store_address_dicts]

		self.store_field = QComboBox()  #add list to drop down
		self.store_field.addItems(sorted(self.store_address_list))
		self.store_field.setToolTip('Select a Store')



		self.field_label_dict = {'First Name: ': self.first_name_field, 'Last Name: ': self.last_name_field, 'Username: ': self.username_field,
								 'Confirmation Code' : self.confirmation_code_field, 'Password: ': self.password_field, 'Confirm Password: ': self.confirm_pass_field,
								 'Email: ': self.email_field, 'Phone: ': self.phone_field, 'Assign Store: ': self.store_field}


		group_box = QGroupBox('Register Manager')
		grid = QGridLayout()

		field_dict = {}
		for i, name in enumerate(self.field_label_dict.keys()):
			field_dict[name] = QLabel(name)
			row, col = divmod(i, 2)

			if col == 0:
				grid.addWidget(field_dict[name], row, col)

			if col == 1:
				col = col + 1
				grid.addWidget(field_dict[name], row, col)

			if col == 0 or col == 2:
				grid.addWidget(self.field_label_dict[name], row, col + 1)



		group_box.setLayout(grid)

		for key, val in self.field_label_dict.items():
			if key != 'Assign Store: ':
				val.textChanged.connect(self.on_text_changed)
		

		self.register_button = QPushButton('Register')
		self.cancel_button = QPushButton('    Cancel    ')
		self.register_button.setEnabled(False)

		self.register_button.clicked.connect(self.accept)
		self.cancel_button.clicked.connect(self.reject)

		self.layout2 = QHBoxLayout()
		self.layout2.addWidget(self.cancel_button)
		self.layout2.addWidget(self.register_button)

		group_box2 = QGroupBox()
		group_box2.setLayout(self.layout2)

		vbox_layout = QVBoxLayout()

		vbox_layout.addWidget(group_box)
		vbox_layout.addWidget(group_box2)

		self.setLayout(vbox_layout)
		self.first_name_field.setFocus()

	def on_text_changed(self):
		fields = [bool(self.first_name_field.text()), bool(self.username_field.text()), bool(self.password_field.text()), bool(self.email_field.text()), bool(self.last_name_field.text()), bool(self.phone_field.text()), bool(self.confirm_pass_field.text()), bool(self.confirmation_code_field.text())]
		self.register_button.setEnabled(sum(fields) == len(fields))

	def accept(self):
		self.username = self.username_field.text()
		self.password = self.password_field.text()
		self.first_name = self.first_name_field.text()
		self.last_name = self.last_name_field.text()
		self.phone = self.phone_field.text()
		self.email = self.email_field.text().lower()
		self.store = self.store_field.currentText()		
		
		self.store_address_id = 1

		confirmation_code = self.confirmation_code_field.text()
		code_query = "select user_codes from system_info where system_id = 2;"
		cursor = connection.cursor()
		cursor.execute(code_query)

		try:
			if len(self.first_name) < 2:
				self.error_window = LoginMessage('first_name_length')
				self.error_window.show()
				return
			elif len(self.last_name) < 2:
				self.error_window = LoginMessage('last_name_length')
				self.error_window.show()
				return
			elif len(self.username) < user_min_len:
				self.error_window = LoginMessage('user_length')
				self.error_window.show()
				return
			elif len(self.password) < pass_min_len:
				self.error_window = LoginMessage('pass_length')
				self.error_window.show()
				return
			elif len(self.phone) != 10 or not self.phone.isdigit():
				self.error_window = LoginMessage('phone')
				self.error_window.show()
				return
			elif not bool(re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)):
				self.error_window = LoginMessage('invalid_email')
				self.error_window.show()
				return
			elif confirmation_code != cursor.fetchall()[0]['user_codes']:
				self.error_window = LoginMessage('confirmation_code')
				self.error_window.show()
				return

			cursor = connection.cursor()
			check_query = "select * from user where username = '{}'".format(self.username)  #check to see if username already exists
			cursor.execute(check_query)

			existing_user_row_count = cursor.rowcount
			if existing_user_row_count != 0:
				self.error_window = LoginMessage('existing_user')
				self.error_window.show()
				return

			create_user = "insert into user values ('{}', '{}', '{}', '{}', 'manager', '{}');".format(self.first_name, self.last_name, self.username, self.password, self.email)
		
			cursor.execute(create_user)
			connection.commit()		

			create_manager = "insert into manages values ('{}', '{}');".format(self.username, self.store_address_id)
				
			print('success')

		except Exception as e:
			print(f"Fuck")
			print(e)
			qApp.quit()

	def reject(self):
		self.nav_window = RegisterNavigation()
		self.nav_window.show()
		self.close()


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