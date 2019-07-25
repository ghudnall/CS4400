#!/usr/bin/env python3

import pymysql
import sys
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtGui import QIcon
import re
import datetime as dt

global user_min_len
user_min_len = 1

global pass_min_len
pass_min_len = 1

global fname_min_len
fname_min_len = 1

global lname_min_len
lname_min_len = 1

global state_list
state_list = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
			  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
			  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
			  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
			  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
			  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
			  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
			  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]

class DbLogin():
	def __init__(self):
		try:
			global connection
			connection = pymysql.connect(host= 'localhost',
                                         user='root',
                                         password= 'blackdog',
                                         db= 'GroceryTech',
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

	def reject(self):
		sys.exit()#login to mysql database

class Login(QWidget):
	def __init__(self):
		super(Login, self).__init__()
		self.setWindowIcon(QIcon('groceries.png'))
		self.setWindowTitle('Login')

		self.username_field = QLineEdit('wellmadeconkey')
		self.password_field = QLineEdit('cordialsamarium')

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

		if len(self.username) >= user_min_len and len(self.password) >= pass_min_len:
			username_query = "select * from userr where username = '{}';".format(self.username)
			cursor.execute(username_query)			#check only if username exists. If it does not, open LoginMessage and say user DNE
			user_row_count = cursor.rowcount
			
			password_query = "select * from userr where PASSWORD = '{}' and USERNAME = '{}';".format(self.password, self.username)

			cursor.execute(password_query)
			password_row_count = cursor.rowcount

			if user_row_count == 0: #if 0 rows affected by username check, throw username DNE window
				self.error_window = LoginMessage('wrong_user')
				self.error_window.show()
			elif password_row_count == 0: #elif 0 rows affected by password check, throw incorrect pass window
				self.error_window = LoginMessage('wrong_password')
				self.error_window.show()
			else:											 #else open next window. username/password correct
				user_type_query = "select user_type from userr where username = '{}' and password = '{}';".format(self.username, self.password)
				cursor.execute(user_type_query)
				self.user_type = cursor.fetchone()['user_type']

				if self.user_type == 'buyer':
					self.open_buyer_window = BuyerFunctionality(self.username)
					self.open_buyer_window.show()
				elif self.user_type == 'deliverer':
					self.open_deliverer_window = DelivererFunctionality(self.username)
					self.open_deliverer_window.show()
				elif self.user_type == 'manager':
					self.open_manager_window = ManagerFunctionality(self.username)
					self.open_manager_window.show()
				self.close()

		elif len(self.username) < user_min_len: #username must be longer than 6 characters
			self.error_window = LoginMessage('invalid_user')
			self.error_window.show()
		elif len(self.password) < pass_min_len: #password must be longer than 6 characters
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
        self.setWindowTitle('Error Message')
        self.layout = QVBoxLayout()

        error_message_dict = {'wrong_password':'Wrong password. Please try again.', 'wrong_user':'The username you entered does not match any accounts.',
        					  'user_length': 'Username must be between 3 and 18 characters.', 'pass_length': 'Password must be between 6 and 18 characters',
        					  'first_name_length': 'First name must be greater than 2 characters', 'last_name_length': 'Last name must be greater than 2 characters',
        					  'existing_user': 'Username already exists. Please choose a different username.', 'invalid_user' : 'Please enter a valid username.', 
        					  'invalid_pass' : 'Please enter a valid password.', 'pass_mismatch': 'Passwords don\'t match.', 'pass_changed': 'Password changed.',
        					  'invalid_email': 'Please enter a valid email address.', 'zip_code': 'Please enter a valid zip code.', 'phone': 'Please enter a valid phone number.',
        					  'confirmation_code' : 'Incorrect confirmation code.', 'unique_payment': 'Payment name must be unique.', 'acct_num_len': 'Account number must be a 9 digit number.',
        					  'routing_len': 'Routing number must be a 9 digit number.', 'state': 'Please enter a US state.', 'address': 'Please enter a valid address.', 'preferred_store': 'Please select a preferred store.',
        					  'acct_num': 'Please enter a valid 9 digit account number.', 'card': 'Please enter a payment name.','routing_num': 'Please enter a valid 9 digit routing number.', 'instructions': 'Delivery instructions must be less than 250 characters.'
        					  }

        self.messagelabel = QLabel(error_message_dict[error_code])
        self.layout.addWidget(self.messagelabel)

        self.ok = QPushButton('OK')
        self.ok.clicked.connect(self.close)
        self.layout.addWidget(self.ok)

        self.setGeometry(800,250,350,100)
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

		self.state_field.addItems(state_list)
		self.preferred_card_name = QLineEdit()
		self.preferred_acct_num_field = QLineEdit()
		self.preferred_routing_num_field = QLineEdit()

		store_query = "select address_id,store_name, concat(house_number, ' ', street) as 'address' from grocerystore natural join address where address_id = id;"
		cursor.execute(store_query)
		store_data = cursor.fetchall()
		store_list = [entry['store_name'] + ' - ' + entry['address'] for entry in store_data]
		store_list.insert(0,'Select a preferred store')

		self.store_dict = {str(str(store['store_name']) + ' - ' + str(store['address'])) : store['address_id'] for store in store_data}

		self.default_store_field = QComboBox()
		self.default_store_field.addItems(store_list)


		self.field_label_dict = {'First Name: ': self.first_name_field, 'Last Name: ': self.last_name_field, 'Username: ': self.username_field,
							'Phone: ': self.phone_field, 'Password: ': self.password_field, 'Confirm Password: ': self.confirm_pass_field,
							'Email: ': self.email_field, 'Preferred Store: ': self.default_store_field, 'State: ': self.state_field, 'Address: ': self.address_field, 'Zip Code: ': self.zip_field,
							'City: ': self.city_field, 'Preferred payment name: ' :self.preferred_card_name, 'Account Number: ': self.preferred_acct_num_field, 'Routing Number: ': self.preferred_routing_num_field}

		field_dict = {}
		grid = QGridLayout()
		group_box = QGroupBox('Buyer Information')
		vbox_layout = QVBoxLayout()

		for i, name in enumerate(self.field_label_dict.keys()):
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
			if key != 'State: ' and key != 'Preferred Store: ':
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
		fields = [bool(self.field_label_dict[field].text()) for field in self.field_label_dict if field != 'State: ' and field != 'Preferred Store: ']
		self.register_button.setEnabled(sum(fields) == len(fields))

	def accept(self):
		self.username = self.field_label_dict['Username: '].text()
		self.password = self.field_label_dict['Password: '].text()
		self.confirm_pass = self.field_label_dict['Confirm Password: '].text()
		self.first_name = self.field_label_dict['First Name: '].text()
		self.last_name = self.field_label_dict['Last Name: '].text()
		self.email = self.field_label_dict['Email: '].text().lower()
		address_raw = self.field_label_dict['Address: '].text()
		self.state = self.field_label_dict['State: '].currentText()
		self.city = self.field_label_dict['City: '].text()
		self.phone = self.field_label_dict['Phone: '].text()
		self.zip = self.field_label_dict['Zip Code: '].text()

		preferred_store = self.default_store_field.currentText()
		payment_name = self.preferred_card_name.text()
		preferred_acct_num = self.preferred_acct_num_field.text()
		preferred_routing_num = self.preferred_routing_num_field.text()

		self.street = 'street'

		try:
			address_split = address_raw.split()
			if len(address_split) < 2 or not address_split[0].isdigit():
				self.error_window = LoginMessage('address')
				self.error_window.show()
				return

			else:
				house_number = address_split[0]
				del address_split[0]
				street = ''
				for i, el in enumerate(address_split):
					street += el
					if i != len(address_split) - 1:
						street += ' '
				street = street.title()

		except:
			self.error_window = LoginMessage('address')
			self.error_window.show()
			return			

		try:
			if len(self.first_name) < fname_min_len:
				self.error_window = LoginMessage('first_name_length')
				self.error_window.show()
				return
			elif len(self.last_name) < lname_min_len:
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
			elif preferred_store == 'Select a preferred store':
				self.error_window = LoginMessage('preferred_store')
				self.error_window.show()
				return

			elif len(payment_name) == 0:
				self.error_window = LoginMessage('card')
				self.error_window.show()
				return
			elif len(preferred_acct_num) != 9:
				self.error_window = LoginMessage('acct_num')
				self.error_window.show()
				return
			elif len(preferred_routing_num) != 9:
				self.error_window = LoginMessage('routing_num')
				self.error_window.show()
				return

			user_check_query = "select * from userr where username = '{}'".format(self.username)  #check to see if username already exists
			cursor.execute(user_check_query)

			existing_user_row_count = cursor.rowcount
			if existing_user_row_count != 0:
				self.error_window = LoginMessage('existing_user')
				self.error_window.show()
				return

			address_id_query = "select max(id) as 'max' from address;"
			cursor.execute(address_id_query)
			max_address_id = cursor.fetchone()['max']

			self.address_id = max_address_id + 1
			default_store_id = self.store_dict[preferred_store]

			create_address = "insert into address values ({}, {}, '{}', '{}', '{}', {});".format(self.address_id, house_number, street, self.city, self.state, self.zip)
			create_user = "insert into userr values ('{}', '{}', '{}', '{}', '{}', '{}');".format(self.username, self.password, 'buyer', self.email, self.first_name, self.last_name)
			create_buyer = "insert into buyer values ('{}', '{}', '{}', '{}', '{}');".format(self.username, self.phone,  self.address_id, payment_name, default_store_id)
			create_payment = "insert into payments values ('{}', '{}', {}, {});".format(self.username, payment_name, preferred_acct_num, preferred_routing_num)

			cursor.execute(create_address)
			connection.commit()
			cursor.execute(create_user)
			cursor.execute(create_buyer)
			cursor.execute(create_payment)
			connection.commit()
			self.loginwindow = Login()
			self.loginwindow.show()
			self.close()

		except Exception as e:
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

		self.last_name_field = QLineEdit()
		self.confirmation_code_field = QLineEdit()
		self.confirm_pass_field = QLineEdit()
	
		self.register_button = QPushButton('Register')
		self.cancel_button = QPushButton('    Cancel    ')
		self.register_button.clicked.connect(self.accept)
		self.cancel_button.clicked.connect(self.reject)
		self.register_button.setEnabled(False)

		group_box1 = QGroupBox('Deliverer Information')
		group_box2 = QGroupBox()

		self.field_label_dict = {'First Name: ': self.first_name_field, 'Last Name: ': self.last_name_field, 'Username: ': self.username_field,
						 'Confirmation Code' : self.confirmation_code_field, 'Password: ': self.password_field, 'Confirm Password: ': self.confirm_pass_field,
						 'Email: ': self.email_field}


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

		group_box1.setLayout(grid)

		for key, val in self.field_label_dict.items():
			val.textChanged.connect(self.on_text_changed)
		
		self.layout2 = QHBoxLayout()
		self.layout2.addWidget(self.cancel_button)
		self.layout2.addWidget(self.register_button)

		group_box2.setLayout(self.layout2)

		vbox_layout = QVBoxLayout()

		vbox_layout.addWidget(group_box1)
		vbox_layout.addWidget(group_box2)

		self.setLayout(vbox_layout)
		self.first_name_field.setFocus()

	def on_text_changed(self):
		fields = [bool(self.first_name_field.text()), bool(self.username_field.text()), bool(self.password_field.text()), bool(self.email_field.text()), bool(self.last_name_field.text()), bool(self.confirm_pass_field.text()), bool(self.confirmation_code_field.text())]
		self.register_button.setEnabled(sum(fields) == len(fields))

	def accept(self):
		self.username = self.username_field.text()
		self.password = self.password_field.text()
		self.first_name = self.first_name_field.text()
		self.last_name = self.last_name_field.text()
		self.email = self.email_field.text().lower()
		self.confirmation_code = self.confirmation_code_field.text()

		code_query = "select user_codes from systeminformation where system_id = 0;"
		cursor = connection.cursor()
		cursor.execute(code_query)
		user_code = str(cursor.fetchone()['user_codes'])

		try:
			if len(self.first_name) < fname_min_len:
				self.error_window = LoginMessage('first_name_length')
				self.error_window.show()
				return
			elif len(self.last_name) < lname_min_len:
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
			elif self.password_field.text() != self.confirm_pass_field.text():
				self.error_window = LoginMessage('pass_mismatch')
				self.error_window.show()
				return

			elif not bool(re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)):
				self.error_window = LoginMessage('invalid_email')
				self.error_window.show()
				return
			elif self.confirmation_code != user_code:
				self.error_window = LoginMessage('confirmation_code')
				self.error_window.show()
				return

			cursor = connection.cursor()
			check_query = "select * from userr where username = '{}'".format(self.username)  #check to see if username already exists
			cursor.execute(check_query)

			existing_user_row_count = cursor.rowcount
			if existing_user_row_count != 0:
				self.error_window = LoginMessage('existing_user')
				self.error_window.show()
				return

			create_user = "insert into userr values ('{}', '{}', '{}', '{}', '{}', '{}');".format(self.username, self.password, 'deliverer', self.email, self.first_name, self.last_name)
			
			cursor.execute(create_user)
			connection.commit()

			self.loginwindow = Login()
			self.loginwindow.show()
			self.close()

		except Exception as e:
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
		self.last_name_field = QLineEdit()
		self.username_field = QLineEdit()
		self.confirmation_code_field = QLineEdit()
		self.password_field = QLineEdit()
		self.confirm_pass_field = QLineEdit()
		self.email_field = QLineEdit()

	
		store_query = "select store_name, house_number, street, address_id from grocerystore natural join address where address_id = id;"
		cursor.execute(store_query)
		store_address_dict_list = cursor.fetchall()
		self.store_address_dict = {'{} - {} {}'.format(store['store_name'], store['house_number'], store['street']): store['address_id'] for store in store_address_dict_list}

		self.store_field = QComboBox()  #add list to drop down
		self.store_field.addItems(sorted(self.store_address_dict.keys()))
		self.store_field.setToolTip('Select a Store')



		self.field_label_dict = {'First Name: ': self.first_name_field, 'Last Name: ': self.last_name_field, 'Username: ': self.username_field,
								 'Confirmation Code' : self.confirmation_code_field, 'Password: ': self.password_field, 'Confirm Password: ': self.confirm_pass_field,
								 'Email: ': self.email_field, 'Assign Store: ': self.store_field}


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
		fields = [bool(self.first_name_field.text()), bool(self.username_field.text()), bool(self.password_field.text()), bool(self.email_field.text()), bool(self.last_name_field.text()), bool(self.confirm_pass_field.text()), bool(self.confirmation_code_field.text())]
		self.register_button.setEnabled(sum(fields) == len(fields))

	def accept(self):
		self.username = self.username_field.text()
		self.password = self.password_field.text()
		self.first_name = self.first_name_field.text()
		self.last_name = self.last_name_field.text()
		self.email = self.email_field.text().lower()
		
		store = self.store_field.currentText()		
		self.store_address_id = self.store_address_dict[store]

		confirmation_code = self.confirmation_code_field.text()
		code_query = "select user_codes from systeminformation where system_id = 1;"
		cursor = connection.cursor()
		cursor.execute(code_query)
		user_code = str(cursor.fetchone()['user_codes'])

		try:
			if len(self.first_name) < fname_min_len:
				self.error_window = LoginMessage('first_name_length')
				self.error_window.show()
				return
			elif len(self.last_name) < lname_min_len:
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
			elif not bool(re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)):
				self.error_window = LoginMessage('invalid_email')
				self.error_window.show()
				return
			elif confirmation_code != user_code:
				self.error_window = LoginMessage('confirmation_code')
				self.error_window.show()
				return

			cursor = connection.cursor()
			check_query = "select * from userr where username = '{}'".format(self.username)  #check to see if username already exists
			cursor.execute(check_query)

			existing_user_row_count = cursor.rowcount
			if existing_user_row_count != 0:
				self.error_window = LoginMessage('existing_user')
				self.error_window.show()
				return

			create_user = "insert into userr values ('{}', '{}', '{}', '{}', '{}', '{}');".format(self.username, self.password, 'manager', self.email, self.first_name, self.last_name)
		
			cursor.execute(create_user)
			connection.commit()		

			create_manager = "insert into manages values ('{}', '{}');".format(self.username, self.store_address_id)
			cursor.execute(create_manager)
			connection.commit()

			self.loginwindow = Login()
			self.loginwindow.show()
			self.close()

		except Exception as e:
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
		self.payment_methods = PaymentMethods(self.username, 'buyer_func', None, None)
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

		self.query  = "select store_name as 'Store', CONCAT (house_number, ' ', street) as 'Address', phone as 'Phone', CONCAT (opening_time, ' - ', closing_time) as 'Hours Today' from grocerystore natural join address where address_id = id;"
		self.tabledata = tablemaker(self.query)
		column_headers = self.tabledata[0]
		rows = self.tabledata[1]

		address_id_query  = "select store_id, store_name as 'Store', CONCAT (house_number, ' ', street) as 'Address' from grocerystore natural join address where address_id = id;"

		cursor.execute(address_id_query)
		store_data = cursor.fetchall()
		self.address_id_dict = {str(store['Store']).strip() + ' '+ str(store['Address']) : store['store_id'] for store in store_data}

		self.table = QTableWidget(len(rows), len(rows[0]), self)
		self.table.horizontalHeader().setStretchLastSection(True)
		self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.table.verticalHeader().setStretchLastSection(True)
		self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

		self.back = QPushButton('Back')
		self.select = QPushButton('Select')

		self.back.clicked.connect(self.accept_back)
		self.select.clicked.connect(self.accept_select)

		button_group_box = QGroupBox()
		hbox_layout = QHBoxLayout()

		hbox_layout.addWidget(self.back)
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
		self.setGeometry(600,150,800,800)

	def rowclicked(self):
		self.select.setEnabled(True)

	def accept_back(self):
		self.buyer_func = BuyerFunctionality(self.username)
		self.buyer_func.show()
		self.close()

	def accept_select(self):
		indexes = self.table.selectionModel().selectedRows()
		for index in indexes:
			store_name = [self.table.item(index.row(),i).text() for i in range(self.table.columnCount())][0]
			store_address = [self.table.item(index.row(),i).text() for i in range(self.table.columnCount())][1]

		store_key = str(store_name) +' '+ str(store_address)
		store_id = self.address_id_dict[store_key]

		order_id_query = "select MAX(order_id) as max_id from orderr;"
		cursor.execute(order_id_query)
		order_id = int(cursor.fetchone()['max_id']) + 1

		order_info_dict = {'username': self.username, 'order_id': order_id, 'store_id': store_id, 'delivery_instructions': None, 'delivery_time': None, 'order_placed_date': None, 
							'order_placed_time': None, 'deliverer_username': 'chivalrouspotatoes', 'delivery_time': None, 'delivery_date': None, 'items': {}, 'price': {},
							'description': {}}

		self.store_homepage = StoreHomepage(order_info_dict)
		self.store_homepage.show()
		self.close()
		
