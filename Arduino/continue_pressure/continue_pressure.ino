int button = 51; // Biến khai báo chân của button
String text;
String sensor;
float i=0;
double pressure = 0;
float val =0;
void PressSure_func(float k);
unsigned long waitTime = 500; // Bạn cần nhấn giữ 500 mili giây để hệ thống xem đó là một sự kiến nhấn giữ.

boolean ledStatus = 0; // tương tự với LOW - mặc định đèn sẽ tắt

boolean lastButtonStatus = 0; //Biến dùng để lưu trạng thái của phím bấm. Mặc định là 0 <=> LOW <=> chưa nhấn
boolean buttonLongPress = 0; // Mặc định là không có sự kiện nhấn giữ.

unsigned long lastChangedTime;

void setup() {
 
  pinMode(button,INPUT); // Đặt chân button là INPUT - hiển nhiên rồi
  pinMode(50, OUTPUT); //chân kích van 2
  pinMode(44, OUTPUT); //chân kích van 1
  pinMode(40, OUTPUT); //chân led 44
  pinMode(A0, INPUT);
  Serial.begin(115200); //Bật Serial để debug
  Serial.println("CLEARSHEET");// xóa dữ liệu trên sheet đầu tiên của file excel
Serial.println("LABEL,Date,Time,Pressure,Length");
}

void loop() {
  boolean reading = digitalRead(button); // đọc giá trị của button
  if (reading != lastButtonStatus) 
  {   
    lastButtonStatus = reading; //Cập nhập trạng thái cuối cùng.
    lastChangedTime = millis(); //Cập nhập thời gian
  
    if( reading == HIGH) 
    {
      Serial.println("Da bat van");
      digitalWrite(50,HIGH); 
      digitalWrite(44,HIGH); 
    }
    else
    {
      Serial.println("Da tat van");
      digitalWrite(50,LOW); 
      digitalWrite(44,LOW); 
    }
   }
   
  } // Còn nếu bạn đang nhấn giữ button hoặc thả nó thời gian dài chỉ sẽ không ảnh hưởng đến việc này


void PressSure_func(float k)
{
      Serial.println("Da bat van"+ String(k));
      digitalWrite(50,HIGH); 
      digitalWrite(44,HIGH); 
   while(pressure < k)
      {
         val = analogRead(A0)*5.0/1023;
       pressure = (val-1)*0.001/0.004;
       sensor = String(pressure,3);
       text = String(val,3);
       digitalWrite(50,HIGH);    
         Serial.println( (String) "DATA,TIME," + millis() +","+ text+","+sensor);    
       delay(50);
         Serial.print("pressure : ");
          Serial.println(pressure,3);
           Serial.print("val : ");
          Serial.println(val,3);
        
      }
    Serial.println("Da tat van"+String(k));
//    delay(3000);
    digitalWrite(50,LOW);
    digitalWrite(44,HIGH); 

}
