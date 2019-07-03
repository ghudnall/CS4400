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
                                         db= 'store',
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
			global cursor
			cursor = connection.cursor()
			self.loginwindow = Login()
			self.loginwindow.show()

		except Exception as e:
			print(f"Couldn't log in to MySQL server on ")
			print(e)
			sys.exit()

		clear_cart = "delete from cart;"
		cursor.execute(clear_cart)
		connection.commit()
	def reject(self):
		sys.exit()#login to mysql database

class Login(QWidget):
	def __init__(self):
		super(Login, self).__init__()
		self.setWindowIcon(QIcon('groceries.png'))
		self.setWindowTitle('Login')

		self.username_field = QLineEdit('luna123')
		self.password_field = QLineEdit('luna123')

		form_group_box = QGroupBox('User Login')

		self.layout = QFormLayout()
		self.layout.addRow(QLabel('Username:'), self.username_field)
		self.layout.addRow(QLabel('Password:'),self.password_field)

		buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		self.layout.addWidget(buttons)

		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		form_group_box.setLayout(self.layout)

		new_user_box = QGroupBox ('New User?')
		self.layout2 = QVBoxLayout()

		self.signup = QPushButton('Register')
		self.signup.clicked.connect(self.make_account)

		self.layout2.addWidget(self.signup)
		new_user_box.setLayout(self.layout2)

		vbox_layout = QVBoxLayout()
		vbox_layout.addWidget(form_group_box)
		vbox_layout.addWidget(new_user_box)
		self.setLayout(vbox_layout)
		self.setGeometry(740,200,500,100)
		self.username_field.setFocus()

	def accept(self):
		self.username = self.username_field.text()
		self.password = self.password_field.text()

		if len(self.username) >= 3 and len(self.password) >= 6:
			username_query = "select * from user where username = '{}';".format(self.username)
			cursor.execute(username_query)			#check only if username exists. If it does not, open LoginMessage and say user DNE
			user_row_count = cursor.rowcount
			
			password_query = "select * from user where PASSWORD = '{}' and USERNAME = '{}';".format(self.password, self.username)

			cursor.execute(password_query)
			password_row_count = cursor.rowcount

			if user_row_count == 0: #if 0 rows affected by username check, throw username DNE window
				self.error_window = LoginMessage('wrong_user')
				self.error_window.show()
			elif password_row_count == 0: #elif 0 rows affected by password check, throw incorrect pass window
				self.error_window = LoginMessage('wrong_password')
				self.error_window.show()
			else:											 #else open next window. username/password correct
				user_type_query = "select user_type from user where username = '{}' and password = '{}';".format(self.username, self.password)
				cursor.execute(user_type_query)
				self.user_type = cursor.fetchone()['user_type']

				if self.user_type == 'buyer':
					self.open_buyer_window = BuyerFunctionality(self.username)
					self.open_buyer_window.show()
				elif self.user_type == 'manager':
					print('open manager')
				elif self.user_type == 'deliverer':
					print('open deliverer')
				self.close()

		elif len(self.username) < 3: #username must be longer than 6 characters
			self.error_window = LoginMessage('invalid_user')
			self.error_window.show()
		elif len(self.password) < 6: #password must be longer than 6 characters
			self.error_window = LoginMessage('invalid_pass')
			self.error_window.show()

	def reject(self):
		self.close()
	def make_account(self):
		self.newuser_window = RegisterNavigation()
		self.newuser_window.show()
		self.close()#login to main window

