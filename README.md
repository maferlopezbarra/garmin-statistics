# Garmin Statistics

A end-to-end data engineering and analytics project built with Python and SQLite.

The project processes Garmin JSON exports, stores the data in a SQLite database, and analyzes running performance and recovery metrics using Jupyter Notebook.

## Tech Stack

- Python
- SQLite
- SQL
- pandas
- matplotlib
- JupyterLab

## Data Pipeline

Garmin JSON exports  
↓  
Python ETL  
↓  
SQLite database  
↓  
SQL views  
↓  
Jupyter Notebook  
↓  
Analysis & visualization

## Project Structure

```text
garmin-statistics/
├── data/
├── notebooks/
│   └── garmin_analysis.ipynb
├── src/
│   ├── activities.py
│   ├── hrv.py
│   ├── sleep.py
│   └── main.py
├── .gitignore
├── requirements.txt
└── README.md
```
## What the Project Does

### Data ingestion

Python scripts process Garmin JSON exports and load into SQLite tables:

* Running activities
* HRV data
* Sleep data

The ingestion process can be re-run without creating duplicate records.

### Data transformation

SQL views transform the activity data into analysis-ready metrics such as:

* Distance
* Pace
* VO₂ Max
* Average and maximum heart rate
* Cadence
* Stride length

### Analysis

The Jupyter Notebook performs exploratory data analysis and visualizes relationships between running performance and recovery metrics.

Some of the main correlations found in the dataset are:

| Relationship | Correlation |
| :---: | :---: |
| Pace ↔ Average heart rate | -0.902 |
| Pace ↔ Stride length | -0.867 |
| Pace ↔ Cadence | -0.825 |
| Stress ↔ HRV | -0.812 |


These correlations show strong associations within this dataset; they do not imply causation.

## How to Run

- Clone the repository and install the dependencies:

```Bash
git clone https://github.com/maferlopezbarra/garmin-statistics

cd garmin-statistics

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt
```

- Add your Garmin data exports to the appropriate data/ directory.

- Run the ETL pipeline:

```Bash
python -m src.main
```

- Start JupyterLab:

```Bash
jupyter lab
```

- Open the notebook in:

```Plain Text
notebooks/
```

## Data Privacy

The repository does not include personal Garmin data.

To reproduce the project, use your own Garmin data exports.

## Limitations

This analysis is based on data from a single athlete. Correlations describe relationships within this dataset and should not be interpreted as causal relationships or general conclusions about running performance.

## Author

Maria Fernanda López Barra