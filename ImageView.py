from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import Qt, QSize


class ImageView(QLabel):

    def __init__(self, img_w):
        QLabel.__init__(self, img_w)
        self.img = None

    def uploadImg(self, path_img):
        self.img = QPixmap(path_img)
        self.setMax = False
        self.resizeImg()

    def resizeImg(self):
        if self.img.width() > self.img.height():
            img_resized = self.img.scaledToWidth(512)
        else:
            img_resized = self.img.scaledToHeight(512)
        self.setMaximumSize(img_resized.width(), img_resized.height())
        self.setPixmap(img_resized)
        self.adjustSize()
        self.setMax = True

    def rotateRight(self):
        self.img = self.img.transformed(QTransform().rotate(90))
        self.resizeImg()

    def rotateLeft(self):
        self.img = self.img.transformed(QTransform().rotate(-90))
        self.resizeImg()

    #ridimensionamento dell'immagine con la finestra
    def resizeEvent(self, event):
        if self.img != None and self.setMax == True:
            self.setPixmap(self.img.scaled(QSize(self.size().width(), self.size().height()), Qt.KeepAspectRatio))
        super().resizeEvent(event)
