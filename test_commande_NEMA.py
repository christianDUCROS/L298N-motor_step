#programme principal
import l298n
import time

moteur_NEMA1 = l298n.L298N (2,3,4,5) 


print("roue libre")
moteur_NEMA.roue_libre()
time.sleep(1)

while (True):
    #1 tour = 200 pas, sens horaire(-1), halfstep(0), periode de 10ms entre chaque pas  
    moteur_NEMA1.rotation(200,-1,0,10)
    #90 degres sens horaire(-1), halfstep(0) periode de 10ms entre chaque pas  
    moteur_NEMA1.angle(90,-1,0,10)
    #2 tours --> 400pas, sens horaire(1),fullstep(1) periode de 100ms entre chaque pas  
    moteur_NEMA1. rotation(400,1,1,100)