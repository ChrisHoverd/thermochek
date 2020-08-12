import numpy as np
import cv2
import gpiozero as gpio
from time import sleep

red_led = gpio.LED(17)
green_led = gpio.LED(18)

class CSVtoTempArray():
    
    def __init__(self,path,size):
        self.size = size
        self.path = path
        self.tempList = np.genfromtxt(path,delimiter=",", encoding="UTF-8-sig") #imports a csv file into a numpy array
        print ("A CSVtoTempArray has been instantiated")
        
    def reshapeArray(self):
        self.tempArray= np.reshape(self.tempList, self.size)
        print("An array has been reshaped")
    
    def tempArraytoGreyscale(self):
        max_temp = np.amax(self.tempList)
        min_temp = np.amin(self.tempList)
        temp_range = max_temp - min_temp
        self.greyscaleArray = np.empty(self.size,dtype=np.uint8)
        for x in range(len(self.greyscaleArray)):
            for y in range(len(self.greyscaleArray[0])):
                p_val = self.tempArray[x,y]
                value_scaled = (((p_val - min_temp) / (temp_range)) * 255)
                int_val = int(round(value_scaled))
                self.greyscaleArray[x][y] = int_val
        print("An array has been imaged")
        
    def findFaces(self):
        print("Finding faces...")
        path = "haarcascade_frontalface_default.xml"
        face_cascade = cv2.CascadeClassifier(path)

        #create a face cascade
        self.faces = face_cascade.detectMultiScale(self.greyscaleArray, scaleFactor=1.2, minNeighbors=5, minSize=(5, 5))
        

    def showFaces(self):
        temp_warning = 38
        self.face_number = 1
        for (x, y, w, h) in self.faces:
            cv2.rectangle(self.greyscaleArray, (x, y), (x + w, y + h), (255), 2)
            temps_in_faces = []
            high_temp_in_faces = []
            individual_face = self.greyscaleArray[y:y+h, x:x+w]
            face_text = ("Face " + str(self.face_number))
            cv2.namedWindow(face_text, cv2.WINDOW_AUTOSIZE)
            cv2.imshow(face_text, individual_face)
            cv2.moveWindow(face_text, 0, 0)
            for xp in range(x,x+w):
                for yp in range(y,y+h):
                    pixel_temp = self.tempList[yp][xp]
                    rounded_pixel_temp = int(round(pixel_temp))
                    temps_in_faces.append(rounded_pixel_temp)
                    if rounded_pixel_temp>=temp_warning:
                        high_temp_in_faces.append(rounded_pixel_temp)
                        cv2.circle(self.greyscaleArray,((xp),(yp)),1,(0),2)
            local_temp = max(temps_in_faces)
            if local_temp>=temp_warning:
                alarmdisp = "High Temp!"
                red_led.on()
            else:
                alarmdisp="No Temp!"
                green_led.on()

            display = "(" + str(self.face_number)+") "+ str(local_temp) +" C, "+ alarmdisp
            cv2.putText(self.greyscaleArray,display,(x-40,y-5),cv2.FONT_HERSHEY_SIMPLEX,0.4,(255),1,cv2.LINE_AA)
            self.face_number += 1
            
        print(str(len(self.faces)) + " faces found")
        cv2.namedWindow("GreyScale", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("GreyScale", self.greyscaleArray)
        cv2.moveWindow("GreyScale", 0,0)

        key = cv2.waitKey(0) & 0xFF
    
        if key == ord("q"):
            cv2.destroyAllWindows()
            red_led.off()
            green_led.off()

img = CSVtoTempArray("FLIR0210.csv",(240,320))
img.reshapeArray()
img.tempArraytoGreyscale()
img.findFaces()
img.showFaces()
