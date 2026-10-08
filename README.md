# Cloud-Based Water Quality Monitoring System

A college-friendly mini project for monitoring water-quality parameters through a web dashboard.

## Features

- Dashboard for latest water-quality readings
- pH monitoring
- Turbidity monitoring
- Temperature monitoring
- TDS monitoring
- Dissolved oxygen monitoring
- Automatic demo status calculation
- Good / Needs Attention alert
- Add new sensor readings
- Reading history
- Delete readings
- JSON REST-style API
- SQLite database
- Responsive frontend

## Important Note

The threshold values in this educational project are simplified demo values. They should not be used to certify whether real drinking water is safe.

## Project Structure

```text
Cloud-Based-Water-Quality-Monitoring/
│
├── app.py
├── requirements.txt
├── README.md
├── water_quality.db       # created automatically
│
├── templates/
│   ├── index.html
│   ├── add_reading.html
│   └── history.html
│
└── static/
    ├── style.css
    └── script.js
```

## Run in VS Code

### 1. Open the project

Extract the ZIP and open the folder in VS Code.

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate it on Windows

```bash
venv\Scripts\activate
```

### 4. Install Flask

```bash
pip install -r requirements.txt
```

### 5. Start the application

```bash
python app.py
```

### 6. Open the website

```text
http://127.0.0.1:5000
```

## Add Sensor Data

Open:

```text
http://127.0.0.1:5000/add
```

Enter:

- Location
- pH
- Turbidity
- Temperature
- TDS
- Dissolved Oxygen

The application automatically classifies the reading as `Good` or `Needs Attention`.

## API Endpoints

All readings:

```text
http://127.0.0.1:5000/api/readings
```

Latest reading:

```text
http://127.0.0.1:5000/api/latest
```

## Cloud Computing Concept

For a real cloud implementation:

```text
Water Sensors
      ↓
IoT Gateway
      ↓
Cloud API
      ↓
Cloud Database
      ↓
Web Dashboard
      ↓
Alerts / Reports
```

The Flask API can be deployed to AWS, Azure, Google Cloud, Render or another cloud platform. SQLite can be replaced by a managed cloud database such as PostgreSQL, MySQL or a cloud NoSQL database.

## Technologies

Frontend:
- HTML5
- CSS3
- JavaScript

Backend:
- Python
- Flask

Database:
- SQLite

API:
- REST-style JSON API
