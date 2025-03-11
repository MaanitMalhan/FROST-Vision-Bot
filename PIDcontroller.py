import matplotlib.pyplot as plt
import numpy as np

# Increase Kp to make the system more responsive but watch for overshoot.
# Increase Ki to eliminate steady-state error but be careful with integral windup, which can cause instability.
# Increase Kd to smooth the response by reducing oscillations, though too much can cause a slow response.

def PIDcontroller():
    motor_speed = int(input("Input initial motor speed: "))  # Initial motor speed (RPM)
    setpoint = int(input("Input desired motor speed: ")) # Desired motor speed (RPM)
    Kp = 0.1        # Proportional gain
    Ki = 0.01       # Integral gain
    Kd = 0.05       # Derivative gain
    dt = 0.1        # Time step for simulation (seconds)
    sim_time = 150   # Total simulation time (seconds)

    integral = 0
    previous_error = 0

    # Store data for plotting
    time_data = []
    speed_data = []

    

    for t in np.arange(0, sim_time, dt):
        # Calculate error between setpoint and current motor speed
        error = setpoint - motor_speed

    # Proportional term
        P_out = Kp * error
        
        # Integral term (accumulation of past errors)
        integral += error * dt
        I_out = Ki * integral
        
        # Derivative term (rate of change of error)
        derivative = (error - previous_error) / dt
        D_out = Kd * derivative

    # Calculate the total control output
        control_output = P_out + I_out + D_out
        
        # Simulate the motor speed response (simplified linear response)
        motor_speed += control_output * dt

    # Update the previous error for the next iteration
        previous_error = error
        
        # Save data for plotting
        time_data.append(t)
        speed_data.append(motor_speed)
    

    # Plot the motor speed over time
    plt.plot(time_data, speed_data)
    plt.title('DC Motor Speed with PID Control')
    plt.xlabel('Time (s)')
    plt.ylabel('Speed (RPM)')
    plt.grid(True)
    plt.show()

    return speed_data

def main():
    speed_data = PIDcontroller()
    print("Speed Data at every 10th step:")
    for i in range(0, len(speed_data), 10): # prints evert 10 values
        print(f"Speed {i}: {speed_data[i]}")

if __name__ == "__main__":
    main()