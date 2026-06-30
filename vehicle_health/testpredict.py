from vehicle_health.predict import predict_vehicle_health

result = predict_vehicle_health(
    engine_temp=100,
    battery_voltage=12.0,
    rpm=3500,
    fuel_efficiency=14
)

print(result)