import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        # Simulate depth change based on thrust
        self.depth += thrust * 0.05  # Depth adjustment

    def get_depth(self):
        return self.depth


# Tkinter GUI Class
class PIDGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ROV Depth Control Simulator")

        # Default PID Values
        self.Kp = 1.2
        self.Ki = 0.1
        self.Kd = 0.5
        self.target_depth = 10

        # Create ROV and PID Controller
        self.rov = ROV()
        self.pid = PIDController(self.Kp, self.Ki, self.Kd, self.target_depth)

        # UI Elements
        self.create_widgets()

        # Plot Initialization
        self.time_steps = []
        self.depth_values = []
        self.time_counter = 0

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.ax.set_ylim(-2, 15)  # Depth range
        self.ax.set_xlim(0, 50)
        self.ax.set_xlabel("Time Steps")
        self.ax.set_ylabel("Depth (m)")
        self.ax.set_title("ROV Depth Control")
        self.depth_line, = self.ax.plot([], [], 'r-', lw=2, label="Depth")
        self.ax.axhline(self.target_depth, color='blue', linestyle='--', label="Target Depth")
        self.ax.legend()

        # Embed Matplotlib Plot in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=6, padx=10, pady=10)

        # Initialize Animation
        self.ani = None

    def create_widgets(self):
        # Depth Input
        ttk.Label(self.root, text="Desired Depth:").grid(row=0, column=0)
        self.depth_entry = ttk.Entry(self.root)
        self.depth_entry.grid(row=0, column=1)
        self.depth_entry.insert(0, str(self.target_depth))

        # Simulate Button
        self.simulate_button = ttk.Button(self.root, text="Simulate", command=self.start_simulation)
        self.simulate_button.grid(row=1, column=0, columnspan=2, pady=5)

    def start_simulation(self):
        # Get desired depth from user input
        self.target_depth = float(self.depth_entry.get())

        # Reset ROV and PID Controller
        self.rov = ROV()
        self.pid = PIDController(self.Kp, self.Ki, self.Kd, self.target_depth)

        # Reset Data Storage
        self.time_steps = []
        self.depth_values = []
        self.time_counter = 0

        # Reset Target Depth Line
        self.ax.axhline(self.target_depth, color='blue', linestyle='--', label="Target Depth")
        self.canvas.draw()

        # Start Animation
        if self.ani is not None:
            self.ani.event_source.stop()
        self.ani = FuncAnimation(self.fig, self.update_plot, frames=100, interval=100)

    def update_plot(self, frame):
        current_depth = self.rov.get_depth()
        control_signal = self.pid.compute(current_depth)
        self.rov.apply_thrust(control_signal)

        # Store Data
        self.time_steps.append(self.time_counter)
        self.depth_values.append(current_depth)
        self.time_counter += 1

        # Update depth plot
        self.depth_line.set_data(self.time_steps, self.depth_values)
        self.ax.set_xlim(max(0, self.time_counter - 50), max(50, self.time_counter))

        self.canvas.draw()


# Run the GUI
root = tk.Tk()
app = PIDGUI(root)
root.mainloop()

