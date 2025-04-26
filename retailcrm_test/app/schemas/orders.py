from pydantic import BaseModel


class SerializedOrder(BaseModel):
    external_id: int
    number: str


class OrderCreate(BaseModel):
    order: SerializedOrder


class OrderCreateResponse(BaseModel):
    order_id: int


class SerializedPayment(BaseModel):
    external_id: int
    number: str
    order_id: int
    amount: float
    type: str


class PaymentCreate(BaseModel):
    payment: SerializedPayment


class PaymentCreateResponse(BaseModel):
    payment_id: int
