import csv
import os
import logging
from win10toast import ToastNotifier

from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, \
    QWidget, QProgressBar, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout

from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget

from PyQt5.QtWidgets import QDateTimeEdit
from PyQt5.QtCore import QDateTime
from PyQt5.QtCore import QThread
from win10toast import ToastNotifier

from PyQt5.QtCore import QTime, QTimer, pyqtSignal
from PyQt5.QtCore import QTime  # Import QTime from QtCore, not QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QProgressBar, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout, QDialog, QFormLayout, QLineEdit, QVBoxLayout, QTimeEdit  # Ensure QTimeEdit is imported from QtWidgets


from PyQt5.QtCore import Qt, QSize
from PyQt5.QtCore import QTime
from PyQt5.QtGui import QColor, QPalette, QIcon


from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QVBoxLayout

from StatisticsPage import StatisticsPage


class NotificationThread(QThread):
    def __init__(self, title, message, duration):
        QThread.__init__(self)
        self.title = title
        self.message = message
        self.duration = duration

    def run(self):
        toaster = ToastNotifier()
        toaster.show_toast(self.title, self.message, duration=self.duration)

class TimePickerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Set Alarm')
        layout = QVBoxLayout(self)

        self.timeEdit = QTimeEdit(self)
        self.timeEdit.setTime(QTime.currentTime())
        layout.addWidget(self.timeEdit)

        self.setButton = QPushButton('Set Alarm', self)
        self.setButton.clicked.connect(self.accept)
        layout.addWidget(self.setButton)

    def selected_time(self):
        return self.timeEdit.time()

