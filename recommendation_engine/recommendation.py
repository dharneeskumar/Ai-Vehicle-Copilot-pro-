def generate_recommendation(
    drowsiness_status,
    distraction_status,
    vehicle_status,
    risk_level,
    fault_type="Healthy",
    battery_life_months=12,
    service_due_km=5000,
    fuel_level=100
):
    recommendations = []

    # Driver Drowsiness

    if drowsiness_status.lower() == "drowsy":

        recommendations.append("driver_appears_drowsy")
        recommendations.append("consider_stopping_and_drinking_water")

    # Driver Distraction

    if distraction_status.lower() == "distracted":

        recommendations.append("avoid_mobile_phone_usage")
        recommendations.append("keep_eyes_on_road")

    # Vehicle Health

    vehicle_status = vehicle_status.lower()

    if vehicle_status == "warning":

        recommendations.append("vehicle_health_warning_detected")
        recommendations.append("monitor_engine_parameters")

    elif vehicle_status == "critical":

        recommendations.append("critical_vehicle_condition_detected")
        recommendations.append("avoid_long_distance_travel")

    # Fault-Based Recommendations

    if fault_type == "engine_overheating":

        recommendations.append("inspect_radiator_coolant_and_fan")
        recommendations.append(
            "reduce_engine_load_until_maintenance_completed"
        )

    elif fault_type == "battery_degradation":

        recommendations.append(
            "check_battery_health_and_charging_system"
        )

        recommendations.append(
            "inspect_battery_terminals_for_corrosion"
        )

    elif fault_type == "abnormal_engine_rpm":

        recommendations.append(
            "inspect_throttle_body_and_fuel_injection_system"
        )

        recommendations.append(
            "perform_engine_diagnostics"
        )

    elif fault_type == "fuel_efficiency_loss":

        recommendations.append(
            "inspect_air_filter_and_fuel_injectors"
        )

        recommendations.append(
            "check_fuel_delivery_system"
        )

    # Battery Life

    if battery_life_months <= 3:

        recommendations.append(
            "battery_replacement_planning_strongly_recommended"
        )

    elif battery_life_months <= 6:

        recommendations.append(
            "battery_health_inspection_recommended"
        )

    # Service Due

    if service_due_km <= 500:

        recommendations.append(
            "vehicle_service_due_immediately"
        )

    elif service_due_km <= 1500:

        recommendations.append(
            "schedule_vehicle_service_soon"
        )



    # Fuel Level

    if fuel_level <= 15:

        recommendations.append(
            "fuel_level_low"
    )

        recommendations.append(
            "refuel_vehicle_soon"
    )

    # Risk Level

    risk_level = risk_level.lower()

    if risk_level == "low":

        recommendations.append(
            "vehicle_and_driver_conditions_normal"
        )

    elif risk_level == "medium":

        recommendations.append(
            "exercise_caution_and_monitor_alertness"
        )

    elif risk_level == "high":

        recommendations.append(
            "high_risk_detected_reduce_speed"
        )

        recommendations.append(
            "consider_short_break"
        )

    elif risk_level == "critical":

        recommendations.append(
            "critical_risk_detected_stop_vehicle"
        )

        recommendations.append(
            "seek_immediate_assistance"
        )

    # Default

    if len(recommendations) == 0:

        recommendations.append(
            "no_issues_detected_continue_safe_driving"
        )

    return recommendations