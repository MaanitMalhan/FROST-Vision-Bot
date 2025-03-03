from pwm import PWMController  

LEFT_MOTOR_PIN = 12
RIGHT_MOTOR_PIN = 13

# Set initial frequency
FREQUENCY = 1000  # Hz

left_motor = 100#PWMController(LEFT_MOTOR_PIN, FREQUENCY)
right_motor = 1000#PWMController(RIGHT_MOTOR_PIN, FREQUENCY)

        

try:
    while True:
        # Get user input for motor speeds
        left_speed = int(input("left"))
        right_speed = int(input("right"))

        # Set motor speeds using duty cycle
        left_motor.set_duty_cycle(left_speed)
        right_motor.set_duty_cycle(right_speed)

except KeyboardInterrupt:
    print("\nStopping motors and cleaning up...")
    left_motor.cleanup()
    right_motor.cleanup()
