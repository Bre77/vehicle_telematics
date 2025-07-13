# EdgeHub SDK Architecture and Implementation Guide

## Overview

The EdgeHub SDK is a TypeScript-based gRPC service that acts as a bridge between external applications and an internal MQTT broker. It provides a standardized API for data ingestion, discovery, and real-time streaming of IoT sensor data, logs, and other telemetry information.

## Architecture

### High-Level Architecture

```
┌─────────────────┐    gRPC     ┌─────────────────┐    MQTT     ┌─────────────────┐
│   Client Apps   │ ◄────────► │   EdgeHub SDK   │ ◄────────► │   MQTT Broker   │
│                 │             │                 │             │  (localhost:1884)│
│ - OBD Scanner   │             │ - gRPC Server   │             │                 │
│ - Sensor Apps   │             │ - MQTT Client   │             │ - Sensor Data   │
│ - Log Clients   │             │ - Data Bridge   │             │ - Log Events    │
└─────────────────┘             └─────────────────┘             └─────────────────┘
```

### Core Components

1. **gRPC Server** (`server.ts`) - Main service implementation
2. **MQTT Bridge** (`mqtt_helpers.ts`) - MQTT client management
3. **Data Helpers** (`helpers.ts`) - Data transformation and discovery
4. **Configuration** (`constants.ts`) - System constants and paths
5. **Logging** (`logger.ts`) - Centralized logging

## Core Service Implementation

### EdgeHubSdk Class

The main service class implements the `EdgeHubServiceServer` interface and provides four primary gRPC endpoints:

```typescript
class EdgeHubSdk implements EdgeHubServer {
    mqttProducer: MqttClient;           // For publishing data
    hubId: string;                      // Hub identifier
    subscribers: { [topic: string]: MqttClient }; // Topic subscriptions
}
```

### gRPC Service Endpoints

#### 1. Discovery Service
```typescript
getDiscovery(call, callback) → GetDiscoveryResponse
```
- **Purpose**: Returns available sensors, data streamers, and topics
- **Data Sources**: 
  - `/etc/splunk/splunkiotpuck/sensor_config.json` (sensors)
  - `/etc/splunk/splunkiotpuck/hub_services_config.json` (data streamers)
- **Response**: List of `DiscoveryInfo` objects with topic names and metadata

#### 2. Data Reading Services
```typescript
getReading(call, callback) → GetReadingResponse        // Single read
getReadingStreamResponse(stream) → Stream<GetReadingResponse> // Continuous stream
```
- **Purpose**: Subscribe to MQTT topics and return data
- **Flow**:
  1. Create MQTT subscriber for requested topic
  2. Wait for MQTT message
  3. Transform message to gRPC response
  4. Return data (single) or stream continuously

#### 3. Data Publishing Services
```typescript
sendData(call, callback) → SendDataResponse           // Single publish
sendDataStream(stream) → Stream<SendDataResponse>     // Continuous publish
```
- **Purpose**: Accept data from clients and publish to MQTT
- **Flow**:
  1. Receive `SendDataRequest` with topic and data fields
  2. Convert protobuf `Struct` to JSON
  3. Publish JSON to MQTT broker
  4. Return success/failure response

## Data Flow Patterns

### 1. Data Ingestion (Client → MQTT)
```
Client App → gRPC SendData → JSON Conversion → MQTT Publish → Internal Systems
```

### 2. Data Consumption (MQTT → Client)
```
Internal Systems → MQTT → Message Transformation → gRPC Response → Client App
```

### 3. Discovery Flow
```
Client → gRPC GetDiscovery → File System Read → Available Topics/Sensors → Client
```

## Message Transformation

The SDK handles multiple data formats and transforms them into standardized gRPC responses:

### Supported Data Types

1. **Sensor Data** (`SensorDatapoint`)
   - Topic pattern: `edgehub/{category}/{type}/values`
   - Contains: sensor ID, timestamp, value, channel info

2. **Log Events** (`LogEvent`)
   - Topics: `edgehub/opcua`, `edgehub/modbus`
   - Contains: structured log records with timestamps

3. **SNMP Events** (`SNMPEvent`)
   - Topic: `edgehub/snmp`
   - Contains: SNMP-specific telemetry data

4. **Generic JSON**
   - Any other topic
   - Raw JSON data passed through

### Transformation Logic
```typescript
function createGetReadingResponse(topicName: string, message: Buffer): GetReadingResponse {
    if (topicName === SDK_MODBUS_TOPIC || topicName === SDK_OPCUA_TOPIC) {
        const logEvent = LogEvent.decode(message);
        return handleLogEvent(logEvent, topicName);
    } else if (topicName === SDK_SNMP_TOPIC) {
        const snmpEvent = SNMPEvent.decode(message);
        return handleSnmpEvent(snmpEvent, topicName);
    } else if (SDK_VALID_SENSOR_TOPIC(topicName)) {
        const sensorDataPoint = SensorDatapoint.decode(message);
        return handleSensorDataPoint(sensorDataPoint, topicName);
    } else {
        const jsonObject = JSON.parse(message.toString());
        return handleJsonEvent(jsonObject, topicName);
    }
}
```

