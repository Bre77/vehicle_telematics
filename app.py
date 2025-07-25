import obd
from obd.utils import OBDStatus
import grpc
import os
import time
import edgehub.v3.edgehub_pb2_grpc as edgehub_pb2_grpc
import edgehub.v3.edgehub_pb2 as edgehub_pb2
from google.protobuf.struct_pb2 import Struct

host_ip = os.getenv('SDK_HOSTNAME') or "host.docker.internal"
host_port = os.getenv('SDK_PORT') or "50051"

obd.Unit.default_format = "~"
METRICS = [
    (obd.commands.ELM_VOLTAGE, "OBDVoltage"),
    (obd.commands.CONTROL_MODULE_VOLTAGE, "ECUVoltage"),
    (obd.commands.SPEED, "Speed"),
    (obd.commands.RPM, "RPM"),
    (obd.commands.INTAKE_TEMP, "IntakeTemp"),
    (obd.commands.RUN_TIME, "RunTime"),
    (obd.commands.FUEL_LEVEL, "FuelLevel"),
    (obd.commands.AMBIANT_AIR_TEMP, "AirTemp"),
    (obd.commands.HYBRID_BATTERY_REMAINING, "HybridBattery"),
    (obd.commands.RELATIVE_ACCEL_POS, "Accelerator"),
    (obd.commands.ABSOLUTE_LOAD, "EngineLoad"),
    (obd.commands.ENGINE_LOAD, "CalculatedEngineLoad"),
    (obd.commands.COOLANT_TEMP, "CoolantTemp"),
]


def main():
    sdk = edgehub_pb2_grpc.EdgeHubServiceStub(
        grpc.insecure_channel(f"{host_ip}:{host_port}")
    )
    def send(message):
        print(message)
        data_struct = Struct()
        data_struct.update(message)
        data_request = edgehub_pb2.SendDataRequest(
            topic_name="obd",
            fields=data_struct
        )
        sdk.SendData(data_request)
    send({"time":time.time(),"log":"Vehicle Telematics has started"})
    while True:
        connection = obd.OBD()

        send({"time":time.time(),"status":connection.status()})
        while connection.status() in {OBDStatus.OBD_CONNECTED, OBDStatus.CAR_CONNECTED}:
            for command, name in METRICS:
                if not connection.supports(command):
                    continue
                resp = connection.query(command)
                if resp and not resp.is_null():
                    send({
                        "time": int(resp.time    or time.time()),
                        name: float(resp.value.magnitude),
                        "unit": str(resp.value.units)
                    })
            time.sleep(1-(time.time() % 1))
        connection.close()
        time.sleep(5)

if __name__ == "__main__":
    main()
