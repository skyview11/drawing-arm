#include "Arduino.h"
#include <string.h>

using namespace std;

class stepping_motor{
  private:

  int dir;  // 방향 설정 핀 link(LOW : 멀어짐, HIGH : 당김) base(LOW : cw, HIGH : ccw)
  int stp;
  int num;
  int finish = 0;
  long pre = 0;
  long period;

  public:
  stepping_motor() { } // default initiallizer
  stepping_motor(int dir_, int stp_) {
    dir = dir_;
    stp = stp_;

    pinMode(dir, OUTPUT);
    pinMode(stp, OUTPUT);
  } // custom initiallizer
  void run();
  void get_value(int num_, int max_, long period_, float angle);
  int end();
};