class StoreHomepage(QWidget):
	def __init__(self, order_info_dict):
		super(StoreHomepage,self).__init__()
		self.setWindowTitle('Store Homepage')
		self.setWindowIcon(QIcon('groceries.png'))

		self.order_info_dict = order_info_dict

		self.username = order_info_dict['username']
		self.store_id = order_info_dict['store_id']
		self.order_id = order_info_dict['order_id']

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
		self.find_item = FindItem(self.order_info_dict)
		self.find_item.show()
		self.close()
		
	def accept_view_cart_button(self):
		self.order_id = 5
		self.view_cart = Cart(self.order_info_dict)
		self.view_cart.show()
		self.close()

	def accept_cancel_order(self):
		self.buyer_func = BuyerFunctionality(self.order_info_dict['username'])
		self.buyer_func.show()
		self.close()
	def accept_back(self):
		self.storelist = StoreList(self.username)
		self.storelist.show()
		self.close()

class FindItem(QWidget):
	def __init__(self, order_info_dict):
		super(FindItem, self).__init__()
		self.setWindowTitle('Find Item')
		self.setWindowIcon(QIcon('groceries.png'))
		self.order_info_dict = order_info_dict
				
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

		if len(self.order_info_dict['items'].keys()) == 0:
			self.checkout_button.setEnabled(False)

		vbox = QVBoxLayout()
		vbox.addWidget(group_box)
		vbox.addWidget(self.checkout_button)
		vbox.addWidget(self.back_button)
		self.setLayout(vbox)
		self.setGeometry(600,150,800,200)

	def accept_clicked(self, category):
		def show_table():
			self.item_table = ItemTable(self.order_info_dict, category)
			self.item_table.show()
			self.close()
		return show_table

	def checkout(self):
		self.check_out = Checkout(self.order_info_dict)
		self.check_out.show()
		self.close()

	def accept_back(self):
		self.storehome = StoreHomepage(self.order_info_dict)
		self.storehome.show()
		self.close()

