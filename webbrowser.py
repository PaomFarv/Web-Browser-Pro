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
        self.url_bar.focusInEvent = self.clear_url_bar  # Clears on focus

        self.url_bar.returnPressed.connect(self.search)  # Trigger search on Enter

        self.search_button = QPushButton("⌕")
        self.search_button.setFont(QFont("Arial", 15))
        self.search_button.setMinimumHeight(30)
        self.search_button.clicked.connect(self.search)

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

        self.add_tab_button = QPushButton("New Tab")
        self.add_tab_button.setFont(QFont("Arial", 12))
        self.add_tab_button.setMinimumHeight(30)

        # Add all buttons to the horizontal layout
        self.horizontal_layout.addWidget(self.url_bar)
        self.horizontal_layout.addWidget(self.search_button)
        self.horizontal_layout.addWidget(self.home_button)
        self.horizontal_layout.addWidget(self.refresh_button)
        self.horizontal_layout.addWidget(self.backward_button)
        self.horizontal_layout.addWidget(self.forward_button)
        self.horizontal_layout.addWidget(self.add_tab_button)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        self.layout.addLayout(self.horizontal_layout)
        self.layout.addWidget(self.tabs)
        self.window.setLayout(self.layout)

        self.add_new_tab()  # Add initial tab
        self.window.show()

        # Button actions
        self.backward_button.clicked.connect(lambda: self.tabs.currentWidget().back())
        self.forward_button.clicked.connect(lambda: self.tabs.currentWidget().forward())
        self.refresh_button.clicked.connect(lambda: self.tabs.currentWidget().reload())
        self.home_button.clicked.connect(lambda: self.tabs.currentWidget().setUrl(QUrl("https://www.google.com")))
        self.add_tab_button.clicked.connect(self.add_new_tab)

    def clear_url_bar(self, event):
        self.url_bar.clear()
        QLineEdit.focusInEvent(self.url_bar, event)

    def add_new_tab(self):
        new_tab = QWebEngineView()
        new_tab.setUrl(QUrl("https://www.google.com"))

        index = self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentWidget(new_tab)

        new_tab.loadFinished.connect(lambda: self.update_url_bar(new_tab))

    def update_url_bar(self, tab):
        url = tab.url().toString()
        self.url_bar.setText(url)

        title = tab.page().title()
        index = self.tabs.indexOf(tab)
        if index != -1:
            self.tabs.setTabText(index, title)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            QMessageBox.warning(self.window, "Warning", "Cannot close the last tab.")

    def search(self):
        url = self.url_bar.text()
        current_browser = self.tabs.currentWidget()
        
        if isinstance(current_browser, QWebEngineView):
            if url.startswith("http://") or url.startswith("https://"):
                current_browser.setUrl(QUrl(url))
            else:
                current_browser.setUrl(QUrl(f"https://www.google.com/search?q={url}"))

app = QApplication([])

app.setStyleSheet("""
    QWidget {
        background-color: #f0f2f5;
        font-family: "Segoe UI", "Arial", sans-serif;
        font-size: 14px;
        color: #2c2c2c;
    }

    QLineEdit {
        background-color: #ffffff;
        border: 1.5px solid #d0d0d0;
        border-radius: 8px;
        padding: 6px 10px;
        font-size: 14px;
        color: #2c2c2c;
        selection-background-color: #0078d7;
    }

    QLineEdit:focus {
        border: 1.5px solid #0078d7;
        background-color: #ffffff;
    }

    QPushButton {
        background-color: #e4e6eb;
        border: none;
        padding: 8px 14px;
        border-radius: 8px;
        color: #2c2c2c;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    QPushButton:hover {
        background-color: #0078d7;
        color: #ffffff;
    }

    QPushButton:pressed {
        background-color: #005ea6;
    }

    QTabWidget::pane {
        border: 1.5px solid #d0d0d0;
        border-radius: 8px;
        margin-top: 4px;
        background-color: #ffffff;
    }

    QTabBar::tab {
        background: #e4e6eb;
        border: 1px solid #cccccc;
        border-bottom: none;
        padding: 8px 18px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        margin-right: 2px;
        color: #2c2c2c;
    }

    QTabBar::tab:selected {
        background: #ffffff;
        border: 1.5px solid #0078d7;
        border-bottom: 2px solid #ffffff;
        color: #0078d7;
        font-weight: bold;
    }

    QTabBar::tab:hover {
        background-color: #d9e7f8;
    }

    QWebEngineView {
        border: none;
        background-color: #ffffff;
        border-radius: 0px;
    }
""")


web_browser = PaomWebBrowser()
app.exec_()
