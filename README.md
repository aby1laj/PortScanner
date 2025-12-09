# 🔍 Multi-Threaded Python Port Scanner

A fast, lightweight, and banner-grabbing port scanner written in Python.
This tool uses multi-threading to efficiently scan thousands of ports and identify running services based on common ports and banner detection.

---

## 📑 Table of Contents

* [About](#about)
* [Features](#features)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
* [Configuration](#configuration)
* [Example Output](#example-output)
* [Troubleshooting](#troubleshooting)
* [License](#license)

---

## 📘 About

This script scans a specified target (IP or hostname) for open TCP ports within a given range.
When an open port is detected, the scanner attempts to identify:

* The common service (FTP, SSH, HTTP, etc.)
* Banner information
* HTTP/HTTPS server headers
* Web page titles (when available)

---

## ✨ Features

* 🚀 **Multi-threaded scanning** (default: 200 threads)
* 🧪 **Banner grabbing** for deeper fingerprinting
* 🌐 **HTTP/HTTPS title & server extraction**
* 🗂️ Built-in database of common ports
* ⚡ Fast, lightweight, and dependency-free (only built-in Python modules)

---

## 📦 Requirements

This script uses only Python's standard library, but it’s recommended to install requirements if bundled in a separate requirements.txt:

```bash
pip install -r requirements.txt
```

If you don't already have the file, you can create one containing:

```
# requirements.txt (optional)
```

> **Note:** The scanner itself requires no external packages unless modified.

---

## 🔧 Installation

Clone or download the repository, then make the script executable:

```bash
git clone <your-repo-url>
cd <your-project-folder>

chmod +x port_scanner.py
```

---

## ▶️ Usage

Run the scanner using Python 3:

```bash
python3 port_scanner.py
```

You will be prompted to enter the target:

```
Enter target IP or hostname (e.g. scanme.nmap.org):
```

---

## ⚙️ Configuration

Inside the script, you can manually adjust:

| Variable       | Description                               | Default     |
| -------------- | ----------------------------------------- | ----------- |
| `threads`      | Number of worker threads                  | `200`       |
| `timeout`      | Socket timeout per port                   | `1.0`       |
| `start_port`   | First port to scan                        | `1`         |
| `end_port`     | Last port to scan                         | `5000`      |
| `common_ports` | Dictionary of known ports → service names | Pre-defined |

You can customize the port range or thread count to improve accuracy or speed.

---

## 📤 Example Output

```
Scanning scanme.nmap.org | ports 1–5000 | threads: 200
Started: 14:22:11
--------------------------------------------------------------------------------
[+] 22     OPEN → SSH
[+] 80     OPEN → HTTP | HTTP/1.1 200 OK | Server: Apache | Title: Welcome
--------------------------------------------------------------------------------
Open ports on scanme.nmap.org: [22, 80]
Total open ports found: 2
Scan finished: 14:22:19
```

---

## 🛠️ Troubleshooting

### 🔸 "No open ports found"

* Try expanding the port range
* Ensure the target is reachable
* The host may have firewalls blocking scans

### 🔸 Scanning is slow

* Increase the `threads` value
* Reduce timeout (e.g., `timeout = 0.5`)

### 🔸 Missing banners

Some services don’t provide banners unless interacted with in a specific way — this is normal.

---

## 📄 License

This project is released under the **MIT License**.
You are free to modify and distribute it as needed.
