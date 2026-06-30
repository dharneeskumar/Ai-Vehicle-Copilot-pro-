import os
import pickle
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "vehicle_health_model.pkl"
)

ENCODER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "vehicle_health_label_encoder.pkl"
)

try:
    with open(MODEL_PATH, "rb") as file:
        model = pickle.load(file)

    with open(ENCODER_PATH, "rb") as file:
        label_encoder = pickle.load(file)

except Exception as e:
    print(f"Model loading failed: {e}")
    model = None
    label_encoder = None


def predict_vehicle_health(
    engine_temp,
    battery_voltage,
    rpm,
    fuel_efficiency
):
    try:

        if model is None or label_encoder is None:
            return {
                "status": "Model Not Loaded",
                "probability": 0.0,
                "health_score": 0
            }

        features = pd.DataFrame(
            [[
                engine_temp,
                battery_voltage,
                rpm,
                fuel_efficiency
            ]],
            columns=[
                "Engine_Temperature",
                "Battery_Voltage",
                "RPM",
                "Fuel_Efficiency"
            ]
        )

        prediction = model.predict(features)

        status = label_encoder.inverse_transform(
            prediction
        )[0]

        probabilities = model.predict_proba(features)[0]

        confidence = float(
            np.max(probabilities)
        )

        # =================================
        # Vehicle Health Score Calculation
        # =================================

        status_lower = status.lower()

        if status_lower == "healthy":

            health_score = int(
                90 + (confidence * 10)
            )

        elif status_lower == "warning":

            health_score = int(
                60 + (confidence * 29)
            )

        elif status_lower == "critical":

            health_score = int(
                confidence * 59
            )

        else:

            health_score = 50

        health_score = max(
            0,
            min(
                100,
                health_score
            )
        )

        return {
            "status": status,
            "probability": round(
                confidence,
                4
            ),
            "health_score": health_score
        }

    except Exception as e:

        print(
            f"Prediction error: {e}"
        )

        return {
            "status": "Error",
            "probability": 0.0,
            "health_score": 0
        }
if __name__ == "__main__":

    result = predict_vehicle_health(
        engine_temp=95,
        battery_voltage=12.4,
        rpm=3000,
        fuel_efficiency=16
    )

    print("\nVehicle Health Prediction")
    print(result)