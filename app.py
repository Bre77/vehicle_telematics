import obd
import grpc
import os
import time
import edgehub.v3.edgehub_pb2_grpc as edgehub_pb2_grpc
import edgehub.v3.edgehub_pb2 as edgehub_pb2
from google.protobuf.struct_pb2 import Struct
from google.protobuf.timestamp_pb2 import Timestamp

host_ip = os.getenv('SDK_HOSTNAME') or "192.168.1.125"
host_port = os.getenv('SDK_PORT') or "51051"

obd.Unit.default_format = "~"
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

def getTime(t=None):
    t = t or time.time()
    ts = Timestamp()
    ts.FromMilliseconds(millis=round(t * 1000))
    return ts

def main():
    channel = grpc.insecure_channel(f"{host_ip}:{host_port}")
    stub = edgehub_pb2_grpc.EdgeHubServiceStub(channel)

    while True:
        connection = obd.OBD()
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
                    if  command not in ACTIVE:
                        # Add Metric
                        print(f"Adding {command.name}")
                        # Send availability using gRPC
                        availability_struct = Struct()
                        availability_struct.update({
                            "metrics": [command.name],
                            "type": command.desc,
                            "id": command.name,
                            "is_available": True,
                        })
                        availability_request = edgehub_pb2.SendDataRequest(
                            topic_name="edgehub/sensors/availability",
                            fields=availability_struct
                        )
                        try:
                            response = stub.SendData(availability_request)
                            print(f"Availability sent: {response}")
                        except Exception as e:
                            print(f"Error sending availability: {e}")
                        ACTIVE.add(command)

                    # Send sensor data using gRPC
                    data_struct = Struct()
                    data_struct.update({
                        "sensor_id": command.name,
                        "timestamp": timestamp.ToMilliseconds(),
                        "value": resp.value.magnitude,
                        "channel_name": command.name,
                        "channel_unit": str(resp.value.units),
                        "channel_type": command.desc,
                        "is_sensor_enabled": True,
                        "is_anomaly_enabled": False,
                    })
                    data_request = edgehub_pb2.SendDataRequest(
                        topic_name=f"edgehub/sensors/{command.name}/data",
                        fields=data_struct
                    )
                    try:
                        response = stub.SendData(data_request)
                        print(f"Data sent for {command.name}: {response}")
                    except Exception as e:
                        print(f"Error sending data for {command.name}: {e}")

                elif command in ACTIVE:
                    # Remove metric
                    print(f"Removing {command.name}")
                    # Send unavailability using gRPC
                    availability_struct = Struct()
                    availability_struct.update({
                        "metrics": [command.name],
                        "type": command.desc,
                        "id": command.name,
                        "is_available": False,
                    })
                    availability_request = edgehub_pb2.SendDataRequest(
                        topic_name="edgehub/sensors/availability",
                        fields=availability_struct
                    )
                    try:
                        response = stub.SendData(availability_request)
                        print(f"Unavailability sent: {response}")
                    except Exception as e:
                        print(f"Error sending unavailability: {e}")
                    ACTIVE.remove(command)
            time.sleep(1-(time.time() % 1))

        print("Car Disconnected")
        # Remove all active metric
        for command in list(ACTIVE):  # Create a copy to avoid modification during iteration
            print(f"Removing {command.name}")
            # Send unavailability using gRPC
            availability_struct = Struct()
            availability_struct.update({
                "metrics": [command.name],
                "type": command.desc,
                "id": command.name,
                "is_available": False,
            })
            availability_request = edgehub_pb2.SendDataRequest(
                topic_name="edgehub/sensors/availability",
                fields=availability_struct
            )
            try:
                response = stub.SendData(availability_request)
                print(f"Cleanup unavailability sent: {response}")
            except Exception as e:
                print(f"Error sending cleanup unavailability: {e}")
            ACTIVE.remove(command)

        connection.close()
        time.sleep(5)


    print("=== OBD Scanner completed ===")
    channel.close()

if __name__ == "__main__":
    main()
