
#ifndef _STATE_MACHINE_
#define _STATE_MACHINE_

typedef enum { 
  KILL=0, 
  IDLE, 
  TANK, 
  SPIN 
} state_t;

void kill_state(state_t* state);
void idle_state(state_t* state);
void tank_state(state_t* state);
void spin_state(state_t* state);

#endif
