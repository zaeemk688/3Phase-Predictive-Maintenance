# ⚡ QUICK START GUIDE - 3-Phase Predictive Maintenance

## 🚀 START THE SYSTEM (3 Simple Steps)

### Step 1: Start Python Server
```bash
cd d:\final code every thing
.venv\Scripts\Activate.ps1
python server.py
```
✅ You should see:
```
🚀 Starting SCADA Predictive Maintenance Backend...
📡 WebSocket listening on ws://localhost:8000/ws
[+] Device Connected! Total active connections: 1
```

### Step 2: ESP32 Should Auto-Connect
- If already uploaded with firmware ✅
- Serial output shows: `✅ [WS] Link established with Python Server!`
- Server shows: `[+] Device Connected!`

### Step 3: Open Dashboard
```
Browser: file:///d:/final%20code%20every%20thing/flowcharts/flowchart.html
```
✅ You should see live graphs updating every second

---

## 🔌 BUILD & UPLOAD ESP32 (When Code Changed)

```bash
# Terminal:
cd c:\Users\zaeem\Documents\PlatformIO\Projects\test

# Compile
platformio run

# Upload to ESP32
platformio run --target upload

# Watch Serial Monitor
platformio device monitor --baud=115200
```

Expected Serial Output:
```
[BOOT] 3-Phase AI Predictive Node Starting...
[SYS] Relays Armed and set to OPEN (Safe state)
✅ [WIFI] Connected! IP Address: 192.168.10.13
✅ [SYS] All 3 ADS1115 Modules Online (12 Channels Active)
✅ [SYS] WebSocket Subsystem Armed.
📡 [TX] Live Telemetry Streamed to AI Engine.
📡 [TX] Live Telemetry Streamed to AI Engine.
...
```

---

## 🔧 COMMON TASKS

### Update WiFi Credentials
File: `c:\...\test\src\main.cpp` (Lines 14-16)
```cpp
const char* ssid     = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";
const char* serverIP = "YOUR_PC_IP";     // Get from: ipconfig
```
Then: Build → Upload

### Change Server Port
File: `c:\...\test\src\main.cpp` (Line 18)
```cpp
const uint16_t serverPort = 8000;  // Change here if needed
```
File: `d:\final code every thing\server.py` (Last line)
```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Change here
```

### Find DS18B20 Sensor Addresses
1. Upload: `onewire_scanner.cpp.bak`
2. Open Serial Monitor
3. Copy addresses from output
4. Update in `main.cpp` lines 20-22:
```cpp
DeviceAddress probe_A = { 0x28, 0x58, 0x7A, 0x81, 0xE3, 0xE1, 0x3C, 0xCA };
DeviceAddress probe_B = { 0x28, 0xFF, 0x64, 0x18, 0xC3, 0x16, 0x05, 0x1B };
DeviceAddress probe_C = { 0x28, 0x1F, 0xC4, 0x07, 0xD6, 0x01, 0x3C, 0xDF };
```

### Enable/Disable Relay
Relay Control JSON (from server to ESP32):
```json
{"relay":"MC0", "state":0}  // MC0=ON  (state: 0=ON, 1=OFF)
{"relay":"MC1", "state":1}  // MC1=OFF
{"relay":"MC2", "state":0}  // MC2=ON
{"relay":"MC3", "state":1}  // MC3=OFF
```

### Check Sensor Values
Open Serial Monitor → Watch telemetry packets:
```
{
  "env":{"humidity":45,"temp":28.3,"smoke":412,"flame":250},
  "thermal":{"phaseA":28.7,"phaseB":29.1,"phaseC":28.9},
  "main":{"v1":2048,"v2":2045,"v3":2047,"i1":512,...},
  "branch":{"v1":1024,"v2":1023,"v3":1025,"i1":256,...}
}
```

---

## 🐛 QUICK FIXES

| Problem | Fix |
|---------|-----|
| ESP32 won't connect | Check WiFi SSID/password/IP in main.cpp lines 14-18 |
| No temperature readings | Run OneWire scanner, update addresses |
| Dashboard blank | Check server is running, verify file path has %20 for spaces |
| Server won't start | Activate .venv first: `.venv\Scripts\Activate.ps1` |
| ADS1115 not found | Check I2C wiring, run I2C scanner to find addresses |
| No relay response | Ensure JSON format is correct, check relay wiring |

---

## 📊 MONITORING DATA

### Server Logs Show:
```
INFO: 192.168.10.13:60095 - "WebSocket /ws" [accepted]
[+] Device Connected! Total active connections: 1
Incoming Telemetry: {"env":{...}, "thermal":{...}, ...}
```

### Dashboard Shows:
- ✅ Green: System Healthy
- 🟡 Yellow: Warning (check logs)
- 🔴 Red: Critical Alert

### Serial Monitor Shows:
```
[BOOT] ... Starting
[WIFI] Connecting...
✅ [WIFI] Connected!
✅ [SYS] All 3 ADS1115 Modules Online
✅ [WS] Link established with Python Server!
📡 [TX] Live Telemetry Streamed...
```

---

## 📁 KEY FILES REFERENCE

| File | Location | Purpose |
|------|----------|---------|
| Main Firmware | `test/src/main.cpp` | ESP32 code |
| Server | `d:\...\server.py` | Backend |
| Dashboard | `d:\...\flowchart.html` | WebUI |
| Config | `test/platformio.ini` | Build settings |
| Scanner | `test/onewire_scanner.cpp.bak` | Find sensor addresses |

---

## ⏱️ TYPICAL STARTUP SEQUENCE

1. **Terminal 1:** Start Python server (2 seconds)
2. **Terminal 2:** Open Serial Monitor (3 seconds)
3. **Browser:** Open dashboard (1 second)
4. **ESP32 boots** → Connects WiFi → Connects Server (5-10 seconds)
5. **Dashboard** shows live data (starts receiving packets)

**Total Startup Time:** ~30 seconds

---

## 🔐 DEFAULT CREDENTIALS

| Item | Value |
|------|-------|
| WiFi SSID | BUSY |
| WiFi Password | 4d65c2ff |
| Server IP | 192.168.10.19 |
| Server Port | 8000 |
| Dashboard | file:///d:/final%20code%20every%20thing/flowcharts/flowchart.html |
| Admin Access | Full (no authentication) |

---

## 📞 EMERGENCY ACTIONS

### Stop Everything
```bash
Ctrl+C  in Python terminal (stop server)
Unplug ESP32 or toggle relay MC0 to OFF
```

### Emergency Stop (Hardware)
- **Relay MC0:** Master Emergency Contactor (cuts all power)
- **Relay MC1:** Phase A Branch
- **Relay MC2:** Phase B Branch  
- **Relay MC3:** Phase C Branch

### Clear Fault Logs
```bash
# Delete database
rm d:\final code every thing\database.db

# Restart server
python server.py
```

---

**Last Updated:** 2026-06-22  
**Version:** 1.0  
**Status:** ✅ READY TO USE