class HomePage(QMainWindow):
    def __init__(self, user_name, weight=None, height=None):
        super().__init__()
        self.user_name = user_name
        self.weight = weight
        self.height = height
        self.stats_page = None
        self.community_page = None
        self.diary_page = None
        self.more_page = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Diabetes Management App')
        self.setGeometry(100, 100, 375, 812)

        central_widget = QWidget(self)
        self.metrics_grid = QGridLayout()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignTop)

        self.welcome_label = QLabel(f'Hello, {self.user_name}', self)
        self.welcome_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.welcome_label)

        main_layout.addLayout(self.metrics_grid)

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_last_glucose_value)
        self.update_timer.timeout.connect(self.update_last_insulin_value)
        self.update_timer.start(60000)  # Update every 60000 milliseconds (1 minute)

        if self.weight and self.height:
            self.weight_height_label = QLabel(f"Weight: {self.weight} kg, Height: {self.height} cm")
            self.metrics_grid.addWidget(self.weight_height_label, 6, 0, 1, 3)  # Span across all columns
        else:
            self.weight_height_label = QLabel("Weight/Height not set")
            self.metrics_grid.addWidget(self.weight_height_label, 6, 0, 1, 3)

        # Metric icons grid setup
        self.metrics_grid = QGridLayout()
        main_layout.addLayout(self.metrics_grid)

        # The health metric widgets
        self.last_glucose_label = self.create_metric_label('Last Glucose')
        self.last_insulin_label = self.create_metric_label('Last Insulin')

        self.glucose_progress = self.create_progress_bar()
        self.insulin_progress = self.create_progress_bar()

        # Adding metric labels and progress bars to the grid layout
        self.metrics_grid.addWidget(self.last_glucose_label, 0, 0)
        self.metrics_grid.addWidget(self.glucose_progress, 1, 0)
        self.metrics_grid.addWidget(self.last_insulin_label, 0, 1)
        self.metrics_grid.addWidget(self.insulin_progress, 1, 1)


        # Glucose Button
        self.glucose_button = QPushButton(QIcon('glucose.png'), "Glucose")
        self.glucose_button.setIconSize(QSize(50, 50))
        self.glucose_button.clicked.connect(self.open_glucose_entry)
        self.metrics_grid.addWidget(self.glucose_button, 3, 0)

        # Insulin Button
        self.insulin_button = QPushButton(QIcon('insulin.png'), "Insulin")
        self.insulin_button.setIconSize(QSize(50, 50))
        self.insulin_button.clicked.connect(self.open_insulin_entry)
        self.metrics_grid.addWidget(self.insulin_button, 3, 1)

        # Medication Button
        self.medication_button = QPushButton(QIcon('medication.png'), "Medication")
        self.medication_button.setIconSize(QSize(50, 50))
        self.medication_button.clicked.connect(self.open_medication_entry)
        self.metrics_grid.addWidget(self.medication_button, 3, 2)

        button_size = QSize(80, 80)

        # Ketone Button
        self.ketone_button = QPushButton(QIcon('ketone.png'), "Ketone")
        self.ketone_button.setIconSize(button_size)
        self.ketone_button.clicked.connect(self.open_ketone_entry)
        self.metrics_grid.addWidget(self.ketone_button, 4, 0)

        # Blood Ketone Button
        self.ketone_blood_button = QPushButton(QIcon('ketone_blood.png'), "Ketone (Blood)")
        self.ketone_blood_button.setIconSize(button_size)
        self.ketone_blood_button.clicked.connect(self.open_ketone_blood_entry)
        self.metrics_grid.addWidget(self.ketone_blood_button, 4, 1)

        # HbA1C Button
        self.hba1c_button = QPushButton(QIcon('hba1c.png'), "HbA1C")
        self.hba1c_button.setIconSize(button_size)
        self.hba1c_button.clicked.connect(self.open_hba1c_entry)
        self.metrics_grid.addWidget(self.hba1c_button, 4, 2)


        # Carbs Button
        self.carbs_button = QPushButton(QIcon('carbs.png'), "Carbs")
        self.carbs_button.setIconSize(button_size)
        self.carbs_button.clicked.connect(self.open_carbs_entry)
        self.metrics_grid.addWidget(self.carbs_button, 5, 0)

        # Blood Pressure Button
        self.blood_pressure_button = QPushButton(QIcon('blood_pressure.png'), "Blood Pressure")
        self.blood_pressure_button.setIconSize(button_size)
        self.blood_pressure_button.clicked.connect(self.open_blood_pressure_entry)
        self.metrics_grid.addWidget(self.blood_pressure_button, 5, 1)

        # Activity Button
        self.activity_button = QPushButton(QIcon('activity.png'), "Activity")
        self.activity_button.setIconSize(button_size)
        self.activity_button.clicked.connect(self.open_activity_entry)
        self.metrics_grid.addWidget(self.activity_button, 5, 2)


        main_layout.addStretch(1)

        # Bottom navigation panel setup
        self.navigation_panel = self.create_navigation_panel()
        main_layout.addLayout(self.navigation_panel)  # Add the navigation panel at the bottom

        # Set the main_layout as the layout for central_widget
        central_widget.setLayout(main_layout)

        # Alarm button setup
        self.alarm_button = QPushButton("Set Alarm for Next Medication")
        self.alarm_button.clicked.connect(self.set_medication_alarm)
        self.metrics_grid.addWidget(self.alarm_button, 1, 2)

        self.alarm_timer = QTimer(self)  # This timer will be used for the alarm
        self.alarm_timer.setSingleShot(True)  # The timer will only trigger once
        self.alarm_timer.timeout.connect(self.show_medication_reminder)

    def set_medication_alarm(self):
        dialog = TimePickerDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # For demonstration purposes, set the alarm to go off in 5 seconds
            seconds_until_alarm = 5

            # Start the timer with the milliseconds until the alarm should go off
            # Multiply seconds by 1000 to convert to milliseconds
            self.alarm_timer.start(seconds_until_alarm * 1000)

    def show_medication_reminder(self):
        notificationThread = NotificationThread("Medication Reminder", "It's time for your medication!", 10)
        # Start the thread
        notificationThread.start()

    def create_metric_label(self, text):
        # Create and return a QLabel object for health metrics
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)


    def open_hba1c_entry(self):
        dialog = HbA1CEntryDialog()
        if dialog.exec():
            hba1c_data = dialog.get_data()
            #self.update_hba1c_metric(hba1c_data['hba1c'])

    def open_carbs_entry(self):
        dialog = CarbsEntryDialog()
        if dialog.exec():
            carbs_data = dialog.get_data()
            #self.update_carbs_metric(carbs_data['carbs'])

    def open_weight_height_entry(self):
        # Presumably opens a dialog to enter or view weight/height
        pass

    def open_activity_entry(self):
        dialog = ActivityEntryDialog()
        if dialog.exec():
            activity_data = dialog.get_data()
            #self.update_activity_metric(activity_data['activity'])


    def open_ketone_entry(self):
        # Assume KetoneEntryDialog is defined similarly to GlucoseEntryDialog
        dialog = KetoneEntryDialog()
        if dialog.exec():
            ketone_data = dialog.get_data()
            # Update ketone metric display with new data
            #self.update_ketone_metric(ketone_data['ketone'])

    def open_ketone_blood_entry(self):
        # Assume KetoneBloodEntryDialog is defined
        dialog = BloodKetoneEntryDialog()
        if dialog.exec():
            ketone_blood_data = dialog.get_data()
            # Update ketone (blood) metric display with new data
            #self.update_ketone_blood_metric(ketone_blood_data['ketone_blood'])

    def open_blood_pressure_entry(self):
        # Assume BloodPressureEntryDialog is defined
        dialog = BloodPressureEntryDialog()
        if dialog.exec():
            blood_pressure_data = dialog.get_data()
            # Update blood pressure metric display with new data
            #self.update_blood_pressure_metric(blood_pressure_data['systolic'], blood_pressure_data['diastolic'])

    def open_glucose_entry(self):
        self.glucose_dialog = GlucoseEntryDialog()
        self.glucose_dialog.data_saved.connect(self.update_last_glucose_value)
        self.glucose_dialog.exec_()

    def open_insulin_entry(self):
        self.insulin_dialog = InsulinEntryDialog()
        self.insulin_dialog.data_saved.connect(self.update_last_insulin_value)
        self.insulin_dialog.exec_()


    def open_medication_entry(self):
        # Assume MedicationEntryDialog is defined
        dialog = MedicationEntryDialog()
        if dialog.exec():
            medication_data = dialog.get_data()
            # Update medication metric display with new data
            #self.update_medication_metric(medication_data['medication'])


    def add_metric(self, title, icon_path, value=None):
        # Create an icon label
        icon_label = QLabel()
        icon_label.setPixmap(QIcon(icon_path).pixmap(50, 50))
        icon_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)


        # Create a text label for the title
        text_label = QLabel(title)
        text_label.setAlignment(Qt.AlignCenter)

        # Calculate the next grid position
        position = self.metrics_grid.count() // 2
        row = position // 3
        col = position % 3

        self.metrics_grid.addWidget(icon_label, row * 2, col)
        self.metrics_grid.addWidget(text_label, row * 2 + 1, col)

        # If a value is provided, create a label for it
        if value:
            value_label = QLabel(value)
            value_label.setAlignment(Qt.AlignCenter)
            self.metrics_grid.addWidget(value_label, row * 2 + 2, col)

    def create_navigation_panel(self):
        panel_layout = QHBoxLayout()
        panel_layout.addWidget(self.create_nav_button('Home', 'home.png'))

        # Note: Ensure the diary_button is properly defined before connecting signals
        self.diary_button = self.create_nav_button('Diary', 'diary.png')
        self.diary_button.clicked.connect(self.show_diary)
        panel_layout.addWidget(self.diary_button)

        # Note: Ensure the community_button is properly defined before connecting signals
        self.community_button = self.create_nav_button('Community', 'community.png')
        self.community_button.clicked.connect(self.show_community)
        panel_layout.addWidget(self.community_button)

        # Defining stats_button before connecting signals to it
        self.stats_button = self.create_nav_button('Statistics', 'statistics.png')
        self.stats_button.clicked.connect(self.show_statistics)
        panel_layout.addWidget(self.stats_button)

        # Note: Ensure the more_button is properly defined before connecting signals
        self.more_button = self.create_nav_button('More', 'more.png')
        self.more_button.clicked.connect(self.show_more)
        panel_layout.addWidget(self.more_button)

        return panel_layout


    def show_diary(self):
        if not self.diary_page:
            self.diary_page = DiaryPage()
        self.close()
        self.diary_page.show()

    def show_community(self):
        if not self.community_page:
            self.community_page = CommunityPage()
        self.close()
        self.community_page.show()

    def show_more(self):
        if not self.more_page:
            self.more_page = MorePage()
        self.close()
        self.more_page.show()

    def show_statistics(self):
        if not self.stats_page:
            self.stats_page = StatisticsPage()
        self.close()
        self.stats_page.show()

    class SettingsPage(QDialog):
        def __init__(self):
            super().__init__()
            self.initUI()

        def initUI(self):
            layout = QVBoxLayout()
            self.notification_toggle_button = QPushButton("Turn Notifications On")
            self.notification_toggle_button.clicked.connect(self.toggle_notifications)
            layout.addWidget(self.notification_toggle_button)
            self.setLayout(layout)

        def toggle_notifications(self):
            # Implement functionality to toggle notifications
            pass

    def create_nav_button(self, title, icon_path):
        # Create a button with an icon
        button = QPushButton(QIcon(icon_path), title)
        button.setIconSize(QSize(24, 24))  # Assume icon size is 24x24
        # You can add more styling and signal-slot connections here
        return button

    def create_metric_label(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        # Additional styling can be applied to label here
        return label

    def create_progress_bar(self):
        bar = QProgressBar()
        bar.setMaximum(100)  # Assuming the values are in percentage
        bar.setTextVisible(False)  # Hide the text inside progress bar
        palette = QPalette()
        palette.setColor(QPalette.Highlight, QColor(100, 149, 237))  # Example color
        bar.setPalette(palette)
        # Additional styling can be applied to progress bar here
        return bar

    # Method to update the welcome message
    def set_welcome_message(self, name):
        self.welcome_label.setText(f'Hello, {name}')

    def set_glucose_level(self, glucose):
        very_low_glucose_threshold = 40  # Define a threshold for "very low" glucose
        high_glucose_threshold = 180
        low_glucose_threshold = 70
        max_glucose_level = 250

        if glucose < very_low_glucose_threshold:
            color = "blue"
            progress_value = 5  # Set a minimum value for visibility
        elif glucose < low_glucose_threshold:
            color = "lightblue"
            progress_value = ((glucose - very_low_glucose_threshold) / (
                        low_glucose_threshold - very_low_glucose_threshold)) * 25  # Example to give some progression in the "low" range
        elif glucose < high_glucose_threshold:
            color = "green"
            progress_value = 25 + ((glucose - low_glucose_threshold) / (
                        high_glucose_threshold - low_glucose_threshold)) * 50  # Fill up to 75% for normal range
        elif glucose < max_glucose_level:
            color = "red"
            progress_value = 75 + ((glucose - high_glucose_threshold) / (
                        max_glucose_level - high_glucose_threshold)) * 25  # Fill up to 100% for high range
        else:
            color = "#8B0000"  # Dark red for very high
            progress_value = 100  # Max out the progress bar

        self.glucose_progress.setValue(int(progress_value))
        self.glucose_progress.setStyleSheet(f"QProgressBar::chunk {{ background-color: {color}; }}")
        self.last_glucose_label.setText(f"Last Glucose: {glucose} mg/dL")

    def get_last_glucose_level_from_csv(self, filename='glucose_data.csv'):
        try:
            with open(filename, 'r') as file:
                last_line = list(csv.reader(file))[-1]
                return float(last_line[1])  # Assuming glucose value is the second column
        except Exception as e:
            print(f"Failed to read glucose value: {e}")
            return None  # or a default value

    def update_last_insulin_value(self):
        """Updates the last insulin value displayed in the UI from the insulin CSV file."""
        try:
            with open('insulin_data.csv', 'r') as file:  # Ensure the filename is correct
                csv_reader = csv.DictReader(file)
                last_record = None
                for row in csv_reader:
                    last_record = row  # This will end up with the last row

                if last_record:
                    # Assuming 'insulin_dose' is the correct column name in your CSV
                    last_insulin_dose = float(last_record['insulin_b'])
                    self.set_insulin_level(last_insulin_dose)
        except Exception as e:
            print(f"Failed to update insulin value: {e}")

    def set_insulin_level(self, dose):
        # Assuming you have maximum and minimum thresholds for insulin dosage
        max_dose = 50  # Maximum insulin dose for the progress bar
        min_dose = 10  # Minimum insulin dose for the progress bar
        very_high_dose = 60  # Define a threshold for "very high" insulin dose
        high_dose = 40  # High threshold
        optimal_dose = 20  # Optimal threshold
        low_dose = 15  # Low threshold

        # Update the label
        self.last_insulin_label.setText(f"Last Insulin: {dose} units")

        # Normalize the value for the progress bar and determine color
        if dose >= very_high_dose:
            normalized_dose = 100
            color = "#8B0000"  # Dark red for very high doses
        elif dose > high_dose:
            normalized_dose = ((dose - high_dose) / (very_high_dose - high_dose)) * 25 + 75  # Scale from 75% to 100%
            color = "red"
        elif dose > optimal_dose:
            normalized_dose = ((dose - optimal_dose) / (high_dose - optimal_dose)) * 25 + 50  # Scale from 50% to 75%
            color = "orange"
        elif dose > low_dose:
            normalized_dose = ((dose - low_dose) / (optimal_dose - low_dose)) * 25 + 25  # Scale from 25% to 50%
            color = "green"
        elif dose >= min_dose:
            normalized_dose = ((dose - min_dose) / (low_dose - min_dose)) * 25  # Scale from 0% to 25%
            color = "blue"
        else:
            normalized_dose = 0
            color = "blue"  # Use blue to indicate doses below the minimum threshold

        # Set progress bar value and color
        self.insulin_progress.setValue(int(normalized_dose))
        self.insulin_progress.setStyleSheet(f"QProgressBar::chunk {{ background-color: {color}; }}")


    def update_last_glucose_value(self):
        """Updates the last glucose value displayed in the UI from the CSV file."""
        try:
            with open('glucose_data.csv', 'r') as file:
                # Read the last line from the CSV file to get the most recent entry
                last_line = list(csv.reader(file))[-1]
                last_glucose_value = last_line[1]  # Assuming the glucose value is in the second column
                # Update the UI with the last glucose value
                self.set_glucose_level(self.get_last_glucose_level_from_csv())
        except Exception as e:
            print(f"Failed to update glucose value: {e}")

    def set_next_medication_time(self):
        # Placeholder for functionality to set the next medication time
        pass


class GlucoseEntryDialog(QDialog):
    data_saved = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Glucose Entry")
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        self.date_time_input = QDateTimeEdit(self)
        self.date_time_input
        self.date_time_input.setDateTime(QDateTime.currentDateTime())
        self.glucose_level_input = QLineEdit(self)  # Assuming a field for glucose level
        self.notes_input = QLineEdit(self)
        form_layout.addRow("Date", self.date_time_input)
        form_layout.addRow("Glucose Level (mg/dL)", self.glucose_level_input)
        form_layout.addRow("Notes", self.notes_input)
        layout.addLayout(form_layout)
        self.save_button = QPushButton("Save", self)
        self.cancel_button = QPushButton("Cancel", self)
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)

    def get_data(self):
        return {
            'date': self.date_time_input.dateTime().toString("yyyy-MM-dd HH:mm:ss"),
            'glucose_level': self.glucose_level_input.text(),
            'notes': self.notes_input.text()
        }

    def write_data_to_csv(self, data, filename='glucose_data.csv'):
        fieldnames = ['date', 'glucose_level', 'notes']
        self.generic_write_data_to_csv(data, filename, fieldnames)

    def accept(self):
        data = self.get_data()
        self.write_data_to_csv(data)
        self.data_saved.emit()  # Emit signal indicating data was saved
        super().accept()



    def generic_write_data_to_csv(self, data, filename, fieldnames):
        file_path = os.path.join(os.getcwd(), filename)
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data)


