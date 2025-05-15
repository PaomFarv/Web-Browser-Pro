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

        self.layout = QHBoxLayout()
        self.horizontal_layout = QVBoxLayout()

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL here...")
        self.url_bar.setMinimumHeight(30)

        self.url_bar.setFont(QFont("Arial", 12))
        self.url_bar.setAlignment(Qt.AlignLeft)

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

        self.add_tab_button = QPushButton("+ New Tab")
        self.add_tab_button.setFont(QFont("Arial", 12))
        self.add_tab_button.setMinimumHeight(30)

        self.horizontal_layout.addWidget(self.add_tab_button)
        self.horizontal_layout.addStretch()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.browser.setStyleSheet("background-color: #ffffff; border-radius: 5px; padding: 5px;")

        self.search_button.clicked.connect(lambda: self.search(self.url_bar.text()))
        self.backward_button.clicked.connect(self.browser.back)
        self.forward_button.clicked.connect(self.browser.forward)
        self.refresh_button.clicked.connect(self.browser.reload)
        self.home_button.clicked.connect(lambda: self.search("https://www.google.com"))

        self.layout.addLayout(self.horizontal_layout)
        self.layout.addWidget(self.browser)
        self.window.setLayout(self.layout)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.addTab(self.browser, "Tab 1")
        self.tabs.setCurrentIndex(0)
        
        self.horizontal_layout.addWidget(self.tabs)
        self.add_tab_button.clicked.connect(self.add_new_tab)

        self.window.show()

    def add_new_tab(self):
        new_tab = QWebEngineView()
        new_tab.setUrl(QUrl("https://www.google.com"))
        
        self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentWidget(new_tab)
        
        new_tab.loadFinished.connect(lambda: self.update_url_bar(new_tab))

    def update_url_bar(self, browser):
        url = browser.url().toString()
        self.url_bar.setText(url)

        # Update the tab title with the page title
        title = browser.page().title()
        index = self.tabs.indexOf(browser)
        if index != -1:
            self.tabs.setTabText(index, title)
        
        # Update the URL bar when the page is loaded
        browser.loadFinished.connect(lambda: self.update_url_bar(browser))

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            QMessageBox.warning(self.window, "Warning", "Cannot close the last tab.")

    def search(self,url):
        if url.startswith("http://") or url.startswith("https://"):
            self.browser.setUrl(QUrl(url))
        else:
            self.browser.setUrl(QUrl("https://www.google.com/search?q=" + url))

app = QApplication([])

app.setStyleSheet("""
    QMainWindow {
        background-color: #808080;
    }

    QLineEdit {
        background-color: #C0C0C0;
        color: white;
        border-radius: 5px;
        padding: 5px;
    }
""")

web_browser = PaomWebBrowser()
app.exec_()