class ItemTable(QWidget):
	def __init__(self, order_info_dict, category):
		super(ItemTable, self).__init__()
		self.setWindowTitle(category)
		self.setWindowIcon(QIcon('groceries.png'))
		self.order_info_dict = order_info_dict
		self.category = category
		self.query  = "SELECT i.item_name as 'Item Name', i.description as 'Description', i.exp_date as 'Expiration Date', i.listed_price as 'Price', i.quantity as 'Quantity' FROM item i, soldat s WHERE s.store_id = '{}' AND i.food_group = '{}' and i.item_id = s.item_id;".format(self.order_info_dict['store_id'], self.category)

		self.tabledata = tablemaker(self.query)
		column_headers = self.tabledata[0]
		self.rows = self.tabledata[1]

		self.table = QTableWidget(len(self.rows), len(self.rows[0]), self)
		self.table.horizontalHeader().setStretchLastSection(True)
		self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.table.verticalHeader().setStretchLastSection(True)
		self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

		self.back = QPushButton('Back')
		self.add_to_cart = QPushButton('Add to Cart')
		self.checkout_button = QPushButton('Checkout')

		self.back.clicked.connect(self.accept_back)
		self.add_to_cart.clicked.connect(self.accept_add_to_cart)
		self.checkout_button.clicked.connect(self.accept_checkout)

		button_group_box = QGroupBox()
		hbox_layout = QHBoxLayout()

		hbox_layout.addWidget(self.back)
		hbox_layout.addWidget(self.add_to_cart)
		hbox_layout.addWidget(self.checkout_button)

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

		if len(self.order_info_dict['items'].keys()) == 0:
			self.checkout_button.setEnabled(False)

		self.add_to_cart.setEnabled(False)
		self.setLayout(vbox_layout)
		self.setGeometry(600,150,1000,500)

	def rowclicked(self):
		if self.rows != [['No Items Found.']]:
			self.add_to_cart.setEnabled(True)

	def accept_back(self):
		self.buyer_func = FindItem(self.order_info_dict)
		self.buyer_func.show()
		self.close()

	def accept_add_to_cart(self):
		indexes = self.table.selectionModel().selectedRows()
		for index in indexes:
			item = [self.table.item(index.row(),i).text() for i in range(self.table.columnCount())]

		self.add_item = AddToCart(self.order_info_dict, item[0], item[4], item[3], item[1], self.category)
		self.add_item.show()
		self.close()

	def accept_checkout(self):
		self.order_id = 1
		self.checkout_window = Checkout(self.order_info_dict)
		self.checkout_window.show()
		self.close()

class AddToCart(QWidget):
	def __init__(self, order_info_dict, item_name, item_quant, item_price, description, category):
		super(AddToCart, self).__init__()
		self.setWindowTitle('Add To Cart')
		self.setWindowIcon(QIcon('groceries.png'))
		self.order_info_dict = order_info_dict
		self.item_name = item_name.title()
		self.item_quant = item_quant
		self.item_price = item_price
		self.description = description
		self.category = category

		if self.item_name in self.order_info_dict['items'].keys():
			num_in_cart = int(self.order_info_dict['items'][self.item_name])
		else:
			num_in_cart = 0

		num_avail = int(self.item_quant) - num_in_cart

		layout = QVBoxLayout()
		self.quantity_field = QLineEdit()
		buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		layout.addWidget(QLabel('How many of {} would you like to add to your cart?'.format(self.item_name)))
		layout.addWidget(QLabel('\tNumber in cart: {}'.format(num_in_cart) + ' | Number available: {}'.format(num_avail)))
		layout.addWidget(self.quantity_field)
		layout.addWidget(buttons)

		self.setLayout(layout)

	def accept(self):
		if not self.quantity_field.text().isdigit() or int(self.quantity_field.text()) > int(self.item_quant):
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Information)
			msg.setWindowTitle('Add To Cart')
			msg.setText('Total quantity must be less than {}.'.format(self.item_quant))
			msg.setStandardButtons(QMessageBox.Ok)
			msg.exec_()
			return

		else:
			if self.item_name in self.order_info_dict['items'].keys():
				if int(self.quantity_field.text()) + self.order_info_dict['items'][self.item_name] > int(self.item_quant):
					msg = QMessageBox()
					msg.setIcon(QMessageBox.Information)
					msg.setWindowTitle('Add To Cart')
					msg.setText('Total quantity must be less than {}.'.format(self.item_quant))
					msg.setStandardButtons(QMessageBox.Ok)
					msg.exec_()
					return
				else:
					self.order_info_dict['items'][self.item_name] += int(self.quantity_field.text())
			else:
				self.order_info_dict['items'][self.item_name] = int(self.quantity_field.text())
				self.order_info_dict['price'][self.item_name] = float(str(self.item_price))
				self.order_info_dict['description'][self.item_name] = self.description

		self.item_table = ItemTable(self.order_info_dict, self.category)
		self.item_table.show()
		self.close()

	def reject(self):
		self.item_table = ItemTable(self.order_info_dict, self.category)
		self.item_table.show()
		self.close()

class Cart(QWidget):
	def __init__(self, order_info_dict):
		super(Cart, self).__init__()
		self.setWindowTitle('Cart')
		self.setWindowIcon(QIcon('groceries.png'))
		self.order_info_dict = order_info_dict

		rows = []
		column_headers = ['Item Name', 'Description', 'Quantity', 'Price']

		for item in self.order_info_dict['items']:
			row = [item, self.order_info_dict['description'][item], str(self.order_info_dict['items'][item]), '$' + str(self.order_info_dict['price'][item])]
			rows.append(row)

		self.total_items = len(rows)

		if self.total_items == 0:
			rows = [['No items in cart.']]

		self.back = QPushButton('Back')
		self.delete_item = QPushButton('Delete Item')
		self.checkout = QPushButton('Checkout')		

		self.back.clicked.connect(self.accept_back)
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
		vbox_layout.addWidget(QLabel('Total Items: '+ str(self.total_items)))
		vbox_layout.addWidget(self.table)
		vbox_layout.addWidget(button_group_box)
		vbox_layout.addWidget(self.checkout)

		if self.total_items == 0:
			self.checkout.setEnabled(False)

		self.delete_item.setEnabled(False)
		self.setLayout(vbox_layout)
		self.setGeometry(600,150,800,600)

	def rowclicked(self):
		if self.total_items == 0:
			self.delete_item.setEnabled(False)
		else:
			self.delete_item.setEnabled(True)

	def accept_back(self):
		self.storehome = StoreHomepage(self.order_info_dict)
		self.storehome.show()
		self.close()

	def accept_delete_item(self):
		indexes = self.table.selectionModel().selectedRows()
		for index in indexes:
			item_name = [self.table.item(index.row(),i).text() for i in range(self.table.columnCount())][0]

		del self.order_info_dict['items'][item_name]
		del self.order_info_dict['price'][item_name]
		del self.order_info_dict['description'][item_name]

		self.store_id = 33
		self.order_id = 4
		self.cart = Cart(self.order_info_dict)
		self.cart.show()
		self.close()

	def accept_checkout(self):
		self.checkout_window = Checkout(self.order_info_dict)
		self.checkout_window.show()
		self.close()
		
