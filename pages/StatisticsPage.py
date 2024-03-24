from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                             QListWidget, QStackedWidget, QListWidgetItem,
                             QPushButton, QHBoxLayout, QLabel, QLineEdit)
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
import pandas as pd
from DIaryPage import DiaryPage


class GraphPage(QWidget):
    def __init__(self, title, csv_path):
        super().__init__()
        self.csv_path = csv_path
        self.initUI(title)

    def initUI(self, title):
        layout = QVBoxLayout()
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.plotGraph(title)

        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plotGraph(self, title):
        # Read the data
        data = pd.read_csv(self.csv_path, parse_dates=True, index_col=0)

        # Plot the graph
        self.ax.clear()
        data.plot(ax=self.ax)
        self.ax.set_title(f'{title}')
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Value')
        self.canvas.draw()


class StatisticsPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Statistics')
        self.setGeometry(100, 100, 375, 812)

        layout = QVBoxLayout()
        self.listWidget = QListWidget()
        self.listWidget.setIconSize(QSize(32, 32))
        self.stackedWidget = QStackedWidget()

        # Add items to the list widget and corresponding pages to the stacked widget
        self.addListItem('Glucose Graph', 'icons/glucose.png',
                         'C:\\Users\\edkly\\PycharmProjects\\pythonProject9\\venv\\pages\\glucose_data.csv')
        self.addListItem('Insulin Graph', 'icons/insulin.png',
                         'C:\\Users\\edkly\\PycharmProjects\\pythonProject9\\venv\\pages\\insulin_data.csv')
        self.addListItem('Ketone Graph', 'icons/glucose.png',
                         'C:\\Users\\edkly\\PycharmProjects\\pythonProject9\\venv\\pages\\ketone_data.csv')
        self.addListItem('Ketone(Blood) Graph', 'icons/insulin.png',
                         'C:\\Users\\edkly\\PycharmProjects\\pythonProject9\\venv\\pages\\blood_ketone_data.csv')
        self.addListItem('HbA1c Graph', 'icons/glucose.png',
                         'C:\\Users\\edkly\\PycharmProjects\\pythonProject9\\venv\\pages\\hba1c_data.csv')
        self.addListItem('Blood Pressure Graph', 'icons/insulin.png',
                         'C:\\Users\\edkly\\PycharmProjects\\pythonProject9\\venv\pages\\blood_pressure_data.csv')


        layout.addWidget(self.listWidget)
        layout.addWidget(self.stackedWidget)
        layout.addLayout(self.create_navigation_panel())


        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.listWidget.currentRowChanged.connect(self.displayPage)

    def addListItem(self, title, icon_path, csv_path=None):
        listItem = QListWidgetItem(QIcon(icon_path), title)
        self.listWidget.addItem(listItem)

        page = GraphPage(title, csv_path) if csv_path else QWidget()
        self.stackedWidget.addWidget(page)

    def displayPage(self, index):
        self.stackedWidget.setCurrentIndex(index)

    def create_navigation_panel(self):
        panel_layout = QHBoxLayout()

        # Assuming other buttons are correctly set up and connected
        home_button = self.create_nav_button('Home', 'home.png')
        diary_button = self.create_nav_button('Diary', 'diary.png')
        community_button = self.create_nav_button('Community', 'statistics.png')
        stats_button = self.create_nav_button('Statistics', 'statistics.png')
        more_button = self.create_nav_button('More', 'more.png')

        # Create and set up the community button
        diary_button = self.create_nav_button('Diary', 'community.png')
        diary_button.clicked.connect(self.show_diary)

        # Add buttons to the panel layout
        panel_layout.addWidget(home_button)
        panel_layout.addWidget(diary_button)
        panel_layout.addWidget(community_button)
        panel_layout.addWidget(stats_button)
        panel_layout.addWidget(more_button)

        return panel_layout

    def show_diary(self):
        if not hasattr(self, 'diary_page'):
            self.diary_page = DiaryPage()
        self.diary_page.show()
        self.close()

    def create_nav_button(self, title, icon_path):
        button = QPushButton(title)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(24, 24))
        return button


# Example usage
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { background-color: #E8EBF0; }")
    ex = StatisticsPage()
    ex.show()
    sys.exit(app.exec_())