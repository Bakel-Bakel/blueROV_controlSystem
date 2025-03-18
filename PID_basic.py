import time
import gii_bluerov as blue

# PID Constants
Kp = 1.2
Ki = 0.1
Kd = 0.5
setpoint = -10  # Desired depth
dt = 0.1  # Time step

# PID Variables
previous_error = 0
integral = 0
current_depth = 0  # Initial depth

# Connect to the Vehicle autopilot.
connection_string="192.168.3.20:14552"
print("Connecting to vehicle on: %s" % (connection_string,))
autopilot = dronekit.connect(connection_string, wait_ready=True)

# Arm to move the robot
autopilot.armed=True

# Simulation Loop
for _ in range(100):  # Run for 100 iterations

    #Read current depth

    error = setpoint - current_depth
    integral += error * dt
    derivative = (error - previous_error) / dt

    # PID Control Output
    control_signal = (Kp * error) + (Ki * integral) + (Kd * derivative)

    # Prevent the ROV from moving up (only allow downward movement)
    control_signal = min(control_signal, 0)  # Clamps the value to a maximum of 0

    #Read current depth

    #Write to the appropraite motors
    blue.move_rov(autopilot, "z","displacement", control_signal)

    # Update error
    previous_error = error

    time.sleep(0.1)  # Simulate time delay

