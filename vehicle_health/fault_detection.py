def detect_fault(
    engine_temp,
    battery_voltage,
    rpm,
    fuel_efficiency
):

    fault_type = "healthy"

    severity = "low"

    # -------------------------
    # Engine Overheating
    # -------------------------

    if engine_temp >= 110:

        fault_type = "engine_overheating"

        severity = "high"

    # -------------------------
    # Battery Degradation
    # -------------------------

    elif battery_voltage < 11.5:

        fault_type = "battery_degradation"

        severity = "medium"

    # -------------------------
    # Excessive RPM
    # -------------------------

    elif rpm > 6000:

        fault_type = "abnormal_engine_rpm"

        severity = "medium"

    # -------------------------
    # Fuel Efficiency Drop
    # -------------------------

    elif fuel_efficiency < 10:

        fault_type = "fuel_efficiency_loss"

        severity = "medium"

    return {

        "fault_type": fault_type,

        "severity": severity

    }


# -----------------------------------
# Testing
# -----------------------------------

if __name__ == "__main__":

    result = detect_fault(
        engine_temp=120,
        battery_voltage=12.5,
        rpm=3000,
        fuel_efficiency=15
    )

    print(result)