class InsulinEntryDialog(QDialog):
    data_saved = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insulin Entry")
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        self.date_time_input = QDateTimeEdit(self)
        self.date_time_input.setDateTime(QDateTime.currentDateTime())
        self.insulin_type_input = QLineEdit(self)  # Assuming a field for insulin type
        self.insulin_dose_input = QLineEdit(self)  # Assuming a field for insulin dose
        self.notes_input = QLineEdit(self)
        form_layout.addRow("Date", self.date_time_input)
        form_layout.addRow("Insulin Type", self.insulin_type_input)
        form_layout.addRow("Insulin Dose", self.insulin_dose_input)
        form_layout.addRow("Notes", self.notes_input)
        layout.addLayout(form_layout)
        self.save_button = QPushButton("Save", self)
        self.cancel_button = QPushButton("Cancel", self)
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)

    def get_data(self):
        return {
            'date': self.date_time_input.dateTime().toString("yyyy-MM-dd HH:mm:ss"),
            'insulin_type': self.insulin_type_input.text(),
            'insulin_dose': self.insulin_dose_input.text(),
            'notes': self.notes_input.text()
        }

    def write_data_to_csv(self, data, filename='insulin_data.csv'):
        fieldnames = ['date', 'insulin_type', 'insulin_dose', 'notes']
        self.generic_write_data_to_csv(data, filename, fieldnames)

    def accept(self):
        data = self.get_data()
        self.write_data_to_csv(data)
        self.data_saved.emit()  # Emit signal indicating data was saved
        super().accept()

    def generic_write_data_to_csv(self, data, filename, fieldnames):
        file_path = os.path.join(os.getcwd(), filename)
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data)


class MedicationEntryDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Medication Entry")
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        self.date_time_input = QDateTimeEdit(self)
        self.date_time_input.setDateTime(QDateTime.currentDateTime())
        self.period_input = QLineEdit(self)
        self.medication_input = QLineEdit(self)
        self.notes_input = QLineEdit(self)
        form_layout.addRow("Date", self.date_time_input)
        form_layout.addRow("Medication", self.medication_input)
        form_layout.addRow("Notes", self.notes_input)
        layout.addLayout(form_layout)
        self.save_button = QPushButton("Save", self)
        self.cancel_button = QPushButton("Cancel", self)
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)

    def get_data(self):
        return {
            'date': self.date_time_input.dateTime().toString("yyyy-MM-dd HH:mm:ss"),
            'medication': self.medication_input.text(),
            'notes': self.notes_input.text()
        }

    def accept(self):
        try:
            data = self.get_data()
            self.write_data_to_csv(data, "medication_data.csv", ['date', 'period', 'medication', 'notes'])
            super().accept()
        except Exception as e:
            print(f"Error when saving data: {e}")
            super().reject()

    def write_data_to_csv(self, data, filename, fieldnames):
        file_path = os.path.join(os.getcwd(), filename)
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data)


class KetoneEntryDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ketone Entry")

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.date_time_input = QDateTimeEdit(self)
        self.date_time_input.setDateTime(QDateTime.currentDateTime())
        self.ketone_input = QLineEdit(self)
        self.notes_input = QLineEdit(self)

        form_layout.addRow("Date", self.date_time_input)
        form_layout.addRow("Ketone", self.ketone_input)
        form_layout.addRow("Notes", self.notes_input)

        layout.addLayout(form_layout)

        self.save_button = QPushButton("Save", self)
        self.cancel_button = QPushButton("Cancel", self)

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)

    def get_data(self):
        return {
            'date': self.date_time_input.dateTime().toString("yyyy-MM-dd HH:mm:ss"),
            'ketone': self.ketone_input.text(),
            'notes': self.notes_input.text()
        }

    def accept(self):
        try:
            data = self.get_data()
            self.write_data_to_csv(data, "ketone_data.csv", ['date', 'ketone', 'notes'])
            super().accept()
        except Exception as e:
            print(f"Error when saving data: {e}")
            super().reject()

    def write_data_to_csv(self, data, filename, fieldnames):
        file_path = os.path.join(os.getcwd(), filename)
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data)

class BloodPressureEntryDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blood Pressure Entry")
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        self.date_time_input = QDateTimeEdit(self)
        self.date_time_input.setDateTime(QDateTime.currentDateTime())
        self.systolic_input = QLineEdit(self)
        self.diastolic_input = QLineEdit(self)
        self.pulse_input = QLineEdit(self)
        self.notes_input = QLineEdit(self)
        form_layout.addRow("Date", self.date_time_input)
        form_layout.addRow("Systolic Pressure", self.systolic_input)
        form_layout.addRow("Diastolic Pressure", self.diastolic_input)
        form_layout.addRow("Pulse", self.pulse_input)
        form_layout.addRow("Notes", self.notes_input)
        layout.addLayout(form_layout)
        self.save_button = QPushButton("Save", self)
        self.cancel_button = QPushButton("Cancel", self)
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)

    def get_data(self):
        return {
            'date': self.date_time_input.dateTime().toString("yyyy-MM-dd HH:mm:ss"),
            'systolic': self.systolic_input.text(),
            'diastolic': self.diastolic_input.text(),
            'pulse': self.pulse_input.text(),
            'notes': self.notes_input.text()
        }

    def write_data_to_csv(self, data, filename='blood_pressure_data.csv'):
        fieldnames = ['date', 'systolic', 'diastolic', 'pulse', 'notes']
        self.generic_write_data_to_csv(data, filename, fieldnames)

    def accept(self):
        data = self.get_data()
        self.write_data_to_csv(data)
        super().accept()

    def generic_write_data_to_csv(self, data, filename, fieldnames):
        file_path = os.path.join(os.getcwd(), filename)
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data)


class ActivityEntryDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Activity Entry")
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        self.date_time_input = QDateTimeEdit(self)
        self.date_time_input.setDateTime(QDateTime.currentDateTime())
        self.period_input = QLineEdit(self)
        self.activity_input = QLineEdit(self)
        self.notes_input = QLineEdit(self)
        form_layout.addRow("Date", self.date_time_input)
        form_layout.addRow("Period", self.period_input)
        form_layout.addRow("Activity", self.activity_input)
        form_layout.addRow("Notes", self.notes_input)
        layout.addLayout(form_layout)
        self.save_button = QPushButton("Save", self)
        self.cancel_button = QPushButton("Cancel", self)
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)

    def get_data(self):
        return {
            'date': self.date_time_input.dateTime().toString("yyyy-MM-dd HH:mm:ss"),
            'period': self.period_input.text(),
            'activity': self.activity_input.text(),
            'notes': self.notes_input.text()
        }

    def write_data_to_csv(self, data, filename='activity_data.csv'):
        fieldnames = ['date', 'period', 'activity', 'notes']
        self.generic_write_data_to_csv(data, filename, fieldnames)

    def accept(self):
        data = self.get_data()
        self.write_data_to_csv(data)
        super().accept()

    def generic_write_data_to_csv(self, data, filename, fieldnames):
        file_path = os.path.join(os.getcwd(), filename)
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data)


class BloodKetoneEntryDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blood Ketone Entry")

        layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        self.date_time_input = QDateTimeEdit(self)
        self.date_time_input.setDateTime(QDateTime.currentDateTime())
        self.period_input = QLineEdit(self)
        self.ketone_input = QLineEdit(self)
        self.notes_input = QLineEdit(self)

        form_layout.addRow("Date", self.date_time_input)
        form_layout.addRow("Period", self.period_input)
        form_layout.addRow("Blood Ketone", self.ketone_input)
        form_layout.addRow("Notes", self.notes_input)

        layout.addLayout(form_layout)

        self.save_button = QPushButton("Save", self)
        self.cancel_button = QPushButton("Cancel", self)

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)

    def get_data(self):
        return {
            'date': self.date_time_input.dateTime().toString("yyyy-MM-dd HH:mm:ss"),
            'period': self.period_input.text(),
            'ketone': self.ketone_input.text(),
            'notes': self.notes_input.text()
        }

    def write_data_to_csv(self, data, filename='blood_ketone_data.csv'):
        fieldnames = ['date', 'period', 'ketone', 'notes']
        self.generic_write_data_to_csv(data, filename, fieldnames)

    def accept(self):
        data = self.get_data()
        self.write_data_to_csv(data)
        super().accept()

    def generic_write_data_to_csv(self, data, filename, fieldnames):
        file_path = os.path.join(os.getcwd(), filename)
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data)


