# 2582426---Christ-University-Smart-Door-Controller

Closes entrance doors at the start of class and reopens automatically after the 10-minute attendance window — removing manual security effort at every block

# Christ University - AI Smart Door Controller

An intelligent access control system designed for Christ University campus infrastructure. This application automates door access management based on scheduled lecture hours, real-time campus events, and automated policy enforcement.

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

flowchart TD
    A[User / Security Admin] -->|Interacts with Web UI| B[Streamlit Dashboard\napp.py]
    
    subgraph Core Engines
        B -->|Queries Timetable Rules| C[Schedule & Policy Module\n10-Min Gate Logic]
        B -->|Passes Prompts & Visuals| D[AI Engines\nllm_engine.py & image_engine.py]
    end

    C -->|Determines Door State| E{Access Granted?}
    D -->|Visual / Text Insights| E

    E -->|Yes: Door Unlocked| F[Update Dashboard Display]
    E -->|No: Gate Locked| F

    F -->|Log Activity & Render Assets| G[Data & Output Layer\nGate Logs, Media Assets, Demo Outputs]
    


## Installation & Usage

### Prerequisites
* Python 3.10 or higher
* Git installed on your system

1. Clone the Repository
```bash
git clone [https://github.com/CHRIST-SDS/2582426---Christ-University-Smart-Door-Controller.git](https://github.com/CHRIST-SDS/2582426---Christ-University-Smart-Door-Controller.git)
cd 2582426---Christ-University-Smart-Door-Controller

2. Set Up Virtual Environment

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

3. Install Dependencies

pip install -r requirements.txt

4. Run the Application

streamlit run app.py



## Screenshots

<img width="1897" height="737" alt="image" src="https://github.com/user-attachments/assets/5912cda5-1c2e-4629-abed-8a51f86c8911" />

<img width="1911" height="727" alt="Screenshot 2026-08-14 213446" src="https://github.com/user-attachments/assets/815788f2-956b-43bc-a0af-4c404dd29ef6" />


---

### Demo Preview 

![AI Smart Door Controller Demo](demo/demo.gif)

> Note: A full-resolution video recording is also available under the [`demo/`](demo/demo.mp4) directory.

An intelligent access control system designed for Christ University campus infrastructure. This application automates door access management based on scheduled lecture hours, real-time campus events, and automated policy enforcement.

---

## Live Application

The project is deployed and running 24/7:
* **Live Dashboard:** [https://smart-door-controller.streamlit.app/](https://smart-door-controller.streamlit.app/)

---