class BuyerAcctInfo(QWidget):
	def __init__(self, username):
		super(BuyerAcctInfo, self).__init__()
		self.username = username
		self.setWindowIcon(QIcon('groceries.png'))
		self.setWindowTitle('Account Information')

		user_info_query = "select * from userr where username = '{}';".format(self.username)
		cursor.execute(user_info_query)
		user_info = cursor.fetchone()

		buyer_info_query = "select * from buyer where username = '{}';".format(self.username)
		cursor.execute(buyer_info_query)
		buyer_info = cursor.fetchone()

		address_query = "select CONCAT(house_number, ' ', street) as 'address', city, state, zip_code from address natural join buyer where address_id = id and username = '{}';".format(self.username)
		cursor.execute(address_query)
		address_info = cursor.fetchone()

		payment_info_query = "select payment_name from payments where username = '{}';".format(self.username)
		cursor.execute(payment_info_query)
		payment_info = cursor.fetchall()

		current_default_query = "select default_payment from buyer where username = '{}';".format(self.username)
		cursor.execute(current_default_query)
		current_default = cursor.fetchone()

		payment_methods = [card['payment_name'] for card in payment_info]

		self.first_name_field = QLineEdit(user_info['first_name'])
		self.last_name_field = QLineEdit(user_info['last_name'])
		self.username_field = QLineEdit(self.username)
		self.phone_field = QLineEdit(str(int(buyer_info['phone'])))
		self.store_address = QLineEdit()
		self.email_field = QLineEdit(user_info['email'])
		self.preferred_card = QComboBox()
		self.preferred_card.addItems(payment_methods)
		self.preferred_card.setCurrentIndex({name: index for index, name in enumerate(payment_methods)}[current_default['default_payment']])

		self.address_field = QLineEdit(str(address_info['address']))
		self.city_field = QLineEdit(address_info['city'])

		store_query = "select store_name, concat(house_number, ' ', street) as 'address' from grocerystore natural join address where address_id = id;"
		cursor.execute(store_query)
		store_list = [entry['store_name'] + ' - ' + entry['address'] for entry in cursor.fetchall()]

		self.store_field = QComboBox()
		self.store_field.addItems(store_list)
		self.state_field = QLineEdit(address_info['state'])
		self.zip_field = QLineEdit(str(address_info['zip_code']))

		self.field_label_dict = {'First Name: ': self.first_name_field, 'Last Name: ': self.last_name_field, 'Username: ': self.username_field,
								  'Phone: ': self.phone_field, 'Preferred Grocery Store: ': self.store_field, 'Address: ': self.address_field, 'City: ': self.city_field,
								 'State: ': self.state_field, 'Zip Code: ': self.zip_field, 'Email: ': self.email_field, 'Preferred Payment Method: ': self.preferred_card}

		group_box1 = QGroupBox('Buyer Account Information')
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

		group_box1.setLayout(grid)

		self.username_field.setEnabled(False)


		hbox = QHBoxLayout()
		self.back_button = QPushButton('Back')
		self.delete_acct = QPushButton('Delete Account')
		self.update_button = QPushButton('Update')

		self.back_button.clicked.connect(self.close_win)
		self.delete_acct.clicked.connect(self.check_delete_acct)
		self.update_button.clicked.connect(self.update_info)


		hbox.addWidget(self.back_button)
		hbox.addWidget(self.delete_acct)
		hbox.addWidget(self.update_button)
		group_box2 = QGroupBox()
		group_box2.setLayout(hbox)

		vbox_layout = QVBoxLayout()

		vbox_layout.addWidget(group_box1)
		vbox_layout.addWidget(group_box2)


		self.setLayout(vbox_layout)
		self.first_name_field.setFocus()
		self.setGeometry(500,200,1000,200)

	def update_info(self):

		for field in self.field_label_dict:
			try:
				if len(self.field_label_dict[field].text()) == 0:
					msg = QMessageBox()
					msg.setIcon(QMessageBox.Information)
					msg.setWindowTitle('Buyer Information')
					msg.setText("Please complete all fields!")
					msg.setStandardButtons(QMessageBox.Ok)
					msg.exec_()
					return
			except:
				pass

		email = self.email_field.text()
		phone = self.phone_field.text()
		state = self.state_field.text().title()
		address = self.address_field.text()
		address_split = address.split()
		zip_code = self.zip_field.text()
		city = self.city_field.text()
		preferred_store = self.store_field.currentText()
		payment_name = self.preferred_card.currentText()
		fname = self.first_name_field.text()
		lname = self.last_name_field.text()

		house_number = address_split[0]
		del address_split[0]

		street = ''
		for i, el in enumerate(address_split):
			street += el
			if i != len(address_split) - 1:
				street += ' '
		street = street.title()


		if len(fname) < fname_min_len:
			self.error_window = LoginMessage('first_name_length')
			self.error_window.show()
			return
		elif len(lname) < lname_min_len:
			self.error_window = LoginMessage('last_name_length')
			self.error_window.show()
			return
		if not bool(re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)):
			self.error_window = LoginMessage('invalid_email')
			self.error_window.show()
			return
		elif len(phone) != 10 or not phone.isdigit():
			self.error_window = LoginMessage('phone')
			self.error_window.show()
			return		
		elif len(zip_code) != 5 or not zip_code.isdigit():
			self.error_window = LoginMessage('zip_code')
			self.error_window.show()
			return
		elif state not in state_list:
			self.error_window = LoginMessage('state')
			self.error_window.show()
			return

		update_user = "update userr set first_name = '{}', last_name = '{}', email = '{}' where username = '{}';".format(fname, lname, email, self.username)
		update_buyer = "update buyer set phone = {}, default_payment = '{}' where username = '{}';".format(phone, payment_name, self.username)
		update_address = "update address set house_number = '{}', street = '{}', city = '{}', state = '{}', zip_code = '{}' where id = (select address_id from buyer where username = '{}');".format(house_number, street, city, state, zip_code, self.username)

		cursor = connection.cursor()
		cursor.execute(update_user)
		cursor.execute(update_buyer)
		cursor.execute(update_address)
		connection.commit()

		update_msg = QMessageBox()
		update_msg.setIcon(QMessageBox.Information)
		update_msg.setWindowTitle('Buyer Information')
		update_msg.setText("Information Updated!")
		update_msg.setStandardButtons(QMessageBox.Ok)
		update_msg.accepted.connect(self.close_win)
		update_msg.exec_()

	def close_win(self):
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
		query = "delete from userr where username = '{}';".format(self.username)
		cursor.execute(query)
		self.login = Login()
		self.login.show()
		self.close()

class OrderHistory(QWidget):
	def __init__(self, username):
		super(OrderHistory, self).__init__()
		self.setWindowTitle('Order History')
		self.setWindowIcon(QIcon('groceries.png'))

		self.username = username

		self.query  = "SELECT * FROM \
						(\
						SELECT O.order_id as 'Order ID', O.order_placed_date as 'Date', IF(is_delivered = 1, 'Yes', 'No') as 'Delivered', GS.store_name as 'Store Name'\
						FROM orderedBy OB, orderr O, deliveredby DB, grocerystore GS, orderfrom OFR\
						WHERE OB.buyer_username = '{}' and O.order_id = DB.order_id and DB.order_id = OB.order_id and GS.store_id = OFR.store_address_id and OFR.order_id = OB.order_id\
						) A\
						natural join\
						(\
						SELECT O.order_id as 'Order ID', sum(SI.quantity * I.listed_price) as 'Total Price', sum(SI.quantity) as 'Total Quantity'\
						FROM orderr O, selectitem SI, item I, orderedby OB\
						WHERE O.order_id = SI.order_id and SI.item_id = I.item_id and O.order_id = OB.order_id and OB.buyer_username = '{}'\
						group by O.order_id\
						) B\
						;".format(self.username, self.username)

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
		self.order_details = QPushButton('View Order Details')
		self.order_details.setEnabled(False)

		self.back.clicked.connect(self.accept_back)
		self.order_details.clicked.connect(self.accept_details)

		hbox_layout = QHBoxLayout()

		hbox_layout.addWidget(self.back)
		hbox_layout.addWidget(self.order_details)

		group_box = QGroupBox()
		group_box.setLayout(hbox_layout)

		vbox_layout = QVBoxLayout()
		vbox_layout.addWidget(self.table)
		vbox_layout.addWidget(group_box)

		self.setLayout(vbox_layout)
		self.setGeometry(500,100,1200,800)

	def rowclicked(self):
		self.order_details.setEnabled(True)

	def accept_back(self):
		self.buyer_func = BuyerFunctionality(self.username)
		self.buyer_func.show()
		self.close()

	def accept_details(self):
		indexes = self.table.selectionModel().selectedRows()
		for index in indexes:
			order_id = [self.table.item(index.row(),i).text() for i in range(self.table.columnCount())][0]
  
class PaymentMethods(QWidget):
	def __init__(self, username, parent_type, store_id = None, order_id = None, order_info_dict = None):
		super(PaymentMethods, self).__init__()
		self.setWindowIcon(QIcon('groceries.png'))
		self.setWindowTitle('Payment Methods')

		self.parent_type = parent_type
		self.username = username
		self.store_id = store_id
		self.order_id = order_id
		self.order_info_dict = order_info_dict

		self.query  = "SELECT payment_name as 'Payment Name', account_number as 'Account Number', routing_number as 'Routing Number', IF(payment_name = default_payment, 'Yes', 'No') AS 'Default' FROM payments natural join buyer WHERE buyer.username = '{}';".format(self.username)

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
		self.diff_payment = QPushButton('Use Different Payment')

		self.back.clicked.connect(self.accept_back)
		self.diff_payment.clicked.connect(self.accept_diff_payment)

		hbox_layout = QHBoxLayout()

		hbox_layout.addWidget(self.back)
		hbox_layout.addWidget(self.diff_payment)

		if self.parent_type == 'checkout':
			self.confirm_order = QPushButton('Confirm Payment Method')
			self.confirm_order.setEnabled(False)
			self.confirm_order.clicked.connect(self.accept_confirm)
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
		if self.parent_type == 'buyer_func' or self.parent_type == 'new':
			self.buyer_func = BuyerFunctionality(self.username)
			self.buyer_func.show()

		elif self.parent_type == 'checkout':
			self.checkout = Checkout(self.order_info_dict)
			self.checkout.show()
		self.close()


	def accept_diff_payment(self):
		if self.parent_type == 'checkout':
			self.new_payment = NewPaymentCheckout(self.username, self.order_info_dict)
			self.new_payment.show()
			self.close()
		else:
			self.new_payment = NewPayment(self.username)
			self.new_payment.show()
			self.close()

	def accept_confirm(self):
		order_placed_time = dt.datetime.now().strftime('%H:%M')
		order_placed_date = dt.datetime.now().strftime('%Y-%m-%d')

		self.order_info_dict['order_placed_time'] = order_placed_time
		self.order_info_dict['order_placed_date'] = order_placed_date

		indexes = self.table.selectionModel().selectedRows()
		for index in indexes:
			payment_name = [self.table.item(index.row(),i).text() for i in range(self.table.columnCount())][0]

		order_id = self.order_info_dict['order_id']
		username = self.order_info_dict['username']
		store_id = self.order_info_dict['store_id']
		delivery_instructions = self.order_info_dict['delivery_instructions']
		delivery_time = self.order_info_dict['delivery_time']
		order_placed_date = self.order_info_dict['order_placed_date']
		order_placed_time = self.order_info_dict['order_placed_time']
		deliverer_username = self.order_info_dict['deliverer_username']
		is_delivered = 0
		delivery_date = self.order_info_dict['delivery_date']
		items = self.order_info_dict['items']

		create_order = "INSERT into orderr values('{}', '{}', '{}', '{}', '{}');".format(order_id, delivery_instructions, delivery_time, order_placed_date, order_placed_time)
		create_orderedby = "INSERT into orderedby values('{}', '{}');".format(order_id, username)
		create_deliveredby = "INSERT into deliveredby values ('{}', '{}', '{}', '{}', '{}');".format(order_id, deliverer_username, is_delivered, delivery_time, delivery_date)
		create_orderfrom = "INSERT into orderfrom values ({}, {});".format(store_id, order_id)
		cursor.execute(create_order)
		cursor.execute(create_orderedby)
		cursor.execute(create_deliveredby)
		connection.commit()
		cursor.execute(create_orderfrom)

		for item in items:
			item_id_query = "SELECT item_id from item where item_name = '{}';".format(item)
			cursor.execute(item_id_query)
			item_id = cursor.fetchone()['item_id']
			quantity_sold = items[item]
			update_items = "UPDATE item set quantity = quantity - {} where item_name = '{}';".format(quantity_sold, item)
			cursor.execute(update_items)

			insert_selectitem = "INSERT into selectitem values('{}', '{}', '{}');".format(item_id, quantity_sold, order_id)
			cursor.execute(insert_selectitem)

		connection.commit()
		
		self.receipt_win = Receipt(self.order_info_dict, payment_name)
		self.receipt_win.show()
		self.close()

