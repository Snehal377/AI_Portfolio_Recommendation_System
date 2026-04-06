import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans


def load_stock_data(ticker):

    data = yf.download(ticker, period="2y")

    data["Return"] = data["Close"].pct_change()

    data["MA5"] = data["Close"].rolling(5).mean()
    data["MA20"] = data["Close"].rolling(20).mean()

    data["Volatility"] = data["Return"].rolling(5).std()

    data["Target"] = data["Return"].shift(-1)

    data = data.dropna()

    return data


def train_model(data):

    features = ["MA5", "MA20", "Volatility"]

    X = data[features]
    y = data["Target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    rf_model = RandomForestRegressor(n_estimators=100)

    rf_model.fit(X_train, y_train)

    lr_model = LinearRegression()

    lr_model.fit(X_train, y_train)

    rf_preds = rf_model.predict(X_test)
    lr_preds = lr_model.predict(X_test)

    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_preds))
    lr_rmse = np.sqrt(mean_squared_error(y_test, lr_preds))


    print(" RF Model RMSE:", rf_rmse)
    print(" LR Model RMSE:", lr_rmse)

    if rf_rmse < lr_rmse:
        print("Using Random Forest")
        return rf_model
    else:
        print("Using Linear Regression")
        return lr_model


def predict_next_return(model, data):

    latest = data.iloc[-1][["MA5", "MA20", "Volatility"]]

    prediction = model.predict([latest])[0]

    return prediction


def get_predicted_return(ticker):

    data = load_stock_data(ticker)

    model = train_model(data)

    prediction = predict_next_return(model, data)

    return prediction


def segment_investor(amount, duration):

    X = np.array([
        [5000, 1],
        [20000, 2],
        [50000, 5],
        [100000, 7],
        [200000, 10],
        [500000, 15]
    ])
    kmeans = KMeans(n_clusters=3, random_state=0)
    kmeans.fit(X)

    user = np.array([[amount, duration]])
    cluster = kmeans.predict(user)[0]

    if cluster == 0:
        return "Low"
    elif cluster == 1:
        return "Medium"
    else:
        return "High" 