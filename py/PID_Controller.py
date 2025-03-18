import time

class PIDController:
    def __init__(self, kp, ki, kd, setpoint, dt=0.1):
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.setpoint = setpoint  # Target depth
        self.dt = dt  # Time step

        self.previous_error = 0
        self.integral = 0

    def compute(self, current_depth):
        error = self.setpoint - current_depth
        self.integral += error * self.dt
        derivative = (error - self.previous_error) / self.dt

        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        self.previous_error = error

        return output


# Simulating the depth control of an ROV
class ROV:
    def __init__(self, initial_depth=0):
        self.depth = initial_depth  # Current depth
        self.thrust = 0  # Thrust force applied

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

pid = PIDController(Kp, Ki, Kd, target_depth)
rov = ROV()

# Simulation loop
for _ in range(1000):
    current_depth = rov.get_depth()
    control_signal = pid.compute(current_depth)
    rov.apply_thrust(control_signal)

    print(f"Depth: {current_depth:.2f}m, Thrust: {control_signal:.2f}")

    time.sleep(0.1)  # Simulating time delay