class LoginMessage(QWidget):
    def __init__(self, error_code):
        super(LoginMessage, self).__init__()
        self.setWindowIcon(QIcon('groceries.png'))
        self.error_code = error_code
        self.setWindowTitle('Login Message')
        self.layout = QVBoxLayout()

        error_message_dict = {'wrong_password':'Wrong password. Please try again.', 'wrong_user':'The username you have entered does not match any accounts.',
        					  'user_length': 'Username must be between 3 and 18 characters.', 'pass_length': 'Password must be between 6 and 18 characters',
        					  'fname_length': 'First name must be greater than 2 characters', 'lname_length': 'Last name must be greater than 2 characters',
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

class RegisterNavigation(QWidget):
	def __init__(self):
		super(RegisterNavigation, self).__init__()
		self.setWindowIcon(QIcon('groceries.png'))
		self.setWindowTitle('Register Navigation') 
		self.layout = QVBoxLayout()

		self.buyer_button = QPushButton('Buyer')
		self.deliverer_button = QPushButton('Deliverer')
		self.manager_button = QPushButton('Manager')
		self.back_button = QPushButton('Back')

		self.layout.addWidget(self.buyer_button)
		self.layout.addWidget(self.deliverer_button)
		self.layout.addWidget(self.manager_button)
		self.layout.addWidget(self.back_button)

		self.buyer_button.clicked.connect(self.accept_buyer)
		self.deliverer_button.clicked.connect(self.accept_deliverer)
		self.manager_button.clicked.connect(self.accept_manager)
		self.back_button.clicked.connect(self.accept_back)

		self.setGeometry(740,200,500,100)
		self.setLayout(self.layout)

	def accept_buyer(self):
		self.new_buyer = NewBuyer()
		self.new_buyer.show()
		self.close()

	def accept_deliverer(self):
		self.new_deliverer = NewDeliverer()
		self.new_deliverer.show()
		self.close()

	def accept_manager(self):
		self.new_manager = NewManager()
		self.new_manager.show()
		self.close()

	def accept_back(self):
		self.login = Login()
		self.login.show()
		self.close()

class NewBuyer(QWidget):
	def __init__(self):
		super(NewBuyer,self).__init__()
		self.setWindowIcon(QIcon('groceries.png'))
		self.setWindowTitle('Register Buyer')
		
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

		self.state_field.addItems(["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
								  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
								  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
								  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
								  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
								  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
								  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
								  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"])


		self.field_label_dict = {'First Name: ': self.first_name_field, 'Last Name: ': self.last_name_field, 'Username: ': self.username_field,
							'Phone: ': self.phone_field, 'Password: ': self.password_field, 'Confirm Password: ': self.confirm_pass_field,
							'Email: ': self.email_field, 'State: ': self.state_field, 'Address: ': self.address_field, 'Zip Code: ': self.zip_field,
							'City: ': self.city_field}

		names = ['First Name: ', 'Last Name: ', 'Username: ', 'Phone: ', 'Password: ', 'Confirm Password: ', 'Email: ', 'State: ', 'Address: ', 'Zip Code: ', 'City: ']

		field_dict = {}
		grid = QGridLayout()
		group_box = QGroupBox('Buyer Information')
		vbox_layout = QVBoxLayout()

		label_made = False
		for i, name in enumerate(names):
			field_dict[name] = QLabel(name)
			row, col = divmod(i,2)
			
			if col == 0:
				grid.addWidget(field_dict[name], row, col)

			if col == 1:
				col = col + 1
				grid.addWidget(field_dict[name], row, col)

			if col == 0 or col == 2:
				grid.addWidget(self.field_label_dict[name], row, col + 1)

		group_box.setLayout(grid)
		vbox_layout.addWidget(group_box)

		for key, val in self.field_label_dict.items():
			if key != 'State: ':
				val.textChanged.connect(self.on_text_changed)

		self.register_button = QPushButton('Register')
		self.cancel_button = QPushButton('    Cancel    ')
		self.register_button.clicked.connect(self.accept)
		self.cancel_button.clicked.connect(self.reject)
		self.register_button.setEnabled(False)
		self.register_button.resize(1,1)
		vbox_layout.addWidget(self.register_button)
		vbox_layout.addWidget(self.cancel_button)

		self.setGeometry(740,200,500,100)
		self.setLayout(vbox_layout)


	def on_text_changed(self):
		fields = [bool(self.field_label_dict[field].text()) for field in self.field_label_dict if field != 'State: ']
		self.register_button.setEnabled(sum(fields) == len(fields))

	def accept(self):
		self.username = self.field_label_dict['Username: '].text()
		self.password = self.field_label_dict['Password: '].text()
		self.confirm_pass = self.field_label_dict['Confirm Password: '].text()
		self.fname = self.field_label_dict['First Name: '].text()
		self.lname = self.field_label_dict['Last Name: '].text()
		self.email = self.field_label_dict['Email: '].text().lower()
		self.address = self.field_label_dict['Address: '].text()
		self.state = self.field_label_dict['State: '].currentText()
		self.city = self.field_label_dict['City: '].text()
		self.phone = self.field_label_dict['Phone: '].text()
		self.zip = self.field_label_dict['Zip Code: '].text()

		self.street = 'street'

		try:
			if len(self.fname) < 2:
				self.error_window = LoginMessage('fname_length')
				self.error_window.show()
				return
			elif len(self.lname) < 2:
				self.error_window = LoginMessage('lname_length')
				self.error_window.show()
				return
			elif len(self.username) < 3:
				self.error_window = LoginMessage('user_length')
				self.error_window.show()
				return
			elif len(self.password) < 6:
				self.error_window = LoginMessage('pass_length')
				self.error_window.show()
				return
			elif self.password != self.confirm_pass:
				self.error_window = LoginMessage('pass_mismatch')
				self.error_window.show()
				return
			elif len(self.zip) != 5 or not self.zip.isdigit():
				self.error_window = LoginMessage('zip_code')
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

			cursor = connection.cursor()
			check_query = "select * from user where username = '{}'".format(self.username)  #check to see if username already exists
			cursor.execute(check_query)

			existing_user_row_count = cursor.rowcount
			if existing_user_row_count != 0:
				self.error_window = LoginMessage('existing_user')
				self.error_window.show()
				return
			create_user = "insert into user values ('{}', '{}', '{}', '{}', 'buyer', '{}');".format(self.fname, self.lname, self.username, self.password, self.email)
			create_buyer = "insert into buyer values ('{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(self.username, self.phone, self.state, self.address, self.street, self.zip, self.city)
						
			cursor.execute(create_user)
			connection.commit()

			cursor.execute(create_buyer)
			connection.commit()
			self.loginwindow = Login()
			self.loginwindow.show()
			self.close()
			print('DONE')

		except Exception as e:
			print(f"Fuck")
			print(e)
			qApp.quit()

	def reject(self):
		self.nav_window = RegisterNavigation()
		self.nav_window.show()
		self.close()

class NewDeliverer(QWidget):
	def __init__(self):
		super(NewDeliverer,self).__init__()
		self.setWindowIcon(QIcon('groceries.png'))
		self.setWindowTitle('Register Deliverer')

		self.first_name_field = QLineEdit()
		self.username_field = QLineEdit()
		self.password_field = QLineEdit()
		self.email_field = QLineEdit()
		self.phone_field = QLineEdit()

		self.last_name_field = QLineEdit()
		self.confirmation_code_field = QLineEdit()
		self.confirm_pass_field = QLineEdit()
	
		self.register_button = QPushButton('Register')
		self.cancel_button = QPushButton('    Cancel    ')
		self.register_button.clicked.connect(self.accept)
		self.cancel_button.clicked.connect(self.reject)
		self.register_button.setEnabled(False)

		group_box1 = QGroupBox('Deliverer Information')
		group_box2 = QGroupBox(' ')

		self.layout1 = QFormLayout()
		self.layout1.addRow(QLabel('First Name:'), self.first_name_field)
		self.layout1.addRow(QLabel('Username:'), self.username_field)
		self.layout1.addRow(QLabel('Password:'),self.password_field)
		self.layout1.addRow(QLabel('Email: '), self.email_field)
		self.layout1.addRow(QLabel('Phone Number: '), self.phone_field)

		self.layout2 = QFormLayout()
		self.layout2.addRow(QLabel('Last Name:'),self.last_name_field)
		self.layout2.addRow(QLabel('Confirmation Code: '), self.confirmation_code_field)
		self.layout2.addRow(QLabel('Confirm Password'), self.confirm_pass_field)

		#enable ok button only when all fields have been filled
		self.first_name_field.textChanged.connect(self.on_text_changed)
		self.username_field.textChanged.connect(self.on_text_changed)
		self.password_field.textChanged.connect(self.on_text_changed)
		self.email_field.textChanged.connect(self.on_text_changed)
		self.phone_field.textChanged.connect(self.on_text_changed)
		self.last_name_field.textChanged.connect(self.on_text_changed)
		self.confirmation_code_field.textChanged.connect(self.on_text_changed)
		self.confirm_pass_field.textChanged.connect(self.on_text_changed)

		self.layout2.addWidget(self.register_button)
		self.layout2.addWidget(self.cancel_button)

		group_box1.setLayout(self.layout1)
		group_box2.setLayout(self.layout2)

		hbox_layout = QHBoxLayout()

		hbox_layout.addWidget(group_box1)
		hbox_layout.addWidget(group_box2)


		self.setLayout(hbox_layout)
		self.first_name_field.setFocus()

	def on_text_changed(self):
		fields = [bool(self.first_name_field.text()), bool(self.username_field.text()), bool(self.password_field.text()), bool(self.email_field.text()), bool(self.last_name_field.text()), bool(self.phone_field.text()), bool(self.confirm_pass_field.text()), bool(self.confirmation_code_field.text())]
		self.register_button.setEnabled(sum(fields) == len(fields))

	def accept(self):
		self.username = self.username_field.text()
		self.password = self.password_field.text()
		self.fname = self.first_name_field.text()
		self.lname = self.last_name_field.text()
		self.phone = self.phone_field.text()
		self.email = self.email_field.text().lower()
		self.confirmation_code = self.confirmation_code_field.text()

		code_query = "select code from system_info where user_type = 'deliverer';"
		cursor = connection.cursor()
		cursor.execute(code_query)

		try:
			if len(self.fname) < 2:
				self.error_window = LoginMessage('fname_length')
				self.error_window.show()
				return
			elif len(self.lname) < 2:
				self.error_window = LoginMessage('lname_length')
				self.error_window.show()
				return
			elif len(self.username) < 3:
				self.error_window = LoginMessage('user_length')
				self.error_window.show()
				return
			elif len(self.password) < 6:
				self.error_window = LoginMessage('pass_length')
				self.error_window.show()
				return
			elif self.password_field.text() != self.confirm_pass_field.text():
				self.error_window = LoginMessage('pass_mismatch')
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
			elif self.confirmation_code != cursor.fetchone()['code']:
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

			create_user = "insert into user values ('{}', '{}', '{}', '{}', 'deliverer', '{}');".format(self.fname, self.lname, self.username, self.password, self.email)
			create_deliverer = "insert into deliverer value ('{}');".format(self.username)

			cursor.execute(create_user)
			connection.commit()

			cursor.execute(create_deliverer)
			connection.commit()
			print(482)
			self.loginwindow = Login()
			self.loginwindow.show()
			self.close()

		except Exception as e:
			print(f"Fuck")
			print(e)
			qApp.quit()

	def reject(self):
		self.nav_window = RegisterNavigation()
		self.nav_window.show()
		self.close()

class NewManager(QWidget):
	def __init__(self):
		super(NewManager,self).__init__()
		self.setWindowIcon(QIcon('groceries.png'))
		self.setWindowTitle('Register Manager')

		self.first_name_field = QLineEdit()
		self.username_field = QLineEdit()
		self.password_field = QLineEdit()
		self.email_field = QLineEdit()
		self.phone_field = QLineEdit()

		self.last_name_field = QLineEdit()
		self.confirmation_code_field = QLineEdit()
		self.confirm_pass_field = QLineEdit()
	
		store_query = "select * from store;"
		cursor.execute(store_query)
		store_list = [entry['store_name'] + ' - ' + entry['address'] for entry in cursor.fetchall()]
		print(store_list)
		self.store_field = QComboBox()  #add list to drop down
		self.store_field.addItems(sorted(store_list))
		self.store_field.setToolTip('Select a Store')

		group_box1 = QGroupBox('Manager Information')
		group_box2 = QGroupBox(' ')

		self.layout1 = QFormLayout()
		self.layout1.addRow(QLabel('First Name:'), self.first_name_field)
		self.layout1.addRow(QLabel('Username:'), self.username_field)
		self.layout1.addRow(QLabel('Password:'),self.password_field)
		self.layout1.addRow(QLabel('Email: '), self.email_field)
		self.layout1.addRow(QLabel('Phone Number: '), self.phone_field)

		self.layout2 = QFormLayout()
		self.layout2.addRow(QLabel('Last Name:'),self.last_name_field)
		self.layout2.addRow(QLabel('Confirmation Code: '), self.confirmation_code_field)
		self.layout2.addRow(QLabel('Confirm Password: '), self.confirm_pass_field)
		self.layout2.addRow(QLabel('Select a Store: '), self.store_field)

		self.first_name_field.textChanged.connect(self.on_text_changed)
		self.username_field.textChanged.connect(self.on_text_changed)
		self.password_field.textChanged.connect(self.on_text_changed)
		self.email_field.textChanged.connect(self.on_text_changed)
		self.phone_field.textChanged.connect(self.on_text_changed)
		self.last_name_field.textChanged.connect(self.on_text_changed)
		self.confirmation_code_field.textChanged.connect(self.on_text_changed)
		self.confirm_pass_field.textChanged.connect(self.on_text_changed)

		self.register_button = QPushButton('Register')
		self.cancel_button = QPushButton('    Cancel    ')
		self.register_button.setEnabled(False)

		self.register_button.clicked.connect(self.accept)
		self.cancel_button.clicked.connect(self.reject)

		self.layout2.addWidget(self.register_button)
		self.layout2.addWidget(self.cancel_button)

		group_box1.setLayout(self.layout1)
		group_box2.setLayout(self.layout2)

		hbox_layout = QHBoxLayout()

		hbox_layout.addWidget(group_box1)
		hbox_layout.addWidget(group_box2)

		self.setLayout(hbox_layout)
		self.first_name_field.setFocus()

	def on_text_changed(self):
		fields = [bool(self.first_name_field.text()), bool(self.username_field.text()), bool(self.password_field.text()), bool(self.email_field.text()), bool(self.last_name_field.text()), bool(self.phone_field.text()), bool(self.confirm_pass_field.text()), bool(self.confirmation_code_field.text())]
		self.register_button.setEnabled(sum(fields) == len(fields))

	def accept(self):
		self.username = self.username_field.text()
		self.password = self.password_field.text()
		self.fname = self.first_name_field.text()
		self.lname = self.last_name_field.text()
		self.phone = self.phone_field.text()
		self.email = self.email_field.text().lower()
		self.store = self.store_field.currentText()
		

		confirmation_code = self.confirmation_code_field.text()
		code_query = "select code from system_info where user_type = 'manager';"
		cursor = connection.cursor()
		cursor.execute(code_query)

		try:
			if len(self.fname) < 2:
				self.error_window = LoginMessage('fname_length')
				self.error_window.show()
				return
			elif len(self.lname) < 2:
				self.error_window = LoginMessage('lname_length')
				self.error_window.show()
				return
			elif len(self.username) < 3:
				self.error_window = LoginMessage('user_length')
				self.error_window.show()
				return
			elif len(self.password) < 6:
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
			elif confirmation_code != cursor.fetchall()[0]['code']:
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

			create_user = "insert into user values ('{}', '{}', '{}', '{}', 'manager', '{}');".format(self.fname, self.lname, self.username, self.password, self.email)
			create_manager = "insert into manager values('{}');".format(self.username)

			cursor.execute(create_user)
			connection.commit()
			cursor.execute(create_manager)
			connection.commit()
			self.loginwindow = Login()
			self.loginwindow.show()
			self.close()

		except Exception as e:
			print(f"Fuck")
			print(e)
			qApp.quit()

	def reject(self):
		self.nav_window = RegisterNavigation()
		self.nav_window.show()
		self.close()

class BuyerFunctionality(QWidget):
	def __init__(self, username):
		super(BuyerFunctionality,self).__init__()
		self.setWindowIcon(QIcon('groceries.png'))
		self.setWindowTitle('Buyer Functionality')

		self.username = username

		self.back = QPushButton('Back')

		vbox_layout = QVBoxLayout()
		grid = QGridLayout()
		group_box = QGroupBox('')
		names = ['New Order', 'Account Information', 'Order History', 'Payment Methods']
		button_dict = {button_name: None for button_name in names}
		for i, name in enumerate(names):
			button_dict[name] = QPushButton(name, self)
			row, col = divmod(i, 2)
			grid.addWidget(button_dict[name], row, col)

		group_box.setLayout(grid)
		vbox_layout.addWidget(group_box)
		vbox_layout.addWidget(self.back)
		self.back.resize(1, 1)

		self.setGeometry(740,200,500,100)
		self.setLayout(vbox_layout)

		button_dict['New Order'].clicked.connect(self.accept_new_order)
		button_dict['Order History'].clicked.connect(self.accept_order_history)
		button_dict['Account Information'].clicked.connect(self.accept_acct_info)
		button_dict['Payment Methods'].clicked.connect(self.accept_payment_methods)
		self.back.clicked.connect(self.accept_back)

	def accept_new_order(self):
		self.new_order = StoreList(self.username)
		self.new_order.show()
		self.close()

	def accept_order_history(self):
		self.order_history = OrderHistory(self.username)
		self.order_history.show()
		self.close()	

	def accept_acct_info(self):
		self.acct_info = BuyerAcctInfo(self.username)
		self.acct_info.show()
		self.close()

	def accept_payment_methods(self):
		self.payment_methods = PaymentMethods('buyer_func', self.username)
		self.payment_methods.show()
		self.close()

	def accept_back(self):
		self.back = Login()
		self.back.show()
		self.close()

class StoreList(QWidget):
	def __init__(self, username):
		super(StoreList, self).__init__()
		self.setWindowTitle('Store List')
		self.setWindowIcon(QIcon('groceries.png'))
		self.username = username

		self.query  = "select store_name as Store, address as Address from store;"
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
		self.select = QPushButton('Select')

		self.back.clicked.connect(self.accept_back)
		self.previous.clicked.connect(self.accept_prev)
		self.next.clicked.connect(self.accept_next)
		self.select.clicked.connect(self.accept_select)

		button_group_box = QGroupBox()
		hbox_layout = QHBoxLayout()

		hbox_layout.addWidget(self.back)
		hbox_layout.addWidget(self.previous)
		hbox_layout.addWidget(self.next)
		hbox_layout.addWidget(self.select)

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

		self.select.setEnabled(False)
		self.setLayout(vbox_layout)
		self.setGeometry(740,200,500,200)

	def rowclicked(self):
		self.select.setEnabled(True)

	def accept_back(self):
		self.buyer_func = BuyerFunctionality(self.username)
		self.buyer_func.show()
		self.close()

	def accept_prev(self):
		print('PREVIOUS')

	def accept_next(self):
		print("NEXT")

	def accept_select(self):
		indexes = self.table.selectionModel().selectedRows()
		for index in indexes:
			store_name = [self.table.item(index.row(),i).text() for i in range(self.table.columnCount())][0]
		print(store_name)
		self.store_homepage = StoreHomepage(self.username, store_name)
		self.store_homepage.show()
		self.close()
		
class StoreHomepage(QWidget):
	def __init__(self, username, store_id):
		super(StoreHomepage,self).__init__()
		self.setWindowTitle('Store Homepage')
		self.setWindowIcon(QIcon('groceries.png'))

		self.username = username
		self.store_id = store_id

		self.find_item = QPushButton('Find Item')
		self.view_cart_button = QPushButton('View Cart')
		self.cancel_order = QPushButton('Cancel Order')
		self.back = QPushButton('Back')

		self.find_item.clicked.connect(self.accept_find_item)
		self.view_cart_button.clicked.connect(self.accept_view_cart_button)
		self.cancel_order.clicked.connect(self.accept_cancel_order)
		self.back.clicked.connect(self.accept_back)

		group_box1 = QGroupBox()
		layout1 = QFormLayout()
		layout1.addWidget(self.find_item)
		layout1.addWidget(self.view_cart_button)
		group_box1.setLayout(layout1)

		group_box2 = QGroupBox()
		layout2 = QFormLayout()
		layout2.addWidget(self.cancel_order)
		layout2.addWidget(self.back)
		group_box2.setLayout(layout2)

		hbox = QHBoxLayout()
		hbox.addWidget(group_box1)
		hbox.addWidget(group_box2)
		self.setLayout(hbox)
		self.setGeometry(740,200,500,100)

	def accept_find_item(self):
		self.find_item = FindItem(self.username, self.store_id)
		self.find_item.show()
		self.close()
		
	def accept_view_cart_button(self):
		self.order_id = 'FIGURE OUT AN ORDER ID'
		self.view_cart = Cart(self.username, self.store_id, self.order_id)
		self.view_cart.show()
		self.close()


	def accept_cancel_order(self):
		print("CANCEL ORDER")
		pass
	def accept_back(self):
		self.storelist = StoreList(self.username)
		self.storelist.show()
		self.close()

class FindItem(QWidget):
	def __init__(self, username, store_id):
		super(FindItem, self).__init__()
		self.setWindowTitle('Find Item')
		self.setWindowIcon(QIcon('groceries.png'))
		self.username = username
		self.store_id = store_id
				
		self.back_button = QPushButton('Back')
		self.checkout_button = QPushButton('Checkout')

		grid = QGridLayout()
		group_box = QGroupBox('Item Categories')

		button_names = ('Beverages', 'Dairy', 'Produce', 'Baking Goods', 'Frozen Foods', 'Canned Goods',
				'Meat', 'Cleaning Products', 'Personal Care', 'Other')
		button_dict = {button: None for button in button_names}

		for i, button in enumerate(button_names):
			button_dict[button] = QPushButton(button, self)
			row, col = divmod(i, 3)
			grid.addWidget(button_dict[button], row, col)

		group_box.setLayout(grid)

		for button in button_dict:
			button_dict[button].clicked.connect(self.accept_clicked(button))

		self.checkout_button.clicked.connect(self.checkout)
		self.back_button.clicked.connect(self.accept_back)

		vbox = QVBoxLayout()
		vbox.addWidget(group_box)
		vbox.addWidget(self.checkout_button)
		vbox.addWidget(self.back_button)
		self.setLayout(vbox)
		self.setGeometry(740,200,500,100)

	def accept_clicked(self, category):
		def show_table():
			self.item_table = ItemTable(self.username, self.store_id, category)
			self.item_table.show()
			self.close()
		return show_table

	def checkout(self):
		self.check_out = Checkout(self.username, self.order_id)
		self.check_out.show()
		self.close()
		print("CHECKOUT")

	def accept_back(self):
		self.storehome = StoreHomepage(self.username, self.store_id)
		self.storehome.show()
		self.close()

class ItemTable(QWidget):
	def __init__(self, username, store_id, category):
		super(ItemTable, self).__init__()
		self.setWindowTitle(category)
		self.setWindowIcon(QIcon('groceries.png'))
		self.username = username
		self.store_id = store_id
		self.category = category

		self.query  = "select item_name as 'Item Name', description as 'Description', exp_date as 'Expriation Date', price as 'Price', num_in_stock as 'Number In Stock' from items where category = '{}';".format(self.category)

		self.tabledata = tablemaker(self.query)
		column_headers = self.tabledata[0]
		self.rows = self.tabledata[1]

		self.table = QTableWidget(len(self.rows), len(self.rows[0]), self)
		self.table.horizontalHeader().setStretchLastSection(True)
		self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.table.verticalHeader().setStretchLastSection(True)
		self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

		self.back = QPushButton('Back')
		self.previous = QPushButton('Previous')
		self.next = QPushButton('Next')
		self.add_to_cart = QPushButton('Add to Cart')

		self.back.clicked.connect(self.accept_back)
		self.previous.clicked.connect(self.accept_prev)
		self.next.clicked.connect(self.accept_next)
		self.add_to_cart.clicked.connect(self.accept_add_to_cart)

		button_group_box = QGroupBox()
		hbox_layout = QHBoxLayout()

		hbox_layout.addWidget(self.back)
		hbox_layout.addWidget(self.previous)
		hbox_layout.addWidget(self.next)
		hbox_layout.addWidget(self.add_to_cart)

		button_group_box.setLayout(hbox_layout)

		self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

		self.table.clicked.connect(self.rowclicked)

		self.table.setHorizontalHeaderLabels(column_headers)
		for i, row in enumerate(self.rows):
		    for j, field in enumerate(row):
		        item = QTableWidgetItem(field)
		        self.table.setItem(i, j, item)

		vbox_layout = QVBoxLayout()
		vbox_layout.addWidget(self.table)
		vbox_layout.addWidget(button_group_box)

		self.add_to_cart.setEnabled(False)
		self.setLayout(vbox_layout)
		self.setGeometry(740,200,500,200)

	def rowclicked(self):
		if self.rows != [['No Items Found.']]:
			self.add_to_cart.setEnabled(True)

	def accept_back(self):
		self.buyer_func = FindItem(self.username, self.store_id)
		self.buyer_func.show()
		self.close()

	def accept_prev(self):
		print('PREVIOUS')

	def accept_next(self):
		print("NEXT")

	def accept_add_to_cart(self):
		indexes = self.table.selectionModel().selectedRows()
		for index in indexes:
			item_name = [self.table.item(index.row(),i).text() for i in range(self.table.columnCount())][0]
		in_cart_check = "select * from cart where item_name = '{}';".format(item_name)
		cursor.execute(in_cart_check)
		item_row_count = cursor.rowcount

		if item_row_count == 1:
			add_to_cart_query = "update cart set number = number + 1 where item_name = '{}';".format(item_name)

		else:
			add_to_cart_query = "insert into cart (item_name, price, number) select item_name, price, 1 from items where item_name = '{}';".format(item_name)
		cursor.execute(add_to_cart_query)
		connection.commit()

class Cart(QWidget):
	def __init__(self, username, store_id, order_id):
		super(Cart, self).__init__()
		self.setWindowTitle('Cart')
		self.setWindowIcon(QIcon('groceries.png'))
		self.username = username
		self.order_id = order_id
		self.store_id = store_id

		self.query  = "select item_name as Item, price as Price, number as Number from cart;"
		self.tabledata = tablemaker(self.query)
		column_headers = self.tabledata[0]
		rows = self.tabledata[1]

		total_items = len(rows)

		self.back = QPushButton('Back')
		self.previous = QPushButton('Previous')
		self.next = QPushButton('Next')
		self.delete_item = QPushButton('Delete Item')
		self.checkout = QPushButton('Checkout')		

		self.back.clicked.connect(self.accept_back)
		self.previous.clicked.connect(self.accept_prev)
		self.next.clicked.connect(self.accept_next)
		self.delete_item.clicked.connect(self.accept_delete_item)
		self.checkout.clicked.connect(self.accept_checkout)


		self.table = QTableWidget(len(rows), len(rows[0]), self)
		self.table.horizontalHeader().setStretchLastSection(True)
		self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.table.verticalHeader().setStretchLastSection(True)
		self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

		button_group_box = QGroupBox()
		hbox_layout = QHBoxLayout()

		hbox_layout.addWidget(self.back)
		hbox_layout.addWidget(self.previous)
		hbox_layout.addWidget(self.next)
		hbox_layout.addWidget(self.delete_item)


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
		vbox_layout.addWidget(QLabel('Total Items: '+ str(total_items)))
		vbox_layout.addWidget(self.table)
		vbox_layout.addWidget(button_group_box)
		vbox_layout.addWidget(self.checkout)

		self.delete_item.setEnabled(False)
		self.setLayout(vbox_layout)
		self.setGeometry(740,200,500,200)

	def rowclicked(self):
		self.delete_item.setEnabled(True)

	def accept_back(self):
		self.storehome = StoreHomepage(self.username, self.store_id)
		self.storehome.show()
		self.close()

	def accept_prev(self):
		print('PREVIOUS')

	def accept_next(self):
		print("NEXT")

	def accept_delete_item(self):
		indexes = self.table.selectionModel().selectedRows()
		for index in indexes:
			item_name = [self.table.item(index.row(),i).text() for i in range(self.table.columnCount())][0]
		delete_item_query = "delete from cart where item_name = '{}';".format(item_name)
		cursor.execute(delete_item_query)
		connection.commit()

		self.cart = Cart(self.username, self.store_id, self.order_id)
		self.cart.show()
		self.close()

	def accept_checkout(self):
		self.checkout_window = Checkout(self.username, self.order_id)
		self.checkout_window.show()
		self.close()
		
class BuyerAcctInfo(QWidget):
	def __init__(self, username):
		super(BuyerAcctInfo, self).__init__()

		self.username = username
		self.setWindowIcon(QIcon('groceries.png'))
		self.setWindowTitle('Account Information')

		user_info_query = "select * from user where username = '{}';".format(self.username)
		cursor = connection.cursor()
		cursor.execute(user_info_query)
		user_info = cursor.fetchone()

		buyer_info_query = "select * from buyer where username = '{}';".format(self.username)
		cursor = connection.cursor()
		cursor.execute(buyer_info_query)
		buyer_info = cursor.fetchone()

		self.first_name_field = QLineEdit(user_info['fname'])
		self.username_field = QLineEdit(self.username)
		self.preferred_store = QComboBox()
		self.store_address = QLineEdit()
		self.email_field = QLineEdit(user_info['email'])
		self.prefered_card = QLineEdit()
		self.address_field = QLineEdit(buyer_info['address'])
		self.city_field = QLineEdit(buyer_info['city'])

		store_query = "select * from store;"
		cursor.execute(store_query)
		store_list = [entry['store_name'] + ' - ' + entry['address'] for entry in cursor.fetchall()]
		self.preferred_store.addItems(sorted(store_list))
		self.preferred_store.setToolTip('Select a Store')


		self.last_name_field = QLineEdit(user_info['lname'])
		self.phone_field = QLineEdit(buyer_info['phone'])
		self.state_field = QLineEdit(buyer_info['state'])
		self.zip_field = QLineEdit(buyer_info['zip'])

		group_box1 = QGroupBox('Buyer Information')
		group_box2 = QGroupBox(' ')

		self.layout1 = QFormLayout()
		self.layout1.addRow(QLabel('First Name: '), self.first_name_field)
		self.layout1.addRow(QLabel('Username: '), self.username_field)
		self.layout1.addRow(QLabel('Preferred Store: '),self.preferred_store)
		self.layout1.addRow(QLabel('Grocery Store Address: '),self.store_address)
		self.layout1.addRow(QLabel('Email: '), self.email_field)
		self.layout1.addRow(QLabel('Preferred Credit Card: '), self.prefered_card)


		self.layout2 = QFormLayout()
		self.layout2.addRow(QLabel('Last Name:'),self.last_name_field)
		self.layout2.addRow(QLabel('Phone Number: '), self.phone_field)
		self.layout2.addRow(QLabel('Address: '), self.address_field)
		self.layout2.addRow(QLabel('City: '), self.city_field)
		self.layout2.addRow(QLabel('State: '), self.state_field)
		self.layout2.addRow(QLabel('Zip Code: '), self.zip_field)

		self.first_name_field.setEnabled(False)
		self.last_name_field.setEnabled(False)
		self.username_field.setEnabled(False)

		buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		buttons.accepted.connect(self.update_info)
		buttons.rejected.connect(self.reject)

		self.delete_acct = QPushButton('Delete Account')
		self.delete_acct.clicked.connect(self.check_delete_acct)

		self.layout2.addWidget(buttons)
		self.layout2.addWidget(self.delete_acct)

		group_box1.setLayout(self.layout1)
		group_box2.setLayout(self.layout2)

		hbox_layout = QHBoxLayout()

		hbox_layout.addWidget(group_box1)
		hbox_layout.addWidget(group_box2)


		self.setLayout(hbox_layout)
		self.first_name_field.setFocus()

	def update_info(self):
		email = self.email_field.text()

		phone = self.phone_field.text()
		state = self.state_field.text()
		address = self.address_field.text()
		street = 'street'
		zip = self.zip_field.text()
		city = self.city_field.text()

		update_user = "update user set email = '{}' where username = '{}';".format(email, self.username)
		update_buyer = "update buyer set phone = '{}', state = '{}', address = '{}', street = '{}', zip = '{}', city = '{}' where username = '{}';".format(phone, state, address, street, zip, city, self.username)

		cursor = connection.cursor()
		cursor.execute(update_user)
		cursor.execute(update_buyer)

		update_msg = QMessageBox()
		update_msg.setIcon(QMessageBox.Information)
		update_msg.setWindowTitle('Buyer Information')
		update_msg.setText("Information Updated!")
		update_msg.setStandardButtons(QMessageBox.Ok)
		update_msg.accepted.connect(self.reject)
		update_msg.exec_()

	def reject(self):
		self.buyer_func = BuyerFunctionality(self.username)
		self.buyer_func.show()
		self.close()

	def check_delete_acct(self):
		msg = QMessageBox()
		msg.setWindowTitle('Delete Account')
		msg.setText("Are you sure you want to delete your account?")
		msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		msg.accepted.connect(self.accept_delete_acct)
		msg.exec_()

	def accept_delete_acct(self):
		query = "delete from buyer where username = '{}';".format(self.username)
		cursor.execute(query)
		query = "delete from user where username = '{}';".format(self.username)
		cursor.execute(query)
		print('delete account')
		self.login = Login()
		self.login.show()
		self.close()

class OrderHistory(QWidget):
	def __init__(self, username):
		super(OrderHistory, self).__init__()
		self.setWindowTitle('Order History')
		self.setWindowIcon(QIcon('groceries.png'))

		self.username = username
		self.query  = "select username, password, fname as 'First Name', lname as 'Last Name' from user;"

		self.tabledata = tablemaker(self.query)
		column_headers = self.tabledata[0]
		rows = self.tabledata[1]

		self.table = QTableWidget(len(rows), len(rows[0]), self)
		self.table.horizontalHeader().setStretchLastSection(True)
		self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.table.verticalHeader().setStretchLastSection(True)
		self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

		self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

		self.table.clicked.connect(self.rowclicked)

		self.table.setHorizontalHeaderLabels(column_headers)
		for i, row in enumerate(rows):
		    for j, field in enumerate(row):
		        item = QTableWidgetItem(field)
		        self.table.setItem(i, j, item)

		self.back = QPushButton('Back')
		self.previous = QPushButton('Previous')
		self.next = QPushButton('Next')
		self.order_details = QPushButton('View Order Details')
		self.order_details.setEnabled(False)

		self.back.clicked.connect(self.accept_back)
		self.previous.clicked.connect(self.accept_prev)
		self.next.clicked.connect(self.accept_next)
		self.order_details.clicked.connect(self.accept_details)

		hbox_layout = QHBoxLayout()

		hbox_layout.addWidget(self.back)
		hbox_layout.addWidget(self.previous)
		hbox_layout.addWidget(self.next)
		hbox_layout.addWidget(self.order_details)

		group_box = QGroupBox()
		group_box.setLayout(hbox_layout)

		vbox_layout = QVBoxLayout()
		vbox_layout.addWidget(self.table)
		vbox_layout.addWidget(group_box)

		self.setLayout(vbox_layout)
		self.setGeometry(740,200,500,200)

	def rowclicked(self):
		self.order_details.setEnabled(True)

	def accept_back(self):
		self.buyer_func = BuyerFunctionality(self.username)
		self.buyer_func.show()
		self.close()

	def accept_prev(self):
		print('PREVIOUS')

	def accept_next(self):
		print('NEXT')

	def accept_details(self):
		print('ORDER DETAILS')
  
class PaymentMethods(QWidget):
	def __init__(self, parent_type, username):
		super(PaymentMethods, self).__init__()
		self.setWindowIcon(QIcon('groceries.png'))
		self.setWindowTitle('Payment Methods')

		self.parent_type = parent_type
		self.username = username
		self.query  = "select payment_name as 'Payment Method', acct_number as 'Account Number', routing_number as 'Routing Number', if(default_payment, 'Yes', 'No') as 'Default' from payments where username = '{}';".format(self.username)

		self.tabledata = tablemaker(self.query)
		column_headers = self.tabledata[0]
		rows = self.tabledata[1]

		self.table = QTableWidget(len(rows), len(rows[0]), self)
		self.table.horizontalHeader().setStretchLastSection(True)
		self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.table.verticalHeader().setStretchLastSection(True)
		self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

		self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

		self.table.clicked.connect(self.rowclicked)

		self.table.setHorizontalHeaderLabels(column_headers)
		for i, row in enumerate(rows):
		    for j, field in enumerate(row):
		        item = QTableWidgetItem(field)
		        self.table.setItem(i, j, item)

		self.back = QPushButton('Back')
		self.confirm_order = QPushButton('Confirm Payment Method')
		self.confirm_order.setEnabled(False)

		self.back.clicked.connect(self.accept_back)
		self.confirm_order.clicked.connect(self.accept_confirm)

		hbox_layout = QHBoxLayout()

		hbox_layout.addWidget(self.back)
		hbox_layout.addWidget(self.confirm_order)

		group_box = QGroupBox()
		group_box.setLayout(hbox_layout)

		vbox_layout = QVBoxLayout()
		vbox_layout.addWidget(self.table)
		vbox_layout.addWidget(group_box)

		self.setLayout(vbox_layout)
		self.setGeometry(700,200,750,400)

	def rowclicked(self):
		self.confirm_order.setEnabled(True)

	def accept_back(self):
		if self.parent_type == 'buyer_func':
			self.buyer_func = BuyerFunctionality(self.username)
			self.buyer_func.show()
		elif self.parent_type == 'checkout':
			# self.checkout = Checkout()
			# self.checkout.show()
			print('RETURN TO CHECKOUT')
		self.close()

	def accept_confirm(self):
		print('CONFIRM ORDER')
		print("OPEN RECEIPT")

class Checkout(QWidget):
	def __init__(self, username, order_id):
		super(Checkout, self).__init__()
		self.setWindowIcon(QIcon('groceries.png'))
		self.setWindowTitle('Checkout')
		self.order_id = order_id           
		self.username = username

		payment_query = "select payment_name from payments where username = '{}';".format(self.username)
		cursor.execute(payment_query)
		payment_list = [payment['payment_name'] for payment in cursor.fetchall()]

		time_list = ['ASAP', '1 hour', '2 hours', '5 hours', '10 hours', '12 hours', '24 hours']

		total_price_query = "select sum(number*price) as total_price from cart;"
		cursor.execute(total_price_query)
		total_price = cursor.fetchone()['total_price']

		if not total_price:
			total_price = '0.00'

		self.payment_dropdown = QComboBox()
		self.payment_dropdown.addItems(sorted(payment_list))
		self.payment_dropdown.setToolTip('Select a payment method.')

		self.time_dropdown = QComboBox()
		self.time_dropdown.addItems(time_list)
		self.time_dropdown.setToolTip('Select a delivery time.')

		self.total_price_field = QLineEdit('$' + str(total_price))
		self.total_price_field.setEnabled(False)

		self.delivery_instructions = QLineEdit()

		self.group_box = QGroupBox('Checkout')
		grid = QGridLayout()

		grid.addWidget(QLabel('Payment: '), 0, 0)
		grid.addWidget(self.payment_dropdown, 0, 1)
		grid.addWidget(QLabel('Delivery Time: '), 0, 2)
		grid.addWidget(self.time_dropdown, 0, 3)
		grid.addWidget(QLabel('Total Price: '), 1, 2)
		grid.addWidget(self.total_price_field, 1, 3)

		self.group_box.setLayout(grid)
		self.layout = QFormLayout()
		self.layout.addWidget(self.group_box)
		self.setLayout(self.layout)



class MainWindow(QMainWindow): # main window. includes buttons for navigating page and taskbars.
	def __init__(self,user_type, username):
		super(MainWindow, self).__init__() 
		self.setWindowIcon(QIcon('groceries.png'))
		self.user_type = user_type           
		self.username = username

		exitButton = QAction('&Exit', self)        
		exitButton.setShortcut('Ctrl+Q')
		exitButton.setStatusTip('Exit application')
		exitButton.triggered.connect(qApp.quit)

		userSettings = QAction('&User Settings', self)        
		userSettings.setStatusTip('Open User Settings')
		userSettings.triggered.connect(self.accept)

		logOut = QAction('&Log Out', self)
		logOut.setStatusTip('Log Out')
		logOut.triggered.connect(self.accept_logout)

		usertable = QAction('&Member Table', self)
		usertable.setStatusTip('Member Table')
		usertable.triggered.connect(self.accept_membertable)

		self.statusBar()

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(userSettings)
		fileMenu.addAction(usertable)
		fileMenu.addAction(logOut)
		fileMenu.addAction(exitButton)

		self.setGeometry(740,200,500,200) #(x,y,width, height)
		self.setWindowTitle('Simple menu')    
		self.show()

	def accept(self):
		self.userSettingsLogin = UserSettingsLogin(self.user_type, self.username)
		self.userSettingsLogin.show()

	def accept_logout(self):
		self.logout_login = Login()
		self.logout_login.show()
		self.close()
	def accept_membertable(self):
		self.membertable = OrderHistory()
		self.membertable.show()
		self.close()
	 
class UserSettingsLogin(QWidget):
	def __init__(self,user_type,username):
		super(UserSettingsLogin, self).__init__()
		self.setWindowIcon(QIcon('groceries.png'))
		self.user_type = user_type
		self.username = username
		self.setWindowTitle('User Settings Login')

		self.username = QLineEdit(username)
		self.username.setEnabled(False)
		self.password = QLineEdit()

		form_group_box = QGroupBox('Reenter your password.')

		self.layout = QFormLayout()
		self.layout.addRow(QLabel('Username:'), self.username)
		self.layout.addRow(QLabel('Password:'),self.password)

		buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)
		self.layout.addWidget(buttons)

		form_group_box.setLayout(self.layout)
		self.setGeometry(500,100, 300, 100) #(x,y,width, height)
		vbox_layout = QVBoxLayout()
		vbox_layout.addWidget(form_group_box)
		self.setLayout(vbox_layout)
		self.password.setFocus()

	def accept(self):
		if len(self.username.text()) >= 6 and len(self.password.text()) >= 6:
			cursor = connection.cursor()

			password_query = "select * from {} where username = '{}' and password = ('{}');".format(self.user_type, self.username.text(), self.password.text())
			cursor.execute(password_query)
			password_row_count = cursor.rowcount

			if password_row_count == 0:
				self.error_window = LoginMessage('wrong_password')
				self.error_window.show()
			else:
				self.main_window = UserSettingsDialog(self.username, self.user_type)
				self.close()
				self.main_window.show()

		elif len(self.username.text()) < 6:
			self.error_window = LoginMessage('invalid_user')
			self.error_window.show()
		elif len(self.password.text()) < 6:
			self.error_window = LoginMessage('invalid_pass')
			self.error_window.show()

	def reject(self):
		self.close()# re enter password to verify identity for user settings

class UserSettingsDialog(QWidget):
	def __init__(self,username, user_type):
		super(UserSettingsDialog,self).__init__()
		self.setWindowIcon(QIcon('groceries.png'))
		self.setWindowTitle('User Settings')
		self.username = username
		self.user_type = user_type

		change_pass_box = QGroupBox('Change Password')
		self.current_pass = QLineEdit()
		self.password1 = QLineEdit()
		self.password2 = QLineEdit()
		self.passok = QPushButton('OK')

		self.pass_layout = QFormLayout()
		self.pass_layout.addRow(QLabel('Old Password:'), self.current_pass)
		self.pass_layout.addRow(QLabel('New Password:'), self.password1)
		self.pass_layout.addRow(QLabel('Re-enter New Password:'),self.password2)
		self.pass_layout.addWidget(self.passok)
		self.passok.clicked.connect(self.pass_accept)

		change_pass_box.setLayout(self.pass_layout)
		self.setGeometry(500,100, 300, 100) #(x,y,width, height)
		vbox_layout = QVBoxLayout()
		vbox_layout.addWidget(change_pass_box)
		self.setLayout(vbox_layout)# user settings page. change password

	def pass_accept(self):
		if self.password1.text() != self.password2.text():
			self.error_window = LoginMessage('pass_mismatch')
			self.error_window.show()

		elif len(self.password1.text()) >= 6:
			cursor = connection.cursor()

			update_password = "update {} set password = '{}' where username = '{}' and password = '{}';".format(self.user_type, self.password1.text(), self.username.text(), self.current_pass.text())
			cursor.execute(update_password)
			connection.commit()
			password_row_count = cursor.rowcount

			if password_row_count == 0:
				self.error_window = LoginMessage('wrong_password')
				self.error_window.show()
			else:
				self.pass_change_success = LoginMessage('pass_changed')
				self.pass_change_success.show()
				self.current_pass.clear()
				self.password1.clear()
				self.password2.clear()
								
		elif len(self.password1.text()) < 6:
			self.error_window = LoginMessage('invalid_pass')
			self.error_window.show()


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

    open = Checkout('gavin', '123')
    open.show()

    sys.exit(app.exec_())



