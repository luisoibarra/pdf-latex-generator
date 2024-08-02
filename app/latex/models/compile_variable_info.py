from typing import Any, Optional, Union

from typing_extensions import Annotated
from pydantic import BaseModel, ValidationError, Field
from pydantic.functional_validators import AfterValidator, model_validator

JSON_VARIABLE_TYPE = "json"
IMAGE_VARIABLE_TYPE = "image"
DATA_VARIABLE_TYPE = "data"

# Order matters
VARIABLE_TYPES = [
    # For values that can be used without any processing after deserialization
    JSON_VARIABLE_TYPE,
    # Indicates that the variable is an image. The value of the variable is the base64 encoded image.
    IMAGE_VARIABLE_TYPE,
    # Indicates that the variable is data. This data should be handled according the information provided.
    DATA_VARIABLE_TYPE,
]

def check_compile_variable_value(val: str) -> str:
    assert val in VARIABLE_TYPES, f"Variable type {val} not in allowed variable types {VARIABLE_TYPES}."
    return val

CompileVariableType = Annotated[str, AfterValidator(check_compile_variable_value)]

class ImageVariableInfo(BaseModel):
    """
    Image information. Will come as value property when type is image.
    """
    base64_image: str
    width: Optional[float]
    height: Optional[float]

class CurveInfo(BaseModel):
    """
    Curve information.
    """
    name: Optional[str]
    end_label: Optional[str]
    line_style: Optional[str]
    scatter: bool
    color: list[float]
    data: list[float]
    x_data: Optional[list[float]]

class DataVariableInfo(BaseModel):
    """
    Data information. Will come as value property when type is data.
    """
    x_axis: Optional[list[float]]
    data: list[CurveInfo]
    upper_data: Optional[list[float]]
    lower_data: Optional[list[float]]
    title: Optional[str]
    x_label: Optional[str]
    y_label: Optional[str]

class CompileVariableInfo(BaseModel):
    """
    Variable information
    """
    name: str
    type: CompileVariableType = JSON_VARIABLE_TYPE

    # This filed will always match with Any, then in model_validator will be enforced the value type 
    # according the type parameter. Union is here for type purposes only.
    value: Union[Any, ImageVariableInfo, DataVariableInfo] = Field(..., union_mode='left_to_right')

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'CompileVariableInfo':
        if self.type == IMAGE_VARIABLE_TYPE:
            if isinstance(self.value, dict):
                self.value = ImageVariableInfo(**self.value)
            elif isinstance(self.value, ImageVariableInfo):
                pass
            else:
                raise ValidationError(f"When CompileVariableInfo.type='{IMAGE_VARIABLE_TYPE}', CompileVariableInfo.value must be a valid dictionary.")
        if self.type == DATA_VARIABLE_TYPE:
            if isinstance(self.value, dict):
                self.value = DataVariableInfo(**self.value)
            elif isinstance(self.value, DataVariableInfo):
                pass
            else:
                raise ValidationError(f"When CompileVariableInfo.type='{DATA_VARIABLE_TYPE}', CompileVariableInfo.value must be a valid dictionary.")
        return self
