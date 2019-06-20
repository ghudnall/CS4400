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
                                         db= 'zoo',
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

		if len(self.username) >= 6 and len(self.password) >= 6:
			username_query = "SQL QUERY CHECK FOR USERNAME"
			print(username_query)
			username_query = "select * from MEMBER where username = '{}';".format(self.username)
			cursor.execute(username_query)			#check only if username exists. If it does not, open LoginMessage and say user DNE
			user_row_count = cursor.rowcount
			
			password_query = "SQL QUERY CHECK FOR MATCHING PASSWORD"
			print(password_query)
			password_query = "select * from MEMBER where PASSWORD = '{}' and USERNAME = '{}';".format(self.password, self.username)

			cursor.execute(password_query)
			password_row_count = cursor.rowcount

			if user_row_count == 0: #if 0 rows affected by username check, throw username DNE window
				self.error_window = LoginMessage('wrong_user')
				self.error_window.show()
			elif password_row_count == 0: #elif 0 rows affected by password check, throw incorrect pass window
				self.error_window = LoginMessage('wrong_password')
				self.error_window.show()
			else: #else open next window. username/password correct
				self.open_buyer_window = BuyerFunctionality(self.username)
				self.open_buyer_window.show()
				self.close()

		elif len(self.username) < 6: #username must be longer than 6 characters
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
        					  'user_length': 'Username must be between 6 and 18 characters.', 'pass_length': 'Password must be between 6 and 18 characters',
        					  'fname_length': 'First name must be greater than 2 characters', 'lname_length': 'Last name must be greater than 2 characters',
        					  'existing_user': 'Username already exists. Please choose a different username.', 'invalid_user' : 'Please enter a valid username.', 
        					  'invalid_pass' : 'Please enter a valid password.', 'pass_mismatch': 'Passwords don\'t match.', 'pass_changed': 'Password changed.',
        					  'invalid_email': 'Please enter a valid email address.'}

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

		self.register_button = QPushButton('Register')
		self.cancel_button = QPushButton('    Cancel    ')
		self.register_button.clicked.connect(self.accept)
		self.cancel_button.clicked.connect(self.reject)
		self.register_button.setEnabled(False)

		group_box1 = QGroupBox('Buyer Information')
		group_box2 = QGroupBox(' ')

		self.layout1 = QFormLayout()
		self.layout1.addRow(QLabel('First Name:'), self.first_name_field)
		self.layout1.addRow(QLabel('Username:'), self.username_field)
		self.layout1.addRow(QLabel('Password:'),self.password_field)
		self.layout1.addRow(QLabel('Email: '), self.email_field)
		self.layout1.addRow(QLabel('Address: '), self.address_field)
		self.layout1.addRow(QLabel('City: '), self.city_field)

		self.layout2 = QFormLayout()
		self.layout2.addRow(QLabel('Last Name:'),self.last_name_field)
		self.layout2.addRow(QLabel('Phone Number: '), self.phone_field)
		self.layout2.addRow(QLabel('Confirm Password'), self.confirm_pass_field)
		self.layout2.addRow(QLabel('State: '), self.state_field)
		self.layout2.addRow(QLabel('Zip Code: '), self.zip_field)


		#enable ok button only when all fields have been filled
		self.first_name_field.textChanged.connect(self.on_text_changed)
		self.username_field.textChanged.connect(self.on_text_changed)
		self.password_field.textChanged.connect(self.on_text_changed)
		self.email_field.textChanged.connect(self.on_text_changed)
		self.address_field.textChanged.connect(self.on_text_changed)
		self.city_field.textChanged.connect(self.on_text_changed)
		self.last_name_field.textChanged.connect(self.on_text_changed)
		self.phone_field.textChanged.connect(self.on_text_changed)
		self.confirm_pass_field.textChanged.connect(self.on_text_changed)
		# self.state_field.textChanged.connect(self.on_text_changed)
		self.zip_field.textChanged.connect(self.on_text_changed)
		
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
		fields = [bool(self.first_name_field.text()), bool(self.username_field.text()), bool(self.password_field.text()), bool(self.email_field.text()), bool(self.address_field.text()), bool(self.city_field.text()), bool(self.last_name_field.text()), bool(self.phone_field.text()), bool(self.confirm_pass_field.text()), bool(self.zip_field.text())]
		self.register_button.setEnabled(sum(fields) == len(fields))


	def accept(self):
		self.username = self.username_field.text()
		self.password = self.password_field.text()
		self.first_name = self.first_name_field.text()
		self.last_name = self.last_name_field.text()

		self.user_type = 'member'

		try:
			if len(self.first_name) < 2:
				self.error_window = LoginMessage('fname_length')
				self.error_window.show()
				return
			elif len(self.last_name) < 2:
				self.error_window = LoginMessage('lname_length')
				self.error_window.show()
				return
			elif len(self.username) < 6:
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
			elif not bool(re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email_field.text())):
				self.error_window = LoginMessage('invalid_email')
				self.error_window.show()
				return


			account_type = 'member'

			cursor = connection.cursor()
			check_query = "select * from {} where username = '{}'".format(account_type, self.username)  #check to see if username already exists
			cursor.execute(check_query)

			existing_user_row_count = cursor.rowcount
			if existing_user_row_count != 0:
				self.error_window = LoginMessage('existing_user')
				self.error_window.show()
				return
			if account_type == 'member':
				add_info = "insert into {} values ('{}', ('{}'), '{}', '{}');".format(account_type, self.username, self.password, self.first_name, self.last_name)
			elif account_type == 'employee':
				add_info = "insert into {} values ('{}', ('{}'), '{}', '{}', '{}');".format(account_type, self.username, self.password, self.first_name, self.last_name, self.cb_job_function.currentText())

			cursor.execute(add_info)
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
		self.first_name = self.first_name_field.text()
		self.last_name = self.last_name_field.text()

		self.user_type = 'member'

		try:
			if len(self.first_name) < 2:
				self.error_window = LoginMessage('fname_length')
				self.error_window.show()
				return
			elif len(self.last_name) < 2:
				self.error_window = LoginMessage('lname_length')
				self.error_window.show()
				return
			elif len(self.username) < 6:
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
			elif not bool(re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email_field.text())):
				self.error_window = LoginMessage('invalid_email')
				self.error_window.show()
				return

			account_type = 'member'

			cursor = connection.cursor()
			check_query = "select * from {} where username = '{}'".format(account_type, self.username)  #check to see if username already exists
			cursor.execute(check_query)

			existing_user_row_count = cursor.rowcount
			if existing_user_row_count != 0:
				self.error_window = LoginMessage('existing_user')
				self.error_window.show()
				return
			if account_type == 'member':
				add_info = "insert into {} values ('{}', ('{}'), '{}', '{}');".format(account_type, self.username, self.password, self.first_name, self.last_name)
			elif account_type == 'employee':
				add_info = "insert into {} values ('{}', ('{}'), '{}', '{}', '{}');".format(account_type, self.username, self.password, self.first_name, self.last_name, self.cb_job_function.currentText())

			cursor.execute(add_info)
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
	
		store_query = "select username from member"
		cursor.execute(store_query)
		store_list = [entry['username'] for entry in cursor.fetchall()]
		self.cb_assign_store = QComboBox()  #add list to drop down
		self.cb_assign_store.addItems(sorted(store_list))
		self.cb_assign_store.setToolTip('Select a Store')

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
		self.layout2.addRow(QLabel('Select a Store: '), self.cb_assign_store)

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
		self.first_name = self.first_name_field.text()
		self.last_name = self.last_name_field.text()

		self.user_type = 'member'

		try:
			if len(self.first_name) < 2:
				self.error_window = LoginMessage('fname_length')
				self.error_window.show()
				return
			elif len(self.last_name) < 2:
				self.error_window = LoginMessage('lname_length')
				self.error_window.show()
				return
			elif len(self.username) < 6:
				self.error_window = LoginMessage('user_length')
				self.error_window.show()
				return
			elif len(self.password) < 6:
				self.error_window = LoginMessage('pass_length')
				self.error_window.show()
				return
			elif not bool(re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email_field.text())):
				self.error_window = LoginMessage('invalid_email')
				self.error_window.show()
				return

			account_type = 'member'

			cursor = connection.cursor()
			check_query = "select * from {} where username = '{}'".format(account_type, self.username)  #check to see if username already exists
			cursor.execute(check_query)

			existing_user_row_count = cursor.rowcount
			if existing_user_row_count != 0:
				self.error_window = LoginMessage('existing_user')
				self.error_window.show()
				return
			if account_type == 'member':
				add_info = "insert into {} values ('{}', ('{}'), '{}', '{}');".format(account_type, self.username, self.password, self.first_name, self.last_name)
			elif account_type == 'employee':
				add_info = "insert into {} values ('{}', ('{}'), '{}', '{}', '{}');".format(account_type, self.username, self.password, self.first_name, self.last_name, self.cb_job_function.currentText())

			cursor.execute(add_info)
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

		self.query  = "select username, password, first_name as 'First Name', last_name as 'Last Name' from member;"
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
			store_id = [self.table.item(index.row(),i).text() for i in range(self.table.columnCount())]
			# store_id = [self.table.item(index.row(), "COLUMN INDEX OF STORE NAME")]

		store_id = 'publix'
		self.store_homepage = StoreHomepage(self.username, store_id)
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

		self.query  = "select username, password, first_name as 'First Name', last_name as 'Last Name' from member;"
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

		self.table.SelectionBehavior(QAbstractItemView.SelectRows)
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

		self.add_to_cart.setEnabled(False)
		self.setLayout(vbox_layout)
		self.setGeometry(740,200,500,200)

	def rowclicked(self):
		self.add_to_cart.setEnabled(True)

	def accept_back(self):
		self.buyer_func = BuyerFunctionality(self.username)
		self.buyer_func.show()
		self.close()

	def accept_prev(self):
		print('PREVIOUS')

	def accept_next(self):
		print("NEXT")

	def accept_add_to_cart(self):
		indexes = self.table.selectionModel().selectedRows()
		for index in indexes:
			store_id = [self.table.item(index.row(),i).text() for i in range(self.table.columnCount())]
			# store_id = [self.table.item(index.row(), "COLUMN INDEX OF STORE NAME")]

		print("ADD THAT SHIT+-")

