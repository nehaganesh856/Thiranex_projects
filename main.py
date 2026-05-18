
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


dates = pd.date_range(start='2022-01-01', periods=36, freq='ME')

sales = [
    200, 220, 250, 270, 300, 320,
    350, 370, 390, 420, 450, 470,
    500, 520, 550, 580, 600, 620,
    650, 670, 700, 730, 760, 780,
    800, 830, 860, 890, 920, 950,
    980, 1000, 1030, 1060, 1090, 1120
]

df = pd.DataFrame({
    'Date': dates,
    'Sales': sales
})

df['Date'] = pd.to_datetime(df['Date'])

df['Month_Number'] = np.arange(len(df))

df['Previous_Sales'] = df['Sales'].shift(1)

df['Rolling_Mean_3'] = df['Sales'].rolling(window=3).mean()

df.dropna(inplace=True)


X = df[['Month_Number', 'Previous_Sales', 'Rolling_Mean_3']]
y = df['Sales']

split_index = int(len(df) * 0.8)

X_train = X[:split_index]
X_test = X[split_index:]

y_train = y[:split_index]
y_test = y[split_index:]


model = LinearRegression()

model.fit(X_train, y_train)

predictions = model.predict(X_test)



mae = mean_absolute_error(y_test, predictions)

rmse = np.sqrt(mean_squared_error(y_test, predictions))

r2 = r2_score(y_test, predictions)

print("\n===== MODEL PERFORMANCE =====")
print(f"Mean Absolute Error : {mae:.2f}")
print(f"Root Mean Squared Error : {rmse:.2f}")
print(f"R2 Score : {r2:.2f}")



plt.figure(figsize=(10, 5))

plt.plot(y_test.values, label='Actual Sales', marker='o')

plt.plot(predictions, label='Predicted Sales', marker='x')

plt.title('Actual vs Predicted Sales')

plt.xlabel('Test Data Points')

plt.ylabel('Sales')

plt.legend()

plt.grid(True)

plt.show()

future_months = 6

last_month_number = df['Month_Number'].iloc[-1]

last_sales = df['Sales'].iloc[-1]

last_rolling_mean = df['Rolling_Mean_3'].iloc[-1]

future_predictions = []

print("\n===== FUTURE SALES FORECAST =====")

for i in range(1, future_months + 1):

    future_month = last_month_number + i

    future_input = pd.DataFrame({
        'Month_Number': [future_month],
        'Previous_Sales': [last_sales],
        'Rolling_Mean_3': [last_rolling_mean]
    })

    future_sale = model.predict(future_input)[0]

    future_predictions.append(future_sale)

    print(f"Month {i} Forecasted Sales: {future_sale:.2f}")

    last_sales = future_sale


plt.figure(figsize=(10, 5))

plt.plot(df['Sales'].values, label='Historical Sales', marker='o')

future_x = np.arange(len(df), len(df) + future_months)

plt.plot(future_x, future_predictions,
         label='Future Forecast',
         marker='x')

plt.title('Sales Forecasting')

plt.xlabel('Time')

plt.ylabel('Sales')

plt.legend()

plt.grid(True)

plt.show()


print("\n===== CLEANED DATASET =====")
print(df.head())

print("\n===== PREDICTED VALUES =====")
print(predictions)