import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from tkinter import *
from tkinter import messagebox

root=Toplevel()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False,False)



path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

#test

def findBeard():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    isFound= False;
    _, img = cap.read()

    # Convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # Gray Scale, Image factor, Number of Neighbours
    # To construct a rectangle around the face detected
    for (x, y, w, h) in faces:

        # create a mask image of the same shape as input image, filled with 0s (black color)
        mask = np.zeros_like(img)
        # create a white filled ellipse
        mask = cv2.ellipse(mask, (int((x + w) / 1.2), y + h), (69, 69), 0, 0, -180, (255, 255, 255), thickness=-1)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)

        # Bitwise AND operation to black out regions outside the mask
        result = np.bitwise_and(img, mask)

        # Converting the final result as HSV inorder to detect colors
        hsv_img = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)

        # Draws a rectangle

        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Black Color
        low_black = np.array([94, 80, 2])
        high_black = np.array([126, 255, 255])

        MASK = cv2.inRange(hsv_img, low_black, high_black)

        # If the MASK only has black pixels caused due to no black colour in the original image
        if cv2.countNonZero(MASK) == 0:
            print("Beard Not Found")
        else:
            print("Beard Found")
            isFound = True
    return isFound

def findEncoding(images):
    encodeList = []
    for img in images :
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def getRole(name):
    fileObj = open("Attendance.csv", "r")  # opens the file in read mode.
    words = fileObj.read().splitlines()  # puts the file into an array.
    fileObj.close()
    for key in words:
        if name in key:
            print(key[-1])
            role = key[-1]
    return role

def printRole(name):
    fileObj = open("Attendance.csv", "r")  # opens the file in read mode.
    words = fileObj.read().splitlines()  # puts the file into an array.
    fileObj.close()
    for key in words:
        if name in key:
            print(key[-1])
def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')



encodeListKnown = findEncoding(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)


success, img = cap.read()
imgS = cv2.resize(img,(0,0), None, 0.25, 0.25 )
imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

facesCurFrame = face_recognition.face_locations(imgS)
encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

for encodeFace, faceLoc in zip(encodesCurFrame,facesCurFrame) :
    matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
    faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
    # print(faceDis)
    matchIndex = np.argmin(faceDis)
    #cv2.imshow('Webcam', img)
    #cv2.waitKey(1)
    if matches[matchIndex]:
        name = classNames[matchIndex].upper()
        print(name)
        y1,x2,y2,x1 = faceLoc
        y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
        cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
        cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
        markAttendance(name)

        img = PhotoImage(file='login.png')
        Label(root, image=img, bg='white').place(x=50, y=50)

        frame = Frame(root, width=350, height=350, bg="white")
        frame.place(x=480, y=70)

        heading = Label(frame, text='Sign in successful', fg='#57a1f8', bg='white',
                            font=('Microsoft YaHei UI Light', 22, 'bold'))
        heading.place(x=100, y=5)

        if(findBeard()):
            if getRole(name) == 'A':
                welcome = Label(frame, text='Welcome Admin SIR', fg='black', bg='white',
                                    font=('Microsoft YaHei UI Light', 14, 'bold'))
                welcome.place(x=100, y=100)
            if getRole(name) == 'U':
                welcome = Label(frame, text='Welcome User SIR', fg='black', bg='white',
                                    font=('Microsoft YaHei UI Light', 14, 'bold'))
                welcome.place(x=100, y=100)
        else:
            if getRole(name) == 'A':
                welcome = Label(frame, text='Welcome Admin Madame', fg='black', bg='white',
                                    font=('Microsoft YaHei UI Light', 14, 'bold'))
                welcome.place(x=100, y=100)
            if getRole(name) == 'U':
                welcome = Label(frame, text='Welcome User Madame', fg='black', bg='white',
                                    font=('Microsoft YaHei UI Light', 14, 'bold'))
                welcome.place(x=100, y=100)


        AffName = Label(frame, text=name, fg='black', bg='white',
                            font=('Bradley Hand ITC', 25,'bold'))
        AffName.place(x=100, y=170)

        Button(frame, width=39, pady=10, text='Access to Home', bg='#57a1f8', fg='white', border=0,).place(x=100,y=240)
        root.mainloop()
    else:
        messagebox.showerror("Invalid","You dont have access here!")


#
















#faceLoc = face_recognition.face_locations(imgMira)[0]
#encodeMira = face_recognition.face_encodings(imgMira)[0]
#cv2.rectangle(imgMira , (faceLoc[3] , faceLoc[0]) , (faceLoc[1] , faceLoc[2]) , (255 , 0 , 255) , 2)

#faceLocTest = face_recognition.face_locations(imgTest)[0]
#encodeTest = face_recognition.face_encodings(imgTest)[0]
#cv2.rectangle(imgTest , (faceLocTest[3] , faceLocTest[0]) , (faceLocTest[1] , faceLocTest[2]) , (255 , 0 , 255) , 2)

#results = face_recognition.compare_faces([encodeMira],encodeTest)
#faceDis = face_recognition.face_distance([encodeMira], encodeTest)









