from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *

class PaomWebBrowser():
    def __init__(self):
        self.window = QWidget()
        self.window.setWindowTitle("Paom's Web Browser")
        self.window.setGeometry(100, 100, 1200, 800)
        self.window.setWindowIcon(QIcon("browsericon.png"))

        self.layout = QVBoxLayout()
        self.horizontal_layout = QHBoxLayout()

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL here...")
        self.url_bar.setMinimumHeight(30)

        self.url_bar.setFont(QFont("Arial", 12))
        self.url_bar.setAlignment(Qt.AlignLeft)
        self.url_bar.mousePressEvent = self.clear_url_bar  # Clear text when clicked

        self.search_button = QPushButton("⌕")
        self.search_button.setFont(QFont("Arial", 15))
        self.search_button.setMinimumHeight(30)

        self.home_button = QPushButton("Home")
        self.home_button.setFont(QFont("Arial", 12))
        self.home_button.setMinimumHeight(30)
        
        self.refresh_button = QPushButton("Reload")
        self.refresh_button.setFont(QFont("Arial", 12))
        self.refresh_button.setMinimumHeight(30)
        
        self.backward_button = QPushButton("<")  
        self.backward_button.setFont(QFont("Arial", 15))
        self.backward_button.setMinimumHeight(30)

        self.forward_button = QPushButton(">")
        self.forward_button.setFont(QFont("Arial", 15))
        self.forward_button.setMinimumHeight(30)
        
        self.horizontal_layout.addWidget(self.url_bar)
        self.horizontal_layout.addWidget(self.search_button)
        self.horizontal_layout.addWidget(self.home_button)
        self.horizontal_layout.addWidget(self.refresh_button)
        self.horizontal_layout.addWidget(self.backward_button)
        self.horizontal_layout.addWidget(self.forward_button)

        self.add_tab_button = QPushButton("New Tab")
        self.add_tab_button.setFont(QFont("Arial", 12))
        self.add_tab_button.setMinimumHeight(30)

        self.horizontal_layout.addWidget(self.add_tab_button)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.browser.setStyleSheet("background-color: #ffffff; border-radius: 5px; padding: 5px;")

        self.search_button.clicked.connect(self.search)
        self.search_button.setShortcut(QKeySequence("Return"))
        
        self.backward_button.clicked.connect(lambda: self.tabs.currentWidget().back())
        self.forward_button.clicked.connect(lambda: self.tabs.currentWidget().forward())
        self.refresh_button.clicked.connect(lambda: self.tabs.currentWidget().reload())
        self.home_button.clicked.connect(lambda: self.tabs.currentWidget().setUrl(QUrl("https://www.google.com")))

        self.layout.addLayout(self.horizontal_layout)
        self.layout.addWidget(self.browser)
        self.window.setLayout(self.layout)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.addTab(self.browser, "Loading...")
        self.browser.loadFinished.connect(lambda: self.update_url_bar(self.browser))
        
        self.layout.addWidget(self.tabs)
        self.add_tab_button.clicked.connect(self.add_new_tab)

        self.window.show() # Default to the initial browser instance

    def clear_url_bar(self, event):
        self.url_bar.clear()  # Clears text when clicked

    def add_new_tab(self):
        new_tab = QWebEngineView()
        new_tab.setUrl(QUrl("https://www.google.com"))
        
        self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentWidget(new_tab)
        
        new_tab.loadFinished.connect(lambda: self.update_url_bar(new_tab))

    def update_url_bar(self, tab):
        url = tab.url().toString()
        self.url_bar.setText(url)

        # Update the tab title with the page title
        title = tab.page().title()
        index = self.tabs.indexOf(tab)
        if index != -1:
            self.tabs.setTabText(index, title)
        
        # Update the URL bar when the page is loaded
        tab.loadFinished.connect(lambda: self.update_url_bar(tab))

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            QMessageBox.warning(self.window, "Warning", "Cannot close the last tab.")

    def search(self):
        url = self.url_bar.text()

        current_browser = self.tabs.currentWidget()  # Get the active tab's web view
        if isinstance(current_browser, QWebEngineView):  
            if url.startswith("http://") or url.startswith("https://"):
                current_browser.setUrl(QUrl(url))  # Apply the URL to the active tab
            else:
                current_browser.setUrl(QUrl(f"https://www.google.com/search?q={url}"))  # Search in Google

app = QApplication([])

app.setStyleSheet("""
    QMainWindow {
        background-color: #F5F5F5; /* Light gray modern background */
    }

    QLineEdit {
        background-color: #FFFFFF;
        color: #333333;
        border: 2px solid #CCCCCC;
        border-radius: 6px;
        padding: 6px;
        font-size: 14px;
        selection-background-color: #0078D7; /* Light blue highlight */
    }

    QPushButton {
        background-color: #EAEAEA;
        color: #333333;
        border-radius: 6px;
        padding: 8px;
        font-weight: bold;
        font-size: 14px;
        border: 2px solid #CCCCCC;
    }

    QPushButton:hover {
        background-color: #0078D7; /* Smooth blue hover effect */
        color: #FFFFFF;
    }

    QTabWidget::pane {
        border: 2px solid #CCCCCC;
        background-color: #FFFFFF;
        border-radius: 8px;
    }

    QTabBar::tab {
        background-color: #EAEAEA;
        color: #333333;
        padding: 6px;
        border: 2px solid #CCCCCC;
        border-radius: 6px;
    }

    QTabBar::tab:selected {
        background-color: #0078D7; /* Blue highlight on active tab */
        font-weight: bold;
        color: #FFFFFF;
    }

    QWebEngineView {
        border-radius: 8px;
        background-color: #FFFFFF;
    }
""")

web_browser = PaomWebBrowser()
app.exec_()