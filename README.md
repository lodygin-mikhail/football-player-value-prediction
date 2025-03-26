# 🎯 Football Transfer Value Prediction Model

## 🔎 Project Overview
This project develops a **machine learning model** to predict football players' transfer market values based on their performance statistics and other relevant factors. The model achieves the following metrics:

- **RMSE:** €9.98 million

- **MAE:** €6.07 million

- **R²:** 0.624

While these results show promise, the model should be considered a foundational tool that can be enhanced with additional data sources.

## Data Sources

📊 **FBref.com Parser (Player Statistics):**

Functionality:

- Automatically scrapes complete player data from Top 5 European leagues (Premier League, La Liga, Bundesliga, Serie A, Ligue 1)

- Collects 150+ statistical features per player including:

    - Basic metrics (goals, assists, minutes played)
    
    - Advanced analytics (xG, xA, progressive passes, defensive actions)
    
    - Position-specific data (clean sheets for GKs, dribbles for forwards)

💰 **Transfermarkt Parser (Market Values):**

Functionality:

Scrapes only the most recent market valuation for each player in Top 5 leagues from Transfermarkt.com

⚙️ **Technical Implementation:**

- In order to update the data, you can run the ***parse_value_data('file name')*** function to get up-to-date data on the transfer price of players and the ***parse_stats_data('file name')*** function to get up-to-date statistical data on players. 

## 🆕 Data Freshness

**stats_data.csv:** Updated through March 2025

**values_data.csv:** Winter 2025 window valuations

## 🛠️ Key Features
The model considers:

- Performance metrics (goals, assists, xG, etc.)

- Player age and position

- League quality ("EPL tax" premium)

- Team performance factors

## ⚠️ Limitations
Current model limitations include:

- Focus on statistical factors only

- Potential bias toward top leagues

- No commercial value considerations

- No contract status information

## ⏳ Future Improvements

Planned enhancements:

- Add social media/commercial metrics

- Incorporate contract information

- Include injury history

- Develop interactive visualization tool

## 🧩 Project Structure

```bash
/football-player-value-prediction
│── /data
│   ├── stats_data.csv       # Player performance data
│   └── values_data.csv     # Market valuation data
│── /notebooks
│   └── football_player_value_prediction.ipynb  # Analysis notebook
│── /src
│   └── /parsers
│       ├── football_stat_parsing_script.csv       # Player performance data
│       └── value_parsing_script.py                # Data collection script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Dependencies
Python 3.11+ with packages listed in requirements.txt
