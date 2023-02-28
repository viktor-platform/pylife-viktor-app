from ..core import File as File
from .external_program import ExternalProgram as ExternalProgram
from io import BytesIO
from typing import Any, Optional, Union

class DSheetPilingAnalysis(ExternalProgram):
    input_file: Any
    def __init__(self, input_file: Union[BytesIO, File]) -> None: ...
    def get_output_file(self, extension: str = ..., *, as_file: bool = ...) -> Optional[Union[BytesIO, File]]: ...
