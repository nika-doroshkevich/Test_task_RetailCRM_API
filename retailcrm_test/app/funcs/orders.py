import json
from typing import Dict, List

import httpx
from app.funcs.logger import logger
from app.schemas.orders import (
    OrderCreate,
    OrderCreateResponse,
    PaymentCreate,
    PaymentCreateResponse,
)
from decouple import config
from fastapi import HTTPException, status

RETAILCRM_API_URL = config("RETAILCRM_API_URL")
RETAILCRM_API_KEY = config("RETAILCRM_API_KEY")

ORDER_PREFIX = "/orders"


async def get_orders_for_customer(customer_id: int) -> List[Dict]:
    """
    Retrieves a list of orders for a specific customer by customer ID.
    """
    params = {"apiKey": RETAILCRM_API_KEY, "filter[customerId]": customer_id}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{RETAILCRM_API_URL}{ORDER_PREFIX}", params=params
            )

            response.raise_for_status()

        return response.json().get("orders", [])

    except Exception as e:
        logger.error(f"Request error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong.",
        )


async def create_order_request(order: OrderCreate) -> OrderCreateResponse:
    """
    Creates a new order in the RetailCRM system.
    """
    payload = {
        "order": json.dumps(
            {
                "externalId": order.order.external_id,
                "number": order.order.number,
            }
        ),
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{RETAILCRM_API_URL}{ORDER_PREFIX}/create",
                data=payload,
                params={"apiKey": RETAILCRM_API_KEY},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

    except Exception as e:
        logger.error(f"Request error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong.",
        )

    order_id = response.json().get("id")

    if not order_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create order.",
        )

    return OrderCreateResponse(order_id=order_id)


async def create_payment_request(payment: PaymentCreate) -> PaymentCreateResponse:
    """
    Creates a new payment associated with an order in the RetailCRM system.
    """
    payload = {
        "payment": json.dumps(
            {
                "external_id": payment.payment.external_id,
                "number": payment.payment.number,
                "amount": payment.payment.amount,
                "type": payment.payment.type,
                "order": {"id": payment.payment.order_id},
            }
        ),
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{RETAILCRM_API_URL}{ORDER_PREFIX}/payments/create",
                data=payload,
                params={"apiKey": RETAILCRM_API_KEY},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

    except Exception as e:
        logger.error(f"Request error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong.",
        )

    payment_id = response.json().get("id")

    if not payment_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create payment.",
        )

    return PaymentCreateResponse(payment_id=payment_id)
