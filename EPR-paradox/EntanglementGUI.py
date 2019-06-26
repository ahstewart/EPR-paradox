import tkinter as tk
import numpy as np
from queue import Queue
import threading
import serial
from tkinter import messagebox
import matplotlib.pyplot as plt

# The program process all GUI interaction in the main thread
# and collects data in a separate thread.

# This part create the data collecting thread.
# The data is stored in a queue, which is shared between both threads.
class dataThread(threading.Thread):
    
    def __init__(self, ser, aQ, bQ, coincidenceQ, trialsQ, exitFlagQ):
        threading.Thread.__init__(self)
        self.exitFlag = True
        
    def run(self):
        while self.exitFlag:
            # The user input duration of collection.
            # The number is shared between threads via a queue
            if not trialsQ.empty():
                self.trials = int(trialsQ.get())
            else:
                self.trials = self.trials
            if not exitFlagQ.empty():
                self.exitFlag = exitFlagQ.get()
            else:
                self.exitFlag = self.exitFlag
            
            # The program collect a set of 41 numbers
            # and extract the value of A, B, and coincidence
            data = np.zeros((self.trials, 41))
            a = 0
            b = 0
            c = 0
            for i in range(self.trials):
                while ser.read()[0] != 255:
                    ser.read()
                r = ser.read(41)
                for j in range(41):
                    data[i][j] = r[j]
            for i in range(self.trials):
                a = a + data[i][0] + (256*data[i][1]) + (256**2*data[i][2]) + (256**3*data[i][3])
                b = b + data[i][5] + (256*data[i][6]) + (256**2*data[i][7]) + (256**3*data[i][8])
                c = c + data[i][20] + (256*data[i][21]) + (256**2*data[i][22]) + (256**3*data[i][23])
            # The data collecting thread puts the new data in the shared queue
            # The number will be used by the main thread
            aQ.put(a)
            bQ.put(b)
            coincidenceQ.put(c)
        # serial port is closed when the thread ends.
        # The serial port closes when the data collecting threads terminates
        # The data collecting thread is terminated by the main thread
        ser.close()
        
