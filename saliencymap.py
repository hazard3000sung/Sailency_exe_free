from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from PyQt5.QtWidgets import *
from scipy import fftpack, ndimage, misc
from scipy.ndimage import uniform_filter
import matplotlib.pyplot as plt
import numpy as np
from skimage import img_as_float
from skimage.io import imread
from skimage.color import rgb2gray
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # left, top, width, height
        self.left = 10
        self.top = 10
        self.width = 260
        self.height = 200

        self.initUI()

    def initUI(self):


        self.setWindowTitle("Image Sailous")
        self.setWindowIcon(QIcon('title.png'))
        self.setGeometry(self.left,self.top,self.width,self.height)

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.resize(630,390)

        self.button = QPushButton('Start Analyze',self)
        self.button.clicked.connect(self.plot)
        self.button.setToolTip('enjoy your program')
        self.button.move(10,10)
        self.button.resize(240,120)

        self.button1 = QPushButton('EXIT',self)
        self.button1.move(10,140)
        self.button1.setToolTip('Quit Program')
        self.button1.resize(240,20)
        self.button1.clicked.connect(QCoreApplication.instance().quit)

        self.button2 = QPushButton('Load 1#',self)
        self.button2.move(10,170)
        self.button2.resize(240,20)
        self.button2.setToolTip('Load Data')
        self.button2.clicked.connect(self.browseSlot)



        self.show()

    def plot(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fname = QtWidgets.QFileDialog.getOpenFileName(None,"File load--()--File load",
                                                        "/","All Files(*);;",'Image Files(*.png *.jpg)',
                                                        options=options)
        image = img_as_float(rgb2gray(imread(fname[0])))

        fft = fftpack.fft2(image)

        logAmplitude = np.log(np.abs(fft))

        phase = np.angle(fft)
        avgLogAmp = uniform_filter(logAmplitude, size=1, mode="nearest")
        spectralResidaul = logAmplitude - avgLogAmp

        saliencyMap = np.abs(fftpack.ifft2(np.exp(spectralResidaul + 1j * phase))) ** 2
        saliencyMap = ndimage.gaussian_filter(saliencyMap, sigma=20)

        plt.imshow(saliencyMap)
        plt.axis('off')
        plt.xlim('off')
        plt.ylim('off')
        plt.show()

    def browseSlot(self):
        self.abel = QLabel()
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _=QtWidgets.QFileDialog.getOpenFileName(None,
                                                          "QFileDialog.getOpenFileName()",
                                                          "",
                                                          "All Files(*);;",
                                                          options=options)
        self.abel.setPixmap(QPixmap(filename))

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
