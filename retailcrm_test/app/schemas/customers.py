from enum import Enum
from typing import Optional

from pydantic import BaseModel


class СontragentType(str, Enum):
    INDIVIDUAL = "individual"
    LEGAL_ENTITY = "legal-entity"
    ENTERPRENEUR = "enterpreneur"


class CustomerContragent(BaseModel):
    contragentType: СontragentType
    legalName: Optional[str] = None
    legalAddress: Optional[str] = None
    INN: Optional[str] = None
    OKPO: Optional[str] = None
    KPP: Optional[str] = None
    OGRN: Optional[str] = None
    OGRNIP: Optional[str] = None
    certificateNumber: Optional[str] = None
    BIK: Optional[str] = None
    bank: Optional[str] = None
    bankAddress: Optional[str] = None
    corrAccount: Optional[str] = None
    bankAccount: Optional[str] = None


class SerializedCustomer(BaseModel):
    email: str
    firstName: str
    lastName: str = None
    patronymic: Optional[str] = None


class CustomerCreate(BaseModel):
    customer: SerializedCustomer
    contragent: CustomerContragent = None


class CustomerCreateResponse(BaseModel):
    customer_id: int
