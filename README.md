# 2582426---Christ-University-Smart-Door-Controller

Closes entrance doors at the start of class and reopens automatically after the 10-minute attendance window — removing manual security effort at every block

# Christ University - AI Smart Door Controller

An intelligent access control system designed for Christ University campus infrastructure. This application automates door access management based on scheduled lecture hours, real-time campus events, and automated policy enforcement.

---

## Demo Preview

![AI Smart Door Controller Demo](demo/demo.gif)

> Note: A full-resolution video recording is also available under the [`demo/`](demo/demo.mp4) directory.

---

## Problem Statement

In academic environments like Christ University, managing physical gate and classroom access manually leads to several operational challenges:
* **Manual Bottlenecks**: Security personnel must manually lock and unlock doors during lecture transitions.
* **Unauthorized Entry**: Unrestricted open access during active lecture hours causes class disruptions.
* **Lack of Timed Automation**: Standard digital lock systems lack integration with institutional schedules and class timetables.

The AI Smart Door Controller solves this by integrating a Streamlit-based control panel with automated policy engines to restrict or grant access seamlessly based on daily schedules.

---

## Features

* **Automated Access Control**: Automatically locks door gates during the first 10 minutes of each lecture period before returning to scheduled access policies.
* **Live Gate Status Panel**: Real-time monitoring of all campus gates (Block 1, Block 2, Block 3, Block 4).
* **Schedule Integration**: Dynamic timetable synchronization supporting classes, morning breaks, lunch breaks, and evening periods.
* **AI Engine Support**: Backend modules (`llm_engine.py` and `image_engine.py`) for smart query handling and visual verification.
* **Interactive Streamlit UI**: User-friendly control dashboard for campus security administrators.

---

## Architecture Diagram



## Screenshots

<img width="1897" height="737" alt="image" src="https://github.com/user-attachments/assets/5912cda5-1c2e-4629-abed-8a51f86c8911" />


---

## Installation & Usage

### Prerequisites
* Python 3.10 or higher
* Git installed on your system

### 1. Clone the Repository
```bash
git clone [https://github.com/CHRIST-SDS/2582426---Christ-University-Smart-Door-Controller.git](https://github.com/CHRIST-SDS/2582426---Christ-University-Smart-Door-Controller.git)
cd 2582426---Christ-University-Smart-Door-Controller
![AI Smart Door Controller Demo](demo/demo.gif)
