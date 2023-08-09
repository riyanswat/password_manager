import sys
import re
import json
import random
import string
import pyperclip as pc
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QFont

class PasswordManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Manager")
        self.initUI()
        self.PASSWORD_LENGTH = 8

    def initUI(self):
        # Widgets
        self.website_label = QLabel("Website:")
        self.website_label.setFont(QFont("Arial", 12))
        self.website_entry = QLineEdit()
        self.website_entry.setFont(QFont("Arial", 12))

        self.email_label = QLabel("Email/ Username:")
        self.email_label.setFont(QFont("Arial", 12))
        self.email_entry = QLineEdit()
        self.email_entry.setFont(QFont("Arial", 12))
        self.email_entry.setText("your_email@gmail.com")

        self.password_label = QLabel("Password:")
        self.password_label.setFont(QFont("Arial", 12))
        self.password_entry = QLineEdit()
        self.password_entry.setFont(QFont("Arial", 12))

        # Buttons
        self.generate_button = QPushButton("Generate")
        self.generate_button.setFont(QFont("Arial", 10))
        self.add_button = QPushButton("Add")
        self.add_button.setFont(QFont("Arial", 10))
        self.search_button = QPushButton("Search")
        self.search_button.setFont(QFont("Arial", 10))
        self.delete_button = QPushButton("Delete password")
        self.delete_button.setFont(QFont("Arial", 10))

        self.setFixedSize(300, 300)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.website_label)
        layout.addWidget(self.website_entry)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_entry)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_entry)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.add_button)
        layout.addWidget(self.search_button)
        layout.addWidget(self.delete_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # connecting functions
        self.generate_button.clicked.connect(self.generate_password)
        self.add_button.clicked.connect(self.add_data)
        self.search_button.clicked.connect(self.find_password)
        self.delete_button.clicked.connect(self.delete_data)

    def generate_password(self):
        nums = [*string.digits]
        letters = [*string.ascii_letters]
        symbols = [*"!@#$%\/"]

        password = []
        for _ in range(self.PASSWORD_LENGTH):
            password.append(random.choice(nums + letters + symbols))

        random.shuffle(password)
        final_pass = "".join(password)
        self.password_entry.setText(final_pass)
        pc.copy(final_pass)


    def add_data(self):
        website = self.website_entry.text().lower()
        email = self.email_entry.text()
        password = self.password_entry.text()

        if not website or \
                not password or \
                re.search('^\s+$', website) or \
                re.search('^\s+|\s+$', website) or \
                re.search('^\s+$', email) or \
                re.search('^\s+$', password):
            QMessageBox.critical(
                self, "Oops", "You've left one or more of the fields empty")
            self.website_entry.clear()
            self.password_entry.clear()
        else:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                data = {}

            data[website] = {
                "email": email,
                "password": password
            }

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

            QMessageBox.information(
                self, "Success", f"You've successfully added {website}!")

            self.website_entry.clear()
            self.password_entry.clear()

    def delete_data(self):
        website = self.website_entry.text().lower()

        if re.search('^\s+$', website) or (not website):
            QMessageBox.information(
                self,
                "Oops",
                "You've left the website field empty"
            )
            return

        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            QMessageBox.critical(
                self,
                "Error",
                "Data file not found."
            )
            self.website_entry.clear()
            return

        if website in data:
            del data[website]
            QMessageBox.information(
                self,
                "Success",
                f"You've successfully deleted {website}!"
            )
        else:
            QMessageBox.critical(
                self,
                "Error",
                f"{website} not found in the saved websites!"
            )

        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)

        self.website_entry.clear()
        self.password_entry.clear()


    def find_password(self):
        website = self.website_entry.text()

        try:
            with open("data.json") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            QMessageBox.critical(
                self,
                "Error",
                "No data file found"
            )
        else:
            if website in data:
                email = data[website]['email']
                password = data[website]['password']
                QMessageBox.information(
                    self,
                    website,
                    f"Email: {email}\nPassword: {password}"
                )
            elif re.search("^\s+$", website):
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Please enter a valid website name."
                )
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"No details for {website} exist."
                )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordManager()
    window.show()
    sys.exit(app.exec())