class NewPayment(QWidget):
	def __init__(self, username):
		super(NewPayment, self).__init__()
		self.setWindowTitle('New Payment')
		self.setWindowIcon(QIcon('groceries'))
		self.username = username

		self.payment_name_field = QLineEdit()
		self.acct_number_field = QLineEdit()
		self.routing_number_field = QLineEdit()
		self.default_payment_field = QComboBox()
		self.default_payment_field.addItems(['Yes', 'No'])

		self.payment_name_field.textChanged.connect(self.on_text_changed)
		self.acct_number_field.textChanged.connect(self.on_text_changed)
		self.routing_number_field.textChanged.connect(self.on_text_changed)

		group_box = QGroupBox()
		layout1 = QFormLayout()
		layout1.addRow(QLabel('Payment Name: '), self.payment_name_field)
		layout1.addRow(QLabel('Account Number: '), self.acct_number_field)
		layout1.addRow(QLabel('Routing Number: '), self.routing_number_field)
		layout1.addRow(QLabel('Default Payment: '), self.default_payment_field)

		group_box.setLayout(layout1)

		hbox = QHBoxLayout()
		self.back_button = QPushButton('Back')
		self.add_payment_button = QPushButton('Add Payment')
		self.add_payment_button.setEnabled(False)

		self.back_button.clicked.connect(self.back)
		self.add_payment_button.clicked.connect(self.add_payment)

		hbox.addWidget(self.back_button)
		hbox.addWidget(self.add_payment_button)
		group_box2 = QGroupBox()
		group_box2.setLayout(hbox)

		vbox = QVBoxLayout()

		vbox.addWidget(group_box)
		vbox.addWidget(group_box2)

		self.setLayout(vbox)
		self.setGeometry(700,200,400,200)


	def on_text_changed(self):
		fields = [bool(self.payment_name_field.text()), bool(self.acct_number_field.text()), bool(self.routing_number_field.text())]
		self.add_payment_button.setEnabled(sum(fields) == len(fields))

	def back(self):
		self.close()

	def add_payment(self):
		payment_name = self.payment_name_field.text()
		account_number = self.acct_number_field.text()
		routing_number = self.routing_number_field.text()

		name_check_query = "select * from payments where payment_name = '{}' and username = '{}';".format(payment_name, self.username)
		cursor.execute(name_check_query)
		payment_name_count = cursor.rowcount

		if payment_name_count != 0:
			self.unique_payment_msg = LoginMessage('unique_payment')
			self.unique_payment_msg.show()
			return

		elif len(account_number) != 9:# or not account_number.isdigit():
			self.acct_len_msg = LoginMessage('acct_num_len')
			self.acct_len_msg.show()
			return

		elif len(routing_number) != 9 or not routing_number.isdigit():
			self.routing_len_msg = LoginMessage('routing_len')
			self.routing_len_msg.show()
			return

		add_payment_query = "insert into payments values ('{}', '{}', '{}', '{}');".format(self.username, payment_name, account_number, routing_number)
		cursor.execute(add_payment_query)
		connection.commit()

		if self.default_payment_field.currentText() == 'Yes':
			update_buyer = "update buyer set default_payment = '{}' where username = '{}';".format(payment_name, self.username)
			cursor.execute(update_buyer)
			connection.commit()

		self.payment_methods = PaymentMethods(self.username, 'new')
		self.payment_methods.show()
		self.close()

class NewPaymentCheckout(QWidget):
	def __init__(self, username, order_info_dict):
		super(NewPaymentCheckout, self).__init__()
		self.setWindowTitle('New Payment')
		self.setWindowIcon(QIcon('groceries'))
		self.username = username
		self.order_info_dict = order_info_dict

		self.payment_name_field = QLineEdit()
		self.acct_number_field = QLineEdit()
		self.routing_number_field = QLineEdit()
		self.default_payment_field = QComboBox()
		self.default_payment_field.addItems(['Yes', 'No'])

		self.payment_name_field.textChanged.connect(self.on_text_changed)
		self.acct_number_field.textChanged.connect(self.on_text_changed)
		self.routing_number_field.textChanged.connect(self.on_text_changed)

		group_box = QGroupBox()
		layout1 = QFormLayout()
		layout1.addRow(QLabel('Payment Name: '), self.payment_name_field)
		layout1.addRow(QLabel('Account Number: '), self.acct_number_field)
		layout1.addRow(QLabel('Routing Number: '), self.routing_number_field)
		layout1.addRow(QLabel('Default Payment: '), self.default_payment_field)

		group_box.setLayout(layout1)

		hbox = QHBoxLayout()
		self.back_button = QPushButton('Back')
		self.add_payment_button = QPushButton('Add Payment')
		self.add_payment_button.setEnabled(False)

		self.back_button.clicked.connect(self.back)
		self.add_payment_button.clicked.connect(self.add_payment)

		hbox.addWidget(self.back_button)
		hbox.addWidget(self.add_payment_button)
		group_box2 = QGroupBox()
		group_box2.setLayout(hbox)

		vbox = QVBoxLayout()

		vbox.addWidget(group_box)
		vbox.addWidget(group_box2)

		self.setLayout(vbox)
		self.setGeometry(700,200,400,200)

	def on_text_changed(self):
		fields = [bool(self.payment_name_field.text()), bool(self.acct_number_field.text()), bool(self.routing_number_field.text())]
		self.add_payment_button.setEnabled(sum(fields) == len(fields))

	def back(self):
		self.close()

	def add_payment(self):
		payment_name = self.payment_name_field.text()
		account_number = self.acct_number_field.text()
		routing_number = self.routing_number_field.text()

		name_check_query = "select * from payments where payment_name = '{}' and username = '{}';".format(payment_name, self.username)
		cursor.execute(name_check_query)
		payment_name_count = cursor.rowcount

		if payment_name_count != 0:
			self.unique_payment_msg = LoginMessage('unique_payment')
			self.unique_payment_msg.show()
			return

		elif len(account_number) != 9:# or not account_number.isdigit():
			self.acct_len_msg = LoginMessage('acct_num_len')
			self.acct_len_msg.show()
			return

		elif len(routing_number) != 9 or not routing_number.isdigit():
			self.routing_len_msg = LoginMessage('routing_len')
			self.routing_len_msg.show()
			return

		add_payment_query = "insert into payments values ('{}', '{}', '{}', '{}');".format(self.username, payment_name, account_number, routing_number)
		cursor.execute(add_payment_query)
		connection.commit()

		if self.default_payment_field.currentText() == 'Yes':
			update_buyer = "update buyer set default_payment = '{}' where username = '{}';".format(payment_name, self.username)
			cursor.execute(update_buyer)
			connection.commit()

		self.payment_window = PaymentMethods(self.order_info_dict['username'], 'checkout', None, None, self.order_info_dict)
		self.payment_window.show()
		self.close()

class Checkout(QWidget):
	def __init__(self, order_info_dict):
		super(Checkout, self).__init__()
		self.setWindowIcon(QIcon('groceries.png'))
		self.setWindowTitle('Checkout')
		self.order_info_dict = order_info_dict

		total_price = 0.00
		for item in self.order_info_dict['items']:
			item_price = float(self.order_info_dict['price'][item])
			item_quant = float(self.order_info_dict['items'][item])

			total_item_price = item_price * item_quant
			total_price += total_item_price
		total_price = round(total_price, 2)

		time_list = ['ASAP', '1 hour', '2 hours', '5 hours', '10 hours', '12 hours', '24 hours']

		self.time_dropdown = QComboBox()
		self.time_dropdown.addItems(time_list)
		self.time_dropdown.setToolTip('Select a delivery time.')

		self.total_price_field = QLineEdit('$' + str(total_price))
		self.total_price_field.setEnabled(False)

		self.delivery_instructions = QTextEdit()
		self.delivery_instructions.resize(4, 100)

		self.back_button = QPushButton('Back')
		self.finalize_button = QPushButton('Choose Payment')

		self.back_button.clicked.connect(self.accept_back)
		self.finalize_button.clicked.connect(self.finalize)

		self.group_box = QGroupBox('Checkout')
		grid = QGridLayout()

		grid.addWidget(QLabel('Delivery Time: '), 0, 0)
		grid.addWidget(self.time_dropdown, 0, 1)
		grid.addWidget(QLabel('Total Price: '), 1, 0)
		grid.addWidget(self.total_price_field, 1, 1)
		grid.addWidget(QLabel('Delivery Instructions: '), 2, 0)
		grid.addWidget(self.delivery_instructions, 2, 1)

		self.group_box.setLayout(grid)
		self.layout = QVBoxLayout()
		self.layout.addWidget(self.group_box)

		hbox = QHBoxLayout()
		group_box2 = QGroupBox()
		hbox.addWidget(self.back_button)
		hbox.addWidget(self.finalize_button)
		group_box2.setLayout(hbox)

		self.layout.addWidget(group_box2)
		self.setLayout(self.layout)
		self.setGeometry(700,150, 500, 400)

	def accept_back(self):
		self.cart = Cart(self.order_info_dict)
		self.cart.show()
		self.close()

	def finalize(self):
		instructions = self.delivery_instructions.toPlainText()
		if len(instructions) > 250:
			self.error_window = LoginMessage('instructions')
			self.error_window.show()
			return
		self.order_info_dict['delivery_time'] = self.time_dropdown.currentText()
		self.order_info_dict['delivery_instructions'] = instructions

		self.payment_window = PaymentMethods(self.order_info_dict['username'], 'checkout', None, None, self.order_info_dict)
		self.payment_window.show()
		self.close()

