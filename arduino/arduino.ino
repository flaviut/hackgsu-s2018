#include <CapacitiveSensor.h>


CapacitiveSensor sensor = CapacitiveSensor(4,2);

void setup() {
  sensor.set_CS_AutocaL_Millis(0xFFFFFFFF);
  Serial.begin(115200);

}

void loop() {
    long reading = sensor.capacitiveSensor(200);
    Serial.println(reading);
    delay(10);
}
