from typing import Dict, List

from app.funcs.orders import (
    create_order_request,
    create_payment_request,
    get_orders_for_customer,
)
from app.schemas.orders import (
    OrderCreate,
    OrderCreateResponse,
    PaymentCreate,
    PaymentCreateResponse,
)
from fastapi import APIRouter

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/{customer_id}", response_model=List[Dict])
async def get_customer_orders(customer_id: int):
    """
    Retrieve all orders associated with a specific customer.
    """
    orders = await get_orders_for_customer(customer_id=customer_id)
    return orders


@router.post("/", response_model=OrderCreateResponse)
async def create_order(
    order: OrderCreate,
):
    """
    Create a new order in RetailCRM.
    """
    order_id = await create_order_request(order=order)
    return order_id


@router.post("/payments", response_model=PaymentCreateResponse)
async def create_payment(
    payment: PaymentCreate,
):
    """
    Create a payment for an order in RetailCRM.
    """
    payment_id = await create_payment_request(payment=payment)
    return payment_id
