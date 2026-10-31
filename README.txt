# Smart Irrigation Dashboard

A local dark-themed Streamlit dashboard for an Arduino Nano connected over USB serial.

## 1. Requirements
- Windows 10/11
- Python 3.10 or newer
- Arduino Nano connected by USB
- Arduino sketch printing lines such as `Soil Moisture Level: 1023`
- Arduino sketch accepting `1` to activate and `0` to deactivate

## 2. Install
Open Command Prompt in this folder and run:

```bat
py -m venv .venv
.venv\Scripts\activate
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

## 3. Run
```bat
py -m streamlit run app.py
```

The dashboard opens in your browser, usually at http://localhost:8501.
Choose COM9 (or the port shown in Device Manager) in the sidebar and use the same baud rate as `Serial.begin(...)` in your Arduino sketch. The default is 9600.

## 4. Important
Close Arduino IDE Serial Monitor before connecting the dashboard. Only one program can normally use COM9 at a time.

The dashboard sends exactly one character (`1` or `0`) without a newline, matching sketches that read commands with `Serial.read()`.

If your sketch uses `Serial.parseInt()` or expects a newline, tell us or adjust the send commands accordingly.

The moisture display is a raw analog value, not a percentage. Calibrate the sensor in dry and wet soil before converting it to a percentage.

The dashboard's ON/OFF text reflects the serial messages/commands. It does not independently verify that a pump or relay physically switched.
