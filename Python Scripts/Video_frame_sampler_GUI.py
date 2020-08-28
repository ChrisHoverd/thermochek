import numpy as np
import cv2
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import gpiozero as gpio
from time import sleep
import time
import tkinter as tk
from tkinter import ttk

class GUI:
    def __init__(self):
        self.master = master
        master.title = ("Thermochek")
        
        self.label = Label(master, text="This is the begining of the GUI")
        self.label.pack()
        
        self.greet_button = Button(master, text="Greet", command = self.greet)
        self.greet_button.pack()
        
        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()
        
        def greet(self):
            print("Greetings")

def findFace():
    red_led = gpio.LED(17)
    green_led = gpio.LED(18)
    path = "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(path)

    camera = PiCamera()
    camera.resolution = (640,480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size = (640,480))

    time.sleep(0.1)

    first_time = time.time()
    for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port = True):
        image = frame.array
        
        if time.time() - first_time > 5:
            print("Looking for faces...")
            faces = face_cascade.detectMultiScale(image, scaleFactor=1.2, minNeighbors=5, minSize=(5, 5))
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (255), 2)
        
            if len(faces) >= 1:
                print("Face(s) detected!")
                green_led.on()
                red_led.off()
            
            else:
                print("No Face(s) detected!")
                red_led.on()
                green_led.off()
                    
            first_time = time.time()
            
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        
        if key == ord("q"):
            cv2.destroyAllWindows()
            red_led.off()
            green_led.off()
            break

    



