from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QLabel, QListWidgetItem
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QIcon
from GuiExifViewer import GuiExifViewer
from Model import model
import sys
from os.path import expanduser
import webbrowser

class ExifViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = GuiExifViewer()
        self.ui.setupUi(self)
        self.initializeExifDataTable()
        self.maps_url = None

        self.ui.button_maps.clicked.connect(self.openMaps)
        self.ui.button_rotateRight.clicked.connect(self.rotateRight)
        self.ui.button_rotateLeft.clicked.connect(self.rotateLeft)
        self.ui.button_previous.clicked.connect(self.uploadPreviousImg)
        self.ui.button_next.clicked.connect(self.uploadNextImg)
        self.ui.button_addImages.clicked.connect(lambda: self.addImgs(
            QFileDialog.getOpenFileNames(self, 'Open file', expanduser("~"), "Image files (*.jpg)")[0]))
        self.ui.button_deleteAllImages.clicked.connect(self.deleteAllImgs)
        self.ui.button_deleteSelectedImages.clicked.connect(
            lambda: self.deleteSelectedImgs(self.ui.listWidget.selectedItems()))
        #doppio click sull'immagine nella lista
        self.ui.listWidget.itemDoubleClicked.connect(lambda: self.uploadImg(self.ui.listWidget.currentItem()))


    def initializeExifDataTable(self):
        self.ui.ExifDataTab.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Exif'))
        self.ui.ExifDataTab.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('Data'))
        self.ui.ExifDataTab.horizontalHeader().setVisible(True)
        self.ui.ExifDataTab.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
        stylesheet = "::section{Background-color:rgb(70,70,70)}"
        self.ui.ExifDataTab.horizontalHeader().setStyleSheet(stylesheet)
        font = self.ui.ExifDataTab.horizontalHeader().font()
        font.setFamily("Dubai Light")
        font.setPointSize(10)
        font.setBold(True)
        self.ui.ExifDataTab.horizontalHeader().setFont(font)
        self.ui.ExifDataTab.setColumnWidth(0, 400)



    #metodi per la visualizzazione nell'interfaccia (View)

    def showImageIntoList(self, img_path):
        #aggiunta dell'immagine o delle immagini alla lista
        for img in img_path:
            icon = QIcon(QPixmap(img))
            item = QListWidgetItem(icon, None)
            item.setToolTip(img)
            self.ui.listWidget.addItem(item)

    def deleteImageIntoListAndPreview(self, sign):
        #rimozione dell'immagine dalla lista
        items = sign[0]
        delCurrentImageUp = sign[1]
        if items == 1:  # flag che indica che devo eliminare tutte le immagini
            self.ui.listWidget.clear()
        else:
            for item in items:
                self.ui.listWidget.takeItem(self.ui.listWidget.row(item))
        if delCurrentImageUp == True:
            self.ui.image.clear()
            self.ui.image.img = None
            self.ui.ExifDataTab.clearContents()
            self.ui.ExifDataTab.setRowCount(0)
            self.ui.image.setText('No image loaded')

    def showImg(self, item_info):
        #mostra l'immagine nell'interfaccia
        path_img = item_info[0]
        indx = item_info[1]
        exif = item_info[2]
        self.ui.image.uploadImg(path_img)
        self.ui.listWidget.clearSelection()
        self.ui.listWidget.setCurrentRow(indx)
        self.showExifData(exif)

    def showExifData(self, exif):
        #mostra i dati exif
        self.ui.ExifDataTab.clearContents()

        if exif == None or len(exif) == 0:
            self.ui.ExifDataTab.setRowCount(1)
            self.ui.ExifDataTab.setItem(0, 0, QtWidgets.QTableWidgetItem('No Exif Data for this image'))
            self.ui.ExifDataTab.setItem(0, 1, QtWidgets.QTableWidgetItem(''))
        else:
            self.ui.ExifDataTab.setRowCount(len(exif))
            items = exif.items()
            is_gps = False
            for i, elem in enumerate(items):
                self.ui.ExifDataTab.setItem(i, 0, QtWidgets.QTableWidgetItem(str(elem[0])))
                self.ui.ExifDataTab.setItem(i, 1, QtWidgets.QTableWidgetItem(str(elem[1])))
                if elem[0] == 'GPSInfo':
                    self.maps_url = 'https://www.google.com/maps/search/?api=1&query=' + elem[1]
                    is_gps = True
            if is_gps == False:
                self.maps_url = None
        self.ui.ExifDataTab.horizontalHeader().setResizeContentsPrecision(-1)



    #metodi che usano il model e applicano i risultati sulla view (controller)

    def rotateRight(self):
        res = model.rotateRight()
        if res:
            self.ui.image.rotateRight()

    def rotateLeft(self):
        res = model.rotateLeft()
        if res:
            self.ui.image.rotateLeft()

    def addImgs(self, imgPaths):
        result = model.addImgs(imgPaths)
        if result != None:
            newElems = result[0]
            newImg = result[1]
            self.showImageIntoList(newElems)
            if newImg != None:
                self.showImg(newImg)

    def uploadPreviousImg(self):
        prevImg = model.uploadPreviousImg()
        if prevImg != None:
            self.showImg(prevImg)

    def uploadNextImg(self):
        nextImg = model.uploadNextImg()
        if nextImg != None:
            self.showImg(nextImg)

    def deleteAllImgs(self):
        allDeleted = model.deleteAllImgs()
        if allDeleted != None:
            self.deleteImageIntoListAndPreview(allDeleted)

    def deleteSelectedImgs(self, items):
        result = model.deleteSelectedImgs(items)
        if result == [1, True]:         # caso in cui tutte le immagini sono state cancellate
            self.deleteImageIntoListAndPreview(result)
        elif result == [None, None]:    # non è stato selezionato nulla
            pass
        else:
            imgUp = result[0]
            removed = result[1]
            if imgUp == None:           #l'immagine eliminata non è quella corrente
                self.deleteImageIntoListAndPreview(removed)
            else:
                self.uploadImg(imgUp[0])
                self.deleteImageIntoListAndPreview(removed)

    def uploadImg(self, imgPath):
        img = model.uploadImg(imgPath)
        self.showImg(img)

    def openMaps(self):
        if self.maps_url != None:
            webbrowser.open(self.maps_url)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ExifViewer()
    window.show()
    sys.exit(app.exec_())
