# **ROV Depth Control using PID (C++ OpenGL Implementation)**  

## **📌 Project Overview**
This project implements a **PID controller** in **C++** to autonomously control the depth of a **Remotely Operated Vehicle (ROV)**. The visualization is done using **OpenGL** and **GLFW**, displaying real-time graphs for:  
✅ **Depth over time (Red line)**  
✅ **Control signal over time (Blue line)**  
✅ **Target depth (Green dashed line)**  
✅ **Real-time numerical values displayed in the OpenGL window**  

This implementation **does not rely on Python or Matplotlib**, making it significantly faster and more efficient.

---

## **🚀 Features**
- **PID Control System** for precise depth regulation.
- **Real-time Visualization** using OpenGL.
- **Graphical Representation** of Depth, Control Signal, and Target Depth.
- **Live Numerical Data Display** within the OpenGL window.
- **Cross-Platform Support** for Linux, Windows, and macOS.

---

## **🔧 Installation**
### **1️⃣ Install Dependencies**
#### **Linux (Ubuntu/Debian)**
```bash
sudo apt-get install libglfw3-dev freeglut3-dev
```
#### **Windows (MSYS2)**
```bash
pacman -S mingw-w64-x86_64-glfw mingw-w64-x86_64-freeglut
```
#### **MacOS (Homebrew)**
```bash
brew install glfw freeglut
```

### **2️⃣ Compile the Code**
```bash
g++ rov_pid.cpp -o rov_pid -lglfw -lGL -lfreeglut -lpthread
```

### **3️⃣ Run the Program**
```bash
./rov_pid
```

---

## **🛠 Usage**
- The **Red Line** represents the **ROV’s Depth** over time.
- The **Blue Line** represents the **PID Control Signal**.
- The **Green Dashed Line** is the **Target Depth**.
- The **Text Display** shows **real-time values** of Depth, Control Signal, and Target Depth.

### **🔹 Expected Output**
A **real-time OpenGL graph** showing:
1. **Depth decreasing toward the target value** (PID control).
2. **Control signal adjustments** (ensuring stability).
3. **Live text updates** for Depth, Control Signal, and Target Depth.

---

## **📜 Code Structure**
```
📂 ROV_Depth_Control_CPP/
│── 📝 README.md   # Project Documentation
│── 📜 rov_pid_opengl_text.cpp   # Main C++ OpenGL Implementation
│── 📜 rov_pid_opengl_multi.cpp  # Alternative with simplified graph
│── 📂 includes/   # (Optional) Header files for modularization
```

---

## **👨‍💻 Contributing**
Feel free to **open issues, report bugs, or suggest improvements** via **pull requests**!

---

## **📜 License**
This project is licensed under the **MIT License**. Feel free to modify and use the code for educational and research purposes.

---

🚢 **Developed for Autonomous Marine Robotics and ROV Navigation!** 🌊🚀
