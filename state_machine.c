
#include "state_machine.h"

// NOTE: states are different than control, states->control
void kill_state(state_t* state) {
  *state = KILL;
  // TODO: set the motor speed to 0, pull disable pins
  // block the MB from doing anything else
  // swallenhardware uses " digitalWrite(enablePin, HIGH); " for blocking/disabling
  while (1) 0;  // lets the run to reset
}

void idle_state(state_t* state) {
  *state = IDLE;
  // TODO: set the motor speed to 0, no blocking
  // disable movement
  
}

void tank_state(state_t* state) {
  *state = TANK;
  // TODO: implement tank state
  // enable movement
}

void spin_state(state_t* state) {
  *state = SPIN;
  // TODO: implement spin state
  // enable movement
}
