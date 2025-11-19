from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class WaterStatus(str, Enum):
    PROPRIA="Própria"
    IMPRORIA="Imprópria"
    AMOSTRAGEM_NAO_REALIZADA="Amostragem Não Realizada"


class BeachLocation(BaseModel):
    id: int
    created_at: datetime
    name: str
    location: str
    city: str
    slug: str
    uf: str = Field(max_length=2)
    location_conde: str

    @field_validator('slug')
    @classmethod
    def validate_slug(cls, v: str) -> str:
        if not v.replace('-', '').replace('_', '').isalnum():
            raise ValueError('Slug deve conter apenas letras, números, - e _')
        return v


class BeachInfo(BaseModel):
    id: int
    created_at: datetime
    location_conde: str
    water_status: WaterStatus
    report_date: datetime
    beach_id: int

    @field_validator('water_status', mode='before')
    @classmethod
    def normalize_water_status(cls, v: str) -> str:
        if v not in ['Própria', 'Imprópria']:
            return 'Amostragem Não Realizada'
        return v

    def to_dict(self) -> dict:
        return {
            'location_code': self.location_code,
            'water_status': self.water_status.value,
            'report_date': self.report_date.isoformat(),
            'beach_id': self.beach_id
        }



