from typing import Any

from typing_extensions import Annotated
from pydantic import BaseModel, ValidationError
from pydantic.functional_validators import AfterValidator

IMAGE_VARIABLE_TYPE = "image"
JSON_VARIABLE_TYPE = "json"

# Order matters
VARIABLE_TYPES = [
    # For values that can be used without any processing after deserialization
    JSON_VARIABLE_TYPE,
    # Indicates that the variable is an image. The value of the variable is the base64 encoded image.
    IMAGE_VARIABLE_TYPE,
]

def check_compile_variable_value(val: str) -> str:
    assert val in VARIABLE_TYPES, f"Variable type {val} not in allowed variable types {VARIABLE_TYPES}."
    return val

CompileVariableType = Annotated[str, AfterValidator(check_compile_variable_value)]

class CompileVariableInfo(BaseModel):
    name: str
    type: CompileVariableType = VARIABLE_TYPES[0] # Defaults to json 
    value: Any
