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

        self.search_button = QPushButton("⌕")
        self.search_button.setFont(QFont("Arial", 12))
        self.search_button.setMinimumHeight(30)
        
        self.refresh_button = QPushButton("↻")
        self.refresh_button.setFont(QFont("Arial", 12))
        self.refresh_button.setMinimumHeight(30)
        
        self.backward_button = QPushButton("<")  
        self.backward_button.setFont(QFont("Arial", 12))
        self.backward_button.setMinimumHeight(30)

        self.forward_button = QPushButton(">")
        self.forward_button.setFont(QFont("Arial", 12))
        self.forward_button.setMinimumHeight(30)
        
        self.horizontal_layout.addWidget(self.url_bar)
        self.horizontal_layout.addWidget(self.search_button)
        self.horizontal_layout.addWidget(self.refresh_button)
        self.horizontal_layout.addWidget(self.backward_button)
        self.horizontal_layout.addWidget(self.forward_button)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.browser.setStyleSheet("background-color: #ffffff; border-radius: 5px; padding: 5px;")

        self.search_button.clicked.connect(lambda: self.search(self.url_bar.text()))
        self.backward_button.clicked.connect(self.browser.back)
        self.forward_button.clicked.connect(self.browser.forward)
        self.refresh_button.clicked.connect(self.browser.reload)

        self.layout.addLayout(self.horizontal_layout)
        self.layout.addWidget(self.browser)

        self.window.setLayout(self.layout)
        self.window.show()

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