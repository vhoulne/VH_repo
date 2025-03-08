from flask import Flask, render_template, jsonify
import numpy as np
import time
from PCA9685 import PCA9685
import math
import threading
import cv2
import argparse
import queue
import requests
###################################################variables########################################
compteur = 0
longueur = 0
hauteur  = 0
indice  = 0
pair   = 0
   ## var pour eval 2 ##
numero=100
compteur_num=0
numero1=4
numero2=5
numero3=10
num_sortie=9
cptbalise=0

def getCompteur():
    global compteur
    print("compteur lu a "+str(compteur))
    return compteur

def setCompteur(v):
    global compteur
    print("compteur modifie de "+str(compteur)+" a "+str(v))
    compteur = v
    
Orientation = 'forward'
Pdroite=0
Pgauche = 0
########################################## placement############################################

def placement() : 
    global cptbalise 
    Motor=MotorDriver()  
    while cptbalise<1:
        if getCompteur() > 0 :       
            Motor.MotorRun(0, 'forward', 0)
            Motor.MotorRun(1, 'forward', 0)
            time.sleep(0.2)
            print(numero)
            if numero==10:                                              #numero à définir
                dist= 5.23*(10**3)*hauteur**(-0.961)                   #distance à vérifier
                print(dist,"ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt")
                if dist >180 :                   #seuil à modifier           
                    temps =1
                    if dist  > 300:
                        temps =1.5
                    Motor.MotorRun(0, 'forward', 55)
                    Motor.MotorRun(1, 'forward', 55)
                    time.sleep(temps)
                    Motor.MotorRun(0, 'forward', 0)
                    Motor.MotorRun(1, 'forward', 0)
                    time.sleep(0.2)
                    setCompteur(0)
                else:
                    cptbalise=1                      
        Motor.MotorRun(0, 'forward', 0)
        Motor.MotorRun(1, 'forward', 30)
        time.sleep(0.3)
        Motor.MotorRun(0, 'forward', 0)
        Motor.MotorRun(1, 'forward', 0)
        time.sleep(0.3)                             #fin balise 1
    cptbalise=0
    Motor.MotorRun(0, 'backward', 0)
    Motor.MotorRun(1, 'backward', 0)
#################################################  fin #######################################

def recherchebalisecerclefin(num) : 
    global cptbalise 
    global compteur_num 
    Motor=MotorDriver()  
    while cptbalise<1:
        if getCompteur() > 0 :       
            Motor.MotorRun(0, 'forward', 0)
            Motor.MotorRun(1, 'forward', 0)
            time.sleep(0.2)
            if numero==num:                                              #numero à définir
                dist= 5.23*(10**3)*hauteur**(-0.961)                   #distance à vérifier
                if dist >40:                   #seuil à modifier
                    if dist > 100:
                        temps =1.3
                    elif dist > 50:
                        temps=0.5
                    else:
                        temps=0.2
                    Motor.MotorRun(0, 'forward', 55)
                    Motor.MotorRun(1, 'forward', 49)
                    time.sleep(temps)
                    Motor.MotorRun(0, 'forward', 0)
                    Motor.MotorRun(1, 'forward', 0)
                    time.sleep(0.2)
                    setCompteur(0)
                else:
                    cptbalise=1                      
        Motor.MotorRun(0, 'forward', 0)
        Motor.MotorRun(1, 'forward', 30)
        time.sleep(0.3)
        Motor.MotorRun(0, 'forward', 0)
        Motor.MotorRun(1, 'forward', 0)
        time.sleep(0.3)
    compteur_num+=1                             #fin balise 1
    cptbalise=0



