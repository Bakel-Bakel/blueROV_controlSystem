#include <GLFW/glfw3.h>
#include <GL/glut.h>  // GLUT for rendering text
#include <iostream>
#include <vector>
#include <cmath>
#include <thread>
#include <chrono>
#include <sstream>

// PID Controller Class
class PIDController {
public:
    PIDController(double kp, double ki, double kd, double setpoint, double dt = 0.1)
        : kp(kp), ki(ki), kd(kd), setpoint(setpoint), dt(dt), previous_error(0), integral(0) {}

    double compute(double current_depth) {
        double error = setpoint - current_depth;
        integral += error * dt;
        double derivative = (error - previous_error) / dt;

        double output = (kp * error) + (ki * integral) + (kd * derivative);
        previous_error = error;

        // Limit output (thrust) to prevent excessive movement
        double max_thrust = 10;
        return std::max(std::min(output, max_thrust), -max_thrust);
    }

private:
    double kp, ki, kd;
    double setpoint;
    double dt;
    double previous_error;
    double integral;
};

// ROV Class
class ROV {
public:
    ROV(double initial_depth = 0) : depth(initial_depth) {}

    void apply_thrust(double thrust) {
        depth += thrust * 0.05;  // Simulated depth change
    }

    double get_depth() const {
        return depth;
    }

private:
    double depth;
};

// OpenGL Variables
std::vector<float> depth_values;
std::vector<float> control_values;
int time_counter = 0;
const int max_points = 100;
const double target_depth = 10.0;
double current_depth = 0;
double control_signal = 0;

// Function to Draw Graphs
void drawGraph(std::vector<float>& values, float r, float g, float b, float y_offset = 0) {
    glColor3f(r, g, b);
    glBegin(GL_LINE_STRIP);
    for (size_t i = 0; i < values.size(); ++i) {
        float x = -1.0f + (2.0f * i / max_points);  // Scale X-axis
        float y = -1.0f + (2.0f * (values[i] + 15) / 30) + y_offset; // Scale Y-axis
        glVertex2f(x, y);
    }
    glEnd();
}

// Function to Render Text in OpenGL
void renderText(float x, float y, const std::string& text, float r, float g, float b) {
    glColor3f(r, g, b);
    glRasterPos2f(x, y);
    for (char c : text) {
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, c);
    }
}

// OpenGL Render Loop
void renderLoop(GLFWwindow* window) {
    while (!glfwWindowShouldClose(window)) {
        glClear(GL_COLOR_BUFFER_BIT);

        // Draw Depth Graph (Red)
        drawGraph(depth_values, 1.0f, 0.0f, 0.0f);

        // Draw Control Signal Graph (Blue)
        drawGraph(control_values, 0.0f, 0.0f, 1.0f, -0.5f);

        // Draw Target Depth Line (Green Dashed)
        glColor3f(0.0f, 1.0f, 0.0f);
        glBegin(GL_LINES);
        glVertex2f(-1.0f, -1.0f + (2.0f * (target_depth + 15) / 30));
        glVertex2f(1.0f, -1.0f + (2.0f * (target_depth + 15) / 30));
        glEnd();

        // Display Current Values as Text
        std::ostringstream depth_text, control_text, target_text;
        depth_text << "Current Depth = " << current_depth << " m";
        control_text << "Control Signal = " << control_signal;
        target_text << "Target Depth = " << target_depth << " m";

        renderText(-0.9f, 0.9f, depth_text.str(), 1.0f, 0.0f, 0.0f);   // Red Text
        renderText(-0.9f, 0.8f, control_text.str(), 0.0f, 0.0f, 1.0f); // Blue Text
        renderText(-0.9f, 0.7f, target_text.str(), 0.0f, 1.0f, 0.0f);  // Green Text

        glfwSwapBuffers(window);
        glfwPollEvents();

        // Simulate Data Updates (PID Control)
        static ROV rov;
        static PIDController pid(1.2, 0.1, 0.5, target_depth);
        current_depth = rov.get_depth();
        control_signal = pid.compute(current_depth);
        rov.apply_thrust(control_signal);

        // Store Data
        if (depth_values.size() >= max_points) {
            depth_values.erase(depth_values.begin());
            control_values.erase(control_values.begin());
        }
        depth_values.push_back(current_depth);
        control_values.push_back(control_signal);

        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}

int main(int argc, char** argv) {
    // Initialize GLUT (for Text Rendering)
    glutInit(&argc, argv);

    // Initialize OpenGL
    if (!glfwInit()) {
        std::cerr << "Failed to initialize GLFW\n";
        return -1;
    }

    GLFWwindow* window = glfwCreateWindow(800, 600, "ROV Depth Control", NULL, NULL);
    if (!window) {
        std::cerr << "Failed to create GLFW window\n";
        glfwTerminate();
        return -1;
    }

    glfwMakeContextCurrent(window);
    glClearColor(0.0f, 0.0f, 0.0f, 1.0f); // Set background color

    // Run the OpenGL render loop
    renderLoop(window);

    glfwDestroyWindow(window);
    glfwTerminate();
    return 0;
}

