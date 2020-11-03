import serial # import Serial Library
import numpy  # Import numpy
import matplotlib.pyplot as plt #import matplotlib library
from drawnow import *

tempF= []
s=[]
arduinoData = serial.Serial('com5', 115200) #Creating our serial object named arduinoData
plt.ion() #Tell matplotlib you want interactive mode to plot live data
cnt=0
setpoint=30
kp=100
ki=5
kd=3
optiune=0
optiune2=0
optiuneKP=0
optiuneKI=0
optiuneSP=0
optiuneKD=0
def Modificare_valori(kp,ki,setpoint,kd):
    while(1):
        print("----------------Modificare Valori---------------");
        print("1)Modificam kp")
        print("2)modificam ki")
        print("3)modificam setpoint")
        print("4)modificam kd")
        print("5)inapoi la Meniu principal")
        optiune2=int(input())
        if(optiune2==1):
            while(1):
                print("----------------Modificare kp---------------");
                print("kp="+str(kp)+" ki="+str(ki)+" setpoint="+str(setpoint)+" kd="+str(kd))
                print("1)  +1")
                print("2)  -1")
                print("3)  +10")
                print("4)  -10")
                print("5)  Inapoi")
                optiuneKP=int(input())
                if(optiuneKP==1):
                    arduinoData.write('1'.encode())
                    kp=kp+1
                elif(optiuneKP==2):
                    arduinoData.write('2'.encode())
                    kp=kp-1
                elif(optiuneKP==3):
                    arduinoData.write('11'.encode())
                    kp=kp+10
                elif(optiuneKP==4):
                    arduinoData.write('22'.encode())
                    kp=kp-10
                elif(optiuneKP==5):
                    Modificare_valori(kp,ki,setpoint,kd)
        elif(optiune2==2):
            while(1):
                print("----------------Modificare ki---------------");
                print("kp="+str(kp)+" ki="+str(ki)+" setpoint="+str(setpoint)+" kd="+str(kd))
                print("1)  +0.1")
                print("2)  -0.1")
                print("3)  Inapoi")
                optiuneKI=int(input())
                if(optiuneKI==1):
                    arduinoData.write('3'.encode())
                    ki=ki+0.1
                elif(optiuneKI==2):
                    arduinoData.write('4'.encode())
                    ki=ki-0.1
                elif(optiuneKI==3):
                    Modificare_valori(kp,ki,setpoint,kd)
        elif(optiune2==3):
            while(1):
                print("----------------Modificare Setpoint---------------");
                print("kp="+str(kp)+" ki="+str(ki)+" setpoint="+str(setpoint)+" kd="+str(kd))
                print("1)  +10")
                print("2)  -10")
                print("3)  Inapoi")
                optiuneSP=int(input())
                if(optiuneSP==1):
                    arduinoData.write('5'.encode())
                    setpoint=setpoint+10
                elif(optiuneSP==2):
                    arduinoData.write('6'.encode())
                    setpoint=setpoint-10
                elif(optiuneSP==3):
                    Modificare_valori(kp,ki,setpoint,kd)
        elif(optiune2==4):
            while(1):
                print("----------------Modificare KD---------------");
                print("kp="+str(kp)+" ki="+str(ki)+" setpoint="+str(setpoint)+" kd="+str(kd))
                print("1)  +0.1")
                print("2)  -0.1")
                print("3)  Inapoi")
                optiuneKD=int(input())
                if(optiuneKD==1):
                    arduinoData.write('7'.encode())
                    kd=kd=+0.1
                elif(optiuneKD==2):
                    arduinoData.write('8'.encode())
                    kd=kd-0.1
                elif(optiuneKD==3):
                    Modificare_valori(kp,ki,setpoint,kd)
        elif(optiune2==5):
            Meniu(kp,ki,setpoint,kd)
            
                    
                
                
                    
                
                
                
                
                
def Meniu(kp,ki,setpoint,kd):
    while(1):
        print("-------------------Meniu----------------------")
        print("kp="+str(kp)+" ki="+str(ki)+" setpoint="+str(setpoint)+" kd="+str(kd))
        print("1)Modificare Valori")
        print("2)Afisare Grafic")
        print("3)Iesire")
        optiune=int(input())
        if(optiune==1):
            Modificare_valori(kp,ki,setpoint,kd)
        elif(optiune==2):
            Grafic(setpoint)
        elif(optiune==3):
            exit(0)
            
        
        
def makeFig(): #Create a function that makes our desired plot
    plt.ylim(20,120)
    #plt.xlim(0,1000)#Set y min and max values
    plt.title("kp="+str(kp)+" ki="+str(ki)+" setpoint="+str(setpoint)+" kd="+str(kd))      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel('Temperatura')                            #Set ylabels
    plt.plot(tempF, 'ro-', label='Temperatura')       #plot the temperature
    plt.legend(loc='upper left')                    #plot the legend
    plt2=plt.twinx()                                #Create a second y axis
    plt.ylim(20,120)                           #Set limits of second y axis- adjust to readings you are getting
    plt2.plot(s, 'b^-', label='setpoint') #plot pressure data
    plt2.set_ylabel('setpoint')                    #label second y axis
    plt2.ticklabel_format(useOffset=False)           #Force matplotlib to NOT autoscale y axis
    plt2.legend(loc='upper right')                  #plot the legend
def Grafic(setpoint):
    cnt=0
    while True: # While loop that loops forever
        while (arduinoData.inWaiting()==0): #Wait here until there is data
            pass #do nothing
        ser_bytes = arduinoData.readline()
        decoded_bytes=0
        try:
            decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8")) #cacatu asta o fost naspa
            print(decoded_bytes)
        except:
            decoded_bytes=0
        tempF.append(decoded_bytes)
        s.append(setpoint)                     #Building our pressure array by appending P readings
        drawnow(makeFig)                       #Call drawnow to update our live graph
        plt.pause(0.001)                     #Pause Briefly. Important to keep drawnow from crashing
        cnt=cnt+1
        if(cnt>1000):                            #If you have 50 or more points, delete the first one from the array
            tempF.pop(0)                       #This allows us to just see the last 50 data points
            s.pop(0)
Meniu(kp,ki,setpoint,kd)
