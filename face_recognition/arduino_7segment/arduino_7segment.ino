int led[8] = {2,3,4,5,6,7,8,9};
char a;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for(int i=0;i<8;i++){
    pinMode(led[i], OUTPUT);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available() > 0){
    a = Serial.read();
    Serial.print("id : ");
    Serial.println(a);
    if(a != '\n'){
      for(int i = 0; i < 8; i++){
        digitalWrite(led[i], HIGH);
      }
    }
    else{
      continue;
    }
    if(a == '1'){
       digitalWrite(led[0], LOW);
       digitalWrite(led[4], LOW);
    }
    else if(a == '2'){
      digitalWrite(led[5], LOW);
      digitalWrite(led[4], LOW);
      digitalWrite(led[7], LOW);
      digitalWrite(led[3], LOW);
      digitalWrite(led[2], LOW);
    }
    else if(a == '3'){
      digitalWrite(led[5], LOW);
      digitalWrite(led[4], LOW);
      digitalWrite(led[7], LOW);
      digitalWrite(led[0], LOW);
      digitalWrite(led[2], LOW);  
    }
    else if(a == '4'){
      digitalWrite(led[6], LOW);
      digitalWrite(led[4], LOW);
      digitalWrite(led[7], LOW);
      digitalWrite(led[0], LOW);
    }
    else if(a == '5'){
      digitalWrite(led[5], LOW);
      digitalWrite(led[6], LOW);
      digitalWrite(led[7], LOW);
      digitalWrite(led[0], LOW);
      digitalWrite(led[2], LOW);
    }
    else if(a == '6'){
      digitalWrite(led[5], LOW);
      digitalWrite(led[6], LOW);
      digitalWrite(led[7], LOW);
      digitalWrite(led[0], LOW);
      digitalWrite(led[2], LOW);
      digitalWrite(led[3], LOW);
    }
    else if(a == '7'){
      digitalWrite(led[5], LOW);
      digitalWrite(led[4], LOW);
      digitalWrite(led[0], LOW);
    }
    else if(a == '8'){
      digitalWrite(led[0], LOW);
      digitalWrite(led[2], LOW);
      digitalWrite(led[3], LOW);
      digitalWrite(led[4], LOW);
      digitalWrite(led[5], LOW);
      digitalWrite(led[6], LOW);
      digitalWrite(led[7], LOW);
    }
    else if(a == '9'){
      digitalWrite(led[0], LOW);
      digitalWrite(led[2], LOW);
      digitalWrite(led[4], LOW);
      digitalWrite(led[5], LOW);
      digitalWrite(led[6], LOW);
      digitalWrite(led[7], LOW);
    }
    else if(a == '0'){
      digitalWrite(led[0], LOW);
      digitalWrite(led[2], LOW);
      digitalWrite(led[3], LOW);
      digitalWrite(led[4], LOW);
      digitalWrite(led[5], LOW);
      digitalWrite(led[6], LOW);
    }
    else if(a == 'q'){
      Serial.end();
    }
    else {
     digitalWrite(led[1], LOW);
    }
  }
}
