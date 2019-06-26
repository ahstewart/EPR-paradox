#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 10:28:30 2018

@author: andrew
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 10:06:09 2018

@author: andrew
"""

import quant
import sys
from PyQt4 import QtGui, QtCore
import serial
import os
import struct
import numpy as np

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#initialize lists that will hold the total photon counts
sumA = []
sumB = []
sumC = []

#open serial port
#ser = serial.Serial('COM1', 19200)

#this is GUI class, it adds functionality to the QtDesigner script quant.Ui which builds the actual GUI structure
class gui(QtGui.QMainWindow, quant.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.Exit)    #connect Exit btn to a qutting method
        self.pushButton.clicked.connect(self.plot)      #connect Plot btn to plotting method
        self.figure = Figure()                          #create matplotlib figures in each of the windows created by quant.Ui
        self.canvas = FigureCanvas(self.figure)
        self.figure2 = Figure()
        self.canvas2 = FigureCanvas(self.figure2)
        self.figure3 = Figure()
        self.canvas3 = FigureCanvas(self.figure3)
        self.scene = QtGui.QGraphicsScene()
        self.scene.addWidget(self.canvas)
        self.scene2 = QtGui.QGraphicsScene()
        self.scene2.addWidget(self.canvas2)
        self.scene3 = QtGui.QGraphicsScene()
        self.scene3.addWidget(self.canvas3)
        self.graphicsView.setScene(self.scene)
        self.graphicsView_2.setScene(self.scene2)
        self.graphicsView_3.setScene(self.scene3)
        self.pushButton_5.clicked.connect(self.copy1)   #connect each of the 16 little btns to their respective methods
        self.pushButton_6.clicked.connect(self.copy2)
        self.pushButton_7.clicked.connect(self.copy3)
        self.pushButton_8.clicked.connect(self.copy4)
        self.pushButton_9.clicked.connect(self.copy5)
        self.pushButton_10.clicked.connect(self.copy6)
        self.pushButton_11.clicked.connect(self.copy7)
        self.pushButton_12.clicked.connect(self.copy8)
        self.pushButton_13.clicked.connect(self.copy9)
        self.pushButton_14.clicked.connect(self.copy10)
        self.pushButton_15.clicked.connect(self.copy11)
        self.pushButton_16.clicked.connect(self.copy12)
        self.pushButton_17.clicked.connect(self.copy13)
        self.pushButton_18.clicked.connect(self.copy14)
        self.pushButton_19.clicked.connect(self.copy15)
        self.pushButton_20.clicked.connect(self.copy16)
        self.pushButton_2.clicked.connect(self.calculate)   #connect Calculate btn to the calculate method
        self.pushButton_4.clicked.connect(self.reset)       #connect Reset btn to the reset method
        self.timer = QtCore.QTimer()                        #create a timer object so that the plot can be refreshed
        self.timer.timeout.connect(self.plot)               #connect timer object to plotting method
        
    def Exit(self):
        sys.exit()
        
    def plot(self):
        t = int(self.lineEdit.text())   #read user input for plot refresh rate
        loop = t * 100
        data = []
        A = []
        B = []
        C = []
        for i in range(t):
#            while ser.read()[0] != 255:     #wait until there is a complete set of readbale data
#                pass
#            s = ser.read(41)
            s = os.urandom(41)
            a = list(struct.unpack('41B', s))   #convert bytes into string of values
            for j in range(len(a)):
                a[j] = str(bin(a[j]))[2:]
            data.append(a)
        for i in range(len(data)):
            A.append(int(''.join(data[i][1:5]), 2))     #split data into photon counts, with C = coincidences
            B.append(int(''.join(data[i][6:10]), 2))
            C.append(int(''.join(data[i][21:25]), 2))
        sumA.append(sum(A))                             #add counts for current interval to total
        sumB.append(sum(B))
        sumC.append(sum(C))
        ax = self.figure.add_subplot(111, position=[.3,.2,.45,.6])      #create axes
        ax2 = self.figure2.add_subplot(111, position=[.3,.2,.45,.6])
        ax3 = self.figure3.add_subplot(111)
        ax.clear()                #clear the previous plot
        ax2.clear()
        ax3.clear()
        ax.plot(sumA)             #plot total counts/coincidences
        ax2.plot(sumB)
        ax3.plot(sumC)
        self.canvas.draw()        #render the plots on the screen
        self.canvas2.draw()
        self.canvas3.draw()
        self.lcdNumber.display(sum(C))       #display coincidences in the LCD number widget
        if self.pushButton_4.isEnabled():               #check whether Reset btn has been pressed
            self.timer.singleShot(loop, self.plot)      #run self.plot again after loop miliseconds have passed
        else:
            ax.cla()                    #if Reset btn has been pressed, clear plots and total photon counts
            ax2.cla()
            ax3.cla()
            self.canvas.draw()
            self.canvas2.draw()
            self.canvas3.draw()
            self.lcdNumber.display(0)
            self.pushButton_4.setEnabled(True)
            del sumA[:]
            del sumB[:]
            del sumC[:]
        
    def calculate(self):                        #method that calculates S and dS and then displays them in the respective text boxes
        one = int(self.lineEdit_4.text())
        two = int(self.lineEdit_5.text())
        three = int(self.lineEdit_6.text())
        four = int(self.lineEdit_7.text())
        five = int(self.lineEdit_9.text())
        six = int(self.lineEdit_10.text())
        seven = int(self.lineEdit_8.text())
        eight = int(self.lineEdit_13.text())
        nine = int(self.lineEdit_12.text())
        ten = int(self.lineEdit_15.text())
        eleven = int(self.lineEdit_11.text())
        twelve = int(self.lineEdit_14.text())
        thirteen = int(self.lineEdit_16.text())
        fourteen = int(self.lineEdit_17.text())
        fifteen = int(self.lineEdit_18.text())
        sixteen = int(self.lineEdit_19.text())
        Sum = float(one+two+three+four+five+six+seven+eight+nine+ten+eleven+twelve+thirteen+fourteen+fifteen+sixteen)
        Num = float(one+four-two-three+five+eight-six-seven+nine+twelve-ten-eleven+thirteen+sixteen-fourteen-fifteen)
        d1 = one * (float(Num-one+1)/float(Sum-one+1))**2
        d4 = four * (float(Num-four+1)/float(Sum-four+1))**2
        d3 = three * (float(Num+three-1)/float(Sum-three+1))**2
        d2 = two * (float(Num+two-1)/float(Sum-two+1))**2
        d5 = five * (float(Num-five+1)/float(Sum-five+1))**2
        d8 = eight * (float(Num-eight+1)/float(Sum-eight+1))**2
        d6 = six * (float(Num+six-1)/float(Sum-six+1))**2
        d7 = seven * (float(Num+seven-1)/float(Sum-seven+1))**2
        d9 = nine * (float(Num-nine+1)/float(Sum-nine+1))**2
        d12 = twelve * (float(Num-twelve+1)/float(Sum-twelve+1))**2
        d10 = ten * (float(Num+ten-1)/float(Sum-ten+1))**2
        d11 = eleven * (float(Num+eleven-1)/float(Sum-eleven+1))**2
        d13 = thirteen * (float(Num-thirteen+1)/float(Sum-thirteen+1))**2
        d16 = sixteen * (float(Num-sixteen+1)/float(Sum-sixteen+1))**2
        d14 = fourteen * (float(Num+fourteen-1)/float(Sum-fourteen+1))**2
        d15 = fifteen * (float(Num+fifteen-1)/float(Sum-fifteen+1))**2
        E1 = float(nine+twelve-ten-eleven)/float(nine+twelve+ten+eleven)
        E2 = float(thirteen+sixteen-fourteen-fifteen)/float(thirteen+sixteen+fourteen+fifteen)
        E3 = float(one+four-two-three)/float(one+four+two+three)
        E4 = float(five+eight-six-seven)/float(five+eight+six+seven)
        S = E1-E2+E3+E4
        S = "%.5f" % (S)
        dS = np.sqrt(d1+d2+d3+d4+d5+d6+d7+d8+d9+d10+d11+d12+d13+d14+d15+d16)
        dS = "%.5f" % (dS)
        self.lineEdit_2.setText(S)
        self.lineEdit_3.setText(dS)
        
    def reset(self):                            #changes the value of the Reset btn so that the plots can be cleared
        self.pushButton_4.setEnabled(False)
        
    def copy1(self):        #these methods all just copy the current value of the LCD number to the respective numbered text boxes
        self.lineEdit_4.setText(str(int(self.lcdNumber.value())))
    
    def copy2(self):
        self.lineEdit_5.setText(str(int(self.lcdNumber.value())))
        
    def copy3(self):
        self.lineEdit_6.setText(str(int(self.lcdNumber.value())))
        
    def copy4(self):
        self.lineEdit_7.setText(str(int(self.lcdNumber.value())))
        
    def copy5(self):
        self.lineEdit_9.setText(str(int(self.lcdNumber.value())))
        
    def copy6(self):
        self.lineEdit_10.setText(str(int(self.lcdNumber.value())))
        
    def copy7(self):
        self.lineEdit_8.setText(str(int(self.lcdNumber.value())))
        
    def copy8(self):
        self.lineEdit_13.setText(str(int(self.lcdNumber.value())))
        
    def copy9(self):
        self.lineEdit_12.setText(str(int(self.lcdNumber.value())))
        
    def copy10(self):
        self.lineEdit_15.setText(str(int(self.lcdNumber.value())))
        
    def copy11(self):
        self.lineEdit_11.setText(str(int(self.lcdNumber.value())))
        
    def copy12(self):
        self.lineEdit_14.setText(str(int(self.lcdNumber.value())))
        
    def copy13(self):
        self.lineEdit_16.setText(str(int(self.lcdNumber.value())))
        
    def copy14(self):
        self.lineEdit_17.setText(str(int(self.lcdNumber.value())))
        
    def copy15(self):
        self.lineEdit_18.setText(str(int(self.lcdNumber.value())))
        
    def copy16(self):
        self.lineEdit_19.setText(str(int(self.lcdNumber.value())))
    
def run():          #runs the GUI
    app = QtGui.QApplication(sys.argv)
    GUI = gui()
    GUI.show()
    app.exec_()

if __name__ == "__main__":
    run()
        