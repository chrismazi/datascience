# Vehicle Theft Analysis Dashboard

This project is a Streamlit dashboard designed for analyzing vehicle theft incidents. It provides various visualizations to help users understand the patterns and characteristics of stolen vehicles.

## Project Structure

```
vehicle-theft-analysis
├── src
│   ├── app.py
│   ├── utils
│   │   └── data_processing.py
│   └── visualizations
│       ├── color_analysis.py
│       ├── temporal_analysis.py
│       └── vehicle_analysis.py
├── data
│   └── stolen_vehicles_enhanced.csv
├── requirements.txt
└── README.md
```

## Overview

The dashboard allows users to explore the following aspects of vehicle theft:

- Total count of stolen vehicles by color
- Temporal patterns of vehicle thefts
- Distribution of stolen vehicle types

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd vehicle-theft-analysis
   ```

2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit application:**
   ```bash
   streamlit run src/app.py
   ```

## Usage Guidelines

- Upon running the application, users will be presented with various filters and visualizations.
- Users can interact with the dashboard to analyze vehicle theft data based on different criteria.

## Dataset

The dataset used for this analysis is located in the `data` directory and is named `stolen_vehicles_enhanced.csv`. It contains detailed information about stolen vehicles, including attributes such as color, vehicle type, and model year.

## Acknowledgments

This project utilizes the following libraries:
- Streamlit
- Pandas
- Matplotlib
- Seaborn

For any questions or contributions, please feel free to reach out!