class Receipt(QWidget):
	def __init__(self, order_info_dict, payment_name):
		super(Receipt, self).__init__()
		self.setWindowTitle('Receipt')
		self.setWindowIcon(QIcon('groceries.png'))
		self.order_info_dict = order_info_dict
		self.payment_name = payment_name

		num_items = sum([value for value in self.order_info_dict['items'].values()])

		self.order_num_field = QLineEdit(str(self.order_info_dict['order_id']))
		self.payment_name_field = QLineEdit(self.payment_name.title())
		self.deliverer_field = QLineEdit('Clio Allitto')
		self.num_items_field = QLineEdit(str(num_items))
		self.time_field = QLineEdit(str(self.order_info_dict['order_placed_time']))
		self.delivery_time_field = QLineEdit(self.order_info_dict['delivery_time'])

		self.order_num_field.setEnabled(False)
		self.payment_name_field.setEnabled(False)
		self.deliverer_field.setEnabled(False)
		self.num_items_field.setEnabled(False)
		self.time_field .setEnabled(False)
		self.delivery_time_field.setEnabled(False)

		groupbox1 = QGroupBox('Receipt')
		layout1 = QFormLayout()

		layout1.addRow(QLabel('Order Number: '), self.order_num_field)
		layout1.addRow(QLabel('Payment Name: '), self.payment_name_field)
		layout1.addRow(QLabel('Deliverer\'s Name: '), self.deliverer_field)
		layout1.addRow(QLabel('Number of Items: '), self.num_items_field)
		layout1.addRow(QLabel('Time Order Placed: '), self.time_field)
		layout1.addRow(QLabel('Time of Delivery: '), self.delivery_time_field)

		groupbox1.setLayout(layout1)

		vbox = QVBoxLayout()
		group_box2 = QGroupBox()
		self.home_button = QPushButton('Home')
		self.home_button.clicked.connect(self.go_home)
		vbox2 = QVBoxLayout()
		vbox2.addWidget(self.home_button)
		group_box2.setLayout(vbox2)

		vbox.addWidget(groupbox1)
		vbox.addWidget(group_box2)

		self.setLayout(vbox)

	def go_home(self):
		self.buyer_func = BuyerFunctionality(self.order_info_dict['username'])
		self.buyer_func.show()
		self.close()

class DelivererFunctionality(QWidget):
	def __init__(self, username):
		super(DelivererFunctionality, self).__init__()
		self.setWindowIcon(QIcon('groceries.png'))
		self.setWindowTitle("Deliverer Functionality")
		self.username = username

		group_box = QGroupBox('Deliverer Functionality')
		grid = QGridLayout()

		self.assignments_button = QPushButton('Assignments')
		self.account_info_button = QPushButton('Account Information')
		self.back_button = QPushButton('Back')

		self.back_button.clicked.connect(self.accept_back)
		self.account_info_button.clicked.connect(self.accept_acct_info)
		self.assignments_button.clicked.connect(self.accept_assignments)

		grid.addWidget(self.assignments_button, 0, 0)
		grid.addWidget(self.account_info_button, 0, 1)
		grid.addWidget(self.back_button, 1, 1)

		group_box.setLayout(grid)

		vbox = QVBoxLayout()
		vbox.addWidget(group_box)

		self.setLayout(vbox)

		self.setGeometry(700,200,600,200)


	def accept_back(self):
		self.loginwindow = Login()
		self.loginwindow.show()
		self.close()

	def accept_acct_info(self):
		self.acct_info = DelivererAcctInfo(self.username)
		self.acct_info.show()
		self.close()

	def accept_assignments(self):
		self.assignments_window = Assignments(self.username)
		self.assignments_window.show()
		self.close()

class DelivererAcctInfo(QWidget):
	def __init__(self, username):
		super(DelivererAcctInfo, self).__init__()

		self.username = username
		self.setWindowIcon(QIcon('groceries.png'))
		self.setWindowTitle('Account Information')

		user_info_query = "select * from userr where username = '{}';".format(self.username)
		cursor = connection.cursor()
		cursor.execute(user_info_query)
		user_info = cursor.fetchone()

		deliverer_info_query = "select * from userr where username = '{}';".format(self.username)
		cursor = connection.cursor()
		cursor.execute(deliverer_info_query)
		deliverer_info = cursor.fetchone()

		self.first_name_field = QLineEdit(user_info['first_name'])
		self.last_name_field = QLineEdit(user_info['last_name'])
		self.username_field = QLineEdit(self.username)
		self.email_field = QLineEdit(user_info['email'])

		self.username_field.setEnabled(False)

		group_box1 = QGroupBox('Deliverer Information')
		grid = QGridLayout()

		grid.addWidget(QLabel('First Name: '), 0, 0)
		grid.addWidget(self.first_name_field, 0, 1)
		grid.addWidget(QLabel('Last Name: '), 0, 2)
		grid.addWidget(self.last_name_field, 0, 3)

		grid.addWidget(QLabel('Username: '), 1, 0)
		grid.addWidget(self.username_field, 1, 1)

		grid.addWidget(QLabel('Email: '), 2, 0)
		grid.addWidget(self.email_field, 2, 1)

		group_box1.setLayout(grid)

		vbox_layout = QVBoxLayout()
		vbox_layout.addWidget(group_box1)

		group_box2 = QGroupBox()

		self.back_button= QPushButton('Back')
		self.delete_acct_button = QPushButton('Delete Account')
		self.update_button = QPushButton('Update')

		self.back_button.clicked.connect(self.back)
		self.delete_acct_button.clicked.connect(self.check_delete_acct)
		self.update_button.clicked.connect(self.update_info)

		hbox_layout = QHBoxLayout()
		hbox_layout.addWidget(self.back_button)
		hbox_layout.addWidget(self.delete_acct_button)
		hbox_layout.addWidget(self.update_button)

		group_box2.setLayout(hbox_layout)

		vbox_layout.addWidget(group_box2)

		self.setLayout(vbox_layout)
		self.setGeometry(740,200,700,100)

	def update_info(self):

		for field in [self.email_field.text(), self.first_name_field.text(), self.last_name_field.text()]:
			try:
				if len(field) == 0:
					msg = QMessageBox()
					msg.setIcon(QMessageBox.Information)
					msg.setWindowTitle('Buyer Information')
					msg.setText("Please complete all fields!")
					msg.setStandardButtons(QMessageBox.Ok)
					msg.exec_()
					return
			except:
				pass

		email = self.email_field.text()
		fname = self.first_name_field.text().title()
		lname = self.last_name_field.text().title()

		if len(fname) < fname_min_len:
			self.error_window = LoginMessage('first_name_length')
			self.error_window.show()
			return
		elif len(lname) < lname_min_len:
			self.error_window = LoginMessage('last_name_length')
			self.error_window.show()
			return
		elif not bool(re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)):
			self.error_window = LoginMessage('invalid_email')
			self.error_window.show()
			return

		update_user = "update userr set first_name = '{}', last_name = '{}', email = '{}' where username = '{}';".format(fname, lname, email, self.username)
		
		cursor = connection.cursor()
		cursor.execute(update_user)
		connection.commit()

		update_msg = QMessageBox()
		update_msg.setIcon(QMessageBox.Information)
		update_msg.setWindowTitle('Deliverer Information')
		update_msg.setText("Information Updated!")
		update_msg.setStandardButtons(QMessageBox.Ok)
		update_msg.accepted.connect(self.back)
		update_msg.exec_()

	def back(self):
		self.deliverer_func = DelivererFunctionality(self.username)
		self.deliverer_func.show()
		self.close()

	def check_delete_acct(self):
		msg = QMessageBox()
		msg.setWindowTitle('Delete Account')
		msg.setText("Are you sure you want to delete your account?")
		msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		msg.accepted.connect(self.accept_delete_acct)
		msg.exec_()

	def accept_delete_acct(self):
		query = "delete from userr where username = '{}';".format(self.username)
		cursor.execute(query)
		connection.commit()
		self.login = Login()
		self.login.show()
		self.close()

class Assignments(QWidget):
	def __init__(self, username):
		super(Assignments, self).__init__()
		self.username = username
		self.setWindowTitle('Assignments')
		self.setWindowIcon(QIcon('groceries.png'))


		self.query  = "SELECT *\
						FROM\
						(\
						SELECT GS.store_name as 'Store Name', O.order_id as 'Order ID', O.order_placed_date as 'Date', O.order_placed_time as 'Time Order Made', O.delivery_time as 'Time of Delivery'\
						FROM orderr O, deliveredby DB, grocerystore GS, orderfrom OFR\
						WHERE DB.deliverer_username = '{}' AND O.order_id = DB.order_id AND GS.store_id = OFR.store_address_id and OFR.order_id = O.order_id\
						) A\
						NATURAL JOIN\
						(\
						SELECT O.order_id as 'Order ID', sum(SI.quantity * I.listed_price) as 'Order Price', sum(SI.quantity) as 'Total Number of Items'\
						FROM orderr O, selectitem SI, item I, deliveredby DB\
						WHERE O.order_id = SI.order_id and SI.item_id = I.item_id and O.order_id = DB.order_id and DB.deliverer_username = '{}'\
						group by O.order_id\
						)B;".format(self.username, self.username)

		self.tabledata = tablemaker(self.query)
		column_headers = self.tabledata[0]
		rows = self.tabledata[1]

		self.table = QTableWidget(len(rows), len(rows[0]), self)
		self.table.horizontalHeader().setStretchLastSection(True)
		self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.table.verticalHeader().setStretchLastSection(True)
		self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

		self.back = QPushButton('Back')
		self.view_assn_details = QPushButton('View Assigment Details')

		self.back.clicked.connect(self.accept_back)
		self.view_assn_details.clicked.connect(self.accept_view_assn_details)

		button_group_box = QGroupBox()
		hbox_layout = QHBoxLayout()

		hbox_layout.addWidget(self.back)
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
		self.setGeometry(500,100,1250,800)

	def rowclicked(self):
		self.view_assn_details.setEnabled(True)

	def accept_back(self):
		self.deliverer_func = DelivererFunctionality(self.username)
		self.deliverer_func.show()
		self.close()

	def accept_view_assn_details(self):
		indexes = self.table.selectionModel().selectedRows()
		for index in indexes:
			order_id = [self.table.item(index.row(),i).text() for i in range(self.table.columnCount())][0]

		self.assignment_details = AssignmentDetails(self.username, order_id)
		self.assignment_details.show()
		self.close()

