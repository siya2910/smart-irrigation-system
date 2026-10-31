# smart-irrigation-system
Arduino-based Smart Irrigation System with a Streamlit dashboard
# 🌱 Smart Irrigation System Using Arduino and Python

An IoT-oriented Smart Irrigation System designed to monitor soil moisture and support efficient water management using an Arduino, a soil moisture sensor, a relay-controlled water pump, and a Python-based Streamlit dashboard.

The project combines hardware and software to demonstrate how soil moisture monitoring can be integrated with a digital dashboard for observing sensor readings and irrigation activity.

## 🚀 Live Dashboard

**Access the deployed application here:**

[🌐 Open Smart Irrigation Dashboard](https://smart-irrigation-system-l5cnedmi6jqvmybrffn2zt.streamlit.app/)

The dashboard provides a visual interface for monitoring soil moisture readings and viewing available monitoring information.

> **Note:** The online Streamlit application runs in the cloud and cannot directly access an Arduino connected to a user's local USB/COM port. Live hardware communication is intended to run through the local computer unless an internet-connected communication method is added. Online demonstration data may be simulated.

---

## 📌 Project Overview

Traditional irrigation methods often rely on fixed schedules or manual observation. This can result in unnecessary water consumption, especially when plants receive water despite already having sufficient soil moisture.

The Smart Irrigation System addresses this problem by using a soil moisture sensor to measure the moisture level of the soil. An Arduino Nano reads the sensor output and can control a miniature water pump through a relay module according to the programmed irrigation logic.

A Python-based dashboard provides a convenient way to observe the system's readings and monitoring history.

### 🎯 Objectives

- Monitor soil moisture using a sensor.
- Read and process sensor values through Arduino Nano.
- Control a water pump using a relay module.
- Reduce unnecessary water usage through moisture-based irrigation logic.
- Display sensor readings through a Python and Streamlit dashboard.
- Maintain a visual record of readings and system activity.
- Demonstrate the integration of embedded hardware and software.

---

## 🧰 Hardware Components

| Component | Purpose |
|---|---|
| Arduino Nano | Main microcontroller |
| Soil Moisture Sensor | Measures soil moisture |
| Relay Module | Controls the water pump circuit |
| Miniature Water Pump | Supplies water to the plant |
| 9V Batteries / Suitable Power Supply | Provides power to the circuit |
| Breadboard | Supports circuit connections |
| Jumper Wires | Connects electronic components |
| USB Cable | Connects Arduino to the computer |

## 💻 Software and Technologies

- **Arduino IDE:** Writing and uploading the microcontroller program.
- **Python:** Serial communication and dashboard functionality.
- **Streamlit:** Building the interactive web dashboard.
- **PySerial:** Communicating with Arduino through the serial port.
- **Pandas:** Organizing and processing readings, where used.
- **GitHub:** Source code hosting and version control.
- **Streamlit Community Cloud:** Hosting the online dashboard.

---

## ⚙️ System Architecture

The project follows this general data flow:

```text
       SOIL
         |
         v
  Soil Moisture Sensor
         |
         v
     Arduino Nano
         |
         +--------------------+
         |                    |
         v                    v
    Relay Module         USB Serial
         |                    |
         v                    v
     Water Pump          Python Program
                              |
                              v
                       Streamlit Dashboard
                              |
                              v
                     Moisture Visualization
                     Readings and History
```

The Arduino handles sensor acquisition and hardware control, while the Python application receives serial data and presents monitoring information through the dashboard.

---

## 🔄 Working Workflow

### 1. Soil Moisture Detection

The soil moisture sensor is placed in the soil near the plant roots.

It detects changes in soil moisture and produces an electrical output corresponding to the moisture condition.

### 2. Data Acquisition by Arduino

The sensor output is connected to the Arduino Nano.

The Arduino continuously reads the sensor value and processes it according to the programmed logic.

### 3. Moisture-Based Irrigation Decision

The Arduino program can compare the sensor reading with a predefined threshold.

- If the soil is dry, the irrigation logic can activate the relay and switch on the pump.
- If the soil has sufficient moisture, the pump can remain switched off.

The threshold should be calibrated using actual dry-soil and wet-soil readings.

### 4. Relay-Based Pump Control

The relay module acts as an electrically controlled switch.

It allows the Arduino to control the miniature water pump without directly powering the pump from an Arduino output pin.

### 5. Serial Communication

The Arduino sends sensor readings to the computer through a USB serial connection.

The Python application reads the incoming serial data using the appropriate COM port and baud rate.

For the development setup, the serial configuration used was:

- **COM Port:** COM9 (may differ on other computers)
- **Baud Rate:** 9600

### 6. Python Dashboard Processing

The Python application receives the serial readings and processes them for display.

The application can organize incoming readings, maintain recent history, and provide data for visualization.

### 7. Streamlit Dashboard Visualization

The Streamlit dashboard provides a user-friendly interface to observe:

- Soil moisture readings.
- Current monitoring information.
- Historical readings.
- Graphical visualization of sensor data.
- Available system and connection status information.

### 8. Continuous Monitoring

The monitoring process can continue as new readings arrive from the Arduino.

This allows users to observe changing soil conditions and understand the irrigation system's operation.

---

## 🖥️ Dashboard Usage

The online dashboard can be accessed without installing the project locally.

### Step 1: Open the application

Visit:

[https://smart-irrigation-system-l5cnedmi6jqvmybrffn2zt.streamlit.app/](https://smart-irrigation-system-l5cnedmi6jqvmybrffn2zt.streamlit.app/)

### Step 2: Explore the dashboard

View the available soil moisture readings, graphs, history, and connection information.

### Step 3: Understand the readings

Observe changes in sensor values and use the visualization to understand soil moisture conditions.

### Step 4: Local hardware monitoring

For direct communication with the Arduino, run the Python dashboard locally on a computer connected to the Arduino through USB.

**Important:** The cloud-hosted dashboard cannot access a local COM port such as COM9. Direct hardware monitoring requires the local application or an additional internet-connected hardware communication method.

---

## 🛠️ Installation and Local Setup

To run the project locally, follow these steps.

### Prerequisites

- Python installed on your computer.
- Arduino IDE.
- Arduino Nano and required hardware components.
- USB cable for Arduino communication.
- Git installed (optional).

### 1. Clone the repository

```bash
git clone https://github.com/siya2910/smart-irrigation-system.git
```

### 2. Open the project directory

```bash
cd smart-irrigation-system
```

### 3. Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Upload the Arduino program

Open the Arduino source code in Arduino IDE, select the correct Arduino board and COM port, and upload the program.

### 6. Connect the Arduino

Connect the Arduino Nano to the computer through USB.

Identify the correct COM port from the Arduino IDE or Windows Device Manager.

### 7. Run the Streamlit dashboard

```bash
streamlit run app.py
```

The application will open in your default browser. If it does not, open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

---

## 📁 Repository Structure

```text
smart-irrigation-system/
│
├── app.py
│   └── Python Streamlit dashboard application
│
├── requirements.txt
│   └── Python project dependencies
│
├── README.md
│   └── Project documentation
│
└── Arduino source code
    └── Add the Arduino sketch here if included
```

---

## 🌟 Key Features

- Soil moisture monitoring.
- Arduino-based sensor data acquisition.
- Relay-based water pump control.
- Serial communication between Arduino and computer.
- Python-based data processing.
- Streamlit-based interactive dashboard.
- Visual monitoring of sensor readings.
- Historical data visualization.
- Cloud-hosted dashboard access.

---

## 🔮 Future Improvements

The project can be extended with additional features:

- ESP32 or Wi-Fi-based communication for remote hardware monitoring.
- Real-time cloud data synchronization.
- Mobile-friendly monitoring interface.
- Automatic irrigation scheduling.
- Multiple soil moisture sensors for different plants.
- Water-level monitoring.
- Notifications when soil moisture becomes too low.
- Cloud-based storage and analytics.
- Improved calibration and irrigation threshold configuration.

---

## ⚠️ Safety and Calibration Notes

- Calibrate the soil moisture sensor before using it for automatic irrigation.
- Sensor readings can vary depending on the soil type and sensor model.
- Use an appropriate external power supply for the water pump.
- Do not power the pump directly from an Arduino GPIO pin.
- Check relay ratings and wiring before operating the pump.
- Keep electrical connections protected from water.

---

## 👩‍💻 Project Information

**Project Name:** Smart Irrigation System Using Arduino and Python

**Repository:** [smart-irrigation-system](https://github.com/siya2910/smart-irrigation-system)

**Live Application:** [Streamlit Smart Irrigation Dashboard](https://smart-irrigation-system-l5cnedmi6jqvmybrffn2zt.streamlit.app/)

**Technologies:** Arduino, Python, Streamlit, Serial Communication, GitHub

---

## 📜 Conclusion

The Smart Irrigation System demonstrates the integration of embedded systems, sensor technology, and software-based monitoring to support efficient irrigation.

By combining soil moisture sensing, Arduino-based control, relay-operated pumping, and a Python dashboard, the project provides a practical demonstration of automation and digital monitoring in agriculture.

The project can be further developed into an internet-connected smart agriculture solution with remote monitoring, cloud-based data collection, and intelligent irrigation control.
