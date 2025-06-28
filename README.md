# Honeypot
# Simple Python TCP Honeypot

## ⚠️ Important Security Warning
This is an educational tool designed to attract and log network traffic for research purposes. **DO NOT** run this on a production server or any machine connected directly to the internet without proper isolation (e.g., a sandboxed Virtual Machine). Running a honeypot can attract malicious actors and poses a real security risk to the host system and network if not handled correctly.

## Overview
This project is a simple, low-interaction TCP honeypot written in Python. It listens on a specific TCP port and logs all incoming connections and data. The primary goal is to create a lightweight "trap" for automated scanners and curious attackers, allowing for the observation of their initial tactics, techniques, and procedures (TTPs) in a controlled environment.

This project demonstrates knowledge of socket programming, multithreading, and fundamental network security concepts.

---

## Features
- **Listens on any TCP Port:** Easily configurable to listen on common targets like Telnet (23), FTP (21), or HTTP (80).
- **Connection Logging:** Logs the IP address and port of every incoming connection.
- **Data Capture:** Captures and logs all raw data sent by the connected client.
- **Timestamping:** Every logged event is timestamped for chronological analysis.
- **Multithreading:** Handles multiple concurrent connections simultaneously without blocking.
- **Fake Banner:** Sends a customizable fake welcome message to make the service appear legitimate.

---

## Technologies Used
- **Language:** Python 3
- **Core Libraries:**
    - `socket` (for low-level network communication)
    - `threading` (to handle concurrent clients)
    - `datetime` (for event timestamping)

---

## Setup and Usage

### 1. Configuration
You can change the listening host and port by modifying the `HOST` and `PORT` variables at the top of the `honeypot.py` script.
```python
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 23         # Listen on port 23 (Telnet)
```

### 2. Running the Honeypot
Run the script from your terminal. You may need `sudo` privileges to bind to ports below 1024.
```bash
sudo python3 honeypot.py
```
The honeypot is now running and will log all activity to `honeypot.log` and the console.

### 3. Testing the Honeypot
From a different terminal (or machine), you can connect to the honeypot using a tool like `netcat` or `telnet`.
```bash
telnet 127.0.0.1 23
```
Anything you type in the `telnet` session will be captured and logged by the honeypot.