class AssignmentDetails(QWidget):
	def __init__(self, username, order_id):
		super(AssignmentDetails, self).__init__()
		self.setWindowTitle('Assignment Details')
		self.setWindowIcon(QIcon('groceries.png'))
		self.username = username
		self.order_id = order_id

		assignment_query = "SQL QUERY"
		status_query = "STATUS QUERY"
		status = 'Delivered'

		delivery_query = "SELECT O.order_placed_time as 'Order Placed', O.delivery_time as 'Delivery Time', IF(DB.is_delivered = 1, 'Delivered', 'Pending') as 'Status', CONCAT(A.house_number, ' ', A.street, ' ', A.city, ', ', A.state,' ', A.zip_code) as 'Buyer Address', GS.store_name as 'Store Name' FROM orderr O, orderfrom OFR, grocerystore GS, address A, orderedby OB, buyer B, deliveredBy DB WHERE O.order_id = OFR.order_id and OFR.store_address_id = GS.store_id and O.order_id = OB.order_id and OB.buyer_username = B.username and B.address_id = A.id and O.order_id = DB.order_id and O.order_id = 13075;"
		cursor.execute(delivery_query)
		delivery_data = cursor.fetchone()

		status_options = ['Pending', 'Delivered']

		self.order_placed_field = QLineEdit(delivery_data['Order Placed'])
		self.delivery_time_field = QLineEdit(delivery_data['Delivery Time'])
		self.status_field = QComboBox()
		self.status_field.addItems(status_options)
		self.status_field.setCurrentIndex({status: index for index, status in enumerate(status_options)}[delivery_data['Status']])
		self.buyer_address_field = QLineEdit(delivery_data['Buyer Address'])
		self.store_name_field = QLineEdit(delivery_data['Store Name'])

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


		items_query = "SELECT I.item_name as 'item_name', SI.quantity as 'quantity' FROM item I, selectitem SI WHERE I.item_id = SI.item_id and SI.order_id = {};".format(self.order_id) 
		cursor.execute(items_query)
		items = cursor.fetchall()

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

		back_button = QPushButton('Back')
		self.update_button = QPushButton('Update Status')
		self.update_button.setEnabled(False)

		back_button.clicked.connect(self.back)
		self.update_button.clicked.connect(self.update_status)

		grid_layout = QGridLayout()
		grid_layout.addWidget(group_box1, 0, 0)
		grid_layout.addWidget(group_box2, 0, 1)
		grid_layout.addWidget(back_button, 1, 0)
		grid_layout.addWidget(self.update_button, 1, 1)

		self.current_status = delivery_data['Status']

		self.status_field.currentIndexChanged.connect(self.changed_status)

		self.setLayout(grid_layout)

	def changed_status(self):
		if self.status_field.currentText() != self.current_status:
			self.update_button.setEnabled(True)

	def back(self):
		self.assignments_window = Assignments(self.username)
		self.assignments_window.show()
		self.close()

	def update_status(self):
		status = self.status_field.currentText()
		if status == 'Delivered':
			new_status = 1
			time = datetime.datetime.now().strftime("%H:%M")
			date = datetime.datetime.now().strftime("%Y-%m-%d")
			update_status_query = "update deliveredBy set is_delivered = {}, delivery_time = '{}', delivery_date = '{}' where deliverer_username = '{}' and order_id = {}".format(new_status, time, date, self.username, self.order_id)
		if status == 'Pending':
			new_status = 0
			update_status_query = "update deliveredBy set is_delivered = {} where deliverer_username = '{}' and order_id = {}".format(new_status, self.username, self.order_id)
		cursor.execute(update_status_query)
		connection.commit()

		self.view_assnments = Assignments(self.username)
		self.view_assnments.show()
		self.close()

class ManagerFunctionality(QWidget):
	def __init__(self, username):
		super(ManagerFunctionality, self).__init__()
		self.setWindowIcon(QIcon('groceries.png'))
		self.setWindowTitle('Manager Functionality')

		self.username = username

		self.revenue_report = QPushButton('View Revenue Report')
		self.account_info_button = QPushButton('Account Information')
		self.view_orders_button = QPushButton('View Orders')
		self.view_inventory_button = QPushButton('View Inventory')
		self.back_button = QPushButton('Back')

		self.revenue_report.clicked.connect(self.accept_revenue_report)
		self.account_info_button.clicked.connect(self.accept_account_info)
		self.view_orders_button.clicked.connect(self.accept_view_orders)
		self.view_inventory_button.clicked.connect(self.accept_view_inventory)
		self.back_button.clicked.connect(self.accept_back)

		group_box = QGroupBox()
		grid = QGridLayout()

		grid.addWidget(self.revenue_report, 0, 0)
		grid.addWidget(self.account_info_button, 0, 1)
		grid.addWidget(self.view_orders_button, 1, 0)
		grid.addWidget(self.view_inventory_button, 1, 1)
		grid.addWidget(self.back_button, 2, 0)

		group_box.setLayout(grid)

		vbox = QVBoxLayout()
		vbox.addWidget(group_box)

		self.setLayout(vbox)
		self.setGeometry(740,200,500,100)

	def accept_revenue_report(self):
		self.rev_report = RevenueReport(self.username)
		self.rev_report.show()
		self.close()
	def accept_account_info(self):
		self.mgr_acct = ManagerAcctInfo(self.username)
		self.mgr_acct.show()
		self.close()
	def accept_view_orders(self):
		self.outstanding_orders = OutstandingOrders(self.username)
		self.outstanding_orders.show()
		self.close()
	def accept_view_inventory(self):
		self.view_inventory = Inventory(self.username)
		self.view_inventory.show()
		self.close()
	def accept_back(self):
		self.loginwindow = Login()
		self.loginwindow.show()
		self.close()

class RevenueReport(QWidget):
	def __init__(self, username):
		super(RevenueReport, self).__init__()
		self.setWindowTitle('Revenue Report')
		self.setWindowIcon(QIcon('groceries.png'))
		self.username = username

		store_info_query = "select sum(SI.quantity) as 'Number of Items Sold: ', sum(SI.quantity * (I.listed_price - I.wholesale_price)) as 'Total Profit: ', sum(SI.quantity * I.listed_price) as 'Total Revenue: ', GS.store_name as 'Store Name: '\
							from selectitem SI, item I, grocerystore GS, orderfrom OFR\
							where SI.item_id = I.item_id and GS.store_id = OFR.store_address_id and OFR.order_id = SI.order_id and OFR.order_id in (select ofr.order_id from orderfrom ofr, grocerystore gs, manages m where gs.store_id = ofr.store_address_id and m.store_address = gs.address_id and m.username = '{}');".format(self.username)
		cursor.execute(store_info_query)
		info = cursor.fetchone()

		if None in info.values():
			store_info_query = "select store_name as 'Store Name: ' from manages natural join grocerystore where store_address = address_id and username = '{}';".format(self.username)
			cursor.execute(store_info_query)
			info = cursor.fetchone()
			info['Number of Items Sold: '] = 0
			info['Revenue: '] = '$0'
			info['Profit: '] = '$0'

		layout = QGridLayout()
		for i, key in enumerate(info.keys()):
			row, col = divmod(i, 1)
			layout.addWidget(QLabel(str(key)), row, col)#, field)
			if key in ['Total Profit: ', 'Total Revenue: ']:
				layout.addWidget(QLabel('$' + str(info[key])), row, col + 1)
			else:
				layout.addWidget(QLabel(str(info[key])), row, col + 1)

		group_box = QGroupBox()
		group_box.setLayout(layout)

		back_button = QPushButton('Back')
		back_button.clicked.connect(self.back)

		vbox = QVBoxLayout()
		vbox.addWidget(group_box)
		vbox.addWidget(back_button)
		self.setLayout(vbox)

		self.setGeometry(740,200,400,100)

	def back(self):
		self.mgr_func = ManagerFunctionality(self.username)
		self.mgr_func.show()
		self.close()