# This part is the main thread.
# The main thread creates 
if __name__ == "__main__":
    
    # Set up queues through which data will be shared between threads
    coincidenceQ = Queue()
    coincidenceQ.put(0)
    coincidenceQ.put(0)
    
    aQ = Queue()
    aQ.put(0)
    aQ.put(0)
    
    bQ = Queue()
    bQ.put(0)
    bQ.put(0)
    
    trialsQ = Queue()
    trialsQ.put(10)
    
    exitFlagQ = Queue()
    
    # Open serial port
    ser = serial.Serial('COM3', 19200)
    
    # Initialize a new thread object to collect data
    collection = dataThread(ser, aQ, bQ, coincidenceQ, trialsQ, exitFlagQ)
    
    # Set up the window
    root = tk.Tk()
    root.title("Entanglement")
    
    frame = tk.Frame(root)
    frame.grid()
    frame.columnconfigure(3, minsize=100)
    frame.rowconfigure(0, minsize=50)
    frame.rowconfigure(1, minsize=20)
    frame.rowconfigure(2, minsize=100)
    frame.rowconfigure(3, minsize=100)
    
    coincidenceLabel = tk.Label(frame, text="0", font='size, 25')
    coincidenceLabel.grid(row=15, column=2, rowspan=3)
    
    A = np.zeros(1)
    B = np.zeros(1)
    C = np.zeros(1)
    t = np.zeros(1)
    
    # Update the window every time a new coincidence number is collected
    def refresher():
        if not coincidenceQ.empty():
            coincidenceLabel['text'] = str(coincidenceQ.get())
        root.after(1000, refresher)
    refresher()
    
    label1 = tk.Label(frame, text="Data Visualization", font='size, 8', anchor='nw')
    label1.grid(row=0, column=0)
    
    wave1 = tk.Label(frame, text="Wave 1", font='size, 8', anchor='n')
    wave1.grid(row=1, column=0)
    
    wave2 = tk.Label(frame, text="Wave2", font='size, 8', anchor='n')
    wave2.grid(row=1, column=1)
    
    coincidence = tk.Label(frame, text="Coincidence", font='size, 8', anchor='nw')
    coincidence.grid(row=6, column=0, columnspan=2)
    
    label2 = tk.Label(frame, text="Timer Settings", font='size, 8', anchor='nw')
    label2.grid(row=0, column=3)
    
    label3 = tk.Label(frame, text="Enter the number of tenths of a second", font='size, 16')
    label3.grid(row=1, column=3, columnspan=3)
    
    # Entry box, user can type in the time interval
    entry = tk.Entry(frame, bg='white', font='size, 16')
    entry.grid(row=2, column=3, columnspan=3)
    def readT(event):
        global trials
        trials = entry.get()
        trialsQ.put(int(trials))
    entry.bind('<Return>', readT)
    
    label4 = tk.Label(frame, text="Control Panel", font='size, 8', anchor='nw')
    label4.grid(row=3, column=3)
    
    labels = []
    for i in range(16):
        label = tk.Label(frame, text=str(i+1), font='size, 8', anchor='nw')
        label.grid(row=4+i, column=3)
        labels.append(label)
    
    # Set up coincidence recording section
    def click(i):
        read[i]['text'] = coincidenceLabel['text']
    read = []
    for i in range(16):
        button = tk.Button(frame, text="", font='size, 8', bg='white', width=10, command=lambda i = i: click(i))
        button.grid(row=4+i, column=4)
        read.append(button)
    
    # Set up buttons to calculate s and ds
    def calculate():
        d = []
        for i in range(len(read)):
            d.append(float(read[i]['text']))
        
        e1 = (d[8]+d[11]-d[9]-d[10]) / np.sum(d[8:12])
        e2 = (d[12]+d[15]-d[13]-d[14]) / np.sum(d[12:16])
        e3 = (d[0]+d[3]-d[1]-d[2]) / np.sum(d[0:4])
        e4 = (d[4]+d[7]-d[5]-d[6]) / np.sum(d[4:8])
        s = e1 - e2 + e3 + e4
        
        ds1 = 2 * (d[1]+d[2]) / (np.sum(d[0:4])**2)
        ds2 = 2 * (d[0]+d[3]) / (np.sum(d[0:4])**2)
        ds3 = 2 * (d[0]+d[3]) / (np.sum(d[0:4])**2)
        ds4 = 2 * (d[1]+d[2]) / (np.sum(d[0:4])**2)
        ds5 = 2 * (d[5]+d[6]) / (np.sum(d[4:8])**2)
        ds6 = 2 * (d[4]+d[7]) / (np.sum(d[4:8])**2)
        ds7 = 2 * (d[4]+d[7]) / (np.sum(d[4:8])**2)
        ds8 = 2 * (d[5]+d[6]) / (np.sum(d[4:8])**2)
        ds9 = 2 * (d[9]+d[10]) / (np.sum(d[8:12])**2)
        ds10 = 2 * (d[8]+d[11]) / (np.sum(d[8:12])**2)
        ds11 = 2 * (d[8]+d[11]) / (np.sum(d[8:12])**2)
        ds12 = 2 * (d[9]+d[10]) / (np.sum(d[8:12])**2)
        ds13 = 2 * (d[13]+d[14]) / (np.sum(d[12:16])**2)
        ds14 = 2 * (d[12]+d[15]) / (np.sum(d[12:16])**2)
        ds15 = 2 * (d[12]+d[15]) / (np.sum(d[12:16])**2)
        ds16 = 2 * (d[13]+d[14]) / (np.sum(d[12:16])**2)
        
        nds1 = d[0] * ds1**2
        nds2 = d[1] * ds2**2
        nds3 = d[2] * ds3**2
        nds4 = d[3] * ds4**2
        nds5 = d[4] * ds5**2
        nds6 = d[5] * ds6**2
        nds7 = d[6] * ds7**2
        nds8 = d[7] * ds8**2
        nds9 = d[8] * ds9**2
        nds10 = d[9] * ds10**2
        nds11 = d[10] * ds11**2
        nds12 = d[11] * ds12**2
        nds13 = d[12] * ds13**2
        nds14 = d[13] * ds14**2
        nds15 = d[14] * ds15**2
        nds16 = d[15] * ds16**2
        
        ds = np.sqrt(nds1+nds2+nds3+nds4+nds5+nds6+nds7+nds8+nds9+nds10+nds11+nds12+nds13+nds14+nds15+nds16)
        messagebox.showinfo(message = "s = "+str(s) + "\n"
                                        "ds = "+str(ds))
    
    calculate = tk.Button(frame, text="Calculate", font='size, 16', width=10, command=calculate)
    calculate.grid(row=6, column=5, rowspan=2)
    
    # Reset the data collection
    def reset():
        for i in range(16):
            read[i]['text'] = ""
    reset = tk.Button(frame, text="Reset", font='size, 16', width=10, command=reset)
    reset.grid(row=9, column=5, rowspan=2)
    
    # Close serial port, terminate data collection thread, exit the window
    def stop():
        exitFlagQ.put(False)
        root.quit()
        root.destroy()
    stop = tk.Button(frame, text="Stop", font='size, 16', width=10, command=stop)
    stop.grid(row=12, column=5, rowspan=2)
    
    # Start collecting data, launch the window
    collection.start()
    root.mainloop()