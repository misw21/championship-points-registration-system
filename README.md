<div align="center">

# 🏆 Championship Points Registration System (CPRS)

**A Modular, Accessible Desktop Tournament Management & Automated Scoring System**

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.14-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![GUI Framework](https://img.shields.io/badge/GUI-Tkinter%20%2F%20ttk-2B5B84?style=for-the-badge)](https://docs.python.org/3/library/tkinter.html)
[![Architecture](https://img.shields.io/badge/Architecture-3--Tier%20Layered-0EA5E9?style=for-the-badge)]()
[![Accessibility](https://img.shields.io/badge/Accessibility-WCAG%20Themes%20Supported-10B981?style=for-the-badge)]()
[![Data Storage](https://img.shields.io/badge/Storage-JSON%20%26%20CSV%20Export-F59E0B?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

</div>

---

## 📌 Overview

**Championship Points Registration System (CPRS)** is a desktop management suite engineered in Python to streamline competition administration for sports tournaments and academic events. Built with a decoupled **3-tier layered architecture**, CPRS automates the entire competition lifecycle—from participant/team registration with constraint validation, to dynamic score computation, real-time leaderboard generation, and multi-format data persistence (JSON & CSV).

This project showcases a complete **Software Development Life Cycle (SDLC)**, evolving from an initial baseline prototype (**Version 1.0**) to an enterprise-grade accessible application (**Version 2.0**) equipped with accessibility palettes (color-blindness support), auditory feedback, internationalization (Arabic & English), and comprehensive unit testing.

---

## 🔄 Version Evolution (v1.0 ➔ v2.0)

This repository preserves both development milestones to demonstrate iterative design and refactoring:

| Capability / Feature | Version 1.0 (Baseline) | Version 2.0 (Current Release) |
| :--- | :--- | :--- |
| **User Interface** | Basic Tkinter layout | Modernized 4-column responsive grid & card styling |
| **Accessibility** | Single default theme | 5 WCAG-inspired palettes (Protanopia, Deuteranopia, Tritanopia, High Contrast) |
| **Localization (i18n)** | English only | Full bilingual support (English & Arabic) |
| **Audio Feedback** | None | Integrated sound cues with in-app volume slider & mute control |
| **Custom Branding** | Static headers | Dynamic custom logo loading & customizable window titles |
| **Record Editing** | Basic delete/re-entry | In-place name updates for teams, events, and participants |
| **Documentation** | Functional comments | Full docstrings, type annotations, and design flowcharts |

> **Note:** The legacy v1.0 codebase is archived under [legacy/v1.0/](legacy/v1.0/) for historical reference.

---

## ✨ Key Features

### 👤 1. Participant & Team Administration
- **Individual Competitors:** Track participant records with auto-generated unique IDs (\IND0001\), skill levels, age groups, and accumulated scores.
- **Team Roster Enforcement:** Enforce strict team composition rules (5 to 10 members per team), with member role assignments and roster updates.
- **Search & Filter:** Instant querying across participants and teams by name or ID.

### 🎯 2. Event & Competition Configuration
- **Multi-Category Events:** Support for both **Sports** and **Academic** categories.
- **Capacity & Registration Rules:** Configurable maximum participant thresholds, individual vs. group event isolation, and single-event exclusivity locks.
- **Event Lifecycle Tracking:** Dynamic state transitions (\Open\ ➔ \Completed\).

### ⚡ 3. Automated Scoring & Leaderboards
- **Rule-Based Points Engine:** Configurable position-to-points mapping (Default: 1st: 10pts, 2nd: 8pts, 3rd: 6pts, 4th: 4pts, 5th: 2pts).
- **Real-Time Standings:** Real-time recalculation of individual and team rankings with tie-breaking and championship winner identification.
- **Audit Validation:** Strict input validation to prevent duplicate rank entries within the same event.

### ♿ 4. Accessibility & Inclusive UI
- **Color-Blindness Themes:** Dedicated themes optimized for visual impairments:
  - \Default Blue\ (Standard High-Clarity)
  - \High Contrast\ (Maximum Luminescence Difference)
  - \Protanopia\ (Red-Blind Safe)
  - \Deuteranopia\ (Green-Blind Safe)
  - \Tritanopia\ (Blue-Blind Safe)
- **Bilingual Interface:** Instant switching between **English** and **Arabic**.
- **Auditory Feedback:** Integrated Windows audio cues with in-app volume slider and mute controls.

### 💾 5. Data Persistence & Reporting
- **Atomic JSON Storage:** Complete session state persistence, counter management, and automatic backups.
- **CSV Data Export:** Export structured datasets (\individuals.csv\, \	eams.csv\, \events.csv\, \
esults.csv\) with \utf-8-sig\ encoding for Excel compatibility.
- **Tournament Analytics:** Comprehensive summary dashboard reporting total participation, completed events, and unassigned competitors.

---

## 📸 Screenshots & Interface Walkthrough

<div align="center">

### Main Dashboard & Navigation
![Main Dashboard](assets/screenshots/dashboard.png)
*Central control center with quick-action navigation and branding header.*

</div>

| Participant Management | Team Roster Configuration |
| :---: | :---: |
| ![Individual Management](assets/screenshots/individuals.png) | ![Team Management](assets/screenshots/teams.png) |
| *Individual competitor registration & record auditing* | *Team formation with strict 5-10 member enforcement* |

| Event Management & Setup | Smart Registration System |
| :---: | :---: |
| ![Event Management](assets/screenshots/events.png) | ![Registration](assets/screenshots/registration.png) |
| *Category classification and participant limit controls* | *Constraint validation matching participant type to event* |

| Results Entry & Automated Scoring | Real-Time Rankings & Leaderboard |
| :---: | :---: |
| ![Results Entry](assets/screenshots/results.png) | ![Rankings Leaderboard](assets/screenshots/rankings.png) |
| *Rank entry with instant point allocation* | *Global individual and team championship standings* |

---

## 🏛️ System Architecture

The application adopts a clean, decoupled **Layered Architecture** adhering to OOP principles:

`mermaid
graph TD
    A[Tkinter GUI Layer - gui.py] -->|Invokes Commands| B[Business Service Layer - services.py]
    B -->|Enforces Business Logic| C[Data Models Layer - models.py]
    B -->|Requests Persistence| D[Data Access Layer - storage.py]
    D -->|Reads / Writes| E[(JSON Storage - tournament_data_v2/)]
    D -->|Generates| F[CSV Export Engine - exports/]
`

---

## 📂 Project Structure

`	ext
championship-points-registration-system/
├── assets/
│   ├── diagrams/                   # System architectural & flow diagrams
│   └── screenshots/                # Application UI walkthrough screenshots
│       ├── dashboard.png
│       ├── individuals.png
│       ├── teams.png
│       ├── events.png
│       ├── registration.png
│       ├── results.png
│       ├── rankings.png
│       └── settings.png
├── docs/                           # Project requirements, briefs, and reports
│   ├── BTEC_Unit04_Learning_Aim_A_Brief.pdf
│   └── BTEC_Unit04_Learning_Aim_BC_Brief.pdf
├── legacy/                         # Historical baseline prototypes
│   └── v1.0/                       # Initial Version 1.0 implementation
├── src/                            # Version 2.0 Production Source Code
│   ├── __init__.py
│   ├── main.py                     # Application entry point
│   ├── models.py                   # Dataclasses, Enums, and validation logic
│   ├── services.py                 # Core business services & scoring logic
│   ├── storage.py                  # JSON persistence & CSV export layer
│   └── gui.py                      # Tkinter graphical user interface
├── tests/
│   ├── __init__.py
│   └── test_tournament.py          # Comprehensive unittest suite
├── .gitignore                      # Python & IDE exclusion rules
├── LICENSE                         # MIT License
├── README.md                       # Project documentation
└── requirements.txt                # Project dependencies (Pillow)


---

## ⚙️ Requirements & Prerequisites

- **Operating System:** Windows 10/11, macOS, or Linux.
- **Python Version:** Python 3.10 or higher.
- **Dependencies:**
  - \	kinter\ (Standard Python library)
  - \Pillow >= 10.0.0\ (Optional, for custom image logo rendering)

---

## 🚀 Installation & Setup

### 1. Clone or Download the Project
`ash
git clone https://github.com/your-username/championship-points-registration-system.git
cd championship-points-registration-system
`

### 2. Install Dependencies (Optional for PIL)
`ash
pip install -r requirements.txt
`

### 3. Run the Application
`ash
python src/main.py
`

---

## 🧪 Running Automated Tests

`ash
python -m unittest discover -s tests -p "test_*.py" -v
`

---

## 📄 License

This project is open-source and licensed under the [MIT License](LICENSE).

---

## 👨‍💻 Author

Developed by **Mamoun Sraiheen**  
*Passionate Software Developer & Computer Science Student*
