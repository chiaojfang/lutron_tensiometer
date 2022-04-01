//#define us // for slower speeds

#define steps 200
#define fraction 8
int T = 60; // seconds for each mm
int DIR = 1; //0:UP 1:DOWN
int start = 0;

#ifdef us
unsigned long INT = 1000000 / steps * T / fraction;
#else
unsigned long INT = 1000 / steps * T / fraction;
#endif

void setup() {
  pinMode(2, OUTPUT);  
  pinMode(3, OUTPUT);

  Serial.begin(9600);
  delay(100);
  Serial.println("\nStart (s)");
  Serial.print("T: "); Serial.print(T); Serial.print(" INT: "); Serial.println(INT);

  if (DIR == 0){
    digitalWrite(3, HIGH);
    Serial.println("UP (u)");
  }
  else if (DIR == 1){
    digitalWrite(3, LOW);
    Serial.println("DOWN (d)");
  }
  Serial.println("Ready");
}

int r, count, calibrate=0;
void loop() {
  r = Serial.read();
  if(r != -1){
    if(r == 's') {start = 1;  Serial.println("Start (s)");}
    else if(r == 'p') {start = 0; Serial.println("Pause (p)");}
    else if(r == 'u') {digitalWrite(3, HIGH); Serial.println("UP (u)");}
    else if(r == 'd') {digitalWrite(3, LOW); Serial.println("DOWN (d)");}
    else if(r == 'c') {count = 0; calibrate=1; start=1; Serial.println("Calibrate Start (c)");}// go 100 steps for calibration //TODO
    else if(r == 't') {
      T = Serial.parseInt();
      #ifdef us
      INT = 1000000 / steps * T / fraction;
      #else
      INT = 1000 / steps * T / fraction;
      #endif
      Serial.print("T: "); Serial.print(T); Serial.print(" INT: "); Serial.println(INT);
    }
  }
  if(calibrate == 1){
    if(count >= steps*fraction/2) {start = 0; calibrate = 0; Serial.println("Calibrate Stop.");}
    count++;  
  }
  if(start == 1){   
#ifdef us
    digitalWrite(2, HIGH);
    delayMicroseconds(INT);
    digitalWrite(2, LOW);
    delayMicroseconds(INT);
#else
    digitalWrite(2, HIGH);
    delay(INT);
    digitalWrite(2, LOW);
    delay(INT);
#endif
  }
}
