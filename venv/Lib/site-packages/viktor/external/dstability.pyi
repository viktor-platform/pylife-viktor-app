from ..core import File as File
from .external_program import ExternalProgram as ExternalProgram
from typing import Any, Optional

class DStabilityAnalysis(ExternalProgram):
    input_file: Any
    def __init__(self, input_file: File) -> None: ...
    def get_output_file(self, extension: str = ...) -> Optional[File]: ...
