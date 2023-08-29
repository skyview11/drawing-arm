#include "step_motor.h"

void stepping_motor::run() {
  long cur = micros();
  if (num > 0) {
    if (cur - pre <= period) {
      digitalWrite(stp, HIGH);
    } else {
      digitalWrite(stp, LOW);
      pre = cur;
      num--;
    }
  } else {
    finish = 1;
  }
}

void stepping_motor::get_value(int num_, int max_, long period_, float angle) {
  num = num_;

  if (num) {
    period = long(period_ * max_ / num);
  } else {
    period = period_;
  }

  if (angle > 0) {
    digitalWrite(dir, HIGH);
  } else {
    digitalWrite(dir, LOW);
  }
  
  finish = 0;
}

int stepping_motor::end() {
  return finish;
}
