# formula1-web
- Streamlit web app visualizing data of Formula 1 (https://en.wikipedia.org/wiki/Formula_One) and calculate an optimal race strategy based on simple assumption.
- Something like demo

# Structure

```
.
├── app.py
├── data
│   ├── circuits.csv
│   ├── constructor_results.csv
│   ├── constructors.csv
│   ├── constructor_standings.csv
│   ├── drivers.csv
│   ├── driver_standings.csv
│   ├── lap_times.csv
│   ├── pit_stops.csv
│   ├── qualifying.csv
│   ├── races.csv
│   ├── results.csv
│   ├── seasons.csv
│   └── status.csv
├── modules
│   ├── __init__.py
│   └── strategy_maker.py
├── Pipfile
├── Pipfile.lock
├── README.md
├── requirements.txt
└── views
    ├── __init__.py
    ├── qualify_result.py
    ├── race_lap_result.py
    ├── season_result.py
    └── strategy.py
```

# Data source
- https://www.kaggle.com/rohanrao/formula-1-world-championship-1950-2020

# How to deploy
- `streamlit run app.py`