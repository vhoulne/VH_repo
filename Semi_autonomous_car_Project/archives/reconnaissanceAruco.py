import argparse
import time
import cv2 
import numpy as np
import math

#------------------------------------------------------------------------------
global Pdroite
global Pgauche
global Orientation

global longueur 
global hauteur  
global indice  
global pair 
longueur = 0
hauteur  = 0
indice  = 0
pair   = 0

Orientation = 'forward'
Pdroite=0
Pgauche = 0


def reco():
    global indice
    global longueur
    global hauteur
    global pair

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
                #print(pair , "pair")
                print("hauteur", hauteur)
                #print("longueuer", longueur)


        else :
            indice =0     
    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()  

reco()
