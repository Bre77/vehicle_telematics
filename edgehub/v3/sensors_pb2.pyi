from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MLModelType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    knn: _ClassVar[MLModelType]
    hst: _ClassVar[MLModelType]
    mltk: _ClassVar[MLModelType]
knn: MLModelType
hst: MLModelType
mltk: MLModelType

class SensorSettings(_message.Message):
    __slots__ = ("is_sensor_enabled", "is_anomaly_enabled", "upload_rate", "model_type", "mltk_model_id")
    IS_SENSOR_ENABLED_FIELD_NUMBER: _ClassVar[int]
    IS_ANOMALY_ENABLED_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_RATE_FIELD_NUMBER: _ClassVar[int]
    MODEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    MLTK_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    is_sensor_enabled: bool
    is_anomaly_enabled: bool
    upload_rate: int
    model_type: MLModelType
    mltk_model_id: str
    def __init__(self, is_sensor_enabled: bool = ..., is_anomaly_enabled: bool = ..., upload_rate: _Optional[int] = ..., model_type: _Optional[_Union[MLModelType, str]] = ..., mltk_model_id: _Optional[str] = ...) -> None: ...

class SensorChannel(_message.Message):
    __slots__ = ("name", "unit", "type")
    NAME_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    unit: str
    type: str
    def __init__(self, name: _Optional[str] = ..., unit: _Optional[str] = ..., type: _Optional[str] = ...) -> None: ...

class SensorDimension(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class SensorDatapoint(_message.Message):
    __slots__ = ("timestamp", "value", "channel", "is_sensor_enabled", "is_anomaly_enabled", "additional_details", "dimensions", "sensor_id", "sensor_has_error", "model_type", "mltk_model_id", "sensor_category")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    IS_SENSOR_ENABLED_FIELD_NUMBER: _ClassVar[int]
    IS_ANOMALY_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_DETAILS_FIELD_NUMBER: _ClassVar[int]
    DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    SENSOR_ID_FIELD_NUMBER: _ClassVar[int]
    SENSOR_HAS_ERROR_FIELD_NUMBER: _ClassVar[int]
    MODEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    MLTK_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    SENSOR_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    value: float
    channel: SensorChannel
    is_sensor_enabled: bool
    is_anomaly_enabled: bool
    additional_details: bytes
    dimensions: _containers.RepeatedCompositeFieldContainer[SensorDimension]
    sensor_id: str
    sensor_has_error: bool
    model_type: MLModelType
    mltk_model_id: str
    sensor_category: str
    def __init__(self, timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., value: _Optional[float] = ..., channel: _Optional[_Union[SensorChannel, _Mapping]] = ..., is_sensor_enabled: bool = ..., is_anomaly_enabled: bool = ..., additional_details: _Optional[bytes] = ..., dimensions: _Optional[_Iterable[_Union[SensorDimension, _Mapping]]] = ..., sensor_id: _Optional[str] = ..., sensor_has_error: bool = ..., model_type: _Optional[_Union[MLModelType, str]] = ..., mltk_model_id: _Optional[str] = ..., sensor_category: _Optional[str] = ...) -> None: ...

class ExternalSensorAvailability(_message.Message):
    __slots__ = ("metrics", "type", "id", "is_available", "category")
    METRICS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedScalarFieldContainer[str]
    type: str
    id: str
    is_available: bool
    category: str
    def __init__(self, metrics: _Optional[_Iterable[str]] = ..., type: _Optional[str] = ..., id: _Optional[str] = ..., is_available: bool = ..., category: _Optional[str] = ...) -> None: ...

class SensorInfo(_message.Message):
    __slots__ = ("id", "type", "sensor_class", "file_name", "port", "metrics", "settings", "category")
    class SensorMetric(_message.Message):
        __slots__ = ("metric_name", "min_range", "max_range")
        METRIC_NAME_FIELD_NUMBER: _ClassVar[int]
        MIN_RANGE_FIELD_NUMBER: _ClassVar[int]
        MAX_RANGE_FIELD_NUMBER: _ClassVar[int]
        metric_name: str
        min_range: float
        max_range: float
        def __init__(self, metric_name: _Optional[str] = ..., min_range: _Optional[float] = ..., max_range: _Optional[float] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SENSOR_CLASS_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: str
    sensor_class: str
    file_name: str
    port: str
    metrics: _containers.RepeatedCompositeFieldContainer[SensorInfo.SensorMetric]
    settings: SensorSettings
    category: str
    def __init__(self, id: _Optional[str] = ..., type: _Optional[str] = ..., sensor_class: _Optional[str] = ..., file_name: _Optional[str] = ..., port: _Optional[str] = ..., metrics: _Optional[_Iterable[_Union[SensorInfo.SensorMetric, _Mapping]]] = ..., settings: _Optional[_Union[SensorSettings, _Mapping]] = ..., category: _Optional[str] = ...) -> None: ...

class SensorConfig(_message.Message):
    __slots__ = ("sensors",)
    SENSORS_FIELD_NUMBER: _ClassVar[int]
    sensors: _containers.RepeatedCompositeFieldContainer[SensorInfo]
    def __init__(self, sensors: _Optional[_Iterable[_Union[SensorInfo, _Mapping]]] = ...) -> None: ...
