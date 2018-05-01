import sys
import string

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
# from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap

import Data
import res


class Main(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi("Future.ui", self)
        self.ui.setFixedSize(self.ui.width(), self.ui.height())
        # window_flags = QtCore.Qt.WindowFlags()
        # window_flags |= QtCore.Qt.WindowMinimizeButtonHint
        # window_flags |= QtCore.Qt.WindowCloseButtonHint
        # self.setWindowFlags(window_flags)
        self.setWindowTitle("Future Library")
        self.data = Data.Data()  # creating obj for all data

        self.__currentGame = None

        self.__flag = False
        self.__text = str()

        self.__imgPath = None
        self.__gameName = None
        self.__gameDesc = None

        self.ui.MainFrame.setStyleSheet("QFrame {background-image: url(:/data/sky);}")
        self.ui.ResFrame.setStyleSheet("QFrame {background-image: url(:/data/sky);}")
        self.ui.AddFrame.setStyleSheet("QFrame#AddFrame {background-image: url(:/data/sky);}")
        self.ui.GameFrame.setStyleSheet("QFrame {background-image: url(:/data/sky);}")
        self.ui.ResFrame.hide()
        self.ui.GameFrame.hide()
        self.ui.AddFrame.hide()
        self.ui.SearchButton.setEnabled(False)
        self.ui.AddSave.setEnabled(False)
        self.ui.SearchField.setMaxLength(25)
        self.ui.AddGameNameField.setMaxLength(25)
        self.ui.AddGameImg.hide()

        self.ui.AddGameButton.clicked.connect(self.changeFormAdd)
        self.ui.AddCancel.clicked.connect(self.cancelAdd)
        self.ui.AddGameNameField.textChanged.connect(self.isSave)
        self.ui.AddGameDescField.textChanged.connect(self.isSave)
        self.ui.AddGamePicButton.clicked.connect(self.chImg)
        self.ui.AddSave.clicked.connect(self.gameSave)
        self.ui.AllButton.clicked.connect(self.changeFormAll)
        self.ui.FavButton.clicked.connect(self.changeFormFav)
        self.ui.SearchField.textChanged.connect(self.textChanged)
        self.ui.SearchButton.clicked.connect(self.changeFormSearch)
        self.ui.ResBack.clicked.connect(self.changeMainForm)
        # self.ui.ResList.itemEntered.connect(self.itemEntered)
        self.ui.ResList.itemClicked.connect(self.openGameInfo)
        self.ui.GameBack.clicked.connect(self.changeResForm)
        self.ui.AddFavButton.clicked.connect(self.changeFavState)

    def getGamesList(self, data):
        """
        Filling in the list game objects
        :param data: list of games
        """
        self.ui.ResList.clear()
        for i in data:
            self.ui.ResList.addItem("#{} {}".format(str(i.id), i.name))

    def cancelAddMessage(self):
        """
        'Cancelling add game action' message
        :return: 'cancelled or not' state
        """
        self.cancelMessage = QMessageBox()
        self.cancelMessage.setStyleSheet("background-color: white;")
        self.cancelMessage.setIcon(QMessageBox.Warning)
        self.cancelMessage.setText("Are you sure you want to cancel the operation?")
        self.cancelMessage.setWindowTitle("Achtung")
        okButton = self.cancelMessage.addButton('OK', QMessageBox.AcceptRole)
        self.cancelMessage.addButton('Cancel', QMessageBox.RejectRole)
        self.cancelMessage.exec_()
        if self.cancelMessage.clickedButton() == okButton:
            return 1
        else:
            return 0

    def cancelAdd(self):
        """
        Cancelling add game action
        """
        if not self.__flag:
            if self.ui.AddGameNameField.text() or self.ui.AddGameDescField.toPlainText() or \
                    self.ui.AddGameImg.isVisible():
                x = self.cancelAddMessage()
                if x != 1:
                    return
        self.__flag = False
        self.ui.AddFrame.hide()
        self.ui.AddGameImg.hide()
        self.ui.AddSave.setEnabled(False)
        self.ui.AddGameNameField.clear()
        self.ui.AddGameDescField.clear()
        self.ui.MainFrame.show()

    def chImg(self):
        """Getting imge for new game"""
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open file', '/home', 'Graphic Files (*.jpg *.png)')
        if fileName:
            print(fileName)
            self.__imgPath = fileName
            self.ui.AddGameImg.setPixmap(QPixmap(fileName))
            self.ui.AddGameImg.show()
            self.isSave()

    def isSave(self):
        """Checks if game can be save"""
        text = self.ui.AddGameNameField.text()
        if text and text.startswith(tuple(string.ascii_letters)) and self.ui.AddGameDescField.toPlainText() and \
                self.ui.AddGameImg.isVisible():
            if len(text) >= 3 and len(self.ui.AddGameDescField.toPlainText()) > 15:
                self.ui.AddSave.setEnabled(True)
                return
        self.ui.AddSave.setEnabled(False)

    def gameSave(self):
        """Saves game"""
        name = self.ui.AddGameNameField.text()
        desc = self.ui.AddGameDescField.toPlainText()
        image = self.__imgPath
        self.data.addGame(name, desc, image)
        self.gameAdded = QMessageBox()
        self.gameAdded.setStyleSheet("background-color: white;")
        self.gameAdded.setIcon(QMessageBox.Information)
        self.gameAdded.setText("Game added successfully")
        self.gameAdded.setWindowTitle("Yaay")
        self.gameAdded.setStandardButtons(QMessageBox.Ok)
        self.gameAdded.exec_()
        self.__flag = True
        self.cancelAdd()

    def changeFormAdd(self):
        """Changes frame to AddFrame"""
        self.ui.MainFrame.hide()
        print("Add")
        self.ui.AddFrame.show()

    def changeFormAll(self):
        """Changes frame to ResFrame (all filter)"""
        self.ui.MainFrame.hide()
        print("All")
        data = self.data.list
        self.getGamesList(data)
        self.ui.ResFrame.show()
        self.ui.ResName.setText("All games")

    def changeFormFav(self):
        """Changes frame to ResFrame (favorites filter)"""
        self.ui.MainFrame.hide()
        print("Favorites")
        data = self.data.showFav()
        self.getGamesList(data)
        self.ui.ResFrame.show()
        self.ui.ResName.setText("Favorites")

    def textChanged(self):
        """Checks if search can be performed"""
        text = self.ui.SearchField.text()
        if text and text.startswith(tuple(string.ascii_letters)):
            if len(text) >= 3:
                self.ui.SearchButton.setEnabled(True)
                return
        self.ui.SearchButton.setEnabled(False)

    def changeFormSearch(self):
        """Changes frame to ResFrame (search filter)"""
        self.__text = self.ui.SearchField.text()
        self.ui.SearchField.clear()
        self.ui.MainFrame.hide()
        print("Search '", self.__text, "'", sep="")
        data = self.data.showSearch(self.__text)
        self.getGamesList(data)
        self.ui.ResFrame.show()
        self.ui.ResName.setText("Search results")

    def changeMainForm(self):
        """Changes frame to MainFrame"""
        self.ui.ResFrame.hide()
        print("Main")
        self.ui.MainFrame.show()

    # def itemEntered(self, item):
    #     item.setCursor(QtCore.Qt.PointingHandCursor)

    def openGameInfo(self, item):
        """Changes frame to GameFrame"""
        text = item.text()
        print("Game:", text)
        text = text[1:text.index(" ")]
        self.__currentGame = self.data.gameObject(int(text))
        self.ui.ResFrame.hide()
        self.ui.GameName.setText(self.__currentGame.name)
        self.ui.GameDescription.setText(self.__currentGame.description)
        if self.__currentGame.isFavorite:
            self.ui.FavSign.setText("Remove from favorites")
        else:
            self.ui.FavSign.setText("Add to favorites")
        self.ui.GamePicture.setPixmap(QPixmap(self.__currentGame.image))
        self.ui.GameFrame.show()

    def changeResForm(self):
        """Changes frame to ResFrame (back from GameFrame)"""
        self.ui.GameFrame.hide()
        if self.ui.ResName.text() == "Favorites":
            data = self.data.showFav()
            self.getGamesList(data)
        self.ui.ResFrame.show()

    def changeFavState(self):
        """Changes game 'favorite' state"""
        if self.__currentGame.isFavorite:
            self.__currentGame.isFavorite = False
            self.data.jsonUpdateFav(self.__currentGame, False)
            self.ui.FavSign.setText("Add to favorites")
        else:
            self.__currentGame.isFavorite = True
            self.data.jsonUpdateFav(self.__currentGame, True)
            self.ui.FavSign.setText("Remove from favorites")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