class HbA1CEntryDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HbA1C Entry")

        layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        self.date_time_input = QDateTimeEdit(self)
        self.date_time_input.setDateTime(QDateTime.currentDateTime())
        self.period_input = QLineEdit(self)
        self.hba1c_input = QLineEdit(self)
        self.notes_input = QLineEdit(self)

        form_layout.addRow("Date", self.date_time_input)
        form_layout.addRow("Period", self.period_input)
        form_layout.addRow("HbA1C", self.hba1c_input)
        form_layout.addRow("Notes", self.notes_input)

        layout.addLayout(form_layout)

        self.save_button = QPushButton("Save", self)
        self.cancel_button = QPushButton("Cancel", self)

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)

    def get_data(self):
        return {
            'date': self.date_time_input.dateTime().toString("yyyy-MM-dd HH:mm:ss"),
            'period': self.period_input.text(),
            'hba1c': self.hba1c_input.text(),
            'notes': self.notes_input.text()
        }

    def write_data_to_csv(self, data, filename='hba1c_data.csv'):
        fieldnames = ['date', 'period', 'hba1c', 'notes']
        self.generic_write_data_to_csv(data, filename, fieldnames)

    def accept(self):
        data = self.get_data()
        self.write_data_to_csv(data)
        super().accept()

    def generic_write_data_to_csv(self, data, filename, fieldnames):
        file_path = os.path.join(os.getcwd(), filename)
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data)

class CarbsEntryDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Carbs Entry")
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        self.date_time_input = QDateTimeEdit(self)
        self.date_time_input.setDateTime(QDateTime.currentDateTime())
        self.carbs_input = QLineEdit(self)
        self.notes_input = QLineEdit(self)
        form_layout.addRow("Date", self.date_time_input)
        form_layout.addRow("Carbs (grams)", self.carbs_input)
        form_layout.addRow("Notes", self.notes_input)
        layout.addLayout(form_layout)
        self.save_button = QPushButton("Save", self)
        self.cancel_button = QPushButton("Cancel", self)
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)

    def get_data(self):
        return {
            'date': self.date_time_input.dateTime().toString("yyyy-MM-dd HH:mm:ss"),
            'carbs': self.carbs_input.text(),
            'notes': self.notes_input.text()
        }

    def write_data_to_csv(self, data, filename='carbs_data.csv'):
        fieldnames = ['date', 'carbs', 'notes']
        self.generic_write_data_to_csv(data, filename, fieldnames)

    def accept(self):
        data = self.get_data()
        self.write_data_to_csv(data)
        super().accept()

    def generic_write_data_to_csv(self, data, filename, fieldnames):
        file_path = os.path.join(os.getcwd(), filename)
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data)

# Example usage
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { background-color: #E8EBF0; }")
    ex = HomePage('John Doe', weight=70, height=175)
    ex.set_glucose_level(75)  # Set a mock value for glucose level
    ex.set_insulin_level(50)  # Set a mock value for insulin level
    ex.show()
    sys.exit(app.exec_())