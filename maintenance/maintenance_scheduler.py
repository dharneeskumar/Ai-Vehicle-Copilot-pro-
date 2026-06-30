def generate_maintenance_schedule(
    fault_type,
    vehicle_status,
    battery_life_months,
    service_due_km
):

    recommendations = []

    try:

        if fault_type == "Engine Overheating":

            recommendations.append(
                "cooling_system_inspection_required"
            )

            recommendations.append(
                "check_coolant_level_and_radiator"
            )

        elif fault_type == "Battery Degradation":

            recommendations.append(
                "battery_health_inspection_recommended"
            )

            recommendations.append(
                "check_charging_system_and_terminals"
            )

        elif fault_type == "Abnormal Engine RPM":

            recommendations.append(
                "engine_tuning_inspection_recommended"
            )

            recommendations.append(
                "check_throttle_and_fuel_injection_system"
            )

        elif fault_type == "Fuel Efficiency Loss":

            recommendations.append(
                "inspect_fuel_system_components"
            )

            recommendations.append(
                "check_air_filter_and_fuel_injectors"
            )

        if vehicle_status.lower() == "warning":

            recommendations.append(
                "schedule_maintenance_within_15_days"
            )

        elif vehicle_status.lower() == "critical":

            recommendations.append(
                "immediate_vehicle_service_required"
            )

        if battery_life_months <= 3:

            recommendations.append(
                "battery_replacement_planning_recommended"
            )

        elif battery_life_months <= 6:

            recommendations.append(
                "battery_inspection_recommended"
            )

        if service_due_km <= 500:

            recommendations.append(
                "vehicle_service_due_immediately"
            )

        elif service_due_km <= 1500:

            recommendations.append(
                "schedule_vehicle_service_soon"
            )

        if len(recommendations) == 0:

            recommendations.append(
                "vehicle_operating_normally"
            )

            recommendations.append(
                "continue_periodic_maintenance"
            )

        return recommendations

    except Exception as e:

        print(f"Maintenance Scheduler Error: {e}")

        return [
            "unable_to_generate_maintenance_schedule"
        ]