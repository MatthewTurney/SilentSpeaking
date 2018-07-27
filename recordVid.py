import sys
sys.path.append('C:\\Users\\Matthew\\Documents\\silent_speaking\\SilentSpeaking\\LipNet\\evaluation')
from predict import Prebuilt_model
import os
import tkinter
from tkinter import messagebox

top=tkinter.Tk()


def helloCallBack():
    #Warning that video recording is about to start
    messagebox.showinfo("Information","A 3 second video will start recording once you press OK")
    #Call to script that records and saves video
    os.system('python video.py')
    #Call to script that runs the model
    #decodedMessage = os.system('python LipNet/evaluation/predict.py LipNet/evaluation/models/unseen-weights178.h5 LipNet/evaluation/samples/output.mpg')
    #Display decoded text
    decodedMessage = os.popen('python LipNet/evaluation/predict.py LipNet/evaluation/models/unseen-weights178.h5 LipNet/evaluation/samples/output.mpg').read()
    messagebox.showinfo("Information", decodedMessage);

#Button to kick off process
B=tkinter.Button(top,text="Start Recording",command= helloCallBack)
B.pack()
top.mainloop()