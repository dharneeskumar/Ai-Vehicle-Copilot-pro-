import os
import pickle
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATASET_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "vehicle_health_dataset.csv"
)

MODELS_DIR = os.path.join(
    BASE_DIR,
    "models"
)

df = pd.read_csv(DATASET_PATH)

print("\nDataset Loaded Successfully")
print(df.head())

df.fillna(
    df.mean(numeric_only=True),
    inplace=True
)

X = df[
    [
        "Engine_Temperature",
        "Battery_Voltage",
        "RPM",
        "Fuel_Efficiency"
    ]
]

y = df["Status"]

label_encoder = LabelEncoder()

y_encoded = label_encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.4,
    random_state=42,
    stratify=y_encoded
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

y_pred = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\nAccuracy")
print(f"{accuracy:.4f}")

print("\nClassification Report")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_
    )
)

print("\nConfusion Matrix")
print(
    confusion_matrix(
        y_test,
        y_pred
    )
)

os.makedirs(
    MODELS_DIR,
    exist_ok=True
)

MODEL_PATH = os.path.join(
    MODELS_DIR,
    "vehicle_health_model.pkl"
)

ENCODER_PATH = os.path.join(
    MODELS_DIR,
    "vehicle_health_label_encoder.pkl"
)

with open(
    MODEL_PATH,
    "wb"
) as file:
    pickle.dump(
        model,
        file
    )

with open(
    ENCODER_PATH,
    "wb"
) as file:
    pickle.dump(
        label_encoder,
        file
    )

print("\nModel Saved Successfully")
print(MODEL_PATH)

print("\nLabel Encoder Saved Successfully")
print(ENCODER_PATH)