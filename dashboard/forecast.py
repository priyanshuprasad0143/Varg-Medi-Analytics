import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

MONTH_MAPPING = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}


def prepare_monthly_sales(df):
    monthly_sales = (
        df.groupby("Month", as_index=False)
        ["Units_Sold"]
        .sum()
    )

    monthly_sales["Month_Number"] = (
        monthly_sales["Month"]
        .map(MONTH_MAPPING)
    )

    monthly_sales = monthly_sales.sort_values(
        by="Month_Number"
    )

    return monthly_sales


def predict_sales(df):
    monthly_sales = prepare_monthly_sales(df)

    X = monthly_sales[["Month_Number"]]
    y = monthly_sales["Units_Sold"]

    model = LinearRegression()
    model.fit(X, y)

    next_month = np.array([
        [monthly_sales["Month_Number"].max() + 1]
    ])

    prediction = model.predict(next_month)

    return round(prediction[0])


def future_forecast(df, months=6):
    monthly_sales = prepare_monthly_sales(df)

    X = monthly_sales[["Month_Number"]]
    y = monthly_sales["Units_Sold"]

    model = LinearRegression()
    model.fit(X, y)

    last_month = monthly_sales[
        "Month_Number"
    ].max()

    future_months = np.arange(
        last_month + 1,
        last_month + months + 1
    )

    predictions = model.predict(
        future_months.reshape(-1, 1)
    )

    month_names = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]

    forecast_months = []

    for month in future_months:
        forecast_months.append(
            month_names[
                (month - 1) % 12
            ]
        )

    forecast_df = pd.DataFrame({
        "Month": forecast_months,
        "Predicted_Sales":
        predictions.round()
    })

    return forecast_df