# Astronomical Observation Log

A Python project for logging, managing, and analyzing astronomical observations. Developed as the final capstone project for the Python programming course.

---

## Overview

In observational astronomy, keeping an accurate log of telescope sessions (target objects, observer names, optical filters, and exposure durations) is essential. This project organizes observation data using Object-Oriented Programming (OOP), stores records in an SQLite database, analyzes data with Pandas, and visualizes statistics with Matplotlib.

---

## Project Structure

As planned on the whiteboard:

```
ObservationLog/
├── main.py           # Main CLI program and interactive menu
├── Observation.py    # Observation class and subclasses (OOP)
├── database.py       # SQLite database manager (SQL queries)
├── visual.py         # Data visualizations (Matplotlib & Pandas)
├── gui.py            # Desktop user interface (Tkinter)
├── observations.db   # SQLite database file
├── requirements.txt  # Project dependencies
└── README.md         # Project documentation
```

---

## File Descriptions

### 1. `Observation.py`
Contains the core data classes:
- **`Observation`**: Base class holding `target`, `observer`, `filter_name`, `exposure`, `date`, and `notes`. Methods: `exposure_min()`, `summary_info()`, `to_dict()`.
- **`Photometric_observation`**: Inherits from `Observation`, adds central `wavelength` (nm).
- **`spectroscopic_observation`**: Inherits from `Observation`, adds spectral `resolution`.

### 2. `database.py`
Handles all SQLite operations using standard SQL queries:
- Table creation (`CREATE TABLE IF NOT EXISTS Observation ...`)
- CRUD operations: `add_observation`, `get_all`, `search`, `update`, `delete`
- Statistics calculation using SQL aggregate functions (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`)
- Export to Pandas DataFrame via `pd.read_sql_query`

### 3. `visual.py`
Generates scientific charts using Matplotlib:
- Exposure time by target (Bar chart)
- Filter usage breakdown (Pie chart)
- Observer exposure contribution (Horizontal bar chart)
- 4-Panel combined dashboard

### 4. `gui.py`
A simple desktop interface built with Tkinter (`tk`):
- Form to add new observations
- Table view to display and delete records
- Button to trigger Matplotlib plots

### 5. `main.py`
The entry point of the application with an interactive console menu:
1. Add Observation
2. Show Observations
3. Search Observation
4. Update Observation
5. Delete Observation
6. Statistics (SQL & Pandas GroupBy)
7. Visualizations
8. Export to CSV
9. Launch GUI (Tkinter)
0. Exit

---

## Requirements & Installation

The core program runs using standard Python libraries (`sqlite3`, `csv`, `time`). For visualizations and advanced analytics, install:

```bash
pip install -r requirements.txt
```

*(Includes `matplotlib` and `pandas`)*

---

## How to Run

### Console (CLI)
```bash
python main.py
```

### Desktop GUI
```bash
python gui.py
```

---

## Sample Data

On the first run, the database is pre-seeded with sample observations from the class sessions (targets like M31, M45, M33, Moon, Vega and observers from class).
