import time
import gii_bluerov as blue
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# PID Constants
Kp = 1.2
Ki = 0.1
Kd = 0.5
setpoint = 10  # Desired depth
dt = 0.1  # Time step

# Data Storage for Visualization
time_steps = []
depth_values = []
signal_values = []
time_counter = 0

# Set up my visual feedback
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_ylim(-20, 5)  # Depth range
ax.set_xlim(0, 50)
ax.set_xlabel("Time Steps")
ax.set_ylabel("Depth (m)")
ax.set_title("ROV Depth Control")
depth_line, = ax.plot([], [], 'r-', lw=2, label="Depth")
ax.axhline(-setpoint, color='green', linestyle='--', label="Target Depth")  # Target depth line
ax.axhline(0,color="blue", linestyle='--', label = 'Sea Level')
ax.legend()


# Connect to the Vehicle autopilot.
'''connection_string="192.168.3.20:14552"
print("Connecting to vehicle on: %s" % (connection_string,))
autopilot = dronekit.connect(connection_string, wait_ready=True)

# Arm to move the robot
autopilot.armed=True
'''


# PID Variables
previous_error = 0
integral = 0
current_depth = 0
#current_depth = autopilot.location.global_relative_frame.alt  # Initial depth


def compute(current_depth):
    global previous_error, integral

    error = setpoint - current_depth
    integral += error * dt
    derivative = (error - previous_error) / dt

    output = (Kp * error) + (Ki * integral) + (Kd * derivative)
    previous_error = error

    return output  # Only allow downward thrust



def update(frame):
    global current_depth, time_counter

    control_signal = compute(current_depth)

    blue.move_rov (autopilot, "z","displacement", speed_percentage=10)
    
    print(control_signal)

    current_depth += control_signal * 0.05
    #current_depth = autopilot.location.global_relative_frame.alt  # Initial depth
    print(current_depth)

    # Store Data
    time_steps.append(time_counter)
    depth_values.append(-1 * current_depth)  # Negative depth for downward movement
    signal_values.append(control_signal)
    time_counter += 1

    # Update plot
    depth_line.set_data(time_steps, depth_values)
    ax.set_xlim(max(0, time_counter - 50), max(50, time_counter))

    return depth_line


# Animation
ani = FuncAnimation(fig, update, frames=100, interval=100)

# Show plot
plt.show()
