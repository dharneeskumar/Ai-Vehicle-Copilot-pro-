"""
rul_prediction.py

Remaining Useful Life (RUL) Prediction
for Edge AI Automotive Safety & Health Copilot
"""


def predict_rul(
    health_score,
    engine_temp,
    battery_voltage,
    rpm
):

    try:

        # ==================================
        # Battery Remaining Life
        # ==================================

        battery_life_months = int(
            (health_score / 100) * 12
        )

        if battery_voltage < 11.5:

            battery_life_months -= 3

        battery_life_months = max(
            1,
            battery_life_months
        )

        # ==================================
        # Service Due Prediction
        # ==================================

        service_due_km = int(
            (health_score / 100) * 5000
        )

        if engine_temp > 110:

            service_due_km -= 1500

        if rpm > 6000:

            service_due_km -= 1000

        service_due_km = max(
            100,
            service_due_km
        )

        # ==================================
        # RUL Status
        # ==================================

        if health_score >= 80:

            status = "Good"

        elif health_score >= 60:

            status = "Moderate"

        else:

            status = "Poor"

        return {

            "battery_life_months":
                battery_life_months,

            "service_due_km":
                service_due_km,

            "status":
                status

        }

    except Exception as e:

        print(
            f"RUL Prediction Error: {e}"
        )

        return {

            "battery_life_months": 0,

            "service_due_km": 0,

            "status": "Unknown"

        }


# ==================================
# Standalone Testing
# ==================================

if __name__ == "__main__":

    result = predict_rul(

        health_score=85,

        engine_temp=95,

        battery_voltage=12.4,

        rpm=3000

    )

    print("\nRemaining Useful Life Prediction")
    print(result)
