from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CustomerFilter(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    dateFrom: Optional[datetime] = None
    dateTo: Optional[datetime] = None
