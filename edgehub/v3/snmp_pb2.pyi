from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SNMPEvent(_message.Message):
    __slots__ = ("oid_symbolic_name", "snmp_version", "value", "timestamp", "host")
    OID_SYMBOLIC_NAME_FIELD_NUMBER: _ClassVar[int]
    SNMP_VERSION_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    oid_symbolic_name: str
    snmp_version: str
    value: str
    timestamp: int
    host: str
    def __init__(self, oid_symbolic_name: _Optional[str] = ..., snmp_version: _Optional[str] = ..., value: _Optional[str] = ..., timestamp: _Optional[int] = ..., host: _Optional[str] = ...) -> None: ...
