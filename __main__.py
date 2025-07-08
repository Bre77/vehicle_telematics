import obd
import paho.mqtt.client as mqtt
import time
from google.protobuf.timestamp_pb2 import Timestamp
from sensors_pb2 import (
    SensorChannel,
    SensorDatapoint,
    SensorSettings,
    ExternalSensorAvailability,
)


def getTime(t=None):
    t = t or time.time()
    ts = Timestamp()
    ts.FromMilliseconds(millis=round(t * 1000))
    return ts


# obd.logger.removeHandler(obd.console_handler)
obd.Unit.default_format = "~"

PREFIX = f"iotpuck/88e69537-27f0-4da1-89da-4e00fe90750c/sensors"
METRICS = [
    (obd.commands.ELM_VOLTAGE, "OBD Voltage"),
    (obd.commands.CONTROL_MODULE_VOLTAGE, "ECU Voltage"),
    (obd.commands.SPEED, "Speed"),
    (obd.commands.RPM, "RPM"),
    (obd.commands.INTAKE_TEMP, "Intake Temp"),
    (obd.commands.RUN_TIME, "Run Time"),
    (obd.commands.FUEL_LEVEL, "Fuel Level"),
    (obd.commands.AMBIANT_AIR_TEMP, "Air Temp"),
    (obd.commands.HYBRID_BATTERY_REMAINING, "Hybrid Battery"),
    (obd.commands.RELATIVE_ACCEL_POS, "Accelerator"),
    (obd.commands.ABSOLUTE_LOAD, "Engine Load"),
]

print("Connecting MQTT")
client = mqtt.Client()
client.connect("127.0.0.1", 1883, 60)


while True:
    print("Starting v3")
    try:
        connection = obd.OBD()
    except Exception as e:
        print(e)
        break

    print(f"Using OBD adapter at {connection.port_name()}")

    ACTIVE = set()

    while connection.status() in {
        obd.OBDStatus.OBD_CONNECTED,
        obd.OBDStatus.CAR_CONNECTED,
    }:
        for command, label in METRICS:
            if not connection.supports(command):
                continue

            resp = connection.query(command)
            timestamp = getTime()

            if not resp.is_null():
                if not command in ACTIVE:
                    # Add Metric
                    print(f"Adding {command.name}")
                    available = ExternalSensorAvailability(
                        metrics=[command.name],
                        type=command.desc,
                        id=command.name,
                        is_available=True,
                    )
                    client.publish(
                        f"{PREFIX}/availability",
                        payload=available.SerializeToString(),
                    )
                    ACTIVE.add(command)

                data_point = SensorDatapoint(
                    sensor_id=command.name,
                    timestamp=timestamp,
                    value=resp.value.magnitude,
                    channel=SensorChannel(
                        name=command.name,
                        unit=str(resp.value.units),
                        type=command.desc,
                    ),
                    is_sensor_enabled=True,
                    is_anomaly_enabled=False,
                )
                client.publish(
                    f"{PREFIX}/{command.name}/data",
                    payload=data_point.SerializeToString(),
                )

            elif command in ACTIVE:
                # Remove metric
                print(f"Removing {command.name}")
                available = ExternalSensorAvailability(
                    metrics=[command.name],
                    type=command.desc,
                    id=command.name,
                    is_available=False,
                )
                client.publish(
                    f"{PREFIX}/availability",
                    payload=available.SerializeToString(),
                )
                ACTIVE.remove(command)
        time.sleep(1-(time.time() % 1))

    print("Car Disconnected")
    # Remove all active metric
    for command in ACTIVE:
        print(f"Removing {command.name}")
        available = ExternalSensorAvailability(
            metrics=[command.name],
            type=command.desc,
            id=command.name,
            is_available=False,
        )
        client.publish(
            f"{PREFIX}/availability",
            payload=available.SerializeToString(),
        )
        ACTIVE.remove(command)

    connection.close()
    time.sleep(5)

client.disconnect()
