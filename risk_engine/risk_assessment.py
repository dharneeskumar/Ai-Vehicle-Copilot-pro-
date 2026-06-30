

def calculate_risk(
    drowsiness_status,
    distraction_status,
    vehicle_status,
    fault_severity="Low",
    health_score=100,
    battery_life_months=12,
    service_due_km=5000
):

    score = 100

    # ==================================
    # Driver Monitoring Risk
    # ==================================

    if drowsiness_status.lower() == "drowsy":

        score -= 35

    if distraction_status.lower() == "distracted":

        score -= 25

    # ==================================
    # Vehicle Health Risk
    # ==================================

    vehicle_status = vehicle_status.lower()

    if vehicle_status == "warning":

        score -= 20

    elif vehicle_status == "critical":

        score -= 40

    # ==================================
    # Fault Severity Risk
    # ==================================

    fault_severity = fault_severity.lower()

    if fault_severity == "medium":

        score -= 15

    elif fault_severity == "high":

        score -= 30

    # ==================================
    # Health Score Risk
    # ==================================

    if health_score < 60:

        score -= 20

    elif health_score < 80:

        score -= 10

    # ==================================
    # Battery Life Risk
    # ==================================

    if battery_life_months <= 3:

        score -= 15

    elif battery_life_months <= 6:

        score -= 5

    # ==================================
    # Service Due Risk
    # ==================================

    if service_due_km <= 500:

        score -= 15

    elif service_due_km <= 1500:

        score -= 5

    # ==================================
    # Final Score Clamp
    # ==================================

    score = max(
        0,
        min(
            100,
            score
        )
    )

    # ==================================
    # Risk Level
    # ==================================

    if score >= 80:

        risk_level = "Low"

    elif score >= 60:

        risk_level = "Medium"

    elif score >= 40:

        risk_level = "High"

    else:

        risk_level = "Critical"

    return {

        "safety_score": score,

        "risk_level": risk_level

    }


# ==================================
# Testing
# ==================================

if __name__ == "__main__":

    result = calculate_risk(

        drowsiness_status="Drowsy",

        distraction_status="Distracted",

        vehicle_status="Warning",

        fault_severity="High",

        health_score=55,

        battery_life_months=2,

        service_due_km=300

    )

    print("\nRisk Assessment Result")
    print(result)
