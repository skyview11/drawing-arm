#include "step_motor.h"
#include <ros.h>
#include <geometry_msgs/Point.h>

ros::NodeHandle nh;

stepping_motor motor1(5, 6);
stepping_motor motor2(7, 8);
stepping_motor motor3(9, 10);

void moving( const geometry_msgs::Point& cmd_msg){
  float x1;
  float y;
  float z1;
  
  x1 = cmd_msg.y;
  y = cmd_msg.z;
  z1 = cmd_msg.x;
  
  float x = -10.0/1080.0 * (x1 - 1080) + 15.0;//map(x1, 0, 1080, 25, 15);
  float z = 20.0/1920.0 * (z1 - 1920) + 10.0;//map(z1, 0, 1920, -10, 10);

  
  calculate(x, y, z);
//  Serial.print(x1);
//  Serial.print("\t");
//  Serial.print(y);
//  Serial.print("\t");
//  Serial.println(z1);
  
  while(motor1.end() == 0 || motor2.end() == 0 || motor3.end() == 0) {
    motor1.run();
    motor2.run();
    motor3.run();
  }
}

ros::Subscriber<geometry_msgs::Point> sub("/mouse_position", moving);

void setup() {
  nh.initNode();
  nh.subscribe(sub);

// Serial.b/egin(57600);
}

float l1 = 16;
float l2 = 18.3;

long period = 500;

long cur;

int rate = 16;

int state = 0;

int type = 0;

//float i = 0;
// if (type == 0) {
//   Serial.println("Type(1: input, 2: circle, 3: origin) : ");
//   while (Serial.available() == 0) {}
//   type = Serial.parseFloat();
//   Serial.read();
// }

// if (type == 1) {
//   Serial.println("Enter The x Coordinate");
//   while (Serial.available() == 0) {}
//   x = Serial.parseFloat();
//   Serial.read();

//   Serial.println("Enter The y Coordinate");
//   while (Serial.available() == 0) {}
//   y = Serial.parseFloat();
//   Serial.read();

//   Serial.println("Enter The z Coordinate");
//   while (Serial.available() == 0) {}
//   z = Serial.parseFloat();
//   Serial.read();

//   Serial.print("x, y, z = ");
//   Serial.print(x);
//   Serial.print(", ");
//   Serial.print(y);
//   Serial.print(", ");
//   Serial.println(z);

//   type = 0;
// } else if (type == 2) {
//   float rad = i * 3.14 / 180.;
//   x = 20 + 4 * cos(rad);
//   y = -6;
//   z = 4 * sin(rad) * 0.8;
//   // x = 13+i*1.3;
//   // y = -6.2;
//   // z = -i;
//  i = i + 20;
//   if (i <= 360) {
//     type = 2;
//   } else {
//     Serial.println("End");
//     type = 0;
//     i = 0;
//     x = 18.3;
//     y = 16;
//     z = 0;
//   }
// } else if (type == 3) {
//   type = 0;
//   x = 18.3;
//   y = 16;
//   z = 0;
// }

float theta1_pre = 90;
float theta1_cur = 90;
float theta2_pre = 90;
float theta2_cur = 90;
float theta3_pre = 0;
float theta3_cur = 0;

void calculate(float x, float y, float z) {

  float angle1;
  float angle2;
  float angle3;

  int num1;
  int num2;
  int num3;

  float r = sqrt(x * x + y * y + z * z);
  float xz = sqrt(x * x + z * z);

  theta1_cur = (atan2(y, xz) + acos((l1 * l1 + r * r - l2 * l2) / (2 * l1 * r))) * 180 / 3.141592;  // 0 ~ 180
  theta2_cur = acos((l1 * l1 + l2 * l2 - r * r) / (2 * l1 * l2)) * 180 / 3.141592;                  // 0 ~ 180
  theta3_cur = atan2(z, x) * 180 / 3.141592;                                                        // -90 ~ 90

  angle1 = theta1_pre - theta1_cur;
  angle2 = theta2_pre - theta2_cur + angle1;
  angle3 = theta3_pre - theta3_cur;

  theta1_pre = theta1_cur;
  theta2_pre = theta2_cur;
  theta3_pre = theta3_cur;

  num1 = round(rate * abs(angle1) / 0.18);
  num2 = round(rate * abs(angle2) / 0.18);
  num3 = round(4 * rate * abs(angle3) / 1.8);

  long max_ = (num1 > num2) && (num1 > num3) ? num1 : (num2 > num3 ? num2 : num3);

  motor1.get_value(num1, max_, period, -angle1);
  motor2.get_value(num2, max_, period, angle2);
  motor3.get_value(num3, max_, period, angle3);
}



void loop() {
  nh.spinOnce();
  delay(1);
}
