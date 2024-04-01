"""
Micropython Class L298N + moteur NEMA
Pin correspond à la connexion du moteur sur la carte microcontroleur
Attention numéros de Pin et non de broches
 
Direction qui peut prendre 2 valeurs -1 ou 1

Mode : valeur = 1 pour pas entier ou autre valeur pour demi-pas

Periode  = 10 par défaut (ms) --> fréquence de 100Hz

1 tour complet pour moteur NEMA --> 200 pas 
"""
from machine import Pin
from time import sleep_ms  #tempo entre 2 pas ou 2 demipas.

class L298N():
    HALF_STEP = [
            [0, 0, 0, 1],
            [0, 0, 1, 1],
            [0, 0, 1, 0],
            [0, 1, 1, 0],
            [0, 1, 0, 0],
            [1, 1, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 1],
    ]

    FULL_STEP = [
            [0, 0, 1, 1],
            [0, 1, 1, 0],
            [1, 1, 0, 0],
            [1, 0, 0, 1]
    ]
    def __init__(self, Pin1,Pin2,Pin3,Pin4):
        #brochage stepper
        self.pin1 = Pin(Pin1,Pin.OUT)
        self.pin2 = Pin(Pin2,Pin.OUT)
        self.pin3 = Pin(Pin3,Pin.OUT)
        self.pin4 = Pin(Pin4,Pin.OUT)
        self.positiondemipas=0  #permet de mémoriser la position tableau de l'arret du demipas
        self.positionpas=0 #permet de mémoriser la la position tableau de l'arret du pas

    def roue_libre (self): #broche à 0
        self.pin1.off() 
        self.pin2.off()
        self.pin3.off() 
        self.pin4.off()

    
    def deplacer_1demipas (self, direction=1,periode=10):  #direction =1 antihoraire ou -1 horaire
        self.positiondemipas=self.positiondemipas+direction
        if direction==1 and self.positiondemipas>7 :
            self.positiondemipas=0
        if direction==-1  and self.positiondemipas<0 :
            self.positiondemipas=7   
        #print(self.positiondemipas)
        self.pin1(L298N.HALF_STEP[self.positiondemipas][3])
        self.pin2(L298N.HALF_STEP[self.positiondemipas][2])
        self.pin3(L298N.HALF_STEP[self.positiondemipas][1])
        self.pin4(L298N.HALF_STEP[self.positiondemipas][0])
        sleep_ms(periode)

    def deplacer_1pas (self,direction=1,periode=10): #direction =1 antihoraire ou -1 horaire
        self.positionpas=self.positionpas+direction
        if direction==1 and self.positionpas>3 :
            self.positionpas=0
        if direction==-1  and self.positionpas<0 :
            self.positionpas=3   
        #print(self.positionpas)
        self.pin1(L298N.FULL_STEP[self.positionpas][3])   
        self.pin2(L298N.FULL_STEP[self.positionpas][2])
        self.pin3(L298N.FULL_STEP[self.positionpas][1])
        self.pin4(L298N.FULL_STEP[self.positionpas][0])
        sleep_ms(periode) 

    
    def rotation(self,nombrepas,direction=1,mode=1,periode=10): #Par défaut mode=1 Full step antihoraire
        #rotation en tenant compte des 4 paramètres ( nbpas, direction , mode et periode)
         if mode==1:
             for i in range (nombrepas):  #nombrepas=200 --> 1 tour
                 self.deplacer_1pas(direction,periode)
         else :      
             for i in range (nombrepas): #nombrepas=nombredemipas mais nombredemipas=400 --> 1 tour
                 self.deplacer_1demipas(direction,periode)

   
    def angle(self,degree,direction=1,mode=0,periode=10): #Par défaut mode=0 Half step antihoraire
        #rotation d'un angle en compte des 4 paramètres ( angle , direction, mode et période)
        nombredemipas=int(400*degree/360)
        nombrepas=int(200*degree/360)  
        if mode==1 :    #mode=1 Full step
            nbpas=0
            for i in range (nombrepas):
                 self.deplacer_1pas(direction,periode)
                 nbpas+=1
                 print(nbpas) 
        else :           #mode=0 half step
             for i in range (nombredemipas):  #x2 car demi-pas pour respecter l'angle
                 self.deplacer_1demipas(direction,periode)         

