from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import urllib.request

class Downloader(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        # set layout to vertical
        layout = QVBoxLayout()

        # assign elements
        self.url = QLineEdit()
        self.save_location = QLineEdit()
        self.progress = QProgressBar()
        download = QPushButton("Download")
        browse = QPushButton("Browse")

        # adjust elements descriptions for text boxes
        self.url.setPlaceholderText("URL")
        self.save_location.setPlaceholderText("File Save Location")

        # change progress bar to 0% and have percent in center
        self.progress.setValue(0)
        self.progress.setAlignment(Qt.AlignCenter)

        # assign elements to layout for application
        layout.addWidget(self.url)
        layout.addWidget(self.save_location)
        layout.addWidget(browse)
        layout.addWidget(self.progress)
        layout.addWidget(download)

        # set layout to self
        self.setLayout(layout)
        
        # change title of app & remove auto-focus on text-box "save_location"
        self.setWindowTitle("QtDownloader")
        self.setFocus()

        # event handler for clicking download button
        download.clicked.connect(self.download)
        browse.clicked.connect(self.browse_file)

    def browse_file(self):
        save_file = QFileDialog.getSaveFileName(self, caption="Save File As", directory=".", filter="All Files (*.*)")
        self.save_location.setText(QDir.toNativeSeparators(save_file))

    def download(self):
        url = self.url.text()
        save_location = self.save_location.text()

        try: 
            urllib.request.urlretrieve(url, save_location, self.report)
        except Exception:
            QMessageBox.warning(self, "warning", "The Download Failed")
            return
        
        QMessageBox.information(self, "Information", "The Download is Complete")

        self.progress.setValue(0)
        self.url.setText("")
        self.save_location.setText("")


    def report(self, blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percentage = readsofar * 100 / totalsize
            self.progress.setValue(int(percentage))

app = QApplication(sys.argv)
dialog = Downloader()
dialog.show()
app.exec_()