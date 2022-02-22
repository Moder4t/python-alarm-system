import RPi.GPIO as GPIO
import sys
import signal
import time
import logging
from enum import Enum
from courriel import *

#----------------------------------------------------------------------
#pin setup

DOOR = 6
BOUTON = 17
LED_ROUGE = 18
LED_JAUNE = 12

#----------------------------------------------------------------------
#Class d'etat
class States(Enum):
    NoState =0
    DESARMER = 1
    ARMER = 2
    ALARME = 3

#----------------------------------------------------------------------
#Class Events
class Events(Enum):
    No_event =0
    Bouton = 1
    Porte =2   


#----------------------------------------------------------------------
# Class du systeme d'alarme
class AlarmSystem:

    def __init__(self):
#Initialisation par default
        self.state = States.NoState
        self.start = 0
#GPIO Setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
#Input
        GPIO.setup(BOUTON, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(DOOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#Output
        GPIO.setup(LED_ROUGE, GPIO.OUT, initial = GPIO.LOW)
        GPIO.setup(LED_JAUNE, GPIO.OUT, initial = GPIO.LOW)
#Log
        self.log = LogHistory()
#Etat par default
        self.setState(States.DESARMER)

#Allez chercher les evenementes
    def getEvent(self):
#Bouton presser
        if  GPIO.input(BOUTON) == GPIO.HIGH:
            time.sleep(0.2 )
            return Events.Bouton
#Porte ouverte
        elif GPIO.input(DOOR) == GPIO.HIGH:
            time.sleep(0.2 )
            return Events.Porte

#----------------------------------------------------------------------
# Controles des etats
    def setState(self, state):        
#Etat desarmer
        if state == States.DESARMER:
            GPIO.output(LED_ROUGE, GPIO.LOW)
            GPIO.output(LED_JAUNE, GPIO.LOW)
            self.log.debug("DESARMER")
            self.state = States.DESARMER
            print("Systeme desarmer")
#Etat armer
        elif state == States.ARMER:
            GPIO.output(LED_ROUGE, GPIO.HIGH)
            self.log.debug("ARMER")
            self.state = States.ARMER
            print("Systeme armer!")        
#Etat Alarm + envoie de e-mail
        elif state == States.ALARME:
            GPIO.output(LED_JAUNE, GPIO.HIGH)
            mail = email("202195882@collegeahuntsic.qc.ca",
                        "Stephan Whittick",
                        "stephan.whittick@hotmail.com",
                        "Stephan Whittick")
            mail.send("Alarme", "Il y a eu intrustion pendant que l'alarme etait armer!!")
            self.log.critical("ALARM")
            self.state = States.ALARME
            print("Systeme enclancher, alarme sonne")

#----------------------------------------------------------------------
#Controles des evenements
    def doEvent(self, event):
#Quand le bouton est presser
        if event == Events.Bouton:
            if self.state == States.DESARMER:
                self.setState(States.ARMER)

            elif self.state == States.ARMER:
                self.setState(States.DESARMER)
            elif self.state == States.ALARME:
                self.setState(States.DESARMER)

#Quand la porte est ouverte
        elif event == Events.Porte:
            if self.state == States.ARMER:
                self.setState(States.ALARME)
#Termination 
    def terminate(self):
        self.log.debug("terminate")
        GPIO.output(LED_ROUGE, GPIO.LOW)
        GPIO.output(LED_JAUNE, GPIO.LOW)
        GPIO.cleanup()
        sys.exit(0)















