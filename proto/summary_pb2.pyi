from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetSummaryRequest(_message.Message):
    __slots__ = ("url",)
    URL_FIELD_NUMBER: _ClassVar[int]
    url: str
    def __init__(self, url: _Optional[str] = ...) -> None: ...

class GetSummaryResponse(_message.Message):
    __slots__ = ("success", "summarized_text")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    SUMMARIZED_TEXT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    summarized_text: str
    def __init__(self, success: bool = ..., summarized_text: _Optional[str] = ...) -> None: ...