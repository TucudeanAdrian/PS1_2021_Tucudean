#include "DHTesp.h"

#ifdef ESP32
#pragma message(THIS EXAMPLE IS FOR ESP8266 ONLY!)
#error Select ESP8266 board.
#endif
String msg="";
DHTesp dht;
int a;
uint8_t LEDpin = D6;
//int kp=0;
int at=0;
double kp = 100;double ki = 5;double kd = 3; // exemplu valori
double output=512;

  double eroare= 0;

  double suma_erori= 0;

  double eroare_anterioara = 0;

  double derivativa = 0;

  double dt=1; // timp esantionare o secunda

  double setpoint = 30;
void setup()
{
 
  Serial.begin(115200);
  analogWrite(LEDpin, 512);
  String thisBoard= ARDUINO_BOARD;
  Serial.println(thisBoard); 
  dht.setup(2, DHTesp::DHT11); // Connect DHT sensor to GPIO 2 adica D4
}

void loop()
{
  if(Serial.available())
  {
    a=Serial.read()-48;
  }
  delay(dht.getMinimumSamplingPeriod());

 
  float temperature = dht.getTemperature();

 
  Serial.println(temperature, 1);
  
    //erial.println(a);
    
    switch(a)
    {
      case 1: kp=kp+1; break;
      case 2: kp=kp-1; break;
      case 11:kp=kp+10;break;
      case 22:kp=kp-10;break;
      case 3: ki=ki+0.1;break;
      case 4: ki=ki-0.1;break;
      case 5:setpoint=setpoint+10;break;
      case 6:setpoint=setpoint-10;break;
      case 7:kd=kd+0.1;break;
      case 8:kd=kd-0.1;break;
      
     
      
     
      
    
    
    
   
  
  }
  
  a=0;
  //Serial.println(msg);
  eroare = setpoint - temperature;

    suma_erori= suma_erori + eroare * dt;

    derivativa = (eroare - eroare_anterioara) / dt;

    output = (kp * eroare) + (ki * suma_erori ) + (kd * derivativa);
    analogWrite(LEDpin, output);
    eroare_anterioara = eroare;
  //Serial.println(output);
  delay(1000);
}
