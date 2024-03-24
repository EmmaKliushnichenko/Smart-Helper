import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
                             QPushButton, QHBoxLayout, QDialog, QLabel, QComboBox, QMessageBox,
                             QFileDialog, QTextEdit, QSizeGrip)
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
import os





class MorePage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("More Page")
        self.setGeometry(100, 100, 375, 812)  # Width x Height

        layout = QVBoxLayout()

        # List widget for the More options
        self.listWidget = QListWidget()
        self.listWidget.setIconSize(QSize(32, 32))  # Set the icon size

        # Add items to the list widget
        self.addListItem('Share', 'icons/share.png')
        self.addListItem('Privacy policy', 'icons/settings.png')
        self.addListItem('Settings', 'icons/settings.png')

        # Add the list widget to the main layout
        layout.addWidget(self.listWidget)

        # Add navigation panel at the bottom
        layout.addLayout(self.create_navigation_panel())

        self.listWidget.itemClicked.connect(self.onListItemClicked)

        # Set the layout for this widget
        self.setLayout(layout)

    def addListItem(self, title, icon_path):
        listItem = QListWidgetItem(QIcon(icon_path), title)
        self.listWidget.addItem(listItem)

    def onListItemClicked(self, item):
        if item.text() == "Share":
            self.showShareDialog()
        elif item.text() == "Privacy policy":
            self.showPrivacyPolicyDialog()
        elif item.text() == "Settings":
            self.showSettingsPage()

    def showShareDialog(self):
        dialog = ShareDialog(self)
        dialog.exec_()

    def showPrivacyPolicyDialog(self):
        dialog = PrivacyPolicyDialog()
        dialog.exec_()

    def showSettingsPage(self):
        dialog = SettingsPage(self)
        dialog.exec_()

    def create_navigation_panel(self):
        panel_layout = QHBoxLayout()
        home_button = self.create_nav_button('Home', 'home.png')
        diary_button = self.create_nav_button('Diary', 'diary.png')
        community_button = self.create_nav_button('Community', 'community.png')
        stats_button = self.create_nav_button('Statistics', 'statistics.png')
        more_button = self.create_nav_button('More', 'more.png')

        panel_layout.addWidget(home_button)
        panel_layout.addWidget(diary_button)
        panel_layout.addWidget(community_button)
        panel_layout.addWidget(stats_button)
        panel_layout.addWidget(more_button)
        return panel_layout

    def create_nav_button(self, title, icon_path):
        button = QPushButton(title)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(24, 24))
        return button



class ShareDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Share Data")
        self.layout = QVBoxLayout(self)

        self.dataTypeComboBox = QComboBox()
        self.dataTypeComboBox.addItems(["Blood Pressure Data", "Blood Ketone Data", "Activity Data", "Carbs Data", "Glucose Data"])
        self.layout.addWidget(QLabel("Select data type to share:"))
        self.layout.addWidget(self.dataTypeComboBox)

        shareButton = QPushButton("Share")
        shareButton.clicked.connect(self.shareData)
        self.layout.addWidget(shareButton)

    def shareData(self):
        dataType = self.dataTypeComboBox.currentText()
        # Here you'd call a method to handle the actual sharing
        # For example, self.parent().shareData(dataType)
        print(f"Preparing to share {dataType}")  # Placeholder action
        self.accept()

    def shareData(self):
        dataType = self.dataTypeComboBox.currentText()
        # Determine the file based on the selection
        file_map = {
            "Blood Pressure Data": "blood_pressure_data.csv",
            "Blood Ketone Data": "blood_ketone_data.csv",
            "Activity Data": "activity_data.csv",
            "Carbs Data": "carbs_data.csv",
            "Glucose Data": "glucose_data.csv",
        }
        filename = file_map[dataType]

        # Prompt the user to select a save location
        save_path, _ = QFileDialog.getSaveFileName(self, "Save File", filename, "CSV files (*.csv)")
        if save_path:
            # Copy the file to the new location
            import shutil
            try:
                shutil.copyfile(filename, save_path)
                QMessageBox.information(self, "Success", "Data has been saved successfully.")
            except Exception as e:
                try:
                    QMessageBox.critical(self, "Error", f"Failed to save the file: {str(e)}")
                except Exception as inner_e:
                    print(f"Error displaying the error message: {inner_e}")
                    # Additional error handling or logging could go here


class PrivacyPolicyDialog(QDialog):
    def __init__(self, parent=None):  # parent parameter is optional and defaults to None
        super().__init__(parent)
        self.setWindowTitle("Privacy Policy")
        layout = QVBoxLayout(self)

        # Display the privacy policy text
        self.policyText = QTextEdit()
        self.policyText.setPlainText("Your privacy policy goes here...")
        self.policyText.setReadOnly(True)
        layout.addWidget(self.policyText)

        # Agree button
        self.agreeButton = QPushButton("I Agree")
        self.agreeButton.clicked.connect(self.accept)
        layout.addWidget(self.agreeButton)

        self.setLayout(layout)

    def accept(self):
        # Handle the acceptance of the policy here, e.g., save a flag in settings
        super().accept()
        QMessageBox.information(self, "Accepted", "Thank you for accepting the Privacy Policy.")


class SettingsPage(QDialog):  # Inherit from QDialog
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        layout = QVBoxLayout(self)

        self.deleteDataButton = QPushButton("Delete My Data")
        self.deleteDataButton.clicked.connect(self.confirmDataDeletion)
        layout.addWidget(self.deleteDataButton)

    def confirmDataDeletion(self):
        reply = QMessageBox.question(self, "Confirm Deletion",
                                     "Are you sure you want to delete all your data? "
                                     "This action cannot be undone.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.deleteData()

    def deleteData(self):
        # Implement data deletion logic here
        csv_files = [
            "blood_pressure_data.csv",
            "blood_ketone_data.csv",
            "activity_data.csv",
            "carbs_data.csv",
            "glucose_data.csv",
            "medication_data.csv",
            "ketone_data.csv",
            "insulin_data.csv",
            "hba1c_data.csv"
        ]
        for filename in csv_files:
            try:
                os.remove(filename)
            except OSError as e:
                print(f"Error deleting file {filename}: {e.strerror}")
        QMessageBox.information(self, "Data Deleted", "Your data has been successfully deleted.")
        self.accept()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { background-color: #E8EBF0; }")
    more_page = MorePage()
    more_page.show()
    sys.exit(app.exec_())
