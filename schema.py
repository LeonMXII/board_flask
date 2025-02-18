from pydantic import BaseModel, field_validator, ValidationError
from errors import HttpError

class BaseBoardSchema(BaseModel):
    title: str
    description: str
    owner: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str):
        if not value.strip():
            raise ValueError("Заполнить заголовок!")
        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str):
        if not value.strip():
            raise ValueError("Заполнить описание!")
        return value

    @field_validator("owner")
    @classmethod
    def validate_owner(cls, value: str):
        if not value.strip():
            raise ValueError("Заполнить поле владельца!")
        return value


class CreateBoard(BaseBoardSchema):
    pass


class UpdateBoard(BaseModel):
    title: str | None = None
    description: str | None = None
    owner: str | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str | None):
        if value is not None and not value.strip():
            raise ValueError("Заполнить заголовок!")
        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str | None):
        if value is not None and not value.strip():
            raise ValueError("Заполнить описание!")
        return value

    @field_validator("owner")
    @classmethod
    def validate_owner(cls, value: str | None):
        if value is not None and not value.strip():
            raise ValueError("Заполнить поле владельца!")
        return value


def validate_json(schema_cls: type[BaseModel], json_data: dict):
    try:
        schema_obj = schema_cls(**json_data)
        return schema_obj.dict(exclude_unset=True)
    except ValidationError as e:
        errors = e.errors()
        for error in errors:
            error.pop("ctx", None)
        raise HttpError(400, errors)