class ManagerAcctInfo(QWidget):
	def __init__(self, username):
		super(ManagerAcctInfo, self).__init__()

		self.username = username
		self.setWindowIcon(QIcon('groceries.png'))
		self.setWindowTitle('Account Information')

		manager_info_query = "SELECT U.first_name, U.last_name, U.username, U.email, GS.store_name, CONCAT(A.house_number, ' ', A.street, ' ', A.city, ', ', A.state, ' ', A.zip_code) as 'store_address'\
							FROM userr U, manages M, grocerystore GS, address A\
							WHERE U.username = M.username and M.store_address = GS.address_id and GS.address_id = A.id and U.username = '{}';".format(self.username)
		store_phone_query = "select phone from manages natural join grocerystore where address_id = store_address and username = '{}';".format(self.username)

		cursor.execute(manager_info_query)
		manager_info = cursor.fetchone()
		cursor.execute(store_phone_query)
		store_phone = int(cursor.fetchone()['phone'])

		group_box = QGroupBox()
		grid = QGridLayout()

		self.first_name_field = QLineEdit(manager_info['first_name'])
		self.last_name_field = QLineEdit(manager_info['last_name'])
		self.username_field = QLineEdit(self.username)
		self.store_field = QLineEdit(manager_info['store_name'])
		self.store_address_field = QLineEdit(manager_info['store_address'])
		self.email_field = QLineEdit(manager_info['email'])
		self.store_phone_field = QLineEdit(str(store_phone))

		self.username_field.setEnabled(False)
		self.store_field.setEnabled(False)
		self.store_address_field.setEnabled(False)

		group_box1 = QGroupBox('Manager Account Information')
		grid = QGridLayout()

		grid.addWidget(QLabel('First Name: '), 0, 0)
		grid.addWidget(self.first_name_field, 0, 1)
		grid.addWidget(QLabel('Last Name: '), 0, 2)
		grid.addWidget(self.last_name_field, 0, 3)

		grid.addWidget(QLabel('Username: '), 1, 0)
		grid.addWidget(self.username_field, 1, 1)
		grid.addWidget(QLabel('Email: '), 1, 2)
		grid.addWidget(self.email_field, 1, 3)

		grid.addWidget(QLabel('Managed Grocery Store: '), 2, 0)
		grid.addWidget(self.store_field, 2, 1)
		grid.addWidget(QLabel('Grocery Store Address: '), 2, 2)
		grid.addWidget(self.store_address_field, 2, 3)

		grid.addWidget(QLabel('Store Phone Number: '), 3, 0)
		grid.addWidget(self.store_phone_field, 3, 1)


		group_box1.setLayout(grid)

		vbox_layout = QVBoxLayout()
		vbox_layout.addWidget(group_box1)

		group_box2 = QGroupBox()

		self.back_button= QPushButton('Back')
		self.delete_acct_button = QPushButton('Delete Account')
		self.update_button = QPushButton('Update')

		self.back_button.clicked.connect(self.back)
		self.delete_acct_button.clicked.connect(self.check_delete_acct)
		self.update_button.clicked.connect(self.update_info)

		hbox_layout = QHBoxLayout()
		hbox_layout.addWidget(self.back_button)
		hbox_layout.addWidget(self.delete_acct_button)
		hbox_layout.addWidget(self.update_button)

		group_box2.setLayout(hbox_layout)

		vbox_layout.addWidget(group_box2)

		self.setLayout(vbox_layout)
		self.setGeometry(600,150,900,100)

	def update_info(self):
		email = self.email_field.text()
		fname = self.first_name_field.text()
		lname = self.last_name_field.text()
		phone = self.store_phone_field.text()

		for field in [self.email_field.text(), self.first_name_field.text(), self.last_name_field.text(), self.store_phone_field.text()]:
			try:
				if len(field) == 0:
					msg = QMessageBox()
					msg.setIcon(QMessageBox.Information)
					msg.setWindowTitle('Buyer Information')
					msg.setText("Please complete all fields!")
					msg.setStandardButtons(QMessageBox.Ok)
					msg.exec_()
					return
			except:
				pass

		if len(fname) < fname_min_len:
			self.error_window = LoginMessage('first_name_length')
			self.error_window.show()
			return
		elif len(lname) < lname_min_len:
			self.error_window = LoginMessage('last_name_length')
			self.error_window.show()
			return
		elif not bool(re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)):
			self.error_window = LoginMessage('invalid_email')
			self.error_window.show()
			return
		elif len(phone) != 10 or not phone.isdigit():
			self.error_window = LoginMessage('phone')
			self.error_window.show()
			return	

		store_id_query = "select GS.store_id from grocerystore GS, manages M where GS.address_id = M.store_address and M.username = '{}';".format(self.username)
		cursor.execute(store_id_query)
		store_id = cursor.fetchone()['store_id']

		update_user = "update userr set first_name = '{}', last_name = '{}', email = '{}' where username = '{}';".format(fname, lname, email, self.username)
		update_store_phone = "update grocerystore set phone = {} where store_id = {};".format(phone, store_id)

		cursor.execute(update_store_phone)
		cursor.execute(update_user)
		connection.commit()

		update_msg = QMessageBox()
		update_msg.setIcon(QMessageBox.Information)
		update_msg.setWindowTitle('Manager Account Information')
		update_msg.setText("Information Updated!")
		update_msg.setStandardButtons(QMessageBox.Ok)
		update_msg.accepted.connect(self.back)
		update_msg.exec_()

	def back(self):
		self.deliverer_func = ManagerFunctionality(self.username)
		self.deliverer_func.show()
		self.close()

	def check_delete_acct(self):
		msg = QMessageBox()
		msg.setWindowTitle('Delete Account')
		msg.setText("Are you sure you want to delete your account?")
		msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		msg.accepted.connect(self.accept_delete_acct)
		msg.exec_()

	def accept_delete_acct(self):
		query = "delete from userr where username = '{}';".format(self.username)
		cursor.execute(query)
		connection.commit()
		self.login = Login()
		self.login.show()
		self.close()

class Inventory(QWidget):
	def __init__(self, username):
		super(Inventory, self).__init__()

		self.setWindowIcon(QIcon('groceries.png'))
		self.setWindowTitle('Inventory')
		self.username = username

		inventory_query = "SELECT I.item_name as 'Item Name', I.description as 'Description', I.quantity as 'Quantity', CONCAT('$' , I.listed_price) as 'Retail Price', CONCAT('$', I.wholesale_price) as 'Wholesale Price', I.exp_date as 'Expiration Date' FROM item I, soldat S, manages M, grocerystore GS WHERE I.item_id = S.item_id and M.store_address = GS.address_id and GS.store_id = S.store_id and M.username = '{}' GROUP BY I.item_id;".format(self.username)

		self.tabledata = tablemaker(inventory_query)
		column_headers = self.tabledata[0]
		self.rows = self.tabledata[1]

		self.table = QTableWidget(len(self.rows), len(self.rows[0]), self)
		self.table.horizontalHeader().setStretchLastSection(True)
		self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.table.verticalHeader().setStretchLastSection(True)
		self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

		self.back = QPushButton('Back')
		self.view_item = QPushButton('View Item')

		self.back.clicked.connect(self.accept_back)
		self.view_item.clicked.connect(self.accept_view_item)

		button_group_box = QGroupBox()
		hbox_layout = QHBoxLayout()

		hbox_layout.addWidget(self.back)
		hbox_layout.addWidget(self.view_item)

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

		self.view_item.setEnabled(False)
		self.setLayout(vbox_layout)
		self.setGeometry(700,200,800,600)

	def rowclicked(self):
		if self.rows != [['No Items Found.']]:
			self.view_item.setEnabled(True)

	def accept_back(self):
		self.mgr_func = ManagerFunctionality(self.username)
		self.mgr_func.show()
		self.close()

	def accept_view_item(self):
		indexes = self.table.selectionModel().selectedRows()
		for index in indexes:
			item_info = [self.table.item(index.row(),i).text() for i in range(self.table.columnCount())]
		
		self.view_item_window = ViewItem(item_info)
		self.view_item_window.show()

class ViewItem(QWidget):
	def __init__(self, item_info):
		super(ViewItem, self).__init__()
		self.setWindowIcon(QIcon('groceries.png'))
		self.setWindowTitle('Item Details')
		self.item_info = item_info

		group_box = QGroupBox()
		layout = QFormLayout()

		layout.addRow(QLabel('Item Name: '),QLabel(self.item_info[0].title()))
		layout.addRow(QLabel('Description: '), QLabel(self.item_info[1]))
		layout.addRow(QLabel('Quantity: '), QLabel(self.item_info[2]))
		layout.addRow(QLabel('Retail Price: '), QLabel(self.item_info[3]))
		layout.addRow(QLabel('Wholesale Price: '), QLabel(self.item_info[4]))
		layout.addRow(QLabel('Expiration Date: '), QLabel(self.item_info[5]))

		group_box.setLayout(layout)

		vbox = QVBoxLayout()
		vbox.addWidget(group_box)

		self.back_button = QPushButton('Back')
		self.back_button.clicked.connect(self.close)
		vbox.addWidget(self.back_button)

		self.setLayout(vbox)
		self.setGeometry(800,300,300,200)

class OutstandingOrders(QWidget):
	def __init__(self, username):
		super(OutstandingOrders, self).__init__()
		self.username = username
		self.setWindowTitle('Outstanding Orders')
		self.setWindowIcon(QIcon('groceries.png'))

		self.query  = "SELECT store_name, store_address, order_id, date, total_price, total_items, delivery_address\
						FROM(\
						SELECT o.order_id, gs.store_name, CONCAT(ag.house_number, ' ', ag.street, ' ', ag.city, ', ', ag.state, ' ', ag.zip_code) AS 'store_address', CONCAT(ab.house_number, ' ', ab.street, ' ', ab.city, ', ', ab.state, ' ', ab.zip_code) AS 'delivery_address', O.order_placed_date as 'date' \
						FROM orderr o, deliveredby db, orderFROM ofr, grocerystore gs, manages m, address ab, address ag, orderedby ob, buyer b\
						WHERE db.is_delivered = 0 AND o.order_id = db.order_id AND o.order_id = ofr.order_id AND ofr.store_address_id = gs.store_id AND m.store_address = gs.address_id AND gs.address_id = ag.id AND ob.order_id = o.order_id AND ob.buyer_username = b.username AND ab.id = b.address_id AND m.username = '{}'\
						) A NATURAL JOIN\
						(SELECT O.order_id, sum(SI.quantity * I.listed_price) AS 'total_price', sum(SI.quantity) AS 'total_items'\
						FROM orderr O, selectitem SI, item I\
						WHERE O.order_id = SI.order_id and SI.item_id = I.item_id \
						group by O.order_id) B;".format(self.username)


		self.tabledata = tablemaker(self.query)
		column_headers = self.tabledata[0]
		rows = self.tabledata[1]

		self.table = QTableWidget(len(rows), len(rows[0]), self)
		self.table.horizontalHeader().setStretchLastSection(True)
		self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.table.verticalHeader().setStretchLastSection(True)
		self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

		self.back = QPushButton('Back')

		self.back.clicked.connect(self.accept_back)

		button_group_box = QGroupBox()
		hbox_layout = QHBoxLayout()

		hbox_layout.addWidget(self.back)

		button_group_box.setLayout(hbox_layout)

		self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

		self.table.setHorizontalHeaderLabels(column_headers)
		for i, row in enumerate(rows):
		    for j, field in enumerate(row):
		        item = QTableWidgetItem(field)
		        self.table.setItem(i, j, item)

		vbox_layout = QVBoxLayout()
		vbox_layout.addWidget(self.table)
		vbox_layout.addWidget(button_group_box)

		self.setLayout(vbox_layout)
		self.setGeometry(500,100,1200,800)

	def accept_back(self):
		self.mgr_func = ManagerFunctionality(self.username)
		self.mgr_func.show()
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
