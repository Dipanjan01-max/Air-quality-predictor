import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load dataset (try one first, like city_day)
data = pd.read_csv("city_day.csv")

print("Data preview:")
print(data.head())

# Basic info
print("\nData Info:")
print(data.info())

# Drop missing values
data = data.dropna()

# Let's say we want to predict PM2.5 levels based on other pollutants
X = data[['PM10', 'NO2', 'SO2', 'CO', 'O3']]
y = data['PM2.5']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))
print("R² Score:", r2_score(y_test, y_pred))

# Plot
plt.scatter(y_test, y_pred, alpha=0.5)
plt.xlabel("Actual PM2.5")
plt.ylabel("Predicted PM2.5")
plt.title("Air Quality Prediction (PM2.5)")
plt.show()
import joblib

# After training
joblib.dump(model, "air_quality_model.pkl")
