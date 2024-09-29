from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SummaryNewsRequest(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...

class SummaryNewsResponse(_message.Message):
    __slots__ = ("success", "summarized_text")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    SUMMARIZED_TEXT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    summarized_text: str
    def __init__(self, success: bool = ..., summarized_text: _Optional[str] = ...) -> None: ...
