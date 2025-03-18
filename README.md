### **Project Name: ROV Depth Control using PID**  

**Description:**  
This project implements a **PID controller** to autonomously control the depth of a **Remotely Operated Vehicle (ROV)**. The PID algorithm adjusts the thrust applied to the ROV, ensuring it reaches and maintains a **desired depth** without oscillations or overshoot. The control logic prevents **unintended upward movement**, allowing for controlled descent only.  

The project includes:  
✅ A **PID loop** for depth control.  
✅ **Simulation** using Matplotlib (Optional GUI for visualization).  
✅ **Tkinter GUI** to enter the desired depth and start simulations.  
✅ **Real-world implementation** with `blue.move_rov()` function to send commands to the ROV's thrusters.  
✅ **Safety constraints** to prevent overshoot or unintended ascent.  

---

## **📜 README.md**
```markdown
# ROV Depth Control using PID

## 📌 Project Overview
This project implements a **PID controller** for a **Remotely Operated Vehicle (ROV)** to control its **depth autonomously**. It ensures precise depth control while preventing unintended upward movement.

## 🚀 Features
- **PID Control System** for stable depth regulation.
- **Simulation Mode** using Matplotlib for real-time depth tracking.
- **Tkinter GUI** for easy user input (desired depth, PID tuning).
- **Motor Control Logic** using `blue.move_rov()` to send depth commands.
- **Safety Constraints** to prevent oscillations and maintain stable depth.

## 🔧 Installation
Ensure you have Python installed. Install required dependencies:

```bash
pip install matplotlib
```

For GUI mode:
```bash
pip install tkinter
```

## 🛠 Usage

### **1️⃣ Run the Basic PID Control**
This script simulates an ROV reaching a set depth:
```bash
python pid_depth_control.py
```

### **2️⃣ Run the GUI Version**
To start the GUI where you can input depth values:
```bash
python rov_gui.py
```

### **3️⃣ Using PID for Real ROV Motors**
For actual ROV thruster control, use:
```python
blue.move_rov(autopilot, "z", "displacement", control_signal)
```
This sends commands to **descend to the desired depth**.




## 📜 License
MIT License. Feel free to modify and use the code as needed.

---
🚢 **Developed for underwater robotics and marine autonomy!**
```

# blueROV_controlSystem
