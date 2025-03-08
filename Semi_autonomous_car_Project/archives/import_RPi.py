import RPi.GPIO as GPIO
import time

# Configuration des broches GPIO
GPIO.setmode(GPIO.BCM)


AIN1 = 17  
AIN2 = 18  
PWMA = 27  


BIN1 = 22  
BIN2 = 23  
PWMB = 24  

# Configuration des broches comme sorties
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)


def regler_vitesse(moteur, vitesse, sens):
    if sens == "avant":
        GPIO.output(moteur[0], GPIO.HIGH)
        GPIO.output(moteur[1], GPIO.LOW)
    elif sens == "arriere":
        GPIO.output(moteur[0], GPIO.LOW)
        GPIO.output(moteur[1], GPIO.HIGH)
    else:
        GPIO.output(moteur[0], GPIO.LOW)
        GPIO.output(moteur[1], GPIO.LOW)

  
    pwm = GPIO.PWM(moteur[2], 1000) 
    pwm.start(vitesse)

try:
    while True:
        
        regler_vitesse((AIN1, AIN2, PWMA), 100, "avant")
        regler_vitesse((BIN1, BIN2, PWMB), 100, "avant")


except KeyboardInterrupt:
    GPIO.cleanup()