##########################################recherche balise cercle#################################
def recherchebalisecercle(num) : 
    global cptbalise 
    global compteur_num 
    Motor=MotorDriver()  
    while cptbalise<1:
        if getCompteur() > 0 :       
            Motor.MotorRun(0, 'forward', 0)
            Motor.MotorRun(1, 'forward', 0)
            time.sleep(0.2)
            if numero==num:                                              #numero à définir
                dist= 5.23*(10**3)*hauteur**(-0.961)                   #distance à vérifier
                if dist >40:                   #seuil à modifier
                    if dist > 100:
                        temps =1.3
                    elif dist > 50:
                        temps=0.5
                    else:
                        temps=0.2
                    Motor.MotorRun(0, 'forward', 55)
                    Motor.MotorRun(1, 'forward', 55)
                    time.sleep(temps)
                    Motor.MotorRun(0, 'forward', 0)
                    Motor.MotorRun(1, 'forward', 0)
                    time.sleep(0.2)
                    setCompteur(0)
                else:
                    cptbalise=1                      
        Motor.MotorRun(0, 'forward', 0)
        Motor.MotorRun(1, 'forward', 30)
        time.sleep(0.3)
        Motor.MotorRun(0, 'forward', 0)
        Motor.MotorRun(1, 'forward', 0)
        time.sleep(0.3)
    compteur_num+=1                             #fin balise 1
    cptbalise=0
    Motor.MotorRun(0, 'backward', 55)
    Motor.MotorRun(1, 'backward', 55)
    time.sleep(2.5)
    Motor.MotorRun(0, 'backward', 0)
    Motor.MotorRun(1, 'backward', 0)
##############################################
###############################################reconnaissance image##########################

