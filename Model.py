from CurrentState import CurrentState
from PIL.ExifTags import GPSTAGS
import PIL.Image
import collections


class Model:

    def __init__(self):
        self.currentState = CurrentState()

    def addImgs(self, path_imgs):
        try:
            for img in path_imgs:
                if img in self.currentState.values:
                    print('image {} is already in the list'.format(img))
                    path_imgs.remove(img)
            self.currentState.addNewImgs = path_imgs  # set
            if self.currentState.currentImg == None:
                newImg = self.uploadImg(self.currentState.values[0])
                return [path_imgs, newImg]
            return [path_imgs, None]
        except:
            return

    def deleteAllImgs(self):
        res = self.currentState.remove_all_imgs()
        return res

    def deleteSelectedImgs(self, items):
        path_imgs_del = [i.toolTip() for i in items]
        #se c'è una sola immagine
        if collections.Counter(path_imgs_del) == collections.Counter(self.currentState.values):
            return self.deleteAllImgs()
        #altrimenti
        current_img = self.currentState.currentImg
        img_up = None
        if current_img in path_imgs_del:  # if the current img is deleted, upload the next img
            img_up = self.searchUpImg(path_imgs_del[path_imgs_del.index(current_img):])
            img_up = self.uploadImg(img_up)
        if not path_imgs_del:   #nessuna immagine selezionata
            removed = None
        else:
            removed = self.currentState.remove_imgs(path_imgs_del, items)
        return [img_up, removed]

    def searchUpImg(self, next_partial_imgs_del):
        # trovo l'immagine successiva non cancellata
        for img in next_partial_imgs_del:
            next = self.getNextImg(img)
            if next not in next_partial_imgs_del:
                return next

    def uploadImg(self, path_img):
        if type(path_img) != str:
            path_img = path_img.toolTip()
        exif = self.extractExifData(path_img)
        img = self.currentState.upload_img(path_img, exif)
        return img

    def uploadPreviousImg(self):
        current_img = self.currentState.currentImg
        if current_img != None:
            prev_img = self.getPrevImg(current_img)
            prev_img = self.uploadImg(prev_img)
            return prev_img
        else:
            pass
        return None

    def getPrevImg(self, current_img):
        list = self.currentState.values
        indx_prev = (list.index(current_img) - 1) % len(list)
        prev_img = list[indx_prev]
        return prev_img

    def uploadNextImg(self):
        current_img = self.currentState.currentImg
        if current_img != None:
            next_img = self.getNextImg(current_img)
            next_img = self.uploadImg(next_img)
            return next_img
        else:
            return None

    def getNextImg(self, current_img):
        list = self.currentState.values
        indx_next = (list.index(current_img) + 1) % len(list)
        next_img = list[indx_next]
        return next_img

    def extractExifData(self, path_img):
        try:
            img = PIL.Image.open(path_img)
            self.exif = {PIL.ExifTags.TAGS[k]: v
                         for k, v in img._getexif().items()
                         if k in PIL.ExifTags.TAGS}
            if 'GPSInfo' in self.exif.keys():
                latitude = str(self.getCoordinate(self.exif['GPSInfo'][2], self.exif['GPSInfo'][1]))
                longitude = str(self.getCoordinate(self.exif['GPSInfo'][4], self.exif['GPSInfo'][3]))
                self.exif['GPSInfo'] = str(latitude) + "," + str(longitude) #"https://www.google.com/maps/search/?api=1&query=" + str(latitude) + "," + str(longitude)
            return self.exif
        except:
            return None

    def getCoordinate(self, value, cardinal_point):
        d, m, s = value
        if cardinal_point in ['S', 'W']:
            d = -d
            m = -m
            s = -s
        return d + m / 60.0 + s / 3600.0

    def rotateRight(self):
        current_img = self.currentState.currentImg
        if current_img != None:
            return True
        return False

    def rotateLeft(self):
        current_img = self.currentState.currentImg
        if current_img != None:
            return True
        return False

model = Model()
