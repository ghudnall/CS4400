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
		self.confirm_pass = self.confirm_pass_field.text()
		self.fname = self.first_name_field.text()
		self.lname = self.last_name_field.text()
		self.email = self.email_field.text()
		self.address = self.address_field.text()
		self.state = self.state_field.currentText()
		self.city = self.city_field.text()
		self.phone = self.phone_field.text()
		self.zip = self.zip_field.text()

		try:
			if len(self.fname) < 2:
				self.error_window = LoginMessage('fname_length')
				self.error_window.show()
				return
			elif len(self.lname) < 2:
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




			cursor = connection.cursor()
			check_query = "select * from buyer where username = '{}'".format(self.username)  #check to see if username already exists
			cursor.execute(check_query)

			existing_user_row_count = cursor.rowcount
			if existing_user_row_count != 0:
				self.error_window = LoginMessage('existing_user')
				self.error_window.show()
				return

			add_info = "insert into buyer values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(self.fname, self.lname, self.username, self.phone, self.password, self.email, self.state, self.address, self.zip, self.city)
						
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
