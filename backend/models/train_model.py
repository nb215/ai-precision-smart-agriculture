
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
data = pd.read_csv("../datasets/Crop_recommendation.csv")

# Features
X = data[['N','P','K','temperature','humidity','ph','rainfall']]

# Target
y = data['label']

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestClassifier()

model.fit(X_train, y_train)

# Save model
joblib.dump(model, "crop_model.pkl")

print("Model trained and saved")