from PyQt5 import QtWidgets
from Ui_mainWindow import Ui_MainWindow
from PyQt5.QtGui import QImage,QPixmap,QStandardItemModel
from PyQt5.QtCore import QByteArray,QFile
from PyQt5.QtCore import Qt,QDir,QItemSelectionModel
import sys,os

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.W = 1920
        self.H = 1080
        self.IMAGESIZE = self.W*self.H*8
        self.pic = None
        self.picPath = None
        self.pixmap = None
        self.dirModel = QtWidgets.QFileSystemModel(self)
        self.fileModel = QtWidgets.QFileSystemModel(self)
        self.isInterlacing = False

        self.ui.actionTest.triggered.connect(self.test)
        self.ui.actionOpen_Folder.triggered.connect(self.openDir)
        self.ui.treeView.clicked.connect(self.treeViewClicked)
        self.checkbox = QtWidgets.QCheckBox()
        self.checkbox.setText("1080i        ")
        self.ui.statusbar.addPermanentWidget(self.checkbox)
        self.checkbox.stateChanged.connect(self.checkboxClicked)
        # override imageLabel resizeEvent to update pixmap
        self.ui.imageLabel.resizeEvent = self.imageLabelResizeEvent

    def openDir(self,MainWindow):
        "Open folder selecting dialog"
        dialog = QtWidgets.QFileDialog(self)
        path = dialog.getExistingDirectory(None)
        self.dirModel.setRootPath("/")
        self.dirModel.setFilter(QDir.NoDotAndDotDot|QDir.AllDirs)
        self.ui.treeView.setModel(self.dirModel)
        self.ui.treeView.setRootIndex(self.dirModel.index(path))
        self.fileModel.setRootPath(path)
        self.ui.listView.setModel(self.fileModel)
        self.ui.listView.setRootIndex(self.fileModel.index(path))
        self.ui.listView.selectionModel().currentChanged.connect(self.listViewMoved)

    def checkboxClicked(self,state):
        self.isInterlacing = (state==Qt.Checked)
        self.updateImage()
        print(self.isInterlacing)

    def treeViewClicked(self,index):
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        print(path)
        self.ui.listView.setRootIndex(self.fileModel.index(path))

    def listViewMoved(self,index):
        path = self.fileModel.fileInfo(index).absoluteFilePath()
        print(path)
        self.showImage(path)

    def showImage(self, path):
        "Show image on graphics view"
        self.picPath = path
        self.updateImage()
        
    def updateImage(self):
        if(self.picPath):
            self.setWindowTitle(os.path.basename(self.picPath)+" [Raw Image Viewer]")
            self.ui.statusbar.showMessage(self.picPath)
            picFile = QFile(self.picPath)
            if(not picFile.open(QFile.ReadOnly)):
                return
            if(self.isInterlacing):
                self.pic = QImage(picFile.read(self.IMAGESIZE//2),self.W,self.H//2,QImage.Format_Grayscale8)
            else:
                self.pic = QImage(picFile.read(self.IMAGESIZE),self.W,self.H,QImage.Format_Grayscale8)
            self.pixmap = QPixmap.fromImage(self.pic)
            self.ui.imageLabel.setPixmap(self.pixmap.scaled(self.ui.imageLabel.width(),self.ui.imageLabel.height(),Qt.KeepAspectRatio))
        
    def imageLabelResizeEvent(self,event):
        "Override the resize event"
        #resize image label
        self.updateImage()

    def test(self,MainWindow):
        print(self.ui.listView.selectionModel())

        
        
        

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())