## Configuration and Discovery

### Hub Configuration
- **File**: `/etc/splunk/splunkiotpuck/config.json`
- **Purpose**: Contains hub ID (`puckId`) for identification
- **Fallback**: Uses wildcard topic `"+"` if file unavailable

### Sensor Configuration
- **File**: `/etc/splunk/splunkiotpuck/sensor_config.json`
- **Structure**:
```json
{
  "sensors": [
    {
      "id": "sensor_id",
      "type": "sensor_type", 
      "category": "category",
      "metrics": [{"metricName": "metric_name"}],
      "settings": {
        "isSensorEnabled": true,
        "uploadRate": 1000
      }
    }
  ]
}
```

### Data Streamer Configuration
- **File**: `/etc/splunk/splunkiotpuck/hub_services_config.json`
- **Purpose**: Defines available data streaming topics and services

## MQTT Integration

### Connection Details
- **Broker**: `localhost:1884`
- **Protocol**: MQTT v3.1.1
- **QoS**: 0 (fire and forget)
- **Retain**: false

### Client Management
```typescript
// Producer (for publishing)
mqttProducer = createMQTTClient(SDK_MQTT_PRODUCER_ID);

// Subscribers (per topic)
private subscribers: { [topic: string]: mqtt.MqttClient } = {};

// Subscribe to topic
private subscribe(topic: string): MqttClient {
    const client = subscribeToMQTT(topic);
    this.subscribers[topic] = client;
    return client;
}

// Cleanup subscription
private unsubscribe(topic: string) {
    const client = this.subscribers[topic];
    if (client) {
        delete this.subscribers[topic];
        unsubscribeFromMQTT(client, topic);
    }
}
```

## Error Handling and Logging

### Logging Levels
- **DEBUG**: Detailed operation logs
- **INFO**: General operation status
- **ERROR**: Error conditions and failures

### Error Scenarios
1. **MQTT Connection Failures**: Service startup failure
2. **File System Access**: Configuration file read errors
3. **Message Parsing**: Invalid protobuf or JSON data
4. **Topic Subscription**: MQTT subscription failures

## Usage Patterns

### For Client Applications

1. **Discovery**: Call `getDiscovery()` to find available topics
2. **Data Publishing**: Use `sendData()` or `sendDataStream()` to publish sensor data
3. **Data Consumption**: Use `getReading()` or `getReadingStreamResponse()` to consume data
4. **Error Handling**: Check response status and handle connection errors

### Example Client Flow
```typescript
// 1. Discover available topics
const discovery = await stub.getDiscovery({});

// 2. Publish sensor data
const dataRequest = {
    topicName: "edgehub/sensors/temperature/data",
    fields: {
        sensor_id: "temp_01",
        value: 23.5,
        timestamp: Date.now()
    }
};
const response = await stub.sendData(dataRequest);

// 3. Subscribe to data stream
const stream = stub.getReadingStreamResponse({
    topicName: "edgehub/sensors/+/data"
});
stream.on('data', (response) => {
    console.log('Received:', response);
});
```

## Security and Access Control

- **File System Access**: Requires sudo/root access for configuration files
- **Network Access**: gRPC server binds to `0.0.0.0:50051` (insecure)
- **MQTT Access**: Local broker access only (`localhost:1884`)

## Performance Considerations

- **Connection Pooling**: One MQTT client per subscribed topic
- **Message Buffering**: No built-in buffering; relies on MQTT broker
- **Concurrent Streams**: Supports multiple concurrent gRPC streams
- **Memory Management**: Automatic cleanup of MQTT subscriptions on stream end

## Deployment and Operations

### Service Startup
```typescript
const server = new TypedServerOverride();
server.addTypedService<EdgeHubServer>(EdgeHubServiceService, new EdgeHubSdk());
server.bindAsync("0.0.0.0:50051", ServerCredentials.createInsecure(), () => {
    Logger.info("Starting Edge Hub SDK Service");
    server.start();
});
```

### Dependencies
- **Runtime**: Node.js with TypeScript
- **gRPC**: `@grpc/grpc-js` v1.9.15
- **MQTT**: `mqtt` v5.2.0
- **Protobuf**: Generated from `.proto` definitions

### Monitoring
- Console-based logging with DEBUG/INFO/ERROR levels
- MQTT connection status monitoring
- gRPC call success/failure tracking

## Extension Points

1. **Custom Data Handlers**: Add new message type handlers in `helpers.ts`
2. **Authentication**: Implement gRPC interceptors for auth
3. **Data Validation**: Add schema validation for incoming data
4. **Metrics**: Integrate with monitoring systems
5. **Configuration**: Support dynamic configuration updates

This SDK provides a robust foundation for IoT data integration, offering both real-time streaming and batch data processing capabilities through a clean gRPC interface.