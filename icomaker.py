# filename icomaker.py
# pip install PyQt5
# pip install pillow
# pip install cairosvg  
# if not working pipe use conda
#conda install -c conda-forge cairosvg


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image
import os
import tempfile
import cairosvg

class IconApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To ICO 256x256")
        self.file = None
        self.temp_png = None  # For SVG conversion
        layout = QVBoxLayout()
        self.label = QLabel("No image")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        for text, func in [("Upload PNG/JPG/SVG", self.load), ("Convert to ICO", self.convert)]:
            b = QPushButton(text)
            b.clicked.connect(func)
            layout.addWidget(b)

        w = QWidget(); w.setLayout(layout); self.setCentralWidget(w)

    def load(self):
        f, _ = QFileDialog.getOpenFileName(self, "Open", "", "Images (*.png *.jpg *.jpeg *.svg)")
        if f:
            ext = os.path.splitext(f)[-1].lower()
            if ext == ".svg":
                self.temp_png = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
                cairosvg.svg2png(url=f, write_to=self.temp_png)
                self.file = self.temp_png
            else:
                self.file = f
            self.label.setPixmap(QPixmap(self.file).scaled(200, 200, Qt.KeepAspectRatio))

    def convert(self):
        if not self.file:
            return
        out, _ = QFileDialog.getSaveFileName(self, "Save ICO", os.path.join(os.path.dirname(self.file), "icon.ico"), "ICO Files (*.ico)")
        if out:
            Image.open(self.file).convert("RGBA").resize((256,256)).save(out, format="ICO")

app = QApplication(sys.argv)
win = IconApp(); win.show()
sys.exit(app.exec_())
