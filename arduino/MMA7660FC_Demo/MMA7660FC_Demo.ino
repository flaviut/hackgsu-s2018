#include <CapacitiveSensor.h>

/*****************************************************************************/
//	Function:    Get the accelemeter of the x/y/z axis. 
//  Hardware:    Grove - 3-Axis Digital Accelerometer(±1.5g)
//	Arduino IDE: Arduino-1.0
//	Author:	 Frankie.Chu		
//	Date: 	 Jan 10,2013
//	Version: v0.9b
//	by www.seeedstudio.com
//
//  This library is free software; you can redistribute it and/or
//  modify it under the terms of the GNU Lesser General Public
//  License as published by the Free Software Foundation; either
//  version 2.1 of the License, or (at your option) any later version.
//
//  This library is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
//  Lesser General Public License for more details.
//
//  You should have received a copy of the GNU Lesser General Public
//  License along with this library; if not, write to the Free Software
//  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
//
/*******************************************************************************/

#include <Wire.h>
#include "MMA7660.h"
MMA7660 accelemeter;

CapacitiveSensor capSensor = CapacitiveSensor(4, 2);
void setup()
{
	accelemeter.init();  
	Serial.begin(9600);
  capSensor.set_CS_AutocaL_Millis(0xFFFFFFFF);
}
void loop()
{
	float ax,ay,az;
	
	accelemeter.getAcceleration(&ax,&ay,&az);
  long sensorValue = capSensor.capacitiveSensor(200);
  Serial.print(sensorValue); Serial.print(",");
  Serial.print(ax); Serial.print(",");
  Serial.print(ay); Serial.print(",");
  Serial.println(az);
//  Serial.println(sensorValue);
//	Serial.println(ax);
//	Serial.println(ay);
//	Serial.println(az);
	delay(2000);
}


