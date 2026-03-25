import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import joblib

print("Loading dataset...")

# Load dataset
df = pd.read_csv("dataset.csv")

print("Preparing data...")

# Features and target
X = df.drop("crop_yield", axis=1)
y = df["crop_yield"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Training model...")

# Model
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train
model.fit(X_train, y_train)

print("Making predictions...")

# Predict
y_pred = model.predict(X_test)

# Accuracy
score = r2_score(y_test, y_pred)
print(f"Model Accuracy (R2 Score): {score:.2f}")

# Save model
joblib.dump(model, "model.pkl")

print("Model saved successfully!")