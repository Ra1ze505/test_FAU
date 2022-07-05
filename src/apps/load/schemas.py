from typing import Optional

from pydantic import BaseModel, validator


LOAD_TYPES = {'cpu', 'ram'}


class CPULoadSchema(BaseModel):
    cpu_load: float


class RAMLoadSchema(BaseModel):
    ram_load: float


class ResponseLoadSchema(BaseModel):
    cpu: Optional[CPULoadSchema] = None
    ram: Optional[RAMLoadSchema] = None


class LoadSchema(BaseModel):
    types: list[str]

    @validator('types')
    def check_type_in_types(cls, v):
        for t in v:
            assert t in LOAD_TYPES

        return v

    class Config:
        schema_extra = {
            'example': {
                'types': ['cpu', 'ram']
            }
        }



