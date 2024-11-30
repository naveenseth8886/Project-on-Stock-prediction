import pandas as pd
import yfinance as yf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import datetime, timedelta
import streamlit as st
import matplotlib.pyplot as plt

# Streamlit setup
st.title("Stock Price Forecasting Dashboard")
st.sidebar.header("Select Stocks")

# Stock tickers available
tickers = ["AAPL", "MSFT", "TSLA", "TATAMOTORS.NS", "RELIANCE.NS", "NVDA", "SUZLON.NS"]
selected_tickers = st.sidebar.multiselect("Select Stock Ticker(s)", tickers, default=["AAPL", "MSFT"])

forecast_days = st.sidebar.slider("Select the number of forecast days", min_value=5, max_value=90, value=30)

# Fetch stock data for the past two months
def fetch_stock_data(ticker):
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=60)  # Past 2 months
    data = yf.download(ticker, start=start_date, end=end_date, interval="1d")
    
    if data.empty:
        raise ValueError(f"No data found for ticker {ticker} in the last 2 months.")
    
    return data.dropna()

# Visualize historical data
def visualize_historical_data(data, ticker):
    st.subheader(f"Historical Stock Prices for {ticker}")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data.index, data['Close'], label="Closing Price", color="blue")
    ax.set_title(f"Historical Closing Prices for {ticker}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    plt.grid()
    st.pyplot(fig)

# Visualize seasonal decomposition
def visualize_seasonality(data, ticker):
    result = seasonal_decompose(data['Close'], model='additive', period=7)  # Weekly seasonality
    
    st.subheader(f"Seasonal Decomposition for {ticker}")
    fig, axs = plt.subplots(4, 1, figsize=(12, 10))
    axs[0].plot(result.observed, label='Observed', color='blue')
    axs[0].set_title("Observed")
    axs[1].plot(result.trend, label='Trend', color='orange')
    axs[1].set_title("Trend")
    axs[2].plot(result.seasonal, label='Seasonal', color='green')
    axs[2].set_title("Seasonal")
    axs[3].plot(result.resid, label='Residual', color='red')
    axs[3].set_title("Residual")
    plt.tight_layout()
    st.pyplot(fig)

# Select and forecast using ARIMA and SARIMA
def select_and_forecast(data, forecast_days):
    best_model = None
    best_aic = float("inf")
    best_forecast = None
    best_model_type = None
    
    # Test ARIMA models
    for p in range(1, 3):  # Adjust range as needed
        for d in range(0, 2):
            for q in range(1, 3):
                try:
                    model = ARIMA(data['Close'], order=(p, d, q))
                    fitted_model = model.fit()
                    aic = fitted_model.aic
                    if aic < best_aic:
                        best_aic = aic
                        best_model = fitted_model
                        best_forecast = fitted_model.forecast(steps=forecast_days)
                        best_model_type = "ARIMA"
                except:
                    continue
    
    # Test SARIMA models
    for p in range(1, 3):
        for d in range(0, 2):
            for q in range(1, 3):
                for P in range(0, 2):
                    for D in range(0, 2):
                        for Q in range(0, 2):
                            try:
                                model = SARIMAX(data['Close'], order=(p, d, q), seasonal_order=(P, D, Q, 7))
                                fitted_model = model.fit(disp=False)
                                aic = fitted_model.aic
                                if aic < best_aic:
                                    best_aic = aic
                                    best_model = fitted_model
                                    best_forecast = fitted_model.forecast(steps=forecast_days)
                                    best_model_type = "SARIMA"
                            except:
                                continue
    
    return best_model, best_forecast, best_model_type

# Visualize forecasted results
def visualize_forecast(data, forecast, forecast_dates, ticker):
    st.subheader(f"Forecasted Prices for {ticker}")
    
    # Line plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data['Close'], label='Historical Prices', color='blue')
    ax.plot(forecast_dates, forecast, label='Forecasted Prices', color='orange')
    ax.set_title(f"Stock Price Forecast for {ticker}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    st.pyplot(fig)
    
    # Bar chart for forecasted prices
    st.subheader(f"Bar Chart of Forecasted Prices for {ticker}")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(forecast_dates, forecast, color="orange", label="Forecasted Prices")
    ax.set_title(f"Forecasted Prices for {ticker}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    st.pyplot(fig)

# Main function to process each stock
def process_ticker(ticker, forecast_days):
    try:
        # Fetch and process stock data
        data = fetch_stock_data(ticker)
        st.subheader(f"Stock Data for {ticker}")
        st.write(data.tail())
        
        # Visualize historical data
        visualize_historical_data(data, ticker)
        
        # Visualize seasonality
        visualize_seasonality(data, ticker)
        
        # Forecast
        best_model, forecast, model_type = select_and_forecast(data, forecast_days)
        if best_model:
            st.success(f"Selected Model: {model_type}")
            forecast_dates = pd.date_range(data.index[-1], periods=forecast_days + 1, freq='B')[1:]
            forecast_df = pd.DataFrame({
                'Date': forecast_dates,
                'Forecasted Price': forecast
            })
            st.write(forecast_df)
            
            # Visualize forecast
            visualize_forecast(data, forecast, forecast_dates, ticker)
        else:
            st.error(f"No suitable model found for {ticker}.")
    except ValueError as e:
        st.error(e)
    except Exception as e:
        st.error(f"An unexpected error occurred for {ticker}: {e}")

# Streamlit app
if selected_tickers:
    for ticker in selected_tickers:
        process_ticker(ticker, forecast_days)
else:
    st.info("Please select at least one stock ticker to analyze.")
