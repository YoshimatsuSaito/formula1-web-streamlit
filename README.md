# Formula1-Web-Streamlit
- This app allows you to visualize basic Formula 1 data and calculate an optimal race strategy based on simple assumptions.
- You can check the app [here](https://formula1-web-app.streamlit.app/).

## Project Structure

```
.
├── app.py
├── data
├── modules
│   ├── __init__.py
│   └── strategy_maker.py
├── README.md
├── requirements.txt
└── views
    ├── __init__.py
    ├── qualify_result.py
    ├── race_lap_result.py
    ├── season_result.py
    └── strategy.py
```

## Data Preparation Steps
1. Create a Kaggle account and [download the `kaggle.json` file](https://github.com/Kaggle/kaggle-api#api-credentials). Place this file in the `./scripts/` directory.
2. Create a virtual environment as needed.
3. Install the required packages using `pip install -r requirements.txt`.
4. Activate your virtual environment, navigate to the `./scripts` directory and execute `sh download_data.sh`. This will download the necessary CSV files into the `./data/` directory.
- Data source: https://www.kaggle.com/rohanrao/formula-1-world-championship-1950-2020

## Running the App
- Activate your virtual environment and execute `streamlit run app.py` from the root directory of the project.