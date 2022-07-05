import datetime
from typing import Optional

from pydantic import BaseModel, root_validator


class CacheSchema(BaseModel):
    data: datetime.datetime


class ResponseCacheSchema(BaseModel):
    cache: dict[datetime.datetime, dict]


class DeleteCacheSchema(BaseModel):
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None

    @root_validator(pre=True)
    def check_end_start_date(cls, values: dict):
        assert len(values.keys()) != 1, 'You must give two dates or None'

        if len(values.keys()) == 2:
            assert values['start_time'] < values['end_time'], 'end_time must be greater than start_time'
        return values

    class Config:
        schema_extra = {
            'example': {
                'start_time': datetime.datetime.now() - datetime.timedelta(hours=1),
                'end_time': datetime.datetime.now()
            }
        }


