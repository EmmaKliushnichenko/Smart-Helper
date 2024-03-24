import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton, QDialog, QSpinBox, QGridLayout, QComboBox, QMessageBox

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

from CommunityPage import HealthInfoPage

class MealButton(QWidget):
    def __init__(self, text, icon_path, parent=None):
        super().__init__(parent)
        self.text = text
        self.icon_path = icon_path
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.button = QPushButton(self.text)
        self.button.setIcon(QIcon(self.icon_path))
        self.button.setIconSize(QSize(64, 64))
        self.button.clicked.connect(self.on_click)

        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def on_click(self):
        dialog = MealInfoDialog(self.text, self)
        dialog.exec_()

class MealInfoDialog(QDialog):
    def __init__(self, meal_type, parent=None):
        super().__init__(parent)
        self.meal_type = meal_type
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'{self.meal_type} - Meal Information')
        layout = QVBoxLayout()

        self.carbsInput = QSpinBox()
        self.carbsInput.setRange(0, 1000)
        self.insulinInput = QSpinBox()
        self.insulinInput.setRange(0, 100)

        saveButton = QPushButton("Save")
        saveButton.clicked.connect(self.save_data)

        layout.addWidget(QLabel("Carbs (g):"))
        layout.addWidget(self.carbsInput)
        layout.addWidget(QLabel("Insulin (units):"))
        layout.addWidget(self.insulinInput)
        layout.addWidget(saveButton)

        self.setLayout(layout)

    def save_data(self):
        carbs = self.carbsInput.value()
        insulin = self.insulinInput.value()

        QMessageBox.information(self, "Data Saved", f"Information for {self.meal_type} saved:\nCarbs: {carbs}g\nInsulin: {insulin} units")
        self.accept()

class CarbsLogEntry(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        self.carbsGoalInput = QSpinBox()
        self.carbsGoalInput.setMaximum(500)
        self.setGoalButton = QPushButton("Set Daily Carbs Goal")
        self.setGoalButton.clicked.connect(self.setCarbsGoal)

        self.adviceButton = QPushButton("Get Advice")
        self.adviceButton.clicked.connect(self.showAdvice)

        layout.addWidget(QLabel("Daily Carbs Goal:"))
        layout.addWidget(self.carbsGoalInput)
        layout.addWidget(self.setGoalButton)
        layout.addWidget(self.adviceButton)

        self.setLayout(layout)

    def setCarbsGoal(self):
        goal = self.carbsGoalInput.value()
        QMessageBox.information(self, "Goal Set", f"Your daily carbs goal is set to {goal}g.")

    def showAdvice(self):
        QMessageBox.information(self, "Advice", "Remember, balance is key to a healthy diet!")

class ActivityLogEntry(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        self.activityComboBox = QComboBox()
        self.activityComboBox.addItems(["Meditation", "Running", "Cycling", "Jogging"])
        self.logActivityButton = QPushButton("Enter Activity")
        self.logActivityButton.clicked.connect(self.logActivity)

        layout.addWidget(QLabel("Activity:"))
        layout.addWidget(self.activityComboBox)
        layout.addWidget(self.logActivityButton)

        self.setLayout(layout)

    def logActivity(self):
        activity = self.activityComboBox.currentText()
        QMessageBox.information(self, "Great Job!", f"You are cool and great for completing: {activity}!")

class DiaryPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Diary - Diabetes Management App')
        self.setGeometry(100, 100, 375, 812)

        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)

        self.carbsLogEntry = CarbsLogEntry()
        main_layout.addWidget(self.carbsLogEntry)

        self.activityLogEntry = ActivityLogEntry()
        main_layout.addWidget(self.activityLogEntry)

        self.meals_layout = self.create_meals_layout()
        main_layout.addLayout(self.meals_layout)

        self.navigation_panel = self.create_navigation_panel()
        main_layout.addLayout(self.navigation_panel)

        self.setCentralWidget(central_widget)

    def create_meals_layout(self):
        layout = QGridLayout()

        meals = [
            ("Breakfast", "breakfast_icon.png"),
            ("Lunch", "lunch_icon.png"),
            ("Snack", "snack_icon.png"),
            ("Dinner", "dinner_icon.png"),
            ("Before Meal", "before_meal_icon.png"),
            ("After Meal", "after_meal_icon.png")
        ]

        row, col = 0, 0
        for meal, icon in meals:
            meal_button = MealButton(meal, icon, self)
            layout.addWidget(meal_button, row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1

        return layout

    def create_navigation_panel(self):
        panel_layout = QHBoxLayout()

        # Assuming other buttons are correctly set up and connected
        home_button = self.create_nav_button('Home', 'home.png')
        diary_button = self.create_nav_button('Diary', 'diary.png')
        stats_button = self.create_nav_button('Statistics', 'statistics.png')
        more_button = self.create_nav_button('More', 'more.png')

        # Create and set up the community button
        community_button = self.create_nav_button('Community', 'community.png')
        community_button.clicked.connect(self.show_community)

        # Add buttons to the panel layout
        panel_layout.addWidget(home_button)
        panel_layout.addWidget(diary_button)
        panel_layout.addWidget(community_button)
        panel_layout.addWidget(stats_button)
        panel_layout.addWidget(more_button)

        return panel_layout

    def show_community(self):
        if not hasattr(self, 'community_page'):
            self.community_page = HealthInfoPage()
        self.community_page.show()
        self.close()

    def create_nav_button(self, title, icon_path):
        button = QPushButton(title)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(24, 24))
        return button

    def open_log_entry_dialog(self, meal_type):
        dialog = LogEntryDialog(meal_type, self)
        dialog.exec_()


class LogEntryDialog(QDialog):
    def __init__(self, meal_type, parent=None):
        super().__init__(parent)
        self.meal_type = meal_type
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'Log Entry - {self.meal_type}')
        layout = QVBoxLayout()

        label = QLabel(f"You clicked on the {self.meal_type} button!")
        layout.addWidget(label)

        self.setLayout(layout)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { background-color: #E8EBF0; }")
    ex = DiaryPage()
    ex.show()
    sys.exit(app.exec_())
