# Vehicle Telematics with Splunk EdgeHub

A proof-of-concept Edge application for collecting vehicle telemetry data using OBD2 interfaces and the Splunk EdgeHub platform.

## Overview

This project demonstrates how to collect real-time vehicle telematics data using the Splunk EdgeHub and OBD2 (On-Board Diagnostics) interface. The solution captures various vehicle metrics such as speed, RPM, temperature readings, fuel levels, and voltage data, then forwards this information to Splunk for analysis and visualization.

Originally presented at Splunk .conf25 in the session "PLA1080 - You Wouldn't Splunk a Car?" by Brett Adams, Splunk Practice Lead at Deloitte Australia and SplunkTrust member.

## What is Vehicle Telematics?

According to Google AI Overview, Vehicle telematics is a system that uses telecommunications and informatics to collect and transmit data from a vehicle, typically for fleet management or tracking purposes. This project focuses on getting data from vehicles into Splunk for analysis and monitoring.

## Architecture

The solution consists of three main components:

1. **Vehicle CAN Bus & OBD2 Interface**: Communication layer between vehicle electronics and external systems
2. **Splunk EdgeHub**: Edge computing device that connects to the vehicle via USB-to-OBD2 cable
3. **Splunk Platform**: Central data collection and analysis platform

### High-Level Data Flow

```
Vehicle CAN Bus → OBD2 Port → USB-to-OBD2 Cable → EdgeHub → Splunk Platform
```

## EdgeHub Components

- **Splunk OTI App**: Central management point for EdgeHub configuration
- **EdgeHub OS**: Manages connection to Splunk via Secure Gateway, applies device heuristics, and handles Edge SDK messages
- **Edge App**: Docker container responsible for vehicle communication, command execution, response parsing, and data forwarding

## Features

### Supported OBD2 Metrics

The application collects the following vehicle metrics:

- **Performance**: Speed, RPM, Engine Load, Accelerator Position
- **Temperature Monitoring**: Coolant Temperature, Intake Temperature, Ambient Air Temperature
- **Power Systems**: OBD Voltage, ECU Voltage, Fuel Level, Hybrid Battery Level
- **Engine Status**: Run Time

### Use Cases

- **Fleet Management**: Monitor driver behavior, speeding, and aggressive driving patterns
- **Predictive Maintenance**: Identify potential mechanical issues through temperature and voltage monitoring
- **Environmental Monitoring**: Track ambient conditions and their impact on vehicle performance
- **Battery Health**: Monitor 12V system health to predict battery/alternator failures

## Hardware Requirements

- Splunk EdgeHub device
- USB-to-OBD2 cable
- Vehicle with OBD2 port (mandatory in most vehicles since 1996)
- 20V USB Power Delivery power source (vehicles typically provide 12V DC)
- Optional: USB GPS receiver for location tracking

## Installation

### Physical Setup

1. Connect USB-to-OBD2 cable to vehicle's OBD2 port (typically in driver footwell)
2. Route cable to EdgeHub mounting location
3. Connect EdgeHub to 20V USB PD power source
4. Optional: Connect USB GPS receiver

### Software Setup

1. Build the Edge App:
```bash
make all
```

2. Upload `edge.tar.gz` to EdgeHub via admin web interface

3. Configure EdgeHub through Splunk OTI app

## Project Structure

```
vehicle_telematics/
├── app.py              # Main application logic
├── edge.json           # Edge app metadata and configuration
├── Dockerfile          # Docker container definition
├── Makefile            # Build automation
├── requirements.txt    # Python dependencies
├── edgehub/            # EdgeHub SDK protobuf definitions
└── README.md           # This file
```

## Code Overview

The core application is surprisingly simple - all functional parts fit in a few dozen lines of Python:

```python
# Connect to EdgeHub SDK
sdk = edgehub_pb2_grpc.EdgeHubServiceStub(grpc.insecure_channel(f"{host_ip}:{host_port}"))

# Connect to vehicle OBD2 port
connection = obd.OBD()

# Query supported metrics and send to Splunk
for command, name in METRICS:
    if connection.supports(command):
        resp = connection.query(command)
        if resp and not resp.is_null():
            send_data_to_splunk(resp)
```

## Data Analysis Examples

### Driver Behavior Analysis
- Monitor speed patterns and aggressive acceleration
- Analyze hybrid vehicle efficiency (engine on/off cycles)
- Track fuel consumption patterns

### Predictive Maintenance
- Voltage monitoring for battery/alternator health
- Temperature trend analysis for cooling system issues
- Engine load patterns for wear prediction

### Environmental Impact
- Ambient temperature correlation with vehicle performance
- Hybrid battery usage optimization
- Fuel efficiency under different conditions

## Limitations

- OBD2 is an older standard with limited data availability
- Not mandatory in battery electric vehicles
- Requires physical installation and power management
- Limited to standardized OBD2 commands

## Development

### Prerequisites

- Python 3.13+
- Docker with ARM64 support
- Access to Splunk EdgeHub device
- Vehicle with OBD2 port for testing

### Building

```bash
# Generate protobuf files
make protos

# Build Docker image
make docker.tar

# Package for EdgeHub
make edge.tar.gz

# Clean build artifacts
make clean
```

### Testing

```bash
# Test Docker container locally
make test
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

This is a proof-of-concept project originally developed for demonstration purposes. Feel free to fork and extend for your own use cases.