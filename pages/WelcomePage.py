from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QRadioButton, QButtonGroup, QHBoxLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QTransform
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsRotation
from RegistrationPage import RegistrationPage  # This line imports RegistrationPage
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsRotation
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTransform

class WelcomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Welcome to Smart Helper')
        self.setGeometry(100, 100, 375, 812)  # Width x Height

        # Welcome message
        self.welcome_label = QLabel('Welcome to your personal\nSmart Helper', self)
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setFont(QFont('DM Sans', 28, QFont.Bold))
        self.welcome_label.setStyleSheet("color: #061428; line-height: 47px;")
        self.welcome_label.setGeometry(10, 100, 355, 200)  # Adjust the geometry to center the text
        self.welcome_label.setWordWrap(True)

        # Arrow button
        self.arrow_button = QPushButton(self)
        arrow_icon = QIcon(r"C:\\Users\\edkly\\Downloads\\pic.png")
        self.arrow_button.setIcon(arrow_icon)
        icon_size = QSize(100, 100)
        self.arrow_button.setIconSize(icon_size)
        button_size = QSize(icon_size.width() + 20, icon_size.height() + 20)
        self.arrow_button.setFixedSize(button_size)
        self.arrow_button.setStyleSheet("background-color: transparent; border: none;")
        button_x = int(self.width() - button_size.width() - 30)  # Ensure button_x is an integer
        button_y = int((self.height() - button_size.height()) / 1.5)  # Convert button_y to an integer
        self.arrow_button.move(button_x, button_y)
        self.arrow_button.clicked.connect(self.go_to_registration)

    def go_to_registration(self):
        # This function will be called when the arrow button is clicked
        self.registration_window = RegistrationPage()
        self.registration_window.show()
        self.close()  # Close the welcome page

# Example usage
if __name__ == '__main__':
    import sys
    import sys

    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { background-color: #E8EBF0; }")
    welcome_page = WelcomePage()
    welcome_page.show()
    sys.exit(app.exec_())