class Cart(QWidget):
	def __init__(self, username, store_id, order_id):
		super(Cart, self).__init__()
		self.setWindowTitle('Cart')
		self.setWindowIcon(QIcon('groceries.png'))
		self.username = username
		self.order_id = order_id
		self.store_id = store_id

		self.query  = "select username, password, first_name as 'First Name', last_name as 'Last Name' from member;"
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
		self.delete_item = QPushButton('Delete Item')

		self.back.clicked.connect(self.accept_back)
		self.previous.clicked.connect(self.accept_prev)
		self.next.clicked.connect(self.accept_next)
		self.delete_item.clicked.connect(self.accept_delete_item)

		button_group_box = QGroupBox()
		hbox_layout = QHBoxLayout()

		hbox_layout.addWidget(self.back)
		hbox_layout.addWidget(self.previous)
		hbox_layout.addWidget(self.next)
		hbox_layout.addWidget(self.delete_item)

		button_group_box.setLayout(hbox_layout)

		self.table.SelectionBehavior(QAbstractItemView.SelectRows)
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
			store_id = [self.table.item(index.row(),i).text() for i in range(self.table.columnCount())]
			# store_id = [self.table.item(index.row(), "COLUMN INDEX OF STORE NAME")]

		print("Delete Item")
		

class BuyerAcctInfo(QWidget):
	def __init__(self, username):
		super(BuyerAcctInfo, self).__init__()

		self.username = username
		self.setWindowIcon(QIcon('groceries.png'))
		self.setWindowTitle('Account Information')

		fname_query = "select first_name, last_name from MEMBER where username = '{}'".format(self.username)
		cursor = connection.cursor()
		cursor.execute(fname_query)
		name = cursor.fetchone()

		self.first_name_field = QLineEdit(name['first_name'])
		self.username_field = QLineEdit(self.username)
		self.preferred_store = QLineEdit()
		self.store_address = QLineEdit()
		self.email_field = QLineEdit()
		self.prefered_card = QLineEdit()
		self.address_field = QLineEdit()
		self.city_field = QLineEdit()

		self.last_name_field = QLineEdit(name['last_name'])
		self.phone_field = QLineEdit()
		self.state_field = QLineEdit()
		self.zip_field = QLineEdit()

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
		print("UPDATE BUYER INFO")

	def reject(self):
		self.buyer_func = BuyerFunctionality(self.username)
		self.buyer_func.show()
		self.close()

	def check_delete_acct(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		msg.setWindowTitle('Delete Account')
		msg.setText("Are you sure you want to delete your account?")
		msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		msg.accepted.connect(self.accept_delete_acct)
		msg.exec_()

	def accept_delete_acct(self):
		query = "delete from MEMBER where username = '{}';".format(self.username)
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
		self.query  = "select username, password, first_name as 'First Name', last_name as 'Last Name' from member;"

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
		self.query  = "select username, password, first_name as 'First Name', last_name as 'Last Name' from member;"

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
		self.setGeometry(740,200,500,200)

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
	column_headers = [str(k) for k in first_row]
	rows.append([str(v).strip() for v in first_row.values()])
	for row in cursor:
		rows.append([str(v).strip() for v in row.values()])
	return (column_headers, rows)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    # main = Example('gavin')
    # main.show()
    login = DbLogin()
    sys.exit(app.exec_())