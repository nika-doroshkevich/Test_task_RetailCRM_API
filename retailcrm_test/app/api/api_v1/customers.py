from typing import Dict, List

from app.filters.customers import CustomerFilter
from app.funcs.customers import create, get_clients
from app.schemas.customers import CustomerCreate, CustomerCreateResponse
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/", response_model=List[Dict])
async def get_customers(
    filters: CustomerFilter = Depends(),
):
    """
    Retrieve a list of customers from RetailCRM based on optional filters.
    """
    customers = await get_clients(filters=filters)
    return customers


@router.post("/", response_model=CustomerCreateResponse)
async def create_customer(
    customer: CustomerCreate,
):
    """
    Create a new customer in RetailCRM.
    """
    customer_id = await create(customer=customer)
    return customer_id
