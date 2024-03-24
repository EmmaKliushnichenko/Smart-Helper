import openai
import sys
import csv

from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget,
                             QPushButton, QHBoxLayout, QTextEdit, QAction, QMenuBar,
                             QGridLayout, QListWidget, QListWidgetItem, QButtonGroup,
                             QFrame, QSpacerItem, QSizePolicy, QLineEdit, QMessageBox, QDialog, QComboBox)

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont

from MorePage import MorePage

# Set your OpenAI API key here
openai.api_key = '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'

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]


class HealthInfoPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Community')
        self.setGeometry(100, 100, 375, 812)

        # Main layout
        main_layout = QVBoxLayout()

        self.blood_pressure_button = QPushButton(f"Your blood pressure today is: {self.get_last_blood_pressure()}")
        self.blood_pressure_button.clicked.connect(self.ask_about_blood_pressure)
        main_layout.addWidget(self.blood_pressure_button)  # Add to your layout

        # Notification button
        self.notification_button = self.create_notification_button()
        main_layout.addWidget(self.notification_button)

        # Questions list layout
        self.questions_list_layout = self.create_questions_list()  # Store as an instance attribute if needed elsewhere
        main_layout.addLayout(self.questions_list_layout)

        # Horizontal layout for Smart Companion and Feedback buttons
        button_layout = QHBoxLayout()
        self.fab_chat = self.create_fab_chat()
        button_layout.addWidget(self.fab_chat)
        self.feedback_button = self.create_feedback_button()
        button_layout.addWidget(self.feedback_button)
        main_layout.addLayout(button_layout)

        # Spacer to push the navigation panel to the bottom
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer)

        # Navigation panel at the bottom
        navigation_panel = self.create_navigation_panel()
        main_layout.addLayout(navigation_panel)

        # Set the central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_feedback_button(self):
        button = QPushButton("Feedback")
        button.setStyleSheet("""
            QPushButton {
                border-radius: 25px;
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        button.clicked.connect(self.open_feedback_dialog)
        return button

    def open_feedback_dialog(self):
        dialog = FeedbackDialog(self)
        dialog.exec_()

    def create_navigation_panel(self):
        panel_layout = QHBoxLayout()

        # Assuming other buttons are correctly set up and connected
        home_button = self.create_nav_button('Home', 'home.png')
        diary_button = self.create_nav_button('Diary', 'diary.png')
        community_button = self.create_nav_button('Community', 'statistics.png')
        stats_button = self.create_nav_button('Statistics', 'statistics.png')
        more_button = self.create_nav_button('More', 'more.png')

        # Create and set up the community button
        more_button = self.create_nav_button('More', 'more.png')
        more_button.clicked.connect(self.show_more)

        # Add buttons to the panel layout
        panel_layout.addWidget(home_button)
        panel_layout.addWidget(diary_button)
        panel_layout.addWidget(community_button)
        panel_layout.addWidget(stats_button)
        panel_layout.addWidget(more_button)

        return panel_layout

    def show_more(self):
        if not hasattr(self, 'more_page'):
            self.more_page = MorePage()
        self.more_page.show()
        self.close()

    def create_nav_button(self, title, icon_path):
        button = QPushButton(title)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(24, 24))
        return button

    def update_blood_pressure_button(self):
        self.blood_pressure_button.setText(f"Your blood pressure today is: {self.get_last_blood_pressure()}")
        # Questions list
        self.questions_list_layout = self.create_questions_list()
        main_layout.addLayout(self.questions_list_layout)

    def ask_about_blood_pressure(self):
        blood_pressure_value = self.get_last_blood_pressure()
        question = f"My blood pressure today is {blood_pressure_value}. What does this mean?"
        self.open_chat_with_message(question)

    def open_chat_with_message(self, message):
        if not hasattr(self, 'chat_window'):
            self.chat_window = ChatWindow()
        self.chat_window.prepopulate_message(message)
        self.chat_window.show()

    def create_segmented_control(self, titles):
        segmented_layout = QHBoxLayout()
        button_group = QButtonGroup(self)

        for title in titles:
            button = QPushButton(title)
            button_group.addButton(button)
            button.setCheckable(True)
            button.setStyleSheet("QPushButton { margin: 5px; padding: 10px; }")
            segmented_layout.addWidget(button)

        # Only one button can be checked at the same time
        button_group.setExclusive(True)
        button_group.buttonClicked.connect(self.segmented_control_clicked)  # Connect to handler

        return segmented_layout

    def create_notification_button(self):
        # Assuming you want the same style as the smart companion button
        button = QPushButton("Tell me about your day")
        button.setIcon(QIcon("notification.png"))  # Replace with your notification icon
        button.setIconSize(QSize(56, 56))
        button.setStyleSheet("""
            QPushButton { 
                border-radius: 28px;
                background-color: #ADD8E6;  # Light blue color
            }
            QPushButton:pressed {
                background-color: #87CEEB;  # Slightly darker
            }
        """)
        button.clicked.connect(self.show_notification_dialog)
        return button

    def get_last_blood_pressure(self):
        try:
            with open('blood_pressure_data.csv', 'r') as file:
                reader = csv.reader(file)
                last_row = None
                for row in reader:
                    last_row = row
                if last_row:
                    print(f"Last BP row: {last_row}")  # Debug print
                    return f"{last_row[1]} / {last_row[2]}"  # Check column indices
        except FileNotFoundError:
            print("The file doesn't exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
        return "No data"

    def create_questions_list(self):
        questions_layout = QVBoxLayout()

        # Questions with corresponding text to be sent to the smart companion
        questions = [
            "What is blood pressure?",
            "What are the different types of high blood pressure?",
            "What are the treatments for high blood pressure?",
            "What is low blood pressure?",
            "What is heart rate?",
            # Add more questions as needed
        ]

        for question in questions:
            button = QPushButton(question)
            button.clicked.connect(
                lambda _, q=question: self.open_chat_with_message(q))  # Use lambda to capture the question
            questions_layout.addWidget(button)

        return questions_layout

    def open_chat_with_message(self, message):
        # Check if the chat window already exists and create it if not
        if not hasattr(self, 'chat_window'):
            self.chat_window = ChatWindow()
        self.chat_window.prepopulate_message(message)
        self.chat_window.show()

    def show_notification_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("How are you feeling today?")
        layout = QVBoxLayout()

        # Add a label asking about the user's mood
        mood_label = QLabel("How are you today?")
        layout.addWidget(mood_label)

        # Option buttons for the user's mood
        good_button = QPushButton("Good")
        ok_button = QPushButton("Ok")
        bad_button = QPushButton("Bad")

        # Connect buttons to methods
        good_button.clicked.connect(lambda: self.handle_mood_response("Good"))
        ok_button.clicked.connect(lambda: self.handle_mood_response("Ok"))
        bad_button.clicked.connect(lambda: self.handle_mood_response("Bad"))

        # Add buttons to the dialog layout
        layout.addWidget(good_button)
        layout.addWidget(ok_button)
        layout.addWidget(bad_button)

        dialog.setLayout(layout)

        # Make the dialog modal, which blocks input to other windows until this dialog is closed
        dialog.exec_()

    def handle_mood_response(self, mood):
        if mood == "Good":
            QMessageBox.information(self, "Response", "That's very nice to hear!")
        elif mood == "Ok":
            QMessageBox.information(self, "Response", "Hope things get even better!")
        elif mood == "Bad":
            self.ask_follow_up_question()

    def ask_follow_up_question(self):
        reply = QMessageBox.question(self, "Follow-up", "Do you want to talk about it?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.open_chat()  # Assuming this method initiates a chat with the smart companion

    def open_chat(self):
        # Method to initiate a chat. For example, you could show another dialog or window here.
        QMessageBox.information(self, "Chat", "Let's chat!")

    def open_info_dialog(self, title, content):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        layout = QVBoxLayout()
        text_browser = QTextBrowser()
        text_browser.setText(content)
        layout.addWidget(text_browser)
        dialog.setLayout(layout)
        dialog.exec_()  # Make the dialog modal

    def show_question_info(self, question):
        # Placeholder method to display information related to the clicked question
        QMessageBox.information(self, "Question Info", f"Information about: {question}")

    def create_fab_chat(self):
        chat_button = QPushButton("Ask your companion")
        chat_button.setIcon(QIcon("chat.png"))  # Ensure you have a 'chat.png' in your application directory
        chat_button.setIconSize(QSize(56, 56))  # Large, circular icon
        chat_button.setStyleSheet("""
            QPushButton {
                background: #ADD8E6;
                border-radius: 20px;
                border-style: solid;
                border-width: 1px;
                border-color: #A1A19F;
                box-shadow: 0px 0px 1px 1px rgba(0, 0, 0, 0.2);  /* Box shadow effect */
            }
            QPushButton:pressed {
                background-color: #C0C0C0;
            }
            QPushButton:hover {
                background-color: #DCD8CC;
            }
        """)
        chat_button.setFixedSize(208, 80)  # Fixed size for the button
        chat_button.clicked.connect(self.open_chat)
        return chat_button


    def open_chat(self):
        self.chat_window = ChatWindow()
        self.chat_window.show()

    def prepopulate_message(self, message):
        # Append the message to the chat display or set it as the chat input text
        self.append_message("You", message)

    def append_message(self, sender, message):
        # Assuming you have a QTextEdit or similar widget for displaying chat messages:
        formatted_message = f"<b>{sender}:</b> {message}"
        self.chat_display.append(formatted_message)


class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Smart Companion')
        self.description_label = QLabel("This Smart Companion aids in diabetes management with advice and support.")
        self.description_label.setWordWrap(True)
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_input = QLineEdit()
        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.on_send)
        layout = QVBoxLayout()
        layout.addWidget(self.description_label)
        layout.addWidget(self.chat_display)
        layout.addWidget(self.chat_input)
        layout.addWidget(self.send_button)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def prepopulate_message(self, message):
        self.chat_input.setText(message)

    def append_message(self, sender, message):
        formatted_message = f"<b>{sender}:</b> {message}"
        self.chat_display.append(formatted_message)

    def on_send(self):
        user_input = self.chat_input.text()
        if user_input:
            self.append_message("You", user_input)
            try:
                # Using get_completion to send input to GPT-3
                response = get_completion(user_input)
                self.append_message("Smart Companion", response)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            self.chat_input.clear()

class FeedbackDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Feedback")
        self.layout = QVBoxLayout(self)

        # Add form fields
        self.email_input = QLineEdit(self)
        self.feedback_type = QComboBox(self)
        self.feedback_type.addItems(["Bug Report", "Feature Request", "General Feedback"])
        self.feedback_message = QTextEdit(self)

        # Submit button
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.submit_feedback)

        # Layout setup
        self.layout.addWidget(QLabel("Email:"))
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(QLabel("Please tell us, Emma"))
        self.layout.addWidget(QLabel("Feedback Type:"))
        self.layout.addWidget(self.feedback_type)
        self.layout.addWidget(QLabel("Feedback:"))
        self.layout.addWidget(self.feedback_message)
        self.layout.addWidget(self.submit_button)

    def submit_feedback(self):
        # Here you would handle the submission of feedback, such as sending it to a server
        email = self.email_input.text()
        feedback_type = self.feedback_type.currentText()
        feedback_message = self.feedback_message.toPlainText()
        print(f"Feedback submitted: {feedback_type} - {feedback_message} by {email}")
        self.accept()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { background-color: #E8EBF0; }")
    health_info_page = HealthInfoPage()
    health_info_page.show()
    sys.exit(app.exec_())