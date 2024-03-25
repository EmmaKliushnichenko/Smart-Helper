from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QButtonGroup
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QFont
from HomePage import HomePage

class RegistrationPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Registration')
        self.setGeometry(100, 100, 375, 812)

        layout = QVBoxLayout(self)

        # Title Label
        title_label = QLabel('Give us some basic information:', self)
        title_label.setFont(QFont('Arial', 24, QFont.Bold))
        title_label.setStyleSheet('color: #061428;')
        layout.addWidget(title_label)

        # Name Input
        name_label = QLabel('Name', self)
        name_label.setFont(QFont('Arial', 20))
        layout.addWidget(name_label)

        self.name_input = QLineEdit(self)
        self.name_input.setFont(QFont('Arial', 16))
        layout.addWidget(self.name_input)

        # Gender Selection
        gender_label = QLabel('Gender', self)
        gender_label.setFont(QFont('Arial', 20))
        layout.addWidget(gender_label)

        self.gender_combobox = QComboBox(self)
        gender_options = [ "Male", "Female", "Prefer not to say", "Other"]
        self.gender_combobox.addItems(gender_options)
        self.gender_combobox.setFont(QFont('Arial', 14))
        layout.addWidget(self.gender_combobox)


        # Height Input
        height_label = QLabel('Height (cm)', self)
        height_label.setFont(QFont('Arial', 20))
        layout.addWidget(height_label)

        self.height_input = QLineEdit(self)
        self.height_input.setFont(QFont('Arial', 14))
        layout.addWidget(self.height_input)

        # Weight Input
        weight_label = QLabel('Weight (kg)', self)
        weight_label.setFont(QFont('Arial', 20))
        layout.addWidget(weight_label)

        self.weight_input = QLineEdit(self)
        self.weight_input.setFont(QFont('Arial', 14))
        layout.addWidget(self.weight_input)

        # Registration Button
        self.register_button = QPushButton('Continue', self)
        self.register_button.setFont(QFont('Arial', 14))
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

    def register(self):
        # Get the values from the input fields
        name = self.name_input.text()
        height = self.height_input.text()
        weight = self.weight_input.text()
        gender = self.gender_combobox.currentText()

        # After registration, create and show the HomePage with the new user's information
        self.home_page = HomePage(user_name=name, weight=weight, height=height)
        self.home_page.show()
        self.close()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { background-color: #E8EBF0; }")
    registration = RegistrationPage()
    registration.show()
    sys.exit(app.exec_())
