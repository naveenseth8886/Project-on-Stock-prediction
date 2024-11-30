
# Stock Price Analysis and Forecasting Dashboard

This is an interactive **Streamlit** application that provides historical stock price visualization, seasonal decomposition analysis, and future price forecasting using ARIMA models. Users can select multiple stocks, view their past performance, analyze trends, and get future price predictions for selected periods.

---

## Features

- **Historical Data Visualization**: Displays the closing prices of selected stocks for the last two months.
- **Seasonal Decomposition**: Breaks down stock prices into trend, seasonality, and residuals.
- **ARIMA-Based Forecasting**: Predicts future stock prices using the optimal ARIMA model based on AIC/BIC scores.
- **Interactive Dashboard**: Allows users to select stocks, adjust forecast periods, and view results dynamically.

---

## Tech Stack

- **Python**: Core language for computation and modeling.
- **Streamlit**: Framework for creating the interactive dashboard.
- **YFinance**: Library for fetching stock data.
- **Matplotlib**: Visualization of historical and forecasted data.
- **Statsmodels**: ARIMA model building and seasonal decomposition.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/stock-forecasting-dashboard.git
   cd stock-forecasting-dashboard
   ```

2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` should include:
   ```
   pandas
   yfinance
   statsmodels
   streamlit
   matplotlib
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

---

## Usage

1. Select one or more stock tickers from the sidebar (e.g., **AAPL**, **MSFT**, **TSLA**, etc.).
2. Adjust the forecast period using the slider (5–90 days).
3. View:
   - Historical data visualization.
   - Seasonal decomposition (trend, seasonality, residuals).
   - ARIMA-based stock price forecasting.
4. Scroll through the results for each selected ticker.

---

## Screenshots

### 1. Dashboard Overview
*(Add a screenshot showing the main dashboard interface)*

### 2. Historical Data Visualization
*(Add a screenshot showing a plot of historical stock prices)*

### 3. Seasonal Decomposition Analysis
*(Add a screenshot showing observed, trend, seasonality, and residual plots)*

### 4. Forecasted Stock Prices
*(Add a screenshot showing forecasted stock prices plotted alongside historical data)*

---

## Example Workflow

1. **Step 1**: Select multiple tickers (e.g., AAPL, MSFT).
   - *(Screenshot of selecting tickers in the sidebar)*

2. **Step 2**: View the historical trends for each stock.
   - *(Screenshot of historical data visualization for a stock)*

3. **Step 3**: Analyze seasonality.
   - *(Screenshot of seasonal decomposition plots for a stock)*

4. **Step 4**: Check the forecasted stock prices.
   - *(Screenshot of forecasted prices with a plot)*

---

## Customization

### Modify Ticker List
You can extend the list of available stock tickers in the following line:
```python
tickers = ["AAPL", "MSFT", "TSLA", "TATAMOTORS.NS", "RELIANCE.NS", "NVDA", "SUZLON.NS"]
```

### Forecast Model
Adjust ARIMA parameters (`p`, `d`, `q`) for fine-tuning:
```python
for p in range(1, 3):
    for d in range(0, 2):
        for q in range(1, 3):
```

---

## Future Improvements

- Include additional forecasting models like SARIMA, Prophet, etc.
- Add functionality to export results as CSV files.
- Enable comparison of multiple stocks on a single plot.

---

## License

This project is licensed under the MIT License.
