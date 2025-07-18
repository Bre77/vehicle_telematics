from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetDiscoveryResponse(_message.Message):
    __slots__ = ("discovery_info",)
    DISCOVERY_INFO_FIELD_NUMBER: _ClassVar[int]
    discovery_info: _containers.RepeatedCompositeFieldContainer[DiscoveryInfo]
    def __init__(self, discovery_info: _Optional[_Iterable[_Union[DiscoveryInfo, _Mapping]]] = ...) -> None: ...

class DiscoveryInfo(_message.Message):
    __slots__ = ("topic_name", "type", "additional_information")
    TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_INFORMATION_FIELD_NUMBER: _ClassVar[int]
    topic_name: str
    type: str
    additional_information: _struct_pb2.Struct
    def __init__(self, topic_name: _Optional[str] = ..., type: _Optional[str] = ..., additional_information: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class GetReadingRequest(_message.Message):
    __slots__ = ("topic_name",)
    TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    topic_name: str
    def __init__(self, topic_name: _Optional[str] = ...) -> None: ...

class GetReadingResponse(_message.Message):
    __slots__ = ("topic_name", "fields")
    TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    topic_name: str
    fields: _struct_pb2.Struct
    def __init__(self, topic_name: _Optional[str] = ..., fields: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class SendDataRequest(_message.Message):
    __slots__ = ("topic_name", "fields")
    TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    topic_name: str
    fields: _struct_pb2.Struct
    def __init__(self, topic_name: _Optional[str] = ..., fields: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class SendDataResponse(_message.Message):
    __slots__ = ("success", "error")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error: Error
    def __init__(self, success: bool = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class Error(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
