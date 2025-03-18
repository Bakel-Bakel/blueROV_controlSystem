import matplotlib.pyplot as plt
import time
from matplotlib.animation import FuncAnimation

# PID Controller Class
class PIDController:
    def __init__(self, kp, ki, kd, setpoint, dt=0.1):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.dt = dt
        self.previous_error = 0
        self.integral = 0

    def compute(self, current_depth):
        error = self.setpoint - current_depth
        self.integral += error * self.dt
        derivative = (error - self.previous_error) / self.dt

        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)

        self.previous_error = error

        # Limit output (thrust) to prevent excessive movement
        max_thrust = 10
        return max(min(output, max_thrust), -max_thrust)


# ROV Class
class ROV:
    def __init__(self, initial_depth=0):
        self.depth = initial_depth

    def apply_thrust(self, thrust):
        # Simulate depth change based on thrust (simplified physics)
        self.depth += thrust * 0.05  # Assume a basic relationship

    def get_depth(self):
        return self.depth


# PID Gains
Kp = 1.2
Ki = 0.1
Kd = 0.5
target_depth = 10  # Target depth in meters

# Create ROV and PID Controller
rov = ROV()
pid = PIDController(Kp, Ki, Kd, target_depth)

# Data Storage for Visualization
time_steps = []
depth_values = []
thrust_values = []
time_counter = 0

# Set up figure
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_ylim(-2, 15)  # Depth range
ax.set_xlim(0, 50)
ax.set_xlabel("Time Steps")
ax.set_ylabel("Depth (m)")
ax.set_title("ROV Depth Control")
depth_line, = ax.plot([], [], 'r-', lw=2, label="Depth")
thrust_line, = ax.plot([], [], 'b-', lw=2, label="Thrust")
ax.axhline(target_depth, color='green', linestyle='--', label="Target Depth")  # Target depth line
ax.legend()


# Update function for animation
def update(frame):
    global time_counter
    current_depth = rov.get_depth()
    control_signal = pid.compute(current_depth)
    rov.apply_thrust(control_signal)

    # Store Data
    time_steps.append(time_counter)
    depth_values.append(current_depth)
    thrust_values.append(control_signal)
    time_counter += 1

    # Update plots
    depth_line.set_data(time_steps, depth_values)
    thrust_line.set_data(time_steps, thrust_values)
    ax.set_xlim(max(0, time_counter - 50), max(50, time_counter))

    return depth_line, thrust_line


# Animation
ani = FuncAnimation(fig, update, frames=100, interval=100)

# Show plot
plt.show()

