from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RoomRegistrationRequest(_message.Message):
    __slots__ = ["room_name"]
    ROOM_NAME_FIELD_NUMBER: _ClassVar[int]
    room_name: str
    def __init__(self, room_name: _Optional[str] = ...) -> None: ...

class RoomRegistrationResponse(_message.Message):
    __slots__ = ["room_id"]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    room_id: int
    def __init__(self, room_id: _Optional[int] = ...) -> None: ...

class NewsFlash(_message.Message):
    __slots__ = ["news_time", "news_item"]
    NEWS_TIME_FIELD_NUMBER: _ClassVar[int]
    NEWS_ITEM_FIELD_NUMBER: _ClassVar[int]
    news_time: _timestamp_pb2.Timestamp
    news_item: str
    def __init__(self, news_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., news_item: _Optional[str] = ...) -> None: ...

class NewsStreamStatus(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
