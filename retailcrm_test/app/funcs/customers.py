import json
from typing import Dict, List

import httpx
from app.filters.customers import CustomerFilter
from app.funcs.logger import logger
from app.schemas.customers import CustomerCreate, CustomerCreateResponse, СontragentType
from decouple import config
from fastapi import HTTPException, status

RETAILCRM_API_URL = config("RETAILCRM_API_URL")
RETAILCRM_API_KEY = config("RETAILCRM_API_KEY")

CUSTOMER_PREFIX = "/customers"


async def get_clients(filters: CustomerFilter = None) -> List[Dict]:
    """
    Retrieves a list of customers from RetailCRM using the provided filters.
    """
    filters_dict = filters.model_dump(exclude_unset=True)
    params = {
        **{f"filter[{key}]": value for key, value in filters_dict.items() if value},
        "apiKey": RETAILCRM_API_KEY,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{RETAILCRM_API_URL}{CUSTOMER_PREFIX}", params=params
            )

            response.raise_for_status()

        return response.json().get("customers", [])

    except Exception as e:
        logger.error(f"Request error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong.",
        )


async def create(customer: CustomerCreate) -> CustomerCreateResponse:
    """
    Creates a new customer in RetailCRM.
    """
    contragent_type = customer.contragent.contragentType

    if contragent_type == СontragentType.INDIVIDUAL:
        if customer.contragent.OGRN or customer.contragent.KPP:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OGRN and KPP should not be provided for individual contragent.",
            )
    elif contragent_type == СontragentType.LEGAL_ENTITY:
        if customer.contragent.certificateNumber:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="certificateNumber should not be provided for legal-entity contragent.",
            )
    elif contragent_type == СontragentType.ENTERPRENEUR:
        if customer.contragent.OGRN or customer.contragent.KPP:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OGRN and KPP should not be provided for enterpreneur contragent.",
            )

    payload = {
        "customer": json.dumps(
            {
                "email": customer.customer.email,
                "firstName": customer.customer.firstName,
                "lastName": customer.customer.lastName,
                "patronymic": customer.customer.patronymic,
            }
        ),
        "contragent[contragentType]": contragent_type,
        "contragent[legalName]": customer.contragent.legalName,
        "contragent[legalAddress]": customer.contragent.legalAddress,
        "contragent[INN]": customer.contragent.INN,
        "contragent[OKPO]": customer.contragent.OKPO,
        "contragent[KPP]": customer.contragent.KPP,
        "contragent[OGRN]": customer.contragent.OGRN,
        "contragent[OGRNIP]": customer.contragent.OGRNIP,
        "contragent[certificateNumber]": customer.contragent.certificateNumber,
        "contragent[BIK]": customer.contragent.BIK,
        "contragent[bank]": customer.contragent.bank,
        "contragent[bankAddress]": customer.contragent.bankAddress,
        "contragent[corrAccount]": customer.contragent.corrAccount,
        "contragent[bankAccount]": customer.contragent.bankAccount,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{RETAILCRM_API_URL}{CUSTOMER_PREFIX}/create",
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

    customer_id = response.json().get("id")

    if not customer_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create customer.",
        )

    return CustomerCreateResponse(customer_id=customer_id)
