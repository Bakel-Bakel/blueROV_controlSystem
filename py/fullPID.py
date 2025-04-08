# script example to operate the bluerow using python
import threading
import gii_bluerov
import dronekit
from time import sleep
import matplotlib.pyplot as plt

def rovPID():
    # Connect to the Vehicle autopilot.
    connection_string="192.168.3.20:14552"
    print("Connecting to vehicle on: %s" % (connection_string,))
    autopilot = dronekit.connect(connection_string, wait_ready=True)

    # Get some vehicle attributes (state)
    print (" Battery: %s" % autopilot.battery)

    # Arm to move the robot
    autopilot.armed=True
    sleep(5.0)
    print ("%s" % autopilot.armed)
    print(autopilot.location.global_relative_frame.alt)

    # PID Constants
    Kp = 100
    Ki = 25
    Kd = 0
    setpoint = -1  # Desired depth (e.g., 1 meter)
    dt = 0.1      # Time step in seconds

    # PID Variables
    previous_error = 0
    integral = 0
    current_depth = autopilot.location.global_relative_frame.alt  # Initial depth

    def compute(current_depth):
        global previous_error, integral

        error = setpoint - current_depth
        print(f"Error = {error}")
        integral += error * dt
        derivative = (error - previous_error) / dt

        output = (Kp * error) + (Ki * integral) + (Kd * derivative)
        previous_error = error

        return round(output)  # Output is the control signal (thrust)

    # Simulate PID controller over time
    for i in range(50000):  # Run for 5 seconds (50 steps * 0.1s)
        
        control_signal = compute(current_depth)
        gii_bluerov.move_rov (autopilot, "z","displacement", control_signal)
        sleep(0.9)
        # Simulate the system response (very basic physics)
        # Let's say thrust directly changes depth per time step
        current_depth = autopilot.location.global_relative_frame.alt  # You may add damping or system model here

        print(f"Time: {i * dt *10:.1f}s | Depth: {current_depth:.3f}m | Control: {control_signal:.3f}")

    # Disarm after using it
    autopilot.armed=False
    sleep(1.0)
    print ("%s" % autopilot.armed)

def test():
    print("second thread is running")

def visuals():
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
    # Animation
    ani = FuncAnimation(fig, update, frames=100, interval=100)
    # Show plot
    plt.show()


    