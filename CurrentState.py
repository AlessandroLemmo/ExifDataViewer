from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty


class CurrentState:

    def __init__(self):
        super().__init__()
        self.listElem = []
        self.currentImg = None


    @pyqtProperty(object)
    def values(self):
        return self.listElem

    @values.setter
    def addNewImgs(self, newElems):
        for elem in newElems:
            self.listElem.append(elem)

    def remove_imgs(self, path_imgs, items):
        current = False
        for elem in path_imgs:
            self.listElem.remove(elem)
            if elem == self.currentImg:
                current = True
                self.currentImg = None
        return [items, current]

    def remove_all_imgs(self):
        self.listElem = []
        self.currentImg = None
        return [1, True]

    def upload_img(self, path_img, exif):
        self.currentImg = path_img
        indx = self.listElem.index(self.currentImg)
        return [self.currentImg, indx, exif]