def reco():
    global indice
    global longueur
    global hauteur
    global pair
    global numero

    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--type", type=str,
        default="DICT_ARUCO_ORIGINAL",
        help="type of ArUCo tag to detect")
    args = vars(ap.parse_args())

    # define names of each possible ArUco tag OpenCV supports
    ARUCO_DICT = {
        "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    }

    # verify that the supplied ArUCo tag exists and is supported by
    # OpenCV

    # load the ArUCo dictionary and grab the ArUCo parameters
    print("[INFO] detecting '{}' tags...".format(args["type"]))
    arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
    arucoParams = cv2.aruco.DetectorParameters()
    # initialize the video stream and allow the camera sensor to warm up
    print("[INFO] starting video stream...")
    vs = cv2.VideoCapture('/dev/v4l/by-id/usb-Suyin_HD_Camera_200910120001-video-index0',cv2.CAP_V4L2) 
    #,cv2.CAP_V4L2  
    #adresses camera : 
    #usb-Suyin_HD_Camera_200910120001-video-index0
    #usb-Suyin_HD_Camera_200910120001-video-index1                                                    #TEST
    time.sleep(2.0)

    
    while(True):
# grab the frame from the threaded video stream and resize it
        # to have a maximum width of 1000 pixels
        ret, frame = vs.read()
        detector=cv2.aruco.ArucoDetector(arucoDict, arucoParams)
        corners, ids, rejected = detector.detectMarkers(frame)
        # verify *at least* one ArUco marker was detected
        if len(corners) > 0:
            # flatten the ArUco IDs list
            ids = ids.flatten()
                    
            # loop over the detected ArUCo corners
            for (markerCorner, markerID) in zip(corners, ids):
                # extract the marker corners (which are always returned
                # in top-left, top-right, bottom-right, and bottom-left
                # order)
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                # convert each of the (x, y)-coordinate pairs to integers
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))
                
        # verify *at least* one ArUco marker was detected
        if len(corners) > 0:
            indice =1
            setCompteur(10000)
            # flatten the ArUco IDs list
            ids = ids.flatten()
            # loop over the detected ArUCo corners
            for (markerCorner, markerID) in zip(corners, ids):
                # extract the marker corners (which are always returned
                # in top-left, top-right, bottom-right, and bottom-left
                # order)
                
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                # convert each of the (x, y)-coordinate pairs to integers
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))

                #ici, on insère la distance
                longueur = np.abs(topRight[0] - topLeft[0])
                hauteur = np.abs(topRight[1] - bottomRight[1])
 #               print('La longueur est', longueur)
  #              print('La hauteur est', hauteur)
                # draw the bounding box of the ArUCo detection
                cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
                cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
                cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
                cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)
                # compute and draw the center (x, y)-coordinates of the
                # ArUco marker
                cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
                # draw the ArUco marker ID on the frame
                cv2.putText(frame, str(markerID),
                    (topLeft[0], topLeft[1] - 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
                    # show the output frame
                pair = ids[0]%2
                numero = ids[0]
                print(indice)
                print("compteur="+str(getCompteur()))

        else :
            indice =0     
    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()         
################################################  MOTEUR       #################################
Dir = [
    'forward',
    'backward',
]
pwm = PCA9685(0x40, debug=True)
pwm.setPWMFreq(50)
class MotorDriver():
    def __init__(self):
        self.PWMA = 0
        self.AIN1 = 1
        self.AIN2 = 2
        self.PWMB = 5
        self.BIN1 = 3
        self.BIN2 = 4

    def MotorRun(self, motor, index, speed):
        if speed > 100:
            return
        if(motor == 0):
            pwm.setDutycycle(self.PWMA, speed)
            if(index == Dir[0]):
                pwm.setLevel(self.AIN1, 0)
                pwm.setLevel(self.AIN2, 1)
            else:
                pwm.setLevel(self.AIN1, 1)
                pwm.setLevel(self.AIN2, 0)
        else:
            pwm.setDutycycle(self.PWMB, speed)
            if(index == Dir[0]):
                pwm.setLevel(self.BIN1, 0)
                pwm.setLevel(self.BIN2, 1)
            else:
                pwm.setLevel(self.BIN1, 1)
                pwm.setLevel(self.BIN2, 0)

    def MotorStop(self, motor):
        if (motor == 0):
            pwm.setDutycycle(self.PWMA, 0)
        else:
            pwm.setDutycycle(self.PWMB, 0)

###########################CODE SERVEUR###################################
app = Flask(__name__)




@app.route('/')
def index():
    return render_template('rasphtml.html')

@app.route('/traiter_donnees/<variable1>+<variable2>+<variable3>+<auto>', methods=['GET'])
def traiter_donnees(variable1, variable2, variable3,auto):
    global indice
    global longueur
    global hauteur
    global pair
    global numero
    global compteur_num
    global cptbalise
    global num_sortie
    global numero1
    global numero2
    global numero3

    if int(auto)== 0 :
        Pdroite = int(variable1)
        Pgauche = int(variable2)
        Orientation = variable3.strip('"')
#        print(Pdroite,Pgauche,Orientation)
        Motor=MotorDriver()
        Motor.MotorRun(0, Orientation, Pdroite)
        Motor.MotorRun(1, Orientation, Pgauche)
#test
    elif int(auto)==1 :      
        #ne peut etre quitté pour l'isntant
        compteur_num=0
        Motor=MotorDriver()
        Motor.MotorRun(0, 'forward', 55)
        Motor.MotorRun(1, 'forward', 55)
        time.sleep(3)
        Motor.MotorRun(0, 'forward', 0)
        Motor.MotorRun(1, 'forward', 0)
        while compteur_num <4:
            print("recherchebalisecercle")
            placement()
            recherchebalisecercle(numero1)
            recherchebalisecercle(numero2)
            recherchebalisecercle(numero3)
            recherchebalisecerclefin(num_sortie)
    

    return jsonify({'message': 'Données traitées avec succès !'})
   

def serveur():
    global app
    app.run(debug=False,host='137.194.173.24', port=8000)

#############################threading############################################################

thrd1 = threading.Thread(target=serveur, args=[])
thrd1.start()
thread_reco=threading.Thread(target=reco)
thread_reco.start()
thrd1.join()
thread_reco.join()



#######################################################################
